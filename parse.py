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
from helpers import Connection, Node, NodePin, NodePort, Port

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
    for port_name, value in module["ports"].items():
        length = len(value["bits"])
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
    corresponding node. Each node consists of input and output ports.
    To track the dependencies between nodes, this function consists of the
    two dicts in_wires and out_wires which are later used to find the
    dependencies between two nodes.

    Args:
        module: The selected module.

    Returns:
        Dict containing all parsed nodes, the in_wires, and the out_wires.
    """

    nodes = {}
    in_wires = DefaultDict(list)
    out_wires = {}
    # Loop over all nodes and add to the nodes dict.
    for node_name, node in module["cells"].items():
        node_type = node["type"]
        in_ports = []
        out_ports = []
        # Loop over all ports of the current node.
        for port_name, connections in node["connections"].items():
            pins = []
            pin_count = 0
            port_direction = node["port_directions"][port_name]
            # Loop over all pins of the current port.
            for wire in node["connections"][port_name]:
                pin = NodePin(number=pin_count, wire=wire)
                pins.append(pin)
                if port_direction == "input":
                    in_wires[wire].append(node_name)
                else:
                    out_wires[wire] = node_name
                pin_count += 1
            # Set the port direction and add the port to the node.
            if (node["port_directions"][port_name] == "input"):
                in_ports.append(
                    NodePort(type="input", name=port_name, pins=pins))
            else:
                out_ports.append(
                    NodePort(type="output", name=port_name, pins=pins))

        # Add the node to the dict.
        nodes[node_name] = Node(name=node_name,
                                parent_name=node_name,
                                type=node_type,
                                in_ports=in_ports,
                                out_ports=out_ports,
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
        Connections in the format (node_in, node_out, wire).
    """

    connections = []
    for out_wire, node_name in out_wires.items():
        if (out_wire in in_wires):
            for node in in_wires[out_wire]:
                connections.append(
                    Connection(node_in=node, node_out=node_name,
                               wire=out_wire))

    return connections


def add_ports(ports: dict, nodes: dict, in_wires: dict,
              out_wires: dict) -> None:
    """Add the module ports to the dict of nodes.

    Args:
        ports: The parsed ports.
        in_wires: The auxiliary dict to track the input wires.
        out_wires: The auxiliary dict to track the output wires. 
    """
    # Loop over all in/out ports of the module and add to the node dict.
    for port_name, port in ports.items():
        in_ports = []
        out_ports = []
        pins = []
        pin_count = 0
        # Add the in/out connections of the current port.
        for pin_wire in port.pins:
            pin = NodePin(number=pin_count, wire=pin_wire)
            pins.append(pin)
            pin_count += 1
            if port.type == "input":
                out_wires[pin_wire] = port_name
                out_ports.append(
                    NodePort(type="output", name=port_name, pins=pins))
            else:
                in_wires[pin_wire].append(port_name)
                in_ports.append(
                    NodePort(type="input", name=port_name, pins=pins))
        # Add the port to the dict.
        nodes[port_name] = Node(name=port_name,
                                parent_name=port_name,
                                type=port.type,
                                in_ports=in_ports,
                                out_ports=out_ports,
                                stage="",
                                node_color="black")


def add_nodes(module: dict, ports: dict) -> Tuple[list, dict]:
    """Parses the nodes and creates the dependencies between them.

    Reads the nodes of the module in the JSON file and adds them to th
    node dict. Determines the dependencies between the nodes.

    Args:
        module: The selected module.
        ports: The parsed ports.

    Returns:
        Dict containing all nodes and the connection list.
    """
    # Node storage dict.
    nodes = {}
    # Auxiliary variables used to connect the nodes.
    in_wires = DefaultDict(list)
    out_wires = {}

    # Read the netlist and add nodes.
    nodes, in_wires, out_wires = parse_nodes(module)

    # Create pins for each port and add to dict of nodes.
    add_ports(ports, nodes, in_wires, out_wires)

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


def parse_arguments(argv):
    """ Command line argument parsing.
    Args:
        argv: The command line arguments.

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
    args = parser.parse_args(argv)

    if args.version:
        helpers.show_and_exit(__file__, ["networkx", "numpy", "pathlib"])

    return args


def write_circuit(graph: nx.MultiDiGraph,
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


def test_main():
    """ Pytest function.

    """
    res = main([
        "-j", "examples/circuit.json", "-m", "aes_cipher_control", "-o",
        "circuit.pickle"
    ])


def main(argv=None):
    # Configure the logger.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logger.addHandler(console)

    tstp_begin = time.time()
    args = parse_arguments(argv)

    graph = nx.MultiDiGraph()

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
    main()
