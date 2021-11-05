#!/usr/bin/env python3
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import argparse
import copy
import itertools
import json
import logging
import pickle
import time
from typing import DefaultDict, Tuple

import networkx as nx
import numpy
import ray

import helpers
from helpers import Node
from injector_class import FiInjector

"""Part of the fault injection framework for the OpenTitan.

This tool injects faults into the graph created with the parser and evaluates
the effectiveness and if the countermeasure detects these faults.

Typical usage:
>>> ./fi_injector.py -p output/circuit.pickle -f examples/fault_model.json -n 16
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
    parser.add_argument("-n",
                        "--num_cores",
                        dest="num_cores",
                        type="int",
                        required=True,
                        help="Number of cores to use")
    parser.add_argument("--debug",
                        action="store_true",
                        help="Write intermediate graphs as .dot files")
    parser.add_argument("--version",
                        action="store_true",
                        help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        helpers.show_and_exit(__file__, ["networkx", "numpy", "ray", "sympy"])

    return args


def open_fi_models(args) -> dict:
    """ Opens the JSON fault model.
    
    Args:
        args: The input arguments.
    
    Returns:
        The fault model.
    """
    with open(args.fault_model, 'r') as f:
        fi_models = json.load(f)
    return fi_models["fimodels"]


def read_circuit(graph: nx.DiGraph, args) -> nx.DiGraph:
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


def fault_combinations(graph: nx.DiGraph, fi_model: dict) -> list:
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
                logger.error(f"Err: Node {fault_node} not found in graph.")
        # Calculate the cartesian product.
        combinations_for_faulty_nodes = list(
            itertools.product(*faulty_nodes_mapping))
        fault_combinations.append(combinations_for_faulty_nodes)
    # Flatten the list and return.
    return [item for sublist in fault_combinations for item in sublist]


def extract_graph_between_nodes(graph: nx.DiGraph, node_in: str, node_out: str,
                                stage: str) -> nx.DiGraph:
    """ Extract the subgraph between two nodes.
    
    Args:
        graph: The networkx digraph of the circuit.
        node_in: The input node.
        node_out: The output node.
        stage: The current stage.
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
    graph_in_out_node = graph.subgraph(nodes_between_set)

    for node, attribute in graph_in_out_node.nodes(data=True):
        attribute["node"].stage = stage

    return graph_in_out_node


def reconnect_node(graph: nx.DiGraph, node: str, node_new: str,
                   in_out: str) -> nx.DiGraph:
    """ Reconnect a node in the graph.

    Reconnects the node "node" in the graph by removing the input/output edges
    and add a new edge for the node "node_new".
    
    Args:
        graph: The networkx digraph of the circuit.
        node: The node to be reconnected.
        node_new: The new node.
        in_out: Replace input or output edge?
    Returns:
        The subgraph with the reconnected node.
    """
    remove_edges = []

    if in_out == "out":
        # Find all output edges of node.
        for edge in graph.out_edges(graph.nodes[node]["node"].name):
            remove_edges.append((edge[0], edge[1]))
        # Remove the output edges and reconnect with the new node.
        for remove_edge in remove_edges:
            edge_data = graph.get_edge_data(remove_edge[0], remove_edge[1])
            graph.remove_edge(remove_edge[0], remove_edge[1])
            graph.add_edge(node_new,
                           remove_edge[1],
                           name=(edge_data["name"]),
                           out_pin=(edge_data["out_pin"]),
                           in_pin=(edge_data["in_pin"]))
    else:
        #find input edges of register_node and add to list
        for edge in graph.in_edges(graph.nodes[node]["node"].name):
            remove_edges.append((edge[0], edge[1]))

        for remove_edge in remove_edges:
            edge_data = graph.get_edge_data(remove_edge[0], remove_edge[1])
            graph.remove_edge(remove_edge[0], remove_edge[1])
            graph.add_edge(remove_edge[0],
                           node_new,
                           name=(edge_data["name"]),
                           out_pin=(edge_data["out_pin"]),
                           in_pin=(edge_data["in_pin"]))

    return graph


