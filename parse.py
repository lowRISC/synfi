#!/usr/bin/env python3
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import logging
import pickle
import time
from pathlib import Path
from typing import DefaultDict, Tuple

import networkx as nx

import graph_builder
import helpers
from helpers import Node, Port

"""Part of the fault injection framework for the OpenTitan.

This tool parses the JSON netlist created by Yosys or Synopsys and creates
a graph, which is later used for the fault injections.

Typical usage:
>>> ./parse.py -j examples/circuit.json -m aes_cipher_control 
               -o output/circuit.pickle
"""


def parse_ports(module: dict) -> dict:
    """Parses the input and output ports of the selected module.
    
    Args:
        module: The selected module.
    
    Returns:
        Dict containing all ports.
    """
    ports = {}
    for port, value in module["ports"].items():
        length = len(value["bits"])
        port_name = port + "(" + str(length) + ")"
        port = Port(name=port_name,
                    pins=value["bits"],
                    type=value["direction"],
                    length=length)
        ports[port_name] = port

    return ports


def parse_wires(module: dict) -> dict:
    """Parses the netnames of the selected module.
        
    Args:
        module: The selected module.
    
    Returns:
        Dict containing all wires.
    """
    wires = DefaultDict(list)
    for net, value in module["netnames"].items():
        for bit in value["bits"]:
            if bit != (0 or "x"): wires[bit].append(net + "_" + str(bit))
    return wires


def parse_nodes(module: dict) -> dict:
    """Parses the nodes of the selected module.

    Iterates over all nodes in the module and sets the properties of the
    corresponding node. Each node consists of inputs and outputs in the format:
    node = [{input,output}, port_name, wire_name]
    e.g.:
    node_reg = [input, D, reg_d]
    To track the dependencies between nodes, this function consists of the 
    two dicts in_wires and out_wires. These dicts are in the format:
    in_wires[reg_d] = [node_reg]
    and are later used to find the dependencies between two nodes.

    Args:
        module: The selected module.
    
    Returns:
        Dict containing all parsed nodes, the in_wires, and the out_wires.
    """

    nodes = {}
    in_wires = DefaultDict(list)
    out_wires = {}

    for name, node in module["cells"].items():
        node_type = node["type"]
        nodes_in = {}
        nodes_out = {}

        for port, connection in node["connections"].items():
            if (node["port_directions"][port] == "input"):
                nodes_in[connection[0]] = port
                in_wires[connection[0]].append(name)
            else:
                nodes_out[connection[0]] = port
                out_wires[connection[0]] = name

        nodes[name] = Node(name=name,
                           parent_name=name,
                           type=node_type,
                           inputs=nodes_in,
                           outputs=nodes_out,
                           stage="",
                           node_color="black")

    return (nodes, in_wires, out_wires)


def create_connections(in_wires: dict, out_wires: dict) -> list:
    """Creates the connection list for the nodes.

    The dependencies between two nodes are created using the dicts in_wires
    and out_wires. If a node is in both dicts, we connect them.

    Args:
        in_wires: Input wires of a node. in_wires[wire_name] = node_name
        out_wires: Output wires of a node. out_wires[wire_name] = node_name
    
    Returns:
        Connections in the format (node1, node2, wire_name).
    """

    connections = []
    for out_wire, node_name in out_wires.items():
        if (out_wire in in_wires):
            for node in in_wires[out_wire]:
                connections.append((node_name, node, out_wire))

    return connections


def add_pins(ports: dict, nodes: dict, in_wires: dict,
             out_wires: dict) -> None:
    """Adds pins to the list of nodes.

    A port(N) consists of N 1-bit pins. For each of these pins, this
    function creates a new node and connects the pin with the port.
        
    Args:
        ports: The parsed ports.
    """

    for port_name, port in ports.items():
        port_in_pin = {}
        port_out_pin = {}
        for pin in port.pins:
            pin_name = port_name + "_" + str(pin)
            wire_name = "wire_" + port_name + "_" + str(pin)
            # The inputs and outputs of the pin node.
            if port.type == "input":
                in_wires[wire_name].append(pin_name)
                out_wires[pin] = pin_name
                out_wires[wire_name] = port_name
                inp_pin = wire_name
                outp_pin = pin
                port_out_pin[wire_name] = "O"
            else:
                in_wires[pin].append(pin_name)
                out_wires[wire_name] = pin_name
                in_wires[wire_name].append(port_name)
                inp_pin = pin
                outp_pin = wire_name
                port_in_pin[wire_name] = "I1"
            # Add pin to node dict.
            nodes[pin_name] = Node(name=pin_name,
                                   parent_name=pin_name,
                                   type=port.type,
                                   inputs={inp_pin: "I1"},
                                   outputs={outp_pin: "O"},
                                   stage="",
                                   node_color="black")
        # Add port to node dict.
        nodes[port_name] = Node(name=port_name,
                                parent_name=port_name,
                                type=port.type,
                                inputs=port_in_pin,
                                outputs=port_out_pin,
                                stage="",
                                node_color="black")


