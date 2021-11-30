# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import networkx as nx
import numpy as np
import pkg_resources

"""Part of the fault injection framework for the OpenTitan.

This module provides common helper functions used by different modules.
"""

logger = logging.getLogger(__name__)

TERMINAL_COLS = shutil.get_terminal_size((80, 20)).columns
header = "-" * int(TERMINAL_COLS)


@dataclass
class InputPin:
    """ InputPin data class.

    Used by the cell library and the formula builder to describe an input pin
    of a given node.

    """
    node: str
    name: int


@dataclass
class FIResult:
    """ FI data class.

    A result consisting of the fault name, the sat_result, and the fault
    location for a fault injection.
    Used by the Injector Class and the FI Injector module.

    """
    fault_name: str
    sat_result: bool
    fault_location: np.ndarray


def show_and_exit(clitool: str, packages: str) -> None:
    util_path = Path(clitool).resolve().parent
    os.chdir(util_path)
    ver = subprocess.run(
        ["git", "describe", "--always", "--dirty", "--broken"],
        stdout=subprocess.PIPE).stdout.strip().decode('ascii')
    if (ver == ''):
        ver = 'not found (not in Git repository?)'
    sys.stderr.write(clitool + " Git version " + ver + '\n')
    for p in packages:
        sys.stderr.write(p + ' ' + pkg_resources.require(p)[0].version + '\n')
    exit(0)


@dataclass
class Node:
    """ Node class.

    A node represents an element (gate, ...) in the circuit.

    """
    name: str
    parent_name: str
    type: str
    inputs: dict
    outputs: dict
    stage: str
    node_color: str


@dataclass
class Port:
    """ Node class.

    An input or output node of the circuit.

    """
    name: str
    pins: str
    type: str
    length: int


def rename_nodes(graph: nx.DiGraph, suffix: str,
                 ignore_inputs: bool) -> nx.DiGraph:
    """ Rename all nodes of the graph by appending a suffix.

    Args:
        graph: The networkx digraph of the circuit.
        suffix: The suffix, which is appended to the original node name.
        ignore_inputs: Do not rename input nodes.
    Returns:
        The subgraph with the renamed nodes.
    """
    name_mapping = {}
    for node, node_attribute in graph.nodes(data=True):
        if ignore_inputs:
            if (node_attribute["node"].type != "input"):
                name_mapping[node] = node + suffix
                node_attribute[
                    "node"].name = node_attribute["node"].name + suffix
        else:
            name_mapping[node] = node + suffix
            node_attribute["node"].name = node_attribute["node"].name + suffix
    graph = nx.relabel_nodes(graph, name_mapping)

    return graph


def print_graph_stat(graph: nx.DiGraph) -> None:
    """Prints the type and number of gates in the circuit.

    Args:
        graph: The netlist of the circuit.
    """

    gates = []
    for node in graph.nodes().values():
        if "node" in node: gates.append(node["node"].type)

    gates, number = np.unique(gates, return_counts=True)
    for cnt in range(0, len(gates)):
        logger.info(gates[cnt] + ": " + str(number[cnt]))
    logger.info(header)


def ap_check_file_exists(file_path: str) -> Path:
    """Verifies that the provided file path is valid

    Args:
        file_path: The file path.

    Returns:
        The file path.
    """
    path = Path(file_path)
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"File {path} does not exist")
    return path


def ap_check_dir_exists(path: str) -> Path:
    """Verifies that the provided path is valid

    Args:
        path: The path.

    Returns:
        The file path.
    """
    path = Path(path)
    if not path.parent.exists():
        raise argparse.ArgumentTypeError(f"Path {path.parent} does not exist")
    return path


def print_ports(ports: dict) -> None:
    """
    Prints the input and output ports of the selected module.
    """
    in_string = "Inputs:  "
    out_string = "Outputs: "
    for port_name, port in ports.items():
        if port.type == "input":
            in_string += port_name + " "
        else:
            out_string += port_name + " "
    logger.info(header)
    logger.info(in_string)
    logger.info(out_string)
    logger.info(header)