def set_in_out_nodes(graph: nx.DiGraph, node_in: str, node_out: str,
                     rename_string: str, fi_model: dict,
                     stage: str) -> nx.DiGraph:
    """ Add the input and output nodes of the subgraph. 
    
    Args:
        graph: The networkx digraph of the circuit.
        node_in: The input node.
        node_out: The output node.
        rename_string: The suffix, which is appended to the original node name.
        fi_model: The fault model.
        stage: The current stage.
    Returns:
        The subgraph with the input and output nodes.
    """

    # Get the input and output ports defined in the fault model.
    input_nodes = []
    output_nodes = []

    for output_node in fi_model["output_values"]:
        output_nodes.append(output_node)

    for output_node in fi_model["alert_values"]:
        output_nodes.append(output_node)

    for input_node in fi_model["input_values"]:
        input_nodes.append(input_node)

    # Set the type of the node.
    # If the node is in the input/output stage and in the input/output list,
    # set type to input/output.
    stage_type = fi_model["stages"][stage]["type"]
    if (node_in in input_nodes) and (stage_type == "input"):
        in_node_type = "input"
        in_color = "pink"
    else:
        in_node_type = "in_node"
        in_color = "brown"

    if node_out in output_nodes and (stage_type == "output"):
        out_node_type = "output"
        out_color = "grey"
    else:
        out_node_type = "out_node"
        out_color = "yellow"

    # Name of the node including suffix.
    node_in_name = node_in + rename_string
    node_out_name = node_out + rename_string
    if (node_in_name not in graph) or (node_out_name not in graph):
        return graph

    if node_in == node_out:
        # If we have a common in/out node, split this node into two nodes.
        node_in_name_mod = node_in + "_in" + rename_string
        node_out_name_mod = node_out + "_out" + rename_string
        graph.add_node(
            node_in_name_mod, **{
                "node":
                Node(node_in_name_mod, node_in, in_node_type, {}, {}, stage,
                     in_color)
            })
        graph.add_node(
            node_out_name_mod, **{
                "node":
                Node(node_out_name_mod, node_out, out_node_type, {}, {}, stage,
                     out_color)
            })
        graph.nodes[node_in_name_mod]["node"].outputs = graph.nodes[
            node_in_name]["node"].outputs
        graph.nodes[node_in_name_mod]["node"].inputs = graph.nodes[
            node_in_name]["node"].inputs
        graph.nodes[node_out_name_mod]["node"].inputs = graph.nodes[
            node_out_name]["node"].inputs
        graph.nodes[node_out_name_mod]["node"].outputs = graph.nodes[
            node_out_name]["node"].outputs
        # Connect the new nodes with the corresponding edges.
        graph = reconnect_node(graph, node_in_name, node_in_name_mod, "out")
        graph = reconnect_node(graph, node_out_name, node_out_name_mod, "in")
    else:
        # Set type and color of the input and output node.
        graph.nodes[node_in_name]["node"].type = in_node_type
        graph.nodes[node_in_name]["node"].node_color = in_color
        graph.nodes[node_out_name]["node"].type = out_node_type
        graph.nodes[node_out_name]["node"].node_color = out_color
    return graph


