# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import logging

from sympy import Symbol, true

from helpers import InputPin
from nangate45_cell_library import cell_mapping

logger = logging.getLogger(__name__)


class FormulaBuilder:
    """ Class for converting a graph into a boolean formula.

    This class provides functionality to a networkx graph into a boolean formula
    in CNF.
    """
    def __init__(self, graph):
        """ Inits the FormulaBuilder class

        Args:
            graph: The graph to transform.
        """
        self.graph = graph

    def transform_graph(self) -> Symbol:
        """ Transforms the graph into a boolean formula in CNF.

        This function uses the Tseytin transformation to transform the
        differential graph into a boolean formula.

        Returns:
            The boolean formula in CNF.
        """

        sub_expressions = []
        for node, node_attribute in self.graph.nodes(data=True):
            node_type = node_attribute["node"].type
            filter_types = {"null_node", "one_node"}
            if node_type not in filter_types:
                # Here we are collecting the input names and the node name.
                # The node name consists of the node name and the output pin
                # as we could have multiple output pins for a node.
                for wire, out_pin in node_attribute["node"].outputs.items():
                    inputs = {}
                    inputs["node_name"] = InputPin(node, out_pin)
                    # Get the input pins of the current node. As an input pin
                    # can be connected to a node having multiple outputs (e.g.
                    # Q or QN), we have to also store the output pin of the
                    # other edge.
                    for edge in self.graph.in_edges(node):
                        in_node = edge[0]
                        in_pin = self.graph.get_edge_data(edge[0],
                                                          edge[1])["in_pin"]
                        out_pin = self.graph.get_edge_data(edge[0],
                                                           edge[1])["out_pin"]
                        inputs[in_pin] = InputPin(in_node, out_pin)

                    # If there is an input port with input size greater than 1
                    # than we have a predefined input value of one/zero for this
                    # input. Else we ignore input ports.
                    if node_type == "input" and len(inputs) > 1:
                        sub_expressions.append(cell_mapping[node_type](
                            inputs, self.graph))
                    elif node_type != "input":
                        if node_type in cell_mapping:
                            sub_expressions.append(cell_mapping[node_type](
                                inputs, self.graph))
                        else:
                            logger.error(
                                f"Err: Gate type {node_type} not found.")

        # Create the final boolean formula by ANDing all sub expressions.
        cnf = true

        for sub_expression in sub_expressions:
            if sub_expression:
                cnf &= sub_expression

        return cnf
