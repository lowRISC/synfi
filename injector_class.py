# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import copy

import networkx as nx
import ray
from sympy.logic.inference import satisfiable

import helpers
from formula_class import FormulaBuilder
from helpers import FIResult, Node

@ray.remote
class FiInjector:
    """ Class for performing distributed fault injections.

    This class provides functionality to inject faults into the target circuit
    according to the fault model, to create the differential graph, to
    extract the boolean CNF formula of this graph, and to hand the formula to
    a SAT solver.
    """
    def __init__(self, fault_name, target_graph, fault_locations, fault_model,
                 cell_lib):
        """ Inits the injector class

        This function injects faults into the graph by replacing the type of
        the target node with the target type.

        Args:
            fault_name: The fault model name of the current attack.
            target_graph: The graph to be evaluated.
            fault_locations: The location and fault mapping of the faults.
            fault_model: The fault model.
            cell_lib: The imported cell library.
        """
        self.fault_name = fault_name
        self.target_graph = target_graph
        self.fault_locations = fault_locations
        self.fault_model = fault_model
        self.cell_lib = cell_lib

    def _inject_faults(self, fault_location):
        """ Inject faults into the target graph accoding to the fault location.

        This function injects faults into the graph by replacing the type of
        the target node with the target type.

        Args:
            fault_location: The current fault location (location+gate mapping).
        
        Returns:
            The faulty target graph.
        """
        faulty_graph = copy.deepcopy(self.target_graph)
        for node_target, fault_type in fault_location:
            stage = self.fault_model["fault_locations"][node_target]
            # Find the nodes in the target graph which are replaced with the
            # faulty nodes.
            nodes = [
                n for n, d in self.target_graph.nodes(data=True)
                if (d["node"].parent_name == node_target
                    and d["node"].stage == stage)
            ]
            for node in nodes:
                current_type = faulty_graph.nodes[node]["node"].type
                faulty_graph.nodes[node]["node"].type = fault_type
                faulty_graph.nodes[node]["node"].node_color = "red"
                gate_in_type_current = self.cell_lib.gate_in_type[current_type]
                gate_in_type_faulty = self.cell_lib.gate_in_type[fault_type]
                if gate_in_type_current != gate_in_type_faulty:
                    # We need to remap the input pins as the input type
                    # mismatches.
                    in_pin_mapping = self.cell_lib.pin_in_mapping[
                        gate_in_type_current][gate_in_type_faulty]
                    # Update the pin name in the node dict.
                    for pin in faulty_graph.nodes[node]["node"].inputs.keys():
                        faulty_graph.nodes[node]["node"].inputs[
                            pin] = in_pin_mapping[faulty_graph.nodes[node]
                                                  ["node"].inputs[pin]]
                    # Update pin name in the edge.
                    for edge in faulty_graph.in_edges(node):
                        faulty_graph.get_edge_data(
                            edge[0], edge[1])["in_pin"] = in_pin_mapping[
                                faulty_graph.get_edge_data(edge[0],
                                                           edge[1])["in_pin"]]
                gate_out_type_current = self.cell_lib.gate_out_type[
                    current_type]
                gate_out_type_faulty = self.cell_lib.gate_out_type[fault_type]
                if gate_out_type_current != gate_out_type_faulty:
                    # We need to remap the output pins as the output type
                    # mismatches.
                    out_pin_mapping = self.cell_lib.pin_out_mapping[
                        gate_out_type_current][gate_out_type_faulty]
                    # Update the pin name in the node dict.
                    for pin in faulty_graph.nodes[node]["node"].outputs.keys():
                        faulty_graph.nodes[node]["node"].outputs[
                            pin] = out_pin_mapping[faulty_graph.nodes[node]
                                                   ["node"].outputs[pin]]
                    # Update pin name in the edge.
                    for edge in faulty_graph.out_edges(node):
                        faulty_graph.get_edge_data(
                            edge[0], edge[1])["out_pin"] = out_pin_mapping[
                                faulty_graph.get_edge_data(edge[0],
                                                           edge[1])["out_pin"]]
        return faulty_graph

    def _add_in_logic(self, diff_graph):
        """ Add the input logic to the differential graph.

        In the input logic, the input nodes defined in the fault model are
        connected with their predefined value.

        Args:
            diff_graph: The differential graph.

        Returns:
            The differential graph with the input nodes.
        """

        diff_graph_in_logic = copy.deepcopy(diff_graph)
        # Add the null and one node for the predefined values.
        diff_graph_in_logic.add_node(
            "null", **{
                "node":
                Node(name="null",
                     parent_name="null",
                     type="null_node",
                     inputs={},
                     outputs={'0': "O"},
                     stage="",
                     node_color="black")
            })
        diff_graph_in_logic.add_node(
            "one", **{
                "node":
                Node(name="one",
                     parent_name="one",
                     type="one_node",
                     inputs={},
                     outputs={'1': "O"},
                     stage="",
                     node_color="black")
            })
        # Get the input values from the fault model and connect each input node
        # with the null / one node.
        input_values = self.fault_model["input_values"]
        for node, value in input_values.items():
            # Find all input nodes and connect with node.
            nodes = [
                n for n, d in diff_graph.nodes(data=True)
                if (d["node"].parent_name == node and d["node"].type == "input"
                    )
            ]
            for node in nodes:
                if value == 1:
                    diff_graph_in_logic.add_edge("one",
                                                 node,
                                                 name="one_wire",
                                                 out_pin="O",
                                                 in_pin="I1")
                else:
                    diff_graph_in_logic.add_edge("null",
                                                 node,
                                                 name="null_wire",
                                                 out_pin="O",
                                                 in_pin="I1")
        return diff_graph_in_logic

    def _add_xor_xnor(self, diff_graph_out_logic, diff_graph, values, alert):
        """ Add the XORs and XNORs for the output logic to the graph.

        Args:
            diff_graph_out_logic: The differential graph with the output logic.
            diff_graph: The differential graph
            values: The values for the selected nodes.
            alert: The node is an alert node.

        Returns:
            The differential graph with the XORs and XNORs.
        """
        out_nodes_added = []
        out_nodes_faulty_added = []

        for node_target, value in values.items():
            # Add XNOR/XOR node for each output node and connect with this port.
            nodes = [
                n for n, d in diff_graph.nodes(data=True)
                if (d["node"].parent_name == node_target
                    and d["node"].type == "output")
            ]
            for node in nodes:
                if "_faulty" in node:
                    if alert:
                        # For the alert signals, use XNORs.
                        node_name = node + "_xnor"
                        node_type = "xnor"
                    else:
                        # For outputs use XORs.
                        node_name = node + "_xor"
                        node_type = "xor"
                else:
                    node_name = node + "_xnor"
                    node_type = "xnor"
                diff_graph_out_logic.add_node(
                    node_name, **{
                        "node":
                        Node(name=node_name,
                             parent_name=node_name,
                             type=node_type,
                             inputs={0: "I"},
                             outputs={0: "O"},
                             stage="out_stage",
                             node_color="purple")
                    })
                if ("_faulty" in node) and (not alert):
                    out_nodes_faulty_added.append(node_name)
                else:
                    out_nodes_added.append(node_name)
                if value == 1:
                    diff_graph_out_logic.add_edge("one",
                                                  node_name,
                                                  name="one_wire",
                                                  out_pin="O",
                                                  in_pin="I1")
                else:
                    diff_graph_out_logic.add_edge("null",
                                                  node_name,
                                                  name="null_wire",
                                                  out_pin="O",
                                                  in_pin="I1")
                diff_graph_out_logic.add_edge(node,
                                              node_name,
                                              name="node_wire",
                                              out_pin="O",
                                              in_pin="I2")
                diff_graph_out_logic.nodes[node]["node"].outputs = {0: "O"}
                diff_graph_out_logic.nodes[node]["node"].inputs = {0: "I"}
        return out_nodes_added, out_nodes_faulty_added

    def _connect_outputs(self, diff_graph_out_logic, out_nodes, out_logic):
        # Flatten the list.
        out_nodes = [item for sublist in out_nodes for item in sublist]
        # Connect the outputs of the XNOR/XORs with a AND.
        out_name = "output_logic_" + out_logic
        diff_graph_out_logic.add_node(
            out_name, **{
                "node":
                Node(name=out_name,
                     parent_name=out_name,
                     type=out_logic,
                     inputs={0: "I"},
                     outputs={0: "O"},
                     stage="",
                     node_color="purple")
            })
        cntr = 1
        for out_node in out_nodes:
            diff_graph_out_logic.add_edge(out_node,
                                          out_name,
                                          name=out_logic + "_wire",
                                          out_pin="O",
                                          in_pin="A" + str(cntr))
            cntr = cntr + 1

        return out_name

    def _add_out_logic(self, diff_graph):
        """ Add the output logic to the differential graph.

        For the non-faulty graph in the differential graph:
        -XNORs are used to compare the output to the expected output.
        For the faulty graph in the differential graph:
        -XORs are used to compare the output to the expected output.
        -XNORs are used to compare the alert signals to the expected
         alert output signals. We are using XNORs as we are only interested in
         faults manipulating the output but not the alert signal.

        All XNORs/XORs are ANDed to produce the final circuit.

        Args:
            diff_graph: The differential graph.

        Returns:
            The differential graph with the output logic.
        """
        diff_graph_out_logic = copy.deepcopy(diff_graph)
        output_values = self.fault_model["output_values"]
        alert_values = self.fault_model["alert_values"]
        out_nodes_added = []
        out_nodes_faulty_added = []
        # Add the output logic for the output values.
        out_nodes = self._add_xor_xnor(diff_graph_out_logic, diff_graph,
                                       output_values, False)
        out_nodes_added.append(out_nodes[0])
        out_nodes_faulty_added.append(out_nodes[1])
        # Add the output logic for the alert values.
        out_nodes = self._add_xor_xnor(diff_graph_out_logic, diff_graph,
                                       alert_values, True)
        out_nodes_added.append(out_nodes[0])
        out_nodes_faulty_added.append(out_nodes[1])

        # OR all faulty XORs.
        or_output = self._connect_outputs(diff_graph_out_logic,
                                          out_nodes_faulty_added, "or")

        # AND all output nodes (non-faulty and alert).
        and_output = self._connect_outputs(diff_graph_out_logic,
                                           out_nodes_added, "and")

        # Connect the output of the OR logic with the AND output logic.
        num_in_edges = 1
        for edge in diff_graph_out_logic.in_edges(and_output):
            num_in_edges += 1
        diff_graph_out_logic.add_edge(or_output,
                                      and_output,
                                      name="and_wire",
                                      out_pin="O",
                                      in_pin="A" + str(num_in_edges))

        return diff_graph_out_logic

    def _create_diff_graph(self, faulty_graph):
        """ Create the differential graph based on the faulty graph.

        This function creates the differential graph by merging the faulty graph
        and the unmodified target graph into a common graph. The inputs of the
        differential graph are set to predefined values specified in the fault
        model. The output is compared to a predefined value using a XNOR. To
        get a single output port, the output of the XNORs are connected using a
        AND.

        Args:
            faulty_graph: The target graph with the faulty nodes.

        Returns:
            The differential graph.
        """
        orig_graph = copy.deepcopy(self.target_graph)
        faulty_graph_renamed = copy.deepcopy(faulty_graph)
        # Rename the faulty graph.
        faulty_graph_renamed = helpers.rename_nodes(faulty_graph_renamed,
                                                    "_faulty", True)
        # Merge the graphs into a common graph.
        diff_graph = nx.compose(orig_graph, faulty_graph_renamed)

        # Add the input logic. Here, the values are set to a defined value.
        diff_graph_in_logic = self._add_in_logic(diff_graph)

        # Add the output logic. The output logic compares the result with the
        # expected result stored in "output_values" of the fault model.
        diff_graph_out_logic = self._add_out_logic(diff_graph_in_logic)

        return diff_graph_out_logic

    def perform_attack(self) -> FIResult:
        """ Perform the attack.

        Here, the attack on the target graph is conducted. First, a faulty graph
        is created. In this graph, the target fault nodes are replaced according
        to the fault mapping. Then, the differential graph is created and
        converted to a boolean formula.

        Returns:
            The result of the attack.
        """
        results = []
        for fault_location in self.fault_locations:
            # Inject the faults into the target graph.
            faulty_graph = self._inject_faults(fault_location)

            # Create the differential graph.
            diff_graph = self._create_diff_graph(faulty_graph)

            # Transform the differential graph to a boolean formula
            formula_builder = FormulaBuilder(diff_graph, self.cell_lib)
            cnf = formula_builder.transform_graph()

            # Hand the boolean formula to the SAT solver.
            sat_result = satisfiable(cnf)
            if sat_result != False:
                sat_result = True

            results.append(
                FIResult(fault_name=self.fault_name,
                         sat_result=sat_result,
                         fault_location=fault_location))

        return results
