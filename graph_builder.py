# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import networkx as nx

"""Part of the fault injection framework for the OpenTitan.

This module provides functions to build the graph of the netlist.
"""


def add_nodes(nodes: dict, graph: nx.DiGraph) -> None:
    """Add nodes to the graph.

    Args:
        nodes: The dict containing the node information.
        graph: The networkx graph.
    """
    for name, node in nodes.items():
        graph.add_node(name, **{"node": node})


def add_edges(nodes: dict, connections: list, wires: dict,
              graph: nx.DiGraph) -> None:
    """Add edges to the graph.

    Args:
        nodes: The dict containing the node information.
        connections: The connection dependencies of the nodes.
        wires: The wires and their names.
        graph: The networkx graph.
    """

    for connection in connections:
        wire = connection[2]
        wire_name = wires[wire]
        out_pin = nodes[connection[0]].outputs[wire]
        in_pin = nodes[connection[1]].inputs[wire]
        # If the edge is already in the graph, add multiple input and outputs
        # to the edge attribute. Happens when a node_1 has multiple outputs
        # (e.g. Q, QN) which are connected to multiple inputs of node_2.
        if graph.has_edge(connection[0], connection[1]):
            if out_pin != graph[connection[0]][connection[1]]["out_pin"]:
                out_pin_new = []
                out_pin_new.append(out_pin)
                out_pin_new.append(graph[connection[0]][connection[1]]["out_pin"])
                graph[connection[0]][connection[1]]["out_pin"] = out_pin_new
            if in_pin != graph[connection[0]][connection[1]]["in_pin"]:
                in_pin_new = []
                in_pin_new.append(in_pin)
                in_pin_new.append(graph[connection[0]][connection[1]]["in_pin"])
                graph[connection[0]][connection[1]]["in_pin"] = in_pin_new
        else:
            graph.add_edge(connection[0],
                           connection[1],
                           name=wire_name,
                           out_pin=out_pin,
                           in_pin=in_pin)


def build_graph(nodes: dict, connections: list, wires: dict,
                graph: nx.DiGraph) -> None:
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


def write_dot_graph(graph: nx.DiGraph, file_name: Path) -> None:
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

    for edge in graph.edges():
        if "node" in graph.nodes[edge[0]] and graph.nodes[edge[1]]:
            src_cell = graph.nodes[edge[0]]["node"]
            src_str = "\"%s_%s\"" % (src_cell.type, src_cell.name)
            src_color = src_cell.node_color
            if src_color != "black":
                dot += "%s [color = %s];\n" % (src_str, src_color)

            dst_cell = graph.nodes[edge[1]]["node"]
            dst_str = "\"%s_%s\"" % (dst_cell.type, dst_cell.name)
            dst_color = dst_cell.node_color
            if dst_color != "black":
                dot += "%s [color = %s];\n" % (dst_str, dst_color)
            wire_name = "\"%s\"" % (graph.get_edge_data(edge[0],
                                                        edge[1])["name"])

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
