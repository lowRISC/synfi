def add_nodes(nodes, graph):
    """Add nodes to the graph.

    Args:
        nodes: The dict containing the node information.
        graph: The networkx graph.
    """
    for name, node in nodes.items():
        graph.add_node(name, **{"node": node})


def add_edges(nodes, connections, wires, graph):
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
        graph.add_edge(connection[0], connection[1], name=wire_name)


def build_graph(nodes, connections, wires, graph):
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


def write_graph(graph, path, file_name):
    """Dumps the graph of the circuit as a .dot file.

    Args:
        graph: The networkx graph.
        path: The path to store the .dot file.
        file_name: The filename.
    """
    dot = "strict digraph  {\n"
    inputs_dot = "subgraph cluster_inputs {\n label=\"Inputs\"; \n"
    circuit_dot = "subgraph cluster_circuit {\n label=\"Circuit\"; \n"
    faulty_circuit_dot = "subgraph cluster_faulty_circuit {\n label=\"Faulty Circuit\"; \n"
    outputs_dot = "subgraph cluster_outputs {\n label=\"Outputs\"; \n"
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
                inputs_dot += "%s -> %s [ label=%s ];\n" % (src_str, dst_str,
                                                            wire_name)
            elif src_cell.type == "output_pin":
                outputs_dot += "%s -> %s [ label=%s ];\n" % (src_str, dst_str,
                                                             wire_name)
            elif "_faulty" in src_cell.name:
                faulty_circuit_dot += "%s -> %s[ label=%s ];\n" % (
                    src_str, dst_str, wire_name)
            else:
                circuit_dot += "%s -> %s[ label=%s ];\n" % (src_str, dst_str,
                                                            wire_name)

    dot += inputs_dot + "}\n"
    dot += circuit_dot + "}\n"
    dot += faulty_circuit_dot + "}\n"
    dot += outputs_dot + "}\n"
    dot += "}\n"
    with open(path + "/" + file_name + ".dot", "w") as f:
        f.write(dot)
