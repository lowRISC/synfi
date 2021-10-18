import copy

import networkx as nx

import helpers
from helpers import Node


class FiInjector:
    """ Class for performing distributed fault injections. 

    This class provides functionality to inject faults into the target circuit
    according to the fault model, to create the differential graph, to 
    extract the boolean CNF formula of this graph, and to hand the formula to
    a SAT solver.
    """
    def __init__(self, fault_name, target_graph, fault_locations):
        """ Inits the injector class

        This function injects faults into the graph by replacing the type of
        the target node with the target type.
        
        Args:
            fault_name: The fault model name of the current attack.
            target_graph: The graph to be evaluated.
            fault_locations: The location and fault mapping of the faults.
        """
        self.fault_name = fault_name
        self.target_graph = target_graph
        self.fault_locations = fault_locations

    def inject_faults(self):
        """ Inject faults into the target graph accoding to the fault location. 

        This function injects faults into the graph by replacing the type of
        the target node with the target type.
        
        Returns:
            The faulty target graph.
        """
        faulty_graph = copy.deepcopy(self.target_graph)
        for fault_mapping in self.fault_locations:
            # Target node and new gate type.
            node_target = fault_mapping[0]
            fault_type = fault_mapping[1]
            # Find the nodes in the target graph which are replaced with the
            # faulty nodes.
            nodes = [
                n for n, d in self.target_graph.nodes(data=True)
                if d["node"].parent_name == node_target
            ]
            for node in nodes:
                faulty_graph.nodes[node]["node"].type = fault_type
                faulty_graph.nodes[node]["node"].node_color = "red"

        return faulty_graph

    def create_diff_graph(self, faulty_graph):
        """ Create the differential graph based on the faulty graph. 

        This function creates the differential graph by merging the faulty graph
        and the unmodified target graph into a common graph. Additionally, 
        the inputs and outputs are merged.

        Args:
            faulty_graph: The target graph with the faulty nodes.
        
        Returns:
            The differential graph.
        """
        orig_graph = copy.deepcopy(self.target_graph)
        faulty_graph_renamed = copy.deepcopy(faulty_graph)
        # Rename the faulty graph.
        subgraph = helpers.rename_nodes(faulty_graph_renamed, "_faulty")
        # Merge the graphs into a common graph.
        diff_graph = nx.compose(orig_graph, faulty_graph_renamed)

        return diff_graph

    def perform_attack(self):
        """ Perform the attack. 

        Here, the attack on the target graph is conducted. First, a faulty graph
        is created. In this graph, the target fault nodes are replaced according
        to the fault mapping. Then, the differential graph is created.
        """
        # Inject the faults into the target graph.
        faulty_graph = self.inject_faults()

        # Create the differential graph.
        diff_graph = self.create_diff_graph(faulty_graph)