def add_nodes(module: dict, ports: dict) -> Tuple[list, dict]:
    """Parses the nodes and creates the dependencies between them.

    Reads the nodes of the module in the JSON file and adds them to the 
    node dict. Determines the dependencies between the nodes.

    Args:
        module: The selected module.
        ports: The parsed ports.
    
    Returns:
        Dict containing all nodes and the connection list.
    """

    nodes = {}
    in_wires = DefaultDict(list)
    out_wires = {}

    # Add null/one nodes for gates with a 0/1 as input.
    nodes["null"] = Node("null", "null", "null_node", {}, {'0': "O"}, "",
                         "black")
    out_wires['0'] = "null"
    nodes["one"] = Node("one", "one", "one_node", {}, {'1': "O"}, "", "black")
    out_wires['1'] = "one"

    # Read the netlist and add nodes.
    nodes, in_wires, out_wires = parse_nodes(module)

    # Create pins for each port and add to dict of nodes.
    add_pins(ports, nodes, in_wires, out_wires)

    # Connect the nodes.
    connections = create_connections(in_wires, out_wires)

    return (connections, nodes)


def open_module(args) -> dict:
    """ Opens the JSON netlist.
    
    Args:
        args: The input arguments.
    
    Returns:
        The selected module of the netlist.
    """
    module = None
    with open(args.netlist, "r") as circuit_json_file:
        circuit_json = json.load(circuit_json_file)
        module = circuit_json["modules"][args.module]
    return module


def parse_arguments():
    """ Command line argument parsing.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Parse")
    parser.add_argument("-j",
                        "--json",
                        dest="netlist",
                        type=helpers.ap_check_file_exists,
                        required=True,
                        help="Path of the json netlist")
    parser.add_argument("--version",
                        action="store_true",
                        help="Show version and exit.")
    parser.add_argument("--debug",
                        action="store_true",
                        help="Write graph as a .dot file")
    parser.add_argument("-m",
                        "--module",
                        dest="module",
                        required=True,
                        help="The module to analyze")
    parser.add_argument("-o",
                        "--output",
                        dest="outfile",
                        type=helpers.ap_check_dir_exists,
                        required=True,
                        help="The output graph file")
    args = parser.parse_args()

    if args.version:
        helpers.show_and_exit(__file__, ["networkx", "numpy", "pathlib"])

    return args


def write_circuit(graph: nx.DiGraph,
                  outfile: Path,
                  debug: bool = False) -> None:
    """ Writes the circuit to a pickle file.

    Args:
        graph: The graph of the netlist.
        outfile: The pathlib file path.
        debug: If true, write the graph to a .dot file.
    """
    file_name = outfile.with_suffix('.dot')
    if debug: graph_builder.write_dot_graph(graph, file_name)
    with open(outfile, "wb") as f:
        pickle.dump(graph, f)


def main():
    tstp_begin = time.time()
    args = parse_arguments()

    graph = nx.DiGraph()

    # Open the JSON netlist, parse the module, the ports, and the wires.
    module = open_module(args)
    ports = parse_ports(module)
    wires = parse_wires(module)
    helpers.print_ports(ports)

    # Parse nodes, create connections between them, and build the graph.
    connections, nodes = add_nodes(module, ports)
    graph_builder.build_graph(nodes, connections, wires, graph)
    helpers.print_graph_stat(graph)

    # Write the circuit to the output directory in the pickle format.
    write_circuit(graph, args.outfile, args.debug)

    tstp_end = time.time()
    logger.info("parse.py successful (%.2fs)." % (tstp_end - tstp_begin))


if __name__ == "__main__":
    # Configure the logger.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logger.addHandler(console)
    main()
