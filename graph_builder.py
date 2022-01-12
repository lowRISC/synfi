# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import logging
import sys
from pathlib import Path

import networkx as nx

from helpers import Edge

"""Part of the fault injection framework for the OpenTitan.

This module provides functions to build the graph of the netlist.
"""

logger = logging.getLogger(__name__)


def add_nodes(nodes: dict, graph: nx.MultiDiGraph) -> None:
    """Add nodes to the graph.

    Args:
        nodes: The dict containing the node information.
        graph: The networkx graph.
    """
    for name, node in nodes.items():
        graph.add_node(name, **{"node": node})


def add_edges(nodes: dict, connections: list, wires: dict,
              graph: nx.MultiDiGraph) -> None:
    """Add edges to the graph.

    Args:
        nodes: The dict containing the node information.
        connections: The connection dependencies of the nodes.
        wires: The wires and their names.
        graph: The networkx graph.
    """

    for connection in connections:
        edge = Edge(in_port="",
                    in_pin=0,
                    out_port="",
                    out_pin=0,
                    wire=connection.wire)
        for in_port in nodes[connection.node_in].in_ports:
            if in_port.name == connection.port_in:
                for pin in in_port.pins:
                    if pin.wire == connection.wire:
                        edge.in_pin = pin.number
                        edge.in_port = in_port.name
                        break
        for out_port in nodes[connection.node_out].out_ports:
            for pin in out_port.pins:
                if pin.wire == connection.wire:
                    edge.out_pin = pin.number
                    edge.out_port = out_port.name
                    break

        if not edge.in_port or not edge.out_port:
            logger.error(
                f"Could not resolve connection between node {connection.node_out} and {connection.node_in}."
            )
            sys.exit()
        graph.add_edge(connection.node_out, connection.node_in, edge=edge)


def build_graph(nodes: dict, connections: list, wires: dict,
                graph: nx.MultiDiGraph) -> None:
    """Creates the graph of the circuit.

    Build graph by adding nodes and edges to the graph.

    Args:
        nodes: The dict containing the node information.
        connections: The connection dependencies of the nodes.
        wires: The wires and their names.
        graph: The networkx graph.
    """
    add_nodes(nodes, graph)
    add_edges(nodes, connections, wires, graph)


def write_dot_graph(graph: nx.MultiDiGraph, file_name: Path) -> None:
    """Dumps the graph of the circuit as a .dot file.

    Args:
        graph: The networkx graph.
        file_name: The filename.
    """

    DOT_INPUTS = """
        subgraph cluster_inputs {{
            label="Inputs";
            {dot_inputs}
        }}"""

    DOT_CIRCUIT = """
        subgraph cluster_circuit {{
            label="Circuit";
            {dot_circuit}
        }}"""

    DOT_FAULTY_CIRCUIT = """
        subgraph cluster_faulty_circuit {{
            label="Faulty Circuit";
            {dot_faulty_circuit}
        }}"""

    DOT_OUTPUTS = """
        subgraph cluster_outputs {{
            label="Outputs";
            {dot_outputs}
        }}"""

    DOT = """
        strict digraph  {{
            {dot}
        }}
    """

    inputs_list = []
    circuit_list = []
    faulty_circuit_list = []
    outputs_list = []

    dot = ""

    for edge_in, edge_out, edge_data in graph.edges(data=True):
        if "node" in graph.nodes[edge_in] and graph.nodes[edge_out]:
            src_cell = graph.nodes[edge_in]["node"]
            src_str = "\"%s_%s\"" % (src_cell.type, src_cell.name)
            src_color = src_cell.node_color
            if src_color != "black":
                dot += "%s [color = %s];\n" % (src_str, src_color)

            dst_cell = graph.nodes[edge_out]["node"]
            dst_str = "\"%s_%s\"" % (dst_cell.type, dst_cell.name)
            dst_color = dst_cell.node_color
            if dst_color != "black":
                dot += "%s [color = %s];\n" % (dst_str, dst_color)
            wire_name = "\"%s\"" % (edge_data["edge"].wire)

            if src_cell.type == "input":
                inputs_list.append((src_str, dst_str, wire_name))
            elif src_cell.type == "output_pin":
                outputs_list.append((src_str, dst_str, wire_name))
            elif "_faulty" in src_cell.name:
                faulty_circuit_list.append((src_str, dst_str, wire_name))
            else:
                circuit_list.append((src_str, dst_str, wire_name))

    dot_inputs = [
        f"  {src} -> {dst} [ label={name}];" for src, dst, name in inputs_list
    ]
    dot += DOT_INPUTS.format(dot_inputs="\n".join(dot_inputs))

    dot_circuit = [
        f"  {src} -> {dst} [ label={name}];" for src, dst, name in circuit_list
    ]
    dot += DOT_CIRCUIT.format(dot_circuit="\n".join(dot_circuit))

    dot_faulty_circuit = [
        f"  {src} -> {dst} [ label={name}];"
        for src, dst, name in faulty_circuit_list
    ]
    dot += DOT_FAULTY_CIRCUIT.format(
        dot_faulty_circuit="\n".join(dot_faulty_circuit))

    dot_outputs = [
        f"  {src} -> {dst} [ label={name}];" for src, dst, name in outputs_list
    ]
    dot += DOT_OUTPUTS.format(dot_outputs="\n".join(dot_outputs))

    output_dot = DOT.format(dot=dot)

    with open(file_name, "w") as f:
        f.write(output_dot)