def add_in_nodes(graph: nx.DiGraph, subgraph: nx.DiGraph, in_node: str,
                 rename_string: str, stage: str) -> nx.DiGraph:
    """ Add the missing input nodes to the target subgraph.

    The extracted graph is a subgraph of the original graph only
    containing the fault sensitive part of the circuit. However, the input nodes
    of the gates in this subgraph are missing and added in this function.
    
    Args:
        graph: The original digraph of the circuit.
        subgraph: The extracted target graph.
        in_node: The input node of the extracted target graph.
        rename_string: The suffix, which is appended to the original node name.
        stage: The current stage.
    Returns:
        The subgraph augmented with the input nodes.
    """

    subgraph_in_nodes = copy.deepcopy(subgraph)
    orig_graph = copy.deepcopy(graph)
    # Loop over all nodes of the target subgraph and add missing inp. nodes.
    filter_types = {"in_node", "out_node", "input"}
    for node, node_attribute in subgraph.nodes(data=True):
        if (len(subgraph.in_edges(node)) != len(node_attribute["node"].inputs)
            ) and (node_attribute["node"].type
                   not in filter_types) and (node != in_node + rename_string):
            # Get all in edges of the subgraph.
            subgraph_in_edges = subgraph.in_edges(node)
            subgraph_in_edges_name = []
            for edge in subgraph_in_edges:
                subgraph_in_edges_name.append(
                    subgraph.nodes[edge[0]]["node"].parent_name)
            # Determine missing in edges of the subgraph.
            current_node = node_attribute["node"].parent_name
            for edge in orig_graph.in_edges(current_node):
                if edge[0] not in subgraph_in_edges_name:
                    # Name of the new node.
                    node_name = edge[0] + rename_string
                    # Edge data (name, in_pin, out_pin) of the original edge.
                    edge_data = orig_graph.get_edge_data(edge[0], edge[1])
                    # The node attribute of the original graph.
                    node_attr = orig_graph.nodes[edge[0]]["node"]
                    # Add new node and connect.
                    subgraph_in_nodes.add_node(node_name,
                                               **{"node": node_attr})
                    subgraph_in_nodes.add_edge(node_name,
                                               node,
                                               name=(edge_data["name"]),
                                               out_pin=(edge_data["out_pin"]),
                                               in_pin=(edge_data["in_pin"]))
                    # Modify the attributes of the new node.
                    subgraph_in_nodes.nodes[node_name][
                        "node"].node_color = "blue"
                    subgraph_in_nodes.nodes[node_name]["node"].type = "input"
                    subgraph_in_nodes.nodes[node_name]["node"].name = node_name
                    subgraph_in_nodes.nodes[node_name]["node"].stage = stage

    return subgraph_in_nodes


def connect_graphs(graph: nx.DiGraph, subgraph: nx.DiGraph) -> nx.DiGraph:
    """ Connect the subgraphs in the target graph. 

    The target graph consists of several subgraphs with a input and output node.
    This function connects these in/out nodes between the subgraphs.
    
    Args:
        graph: The original digraph of the circuit.
        subgraph: The extracted target graph.
    Returns:
        The extracted target graph with the connected subgraphs.
    """
    subgraph_connected = copy.deepcopy(subgraph)
    in_nodes = DefaultDict(list)
    out_nodes = DefaultDict(list)
    # Iterate over all nodes in the subgraphs and collect the input and output
    # nodes.
    for node, node_attribute in subgraph.nodes(data=True):
        if node_attribute["node"].type == "in_node":
            in_nodes[node_attribute["node"].parent_name].append(node)
        elif node_attribute["node"].type == "out_node":
            out_nodes[node_attribute["node"].parent_name].append(node)

    # Connect the output node of subgraph 1 with the input node of subgraph 2.
    for parent_node, nodes_out in out_nodes.items():
        nodes_in = in_nodes[parent_node]
        for node_out in nodes_out:
            for node_in in nodes_in:
                # Avoid to create a loop between nodes in the same stage.
                if subgraph.nodes[node_in]["node"].stage != subgraph.nodes[
                        node_out]["node"].stage:
                    subgraph_connected.add_edge(node_out,
                                                node_in,
                                                name=node_out + "_" + node_in,
                                                out_pin="Q",
                                                in_pin="I1")
    return subgraph_connected


