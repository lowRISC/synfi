import argparse
import os
import subprocess
import sys

import numpy as np
import pkg_resources

header = "----------------------------"


def show_and_exit(clitool, packages):
    util_path = os.path.dirname(os.path.realpath(clitool))
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


class Node:
    """Class for a node in the circuit."""
    def __init__(self, name, parent_name, type, inputs, outputs, node_color):
        self.name = name
        self.parent_name = parent_name
        self.type = type
        self.inputs = inputs
        self.outputs = outputs
        self.node_color = node_color


class Port:
    """Class for a input or output node in the circuit."""
    def __init__(self, name, pins, type, length):
        self.name = name
        self.pins = pins
        self.type = type
        self.length = length


def print_graph_stat(graph):
    """Prints the type and number of gates in the circuit.

    Args:
        graph: The netlist of the circuit.
    """
    gates = []
    for node in graph.nodes().values():
        if "node" in node: gates.append(node["node"].type)

    gates, number = np.unique(gates, return_counts=True)
    for cnt in range(0, len(gates)):
        print(gates[cnt] + ": " + str(number[cnt]))
    print(header)


def get_registers(graph):
    """Finds all registers in the graph.

    Currently, the register names (e.g. DFFR_X1) need to be manually added.
    In a future version, the register names should be fetched from a config
    file.

    Args:
        graph: The netlist of the circuit.

    Returns:
        List of all register names.    
    """
    registers = []
    for node in graph.nodes().values():
        if ("node" in node) and (node["node"].type == ("DFFR_X1"
                                                       or "DFFS_X1")):
            registers.append(node)
    return registers


def ap_check_file_exists(file_path):
    """Verifies that the provided file path is valid

    Args:
        file_path: The file path.

    Returns:
        The file path.   
    """
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError("File '%s' does not exist" %
                                         file_path)
    return file_path


def ap_check_dir_exists(path):
    """Verifies that the provided path is valid

    Args:
        path: The path.

    Returns:
        The file path.   
    """
    if not os.path.exists(os.path.dirname(path)):
        raise argparse.ArgumentTypeError("Path '%s' does not exist" %
                                         os.path.dirname(path))
    return path


def print_ports(ports):
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
    print(header)
    print(in_string)
    print(out_string)
    print(header)
