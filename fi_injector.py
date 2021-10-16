#!/usr/bin/env python3

import argparse
import copy
import itertools
import json
import os
import pickle
import time

import networkx as nx
import ray

import graph_builder
import helpers

"""Part of the fault injection framework for the OpenTitan.

This tool injects faults into the graph created with the parser and evaluates
the effectiveness and if the countermeasure detects these faults.

Typical usage:
>>> ./python3 fi_injector.py -p output/circuit.pickle -f examples/fault_model.json
"""


def parse_arguments():
    """ Command line argument parsing.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Parse")
    parser.add_argument("-f",
                        "--fault_model",
                        dest="fault_model",
                        type=helpers.ap_check_file_exists,
                        required=True,
                        help="Path of the fault model json file")
    parser.add_argument("-p",
                        "--pickle",
                        dest="circuit_pickle",
                        type=helpers.ap_check_file_exists,
                        required=True,
                        help="Path of the circuit in pickle format")
    parser.add_argument("--debug",
                        action="store_true",
                        help="Write intermediate graphs as .dot files")
    parser.add_argument("--version",
                        action="store_true",
                        help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        helpers.show_and_exit(__file__, ["networkx", "numpy", "ray"])

    return args


def open_fi_models(args):
    """ Opens the JSON fault model.
    
    Args:
        args: The input arguments.
    
    Returns:
        The fault model.
    """
    fi_model_json_file = open(args.fault_model, "r")
    fi_model_json = json.load(fi_model_json_file)
    fi_model_json_file.close()
    fi_models = fi_model_json["fimodels"]
    return fi_models


def read_circuit(graph, args):
    """ Opens the circuit in the pickle file.
    
    Args:
        graph: The networkx digraph.
        args: The input arguments.
    
    Returns:
        The graph stored in the pickle file.
    """
    with open(args.circuit_pickle, 'rb') as f:
        graph = pickle.load(f)
    return graph


def fault_combinations(graph, fi_model):
    """ Calculates all possible fault location combinations based on the model.

    The fault model contains a list of fault targets (gates), the fault mapping
    (e.g., NAND->AND), and the number of simultaneous faults. This function
    generates a list of all possible combinations of these parameters.
    
    Args:
        graph: The networkx digraph of the circuit.
        fi_model: The active fault model
    
    Returns:
        A list containing all fault locations and the corresponding gates.
    """
    simultaneous_faults = fi_model["simultaneous_faults"]
    fault_locations = fi_model["fault_locations"]
    fault_mapping = fi_model["node_fault_mapping"]

    fault_combinations = []
    # Receive all possible fault location combinations using itertools.
    for faulty_nodes in itertools.combinations(fault_locations,
                                               simultaneous_faults):
        faulty_nodes_mapping = []
        # For each fault location combination, loop over all fault mappings.
        for fault_node in faulty_nodes:
            if fault_node in graph.nodes:
                gate_type = graph.nodes[fault_node]["node"].type
                gate_mapping = fault_mapping[gate_type]
                faulty_node_mapping = []
                for gate in gate_mapping:
                    faulty_node_mapping.append((fault_node, gate))
                faulty_nodes_mapping.append(faulty_node_mapping)
            else:
                print("Err: Node " + fault_node + " not found in graph.")
        # Calculate the cartesian product.
        combinations_for_faulty_nodes = list(
            itertools.product(*faulty_nodes_mapping))
        fault_combinations.append(combinations_for_faulty_nodes)
    # Flatten the list and return.
    return [item for sublist in fault_combinations for item in sublist]


def extract_graph_between_nodes(graph, node_in, node_out):
    """ Extract the subgraph between two nodes.
    
    Args:
        graph: The networkx digraph of the circuit.
        node_in: The input node.
        node_out: The output node.
    Returns:
        The subgraph between node_in and node_out.
    """
    # Create a subgraph between in_node and out_node excluding other registers.
    registers = helpers.get_registers(graph)
    nodes_exclude = [
        reg["node"].name for reg in registers
        if reg["node"].name != (node_in or node_out)
    ]
    sub_graph = nx.subgraph_view(graph,
                                 filter_node=lambda n: n in
                                 [node_in, node_out] or n not in nodes_exclude)

    # Find all pathes between in_node and out_node and create the new graph.
    if node_in == node_out:
        paths_between_generator = nx.simple_cycles(sub_graph)
    else:
        paths_between_generator = nx.all_simple_paths(sub_graph,
                                                      source=node_in,
                                                      target=node_out)
    nodes_between_set = {
        node
        for path in paths_between_generator for node in path
    }
    graph_in_out_node = nx.DiGraph(graph.subgraph(nodes_between_set))

    return graph_in_out_node


def extract_graph(graph, fi_model):
    """ Extract the subgraph containing all comb. and seq. logic of interest. 

    The subgraphs between all input and output nodes defined in the fault model
    are created and merged into the extracted graph.
    
    Args:
        graph: The networkx digraph of the circuit.
        fi_model: The active fault model.
    Returns:
        The extracted subgraph of the original graph.
    """
    print("Extracting the target graph...")

    extracted_graphs = []

    # Extract all graphs between the given nodes.
    for node_in in fi_model["nodes_in"]:
        for node_out in fi_model["nodes_out"]:
            extracted_graphs.append(
                extract_graph_between_nodes(graph, node_in, node_out))

    # Merge all graphs into the target graph.
    extracted_graph = nx.compose_all(extracted_graphs)

    print(helpers.header)
    return extracted_graph


def handle_fault_model(graph, fi_model_name, fi_model):
    """ Handles each fault model of the fault model specification file.

    This function first extracts the target sub graph of the main circuit. Then,
    for all possible fault locations in the target graph, the fault is injected,
    the boolean formula is created, and the fault is evaluated using a SAT
    solver.
    
    Args:
        graph: The networkx digraph of the circuit.
        fi_model_name: The name of the active fault model.
        fi_model: The active fault model
    """

    # Extract the target graph from the circuit.
    target_graph = extract_graph(graph, fi_model)

    # Determine all possible fault location combinations.
    fault_locations = fault_combinations(graph, fi_model)


def main():
    tstp_begin = time.time()
    args = parse_arguments()

    # Open the fault model and the graph.
    fi_models = open_fi_models(args)
    graph = nx.DiGraph()
    graph = read_circuit(graph, args)

    # Handle each fault model.
    for fi_model_name, fi_model in fi_models.items():
        handle_fault_model(graph, fi_model_name, fi_model)

    tstp_end = time.time()
    print("fi_injector.py successful (%.2fs)" % (tstp_end - tstp_begin))


if __name__ == "__main__":
    main()
