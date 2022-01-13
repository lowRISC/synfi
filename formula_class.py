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
        # Loop over all nodes of the target graph.
        for node, node_attribute in self.graph.nodes(data=True):
            node_type = node_attribute["node"].type
            filter_types = {"null_node", "one_node", "output_logic_terminate"}
            # Ignore null and one nodes as we are handling them in the injector.
            if node_type not in filter_types:
                # Loop over output ports of the current node (e.g. Q and QN ports).
                for out_node_out, out_node_in, out_edge_data in self.graph.out_edges(
                        node, data=True):
                    inputs = {}
                    port_name = out_edge_data["edge"].out_port
                    node_type_out = node_type + "_" + port_name
                    # Assemble the name of the current node
                    # (=node_name+out_port_name) and translate the name to an
                    # integer value needed by the SAT solver.
                    node_name = node + "_" + port_name
                    if node_name not in node_int:
                        node_int[node_name] = node_int_cntr
                        node_int_cntr += 1
                    inputs["node_name"] = InputPin(node, node_int[node_name])

                    # Loop over all input edges of the current node to find the
                    # nodes connected to the current node.
                    for in_node_out, in_node_in, in_edge_data in self.graph.in_edges(
                            node, data=True):
                        in_node_type = self.graph.nodes[in_node_out][
                            "node"].type
                        # Get the name of the node (=in_node_out+out_port_name)
                        # connected to the input pin of the current node.
                        input_name = in_node_out + "_" + in_edge_data[
                            "edge"].out_port
                        # Get the name of the input port.
                        in_port = in_edge_data["edge"].in_port
                        # Add the name of the node + the in port to the input dict.
                        # Connect zero/ones with the corresponding element.
                        if in_node_type == "null_node":
                            inputs[in_port] = InputPin(input_name,
                                                       self.cell_lib.zero)
                        elif in_node_type == "one_node":
                            inputs[in_port] = InputPin(input_name,
                                                       self.cell_lib.one)
                        else:
                            if input_name not in node_int:
                                node_int[input_name] = node_int_cntr
                                node_int_cntr += 1
                            inputs[in_port] = InputPin(input_name,
                                                       node_int[input_name])

                    # If there is an input port with input size greater than 1
                    # than we have a predefined input value of one/zero for this
                    # input. Else we ignore input ports.
                    if (node_type == "input"
                            or node_type == "input_fault") and len(inputs) > 1:
                        self.cell_lib.cell_mapping[node_type_out](inputs,
                                                                  self.graph,
                                                                  self.solver)
                    elif node_type == "in_node":
                        # As in_nodes can have multiple in/out ports, only
                        # use the edge connected to the current output port.
                        inputs_in_node = {}
                        inputs_in_node["node_name"] = inputs["node_name"]
                        inputs_in_node[port_name] = inputs[port_name]
                        self.cell_lib.cell_mapping[node_type_out](
                            inputs_in_node, self.graph, self.solver)
                    elif node_type != "input":
                        if node_type_out in self.cell_lib.cell_mapping and self.graph.in_edges(
                                node):
                            self.cell_lib.cell_mapping[node_type_out](
                                inputs, self.graph, self.solver)
                        else:
                            # Check if the node_type is in the cell library.
                            type_found, node_type = helpers.check_gate_type(
                                node_type, self.cell_lib.cell_mapping)
                            if type_found:
                                self.cell_lib.cell_mapping[node_type](
                                    inputs, self.graph, self.solver)
                            else:
                                # Report missing gate type for gates with inputs.
                                if self.graph.in_edges(node):
                                    logger.error(
                                        f"Err: Gate type {node_type_out} not found."
                                    )

        return self.solver
