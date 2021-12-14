# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import DefaultDict

from sympy import Symbol

import helpers
from helpers import InputPin

logger = logging.getLogger(__name__)


class FormulaBuilder:
    """ Class for converting a graph into a boolean formula.

    This class provides functionality to a networkx graph into a boolean formula
    in CNF.
    """
    def __init__(self, graph, cell_lib, solver):
        """ Inits the FormulaBuilder class

        Args:
            graph: The graph to transform.
            cell_lib: The imported cell library.
        """
        self.graph = graph
        self.cell_lib = cell_lib
        self.solver = solver

    def transform_graph(self) -> Symbol:
        """ Transforms the graph into a boolean formula in CNF.

        This function uses the Tseytin transformation to transform the
        differential graph into a boolean formula.

        Returns:
            The SAT solver with the clauses.
        """
        node_int = DefaultDict()
        # The SAT solver uses integers as variable names. A logical 1=1, a
        # logical 0=2. The next gate uses 3 as a variable name.
        node_int_cntr = 3
        for node, node_attribute in self.graph.nodes(data=True):
            node_type = node_attribute["node"].type
            filter_types = {"null_node", "one_node"}
            if node_type not in filter_types:
                # Here we are collecting the input names and the node name.
                # The node name consists of the node name and the output pin
                # as we could have multiple output pins for a node.
                for wire, out_pin in node_attribute["node"].outputs.items():
                    inputs = {}
                    node_type_out = node_type + "_" + out_pin
                    # Assemble the name of the current node and translate the
                    # name to an integer value needed by the SAT solver.
                    node_name = node + "_" + out_pin
                    if node_name not in node_int:
                        node_int[node_name] = node_int_cntr
                        node_int_cntr += 1
                    inputs["node_name"] = InputPin(node, node_int[node_name])

                    # Get the input pins of the current node. As an input pin
                    # can be connected to a node having multiple outputs (e.g.
                    # Q or QN), we have to also store the output pin of the
                    # other edge.
                    for edge in self.graph.in_edges(node):
                        in_node = edge[0]
                        in_pins = self.graph.get_edge_data(edge[0],
                                                           edge[1])["in_pin"]
                        out_pin = self.graph.get_edge_data(edge[0],
                                                           edge[1])["out_pin"]
                        for in_pin in in_pins:
                            # Assemble the name of the input pin of the current node
                            # and translate the name to an integer value.
                            input_name = in_node + "_" + out_pin
                            in_node_type = self.graph.nodes[in_node][
                                "node"].type
                            if in_node_type == "null_node":
                                inputs[in_pin] = InputPin(
                                    input_name, self.cell_lib.zero)
                            elif in_node_type == "one_node":
                                inputs[in_pin] = InputPin(
                                    input_name, self.cell_lib.one)
                            else:
                                if input_name not in node_int:
                                    node_int[input_name] = node_int_cntr
                                    node_int_cntr += 1
                                inputs[in_pin] = InputPin(
                                    input_name, node_int[input_name])

                    # If there is an input port with input size greater than 1
                    # than we have a predefined input value of one/zero for this
                    # input. Else we ignore input ports.
                    if (node_type == "input"
                            or node_type == "input_fault") and len(inputs) > 1:
                        self.cell_lib.cell_mapping[node_type_out](inputs,
                                                                  self.graph,
                                                                  self.solver)
                    elif node_type != "input":
                        if node_type_out in self.cell_lib.cell_mapping and self.graph.in_edges(
                                node):
                            self.cell_lib.cell_mapping[node_type_out](
                                inputs, self.graph, self.solver)
                        else:
                            # Report missing gate type for gates with inputs.
                            if self.graph.in_edges(node):
                                logger.error(
                                    f"Err: Gate type {node_type_out} not found."
                                )

        return self.solver