def extract_graph(graph: nx.DiGraph, fi_model: dict) -> nx.DiGraph:
    """ Extract the subgraph containing all comb. and seq. logic of interest. 

    The subgraphs between all input and output nodes defined in the fault model
    are created and merged into the extracted graph.
    
    Args:
        graph: The networkx digraph of the circuit.
        fi_model: The active fault model.
    Returns:
        The extracted subgraph of the original graph.
    """
    extracted_graphs = []

    # Extract all graphs between the given nodes.
    for stage in fi_model["stages"]:
        # Extract the target graph.
        subgraph = copy.deepcopy(graph)
        stage_name = stage
        node_in = fi_model["stages"][stage_name]["input"]
        node_out = fi_model["stages"][stage_name]["output"]
        subgraph = extract_graph_between_nodes(subgraph, node_in, node_out,
                                               stage_name)
        # Rename the nodes to break dependencies between target graphs.
        rename_string = ("_" + stage_name)
        subgraph = helpers.rename_nodes(subgraph, rename_string, False)
        # Set input and output node of the target graphs.
        subgraph = set_in_out_nodes(subgraph, node_in, node_out, rename_string,
                                    fi_model, stage)
        # Add missing input nodes for the gates.
        subgraph = add_in_nodes(graph, subgraph, node_in, rename_string, stage)
        # Append the target graph to the list of graphs.
        extracted_graphs.append(subgraph)
    # Merge all graphs into the target graph.
    extracted_graph = nx.compose_all(extracted_graphs)
    # Connect the subgraphs in the target graph.
    extracted_graph = connect_graphs(graph, extracted_graph)

    return extracted_graph


def evaluate_fault_results(results: list, fi_model: dict) -> None:
    """ Prints the result of the fault attack.

    Summarizes the effective and ineffective faults found in the attack. 
    An effective fault is a fault changing the output value but not triggering 
    the error logic of the fault countermeasure.
    
    Args:
        results: The results of the fault attack.
        fi_model_name: The name of the active fault model.
    """
    ineffective_faults = 0
    effective_faults = 0
    for result_per_fault_model in results:
        for result in result_per_fault_model:
            if result.sat_result:
                effective_faults = effective_faults + 1
            else:
                ineffective_faults = ineffective_faults + 1
    logger.info(
        f"Found {effective_faults * fi_model['simultaneous_faults']} effective faults and {ineffective_faults * fi_model['simultaneous_faults']} ineffective faults."
    )
    logger.info(helpers.header)


def handle_fault_model(graph: nx.DiGraph, fi_model_name: str, fi_model: dict,
                       num_cores: int) -> None:
    """ Handles each fault model of the fault model specification file.

    This function first extracts the target sub graph of the main circuit. Then,
    for all possible fault locations in the target graph, the fault is injected,
    the boolean formula is created, and the fault is evaluated using a SAT
    solver.
    
    Args:
        graph: The networkx digraph of the circuit.
        fi_model_name: The name of the active fault model.
        fi_model: The active fault model.
        num_cores: The number of cores to use for the FI.
    """
    # Extract the target graph from the circuit.
    target_graph = extract_graph(graph, fi_model)

    # Determine all possible fault location combinations.
    fault_locations = fault_combinations(graph, fi_model)

    # Split the fault locations into num_cores shares.
    fl_shares = numpy.array_split(numpy.array(fault_locations), num_cores)

    logger.info(
        f"Injecting {(len(fault_locations) * fi_model['simultaneous_faults']) } faults into {fi_model_name} ..."
    )

    # Use ray to distribute fault injection to num_cores processes.
    workers = [
        FiInjector.remote(fi_model_name, target_graph, fl_share, fi_model)
        for fl_share in fl_shares
    ]

    # Perform the attack and collect the results.
    tasks = [worker.perform_attack.remote() for worker in workers]
    results = ray.get(tasks)

    evaluate_fault_results(results, fi_model)


def main():
    tstp_begin = time.time()
    args = parse_arguments()
    num_cores = args.num_cores
    ray.init(num_cpus=num_cores)

    # Open the fault model and the graph.
    fi_models = open_fi_models(args)
    graph = nx.DiGraph()
    graph = read_circuit(graph, args)

    # Handle each fault model.
    for fi_model_name, fi_model in fi_models.items():
        handle_fault_model(graph, fi_model_name, fi_model, num_cores)

    tstp_end = time.time()
    logger.info("fi_injector.py successful (%.2fs)" % (tstp_end - tstp_begin))


if __name__ == "__main__":
    # Configure the logger.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logger.addHandler(console)
    main()
