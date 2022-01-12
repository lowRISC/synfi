# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import copy
import gc
import logging
import sys

import networkx as nx
import ray
from pysat.solvers import Lingeling

import helpers
from formula_class import FormulaBuilder
from helpers import Edge, FIResult, Node, NodePin, NodePort

logger = logging.getLogger()


@ray.remote
class FiInjector:
    """ Class for performing distributed fault injections.

    This class provides functionality to inject faults into the target circuit
    according to the fault model, to create the differential graph, to
    extract the boolean CNF formula of this graph, and to hand the formula to
    a SAT solver.
    """
    def __init__(self, fault_name, target_graph, graph, fault_locations,
                 fault_model, cell_lib):
        """ Inits the injector class

        This function injects faults into the graph by replacing the type of
        the target node with the target type.

        Args:
            fault_name: The fault model name of the current attack.
            target_graph: The graph to be evaluated.
            graph: The unmodified graph of the whole circuit.
            fault_locations: The location and fault mapping of the faults.
            fault_model: The fault model.
            cell_lib: The imported cell library.
        """
        self.fault_name = fault_name
        self.target_graph = target_graph
        self.graph = graph
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
        for fl in fault_location:
            stage = fl.stage
            node_target = fl.location
            fault_type = fl.mapping
            # Find the nodes in the target graph which are replaced with the
            # faulty nodes.
            nodes = [
                n for n, d in self.target_graph.nodes(data=True)
                if (d["node"].name == node_target and d["node"].stage == stage
                    and d["node"].type != "output")
            ]
            for node in nodes:
                current_type = faulty_graph.nodes[node]["node"].type
                faulty_graph.nodes[node]["node"].type = fault_type
                faulty_graph.nodes[node]["node"].node_color = "red"
                # Update the inport port.
                gate_in_type_current = self.cell_lib.gate_in_type[current_type]
                gate_in_type_faulty = self.cell_lib.gate_in_type[fault_type]
                if gate_in_type_current != gate_in_type_faulty:
                    # We need to remap the input ports as the input type
                    # mismatches.
                    in_port_mapping = self.cell_lib.port_in_mapping[
                        gate_in_type_current][gate_in_type_faulty]
                    # Update the port name in the node dict.
                    for port in faulty_graph.nodes[node]["node"].in_ports:
                        port.name = in_port_mapping[port.name]
                    # Update port name in the edge.
                    for edge_out, edge_in in faulty_graph.in_edges(node):
                        for edge_num, edge_data in faulty_graph.get_edge_data(
                                edge_out, edge_in).items():
                            edge_data["edge"].in_port = in_port_mapping[
                                edge_data["edge"].in_port]
                # Update the output port.
                gate_out_type_current = self.cell_lib.gate_out_type[
                    current_type]
                gate_out_type_faulty = self.cell_lib.gate_out_type[fault_type]
                if gate_out_type_current != gate_out_type_faulty:
                    # We need to remap the output pins as the output type
                    # mismatches.
                    out_port_mapping = self.cell_lib.port_out_mapping[
                        gate_out_type_current][gate_out_type_faulty]
                    # Update the port name in the node dict.
                    for port in faulty_graph.nodes[node]["node"].out_ports:
                        port.name = out_port_mapping[port.name]
                    # Update port name in the edge.
                    for edge_out, edge_in in faulty_graph.out_edges(node):
                        for edge_num, edge_data in faulty_graph.get_edge_data(
                                edge_out, edge_in).items():
                            edge_data["edge"].out_port = in_port_mapping[
                                edge_data["edge"].out_port]

        return faulty_graph

    def _check_port_pin(self, node, ports, port_name, pin_number):
        """ Check if the user provided port and pin for an input/output node
        is valid. Terminates on an error.

        Args:
            node: The provided input/output node.
            ports: The ports of the corresponding node.
            port_name: The provided port name.
            pin_number: The provided pin number.
        """

        for port in ports:
            if port.name == port_name:
                for pin in port.pins:
                    if pin.number == int(pin_number):
                        return

        logger.error(
            f"Provided port/pin {port_name}/{pin_number} for node {node} not found."
        )
        sys.exit()

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
                     in_ports=[],
                     out_ports=[
                         NodePort(name="O",
                                  type="output",
                                  pins=[NodePin(number=0, wire="0")])
                     ],
                     stage="",
                     node_color="black")
            })
        diff_graph_in_logic.add_node(
            "one", **{
                "node":
                Node(name="one",
                     parent_name="one",
                     type="one_node",
                     in_ports=[],
                     out_ports=[
                         NodePort(name="O",
                                  type="output",
                                  pins=[NodePin(number=0, wire="1")])
                     ],
                     stage="",
                     node_color="black")
            })
        # Get the input values from the fault model and connect each input node
        # with the null / one node.
        input_values = self.fault_model["input_values"]
        for node_name, value in input_values.items():
            # Find all input nodes and connect with node.
            nodes = [
                n for n, d in diff_graph.nodes(data=True)
                if (d["node"].parent_name == node_name and (
                    d["node"].type == "input"
                    or d["node"].type == "input_fault"))
            ]
            for node in nodes:
                # Fetch the data for each pin of the provided in node.
                for port_name, port in value.items():
                    for pin_number, pin_value in port.items():
                        value_str = ""
                        node_type = diff_graph.nodes[node]["node"].type
                        # For fault inputs, invert the value.
                        if pin_value == 1 and node_type == "input":
                            value_str = "one"
                        elif pin_value == 1 and node_type == "input_fault":
                            value_str = "null"
                        elif pin_value == 0 and node_type == "input":
                            value_str = "null"
                        else:
                            value_str = "one"
                        # Check if the provided port/pin exists for the node.
                        self._check_port_pin(
                            node, diff_graph.nodes[node]["node"].in_ports,
                            port_name, pin_number)
                        # Connect the null/one node with the input node.
                        edge = Edge(in_port=port_name,
                                    in_pin=pin_number,
                                    out_port="O",
                                    out_pin=0,
                                    wire="")
                        diff_graph_in_logic.add_edge(value_str,
                                                     node,
                                                     edge=edge)

        return diff_graph_in_logic

    def _add_xor_xnor_nodes(self, diff_graph_out_logic, node, value, node_name,
                            node_type, out_port, out_pin):
        """ Add the xor/xnor node.

        In this function, the actual node for the comparison is added to the
        graph.

        Args:
            diff_graph_out_logic: The differential graph with the connected output.
            node: The current node.
            value: The output value set in the fault model.
            node_name: The name of the new node.
            node_type: The type of the new node.
            out_port: The port of the new node.
            out_pin: The pin of the new node.

        """
        diff_graph_out_logic.add_node(
            node_name, **{
                "node":
                Node(name=node_name,
                     parent_name=node_name,
                     type=node_type,
                     in_ports=[
                         NodePort(type="input",
                                  name="I",
                                  pins=[
                                      NodePin(number=0, wire=""),
                                      NodePin(number=1, wire="")
                                  ])
                     ],
                     out_ports=[
                         NodePort(type="output",
                                  name="O",
                                  pins=[NodePin(number=0, wire="")])
                     ],
                     stage="out_stage",
                     node_color="purple")
            })
        null_one = "null"
        if value == 1:
            null_one = "one"
        # Add the connection between and the null/one and the XOR/XNOR node.
        edge = Edge(in_port="I0", in_pin=0, out_port="O", out_pin=0, wire="")
        diff_graph_out_logic.add_edge(null_one, node_name, edge=edge)
        # Add the connection between the output and the XOR/XNOR node.
        edge = Edge(in_port="I1",
                    in_pin=0,
                    out_port=out_port,
                    out_pin=int(out_pin),
                    wire="")
        diff_graph_out_logic.add_edge(node, node_name, edge=edge)

    def _add_output(self, diff_graph_out_logic, diff_graph, values, faulty,
                    alert, exp_fault):
        """ Add the output logic.

        In this function, the comparison with the output value, the alert value
        or the expected fault value is done. Depending on the mode of comparison
        we use XOR or XNOR functions to do this comparison.

        Args:
            diff_graph_out_logic: The differential graph with the connected output.
            diff_graph: The differential graph.
            values: The output values set in the fault model.
            faulty: Is the node a faulty node?
            alert: Is the node an alert node?
            exp_fault: Is the node an expected fault value node?

        Returns:
            A list with the added nodes.
        """
        out_nodes_added = []
        for node_target, ports in values.items():
            nodes = [
                n for n, d in diff_graph.nodes(data=True)
                if (d["node"].parent_name == node_target
                    and d["node"].type == "output")
            ]
            for node in nodes:
                # Fetch the port/pin values provided in the FI model.
                for port_name, port in ports.items():
                    for pin_number, pin_value in port.items():
                        # If the node consists of output edges in the orig.
                        # graph, check the provided ports/pins.
                        if self.graph.out_edges(node):
                            self._check_port_pin(
                                node, diff_graph.nodes[node]["node"].out_ports,
                                port_name, pin_number)
                        if faulty:
                            if "_faulty" in node:
                                node_name = node + "_xor"
                                node_type = "xor"
                                if alert or exp_fault:
                                    node_name = node + "_xnor_alert_exp"
                                if alert or exp_fault:
                                    node_type = "xnor"
                                out_nodes_added.append(node_name)
                                self._add_xor_xnor_nodes(
                                    diff_graph_out_logic, node, pin_value,
                                    node_name, node_type, port_name,
                                    pin_number)
                        else:
                            if "_faulty" not in node:
                                node_name = node + "_xnor"
                                if alert:
                                    node_name = node + "_xnor_alert"
                                node_type = "xnor"
                                out_nodes_added.append(node_name)
                                self._add_xor_xnor_nodes(
                                    diff_graph_out_logic, node, pin_value,
                                    node_name, node_type, port_name,
                                    pin_number)
                        # Update the in_ports and out_ports of the node.
                        add_port = True
                        for out_port in diff_graph_out_logic.nodes[node][
                                "node"].out_ports:
                            if out_port.name == port_name:
                                out_port.pins.append(
                                    NodePin(number=int(pin_number), wire=""))
                                add_port = False
                                break
                        if add_port:
                            diff_graph_out_logic.nodes[node][
                                "node"].out_ports.append(
                                    NodePort(type="output",
                                             name=port_name,
                                             pins=[
                                                 NodePin(
                                                     number=int(pin_number),
                                                     wire="")
                                             ]))

        return out_nodes_added

    def _connect_outputs(self, diff_graph_out_logic, out_nodes, out_logic):
        """ Connect a list of nodes with an output node.

        Each node in the out_nodes list is connected with the output node
        of type out_logic.

        Args:
            diff_graph_out_logic: The differential graph.
            out_nodes: The nodes to connect.
            out_logic: The type of the node.

        Returns:
            The name of the new node.
        """
        # Flatten the list.
        out_nodes = [item for sublist in out_nodes for item in sublist]

        # Connect the outputs of the XNOR/XORs with an AND.
        out_name = "output_logic_" + out_logic
        diff_graph_out_logic.add_node(
            out_name, **{
                "node":
                Node(name=out_name,
                     parent_name=out_name,
                     type=out_logic,
                     in_ports=[NodePort(type="input", name="I", pins=[])],
                     out_ports=[
                         NodePort(type="output",
                                  name="O",
                                  pins=[NodePin(number=0, wire="")])
                     ],
                     stage="",
                     node_color="purple")
            })
        cntr = 1
        for out_node in out_nodes:
            diff_graph_out_logic.nodes[out_name]["node"].in_ports[
                0].pins.append(NodePin(number=cntr, wire=""))
            diff_graph_out_logic.add_edge(out_node,
                                          out_name,
                                          edge=Edge(in_port="A" + str(cntr),
                                                    in_pin=0,
                                                    out_port="O",
                                                    out_pin=0,
                                                    wire=""))
            cntr += 1

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
        fault_values = self.fault_model["output_fault_values"]
        out_and_nodes = []
        out_or_nodes = []
        # Add the output logic for the non-faulty output values.
        out_and_nodes.append(
            self._add_output(diff_graph_out_logic, diff_graph, output_values,
                             False, False, False))
        # Add the output logic for the faulty output values. If there are
        # expected fault values, connect them with an AND, else with an OR.
        if not fault_values:
            out_or_nodes.append(
                self._add_output(diff_graph_out_logic, diff_graph,
                                 output_values, True, False, False))
        else:
            out_and_nodes.append(
                self._add_output(diff_graph_out_logic, diff_graph,
                                 fault_values, True, False, True))
        if alert_values:
            # Add the output logic for the non-faulty output values.
            out_and_nodes.append(
                self._add_output(diff_graph_out_logic, diff_graph,
                                 alert_values, False, True, False))
            # Add the output logic for the faulty output values.
            out_and_nodes.append(
                self._add_output(diff_graph_out_logic, diff_graph,
                                 alert_values, True, True, False))

        # AND all output nodes (non-faulty, alert, expected fault values).
        and_output = self._connect_outputs(diff_graph_out_logic, out_and_nodes,
                                           "and")

        self._connect_outputs(diff_graph_out_logic, [[and_output]],
                              "terminate")

        # Connect the AND node with the terminate node.

        if not fault_values:
            # OR all faulty output nodes.
            or_output = self._connect_outputs(diff_graph_out_logic,
                                              out_or_nodes, "or")
            # Connect the output of the OR logic with the AND output logic.
            num_in_edges = 1
            for edge in diff_graph_out_logic.in_edges(and_output):
                num_in_edges += 1
            edge = Edge(in_port="A" + str(num_in_edges),
                        in_pin=0,
                        out_port="O",
                        out_pin=0,
                        wire="")
            diff_graph_out_logic.add_edge(or_output, and_output, edge=edge)

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
            solver = Lingeling()
            # Inject the faults into the target graph.
            faulty_graph = self._inject_faults(fault_location)

            # Create the differential graph.
            diff_graph = self._create_diff_graph(faulty_graph)

            # Transform the differential graph to a boolean formula
            formula_builder = FormulaBuilder(diff_graph, self.cell_lib, solver)
            solver = formula_builder.transform_graph()

            # Set one to logical one and  zero to logical zero.
            solver.add_clause([self.cell_lib.one])
            solver.add_clause([-self.cell_lib.zero])
            # Hand the boolean formula to the SAT solver.
            sat_result = solver.solve()
            # Invoke the garbage collector.
            del solver
            del formula_builder
            del faulty_graph
            del diff_graph
            gc.collect()
            # Append result.
            results.append(
                FIResult(fault_name=self.fault_name,
                         sat_result=sat_result,
                         fault_location=fault_location))

        return results
