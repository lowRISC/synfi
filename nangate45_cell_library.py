# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import logging

import networkx as nx
from sympy import Symbol, false, true

"""Part of the fault injection framework for the OpenTitan.

This library provides the mapping for a gate type of the Nangate45 library to a 
boolean formula in CNF.
"""
logger = logging.getLogger(__name__)

# Set the clock and reset name and values.
clk_name = "clk_i"
clk_value = true

rst_name = "rst_ni"
rst_value = false

registers = {"DFFS_X1", "DFFR_X1"}

# The dict containing all input pin types for each gate.
gate_in_type = {
    "OAI33_X1": "A3B3",  # "A1", "A2", "A3", "B1", "B2", "B3"
    "AOI221_X1": "A1B2C2",  # "A", "B1", "B2", "C1", "C2"
    "OAI221_X1": "A1B2C2",  # "A", "B1", "B2", "C1", "C2"
    "AOI22_X1": "A2B2",  # "A1", "A2", "B1", "B2"
    "OAI22_X1": "A2B2",  # "A1", "A2", "B1", "B2"
    "OAI211_X1": "A1B1C2",  # "A", "B", "C1", "C2"
    "AOI211_X1": "A1B1C2",  # "A", "B", "C1", "C2"
    "AND4_X1": "A4",  # "A1", "A2", "A3", "A4"
    "AND5_X1": "A5",  # "A1", "A2", "A3", "A4", "A5"
    "AND6_X1": "A6",  # "A1", "A2", "A3", "A4", "A5", "A6"
    "NOR4_X1": "A4",  # "A1", "A2", "A3", "A4"
    "OR4_X1": "A4",  # "A1", "A2", "A3", "A4"
    "NAND4_X1": "A4",  # "A1", "A2", "A3", "A4"
    "OR3_X1": "A3",  # "A1", "A2", "A3"
    "NAND3_X1": "A3",  # "A1", "A2", "A3"
    "NOR3_X1": "A3",  # "A1", "A2", "A3"
    "AND3_X1": "A3",  # "A1", "A2", "A3"
    "OAI21_X1": "A1B2",  # "A", "B1", "B2"
    "AOI21_X1": "A1B2",  # "A", "B1", "B2"
    "MUX2_X1": "A1B1S1",  # "A", "B", "S"
    "NAND2_X1": "A2",  # "A1", "A2"
    "NOR2_X1": "A2",  # "A1", "A2"
    "AND2_X1": "A2",  # "A1", "A2"
    "OR2_X1": "A2",  # "A1", "A2"
    "XNOR2_X1": "A1B1",  # "A", "B"
    "XOR2_X1": "A1B1",  # "A", "B"
    "INV_X1": "A1",  # "A"
    "register": "D1",  # "D"
    "out_node": "D1",  # "D"
    "xnor": "I2",  # "I1", "I2"
    "xor": "I2",  # "I1", "I2"
    "input_formula": "I1",  # "I1"
    "in_node": "I1",  # "I1"
    "output": "I1"  # "I1"
}

# The dict containing all input pin names for each input pin type.
in_type_pins = {
    "A2B2": {"A1", "A2", "B1", "B2", "node_name"},
    "A1B2": {"A", "B1", "B2", "node_name"},
    "A1": {"A", "node_name"},
    "A2": {"A1", "A2", "node_name"},
    "A3": {"A1", "A2", "A3", "node_name"},
    "A4": {"A1", "A2", "A3", "A4", "node_name"},
    "A5": {"A1", "A2", "A3", "A4", "A5", "node_name"},
    "A6": {"A1", "A2", "A3", "A4", "A5", "A6", "node_name"},
    "D1": {"D", "node_name"},
    "A1B1": {"A", "B", "node_name"},
    "A1B1C2": {"A", "B", "C1", "C2", "node_name"},
    "A1B2C2": {"A", "B1", "B2", "C1", "C2", "node_name"},
    "A1B1S1": {"A", "B", "S", "node_name"},
    "A3B3": {"A1", "A2", "A3", "B1", "B2", "B3", "node_name"},
    "I1": {"I1", "node_name"},
    "I2": {"I1", "I2", "node_name"}
}

# The mapping from one input pin type to another used by the injector.
pin_mapping = {
    "A2B2": {
        "A1B1C2": {
            "A1": "A",
            "A2": "B",
            "B1": "C1",
            "B2": "C2"
        }
    },
    "A2B2": {
        "A4": {
            "A1": "A1",
            "A2": "A2",
            "B1": "A3",
            "B2": "A4"
        }
    },
    "A1B1C2": {
        "A2B2": {
            "A": "A1",
            "B": "A2",
            "C1": "B1",
            "C2": "B2"
        }
    },
    "A1B1C2": {
        "A4": {
            "A": "A1",
            "B": "A2",
            "C1": "A3",
            "C2": "A4"
        }
    },
    "A4": {
        "A2B2": {
            "A1": "A1",
            "A2": "A2",
            "A3": "B1",
            "A4": "B2"
        }
    },
    "A4": {
        "A1B1C2": {
            "A1": "A",
            "A2": "B",
            "A3": "C1",
            "A4": "C2"
        }
    },
    "A3": {
        "A1B2": {
            "A1": "A",
            "A2": "B1",
            "A3": "B2"
        }
    },
    "A3": {
        "A1B1S1": {
            "A1": "A",
            "A2": "B",
            "A3": "S"
        }
    },
    "A1B2": {
        "A3": {
            "A": "A1",
            "B1": "A2",
            "B2": "A3"
        }
    },
    "A1B2": {
        "A1B1S1": {
            "A": "A",
            "B1": "B",
            "B2": "S"
        }
    },
    "A1B1S1": {
        "A3": {
            "A": "A1",
            "B": "A2",
            "S": "A3"
        }
    },
    "A1B1S1": {
        "A1B2": {
            "A": "A",
            "B": "B1",
            "S": "B2"
        }
    },
    "A2": {
        "A1B1": {
            "A1": "A",
            "A2": "B"
        }
    },
    "A1B1": {
        "A2": {
            "A": "A1",
            "B": "A2"
        }
    }
}


def validate_inputs(inputs: dict, graph: nx.DiGraph, type: str) -> dict:
    """ Validates the provided input of the gate.

    This function verifies that all inputs are present for the selected gate. 

    Args:
        inputs: The list of provided inputs.
        graph: The networkx graph of the circuit.
        type: The type of the gate.    
    
    Returns:
        The inputs for the gate.
    """
    type_pins = gate_in_type[type]
    expected_inputs = in_type_pins[type_pins]

    if expected_inputs <= inputs.keys():
        input_symbols = {}
        for input_pin, input in inputs.items():
            if graph.nodes[input.node][
                    "node"].type == "input" and clk_name in input.node:
                input_symbols[input_pin] = clk_value
            elif graph.nodes[input.node][
                    "node"].type == "input" and rst_name in input.node:
                input_symbols[input_pin] = rst_value
            elif graph.nodes[input.node]["node"].type == "null_node":
                input_symbols[input_pin] = false
            elif graph.nodes[input.node]["node"].type == "one_node":
                input_symbols[input_pin] = true
            else:
                if input_pin == "node_name":
                    input_symbols[input_pin] = Symbol(input.node + "_" +
                                                      input.out_pin)
                else:
                    input_symbols[input_pin] = Symbol(input.node + "_" +
                                                      input.out_pin)
        return input_symbols
    else:
        logger.error(inputs)
        raise Exception(f"Gate {type} is missing some inputs.")


def AOI22_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AOI22_X1 gate.

    Args:
        inputs: {"A1", "A2", "B1", "B2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!((A1 & A2) | (B1 & B2))".
    """
    p = validate_inputs(inputs, graph, "AOI22_X1")
    return (~p["A1"] | ~p["A2"]
            | ~p["node_name"]) & (p["A1"] | p["B1"] | p["node_name"]) & (
                p["A1"] | p["B2"]
                | p["node_name"]) & (p["A2"] | p["B1"] | p["node_name"]) & (
                    p["A2"] | p["B2"] | p["node_name"]) & (~p["B1"] | ~p["B2"]
                                                           | ~p["node_name"])


def OAI21_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ OAI21_X1 gate.

    Args:
        inputs: {"A", "B1", "B2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(A & (B1 | B2))".
    """
    p = validate_inputs(inputs, graph, "OAI21_X1")
    return (~p["A"] | ~p["B1"]
            | ~p["node_name"]) & (~p["A"] | ~p["B2"] | ~p["node_name"]) & (
                p["A"] | p["node_name"]) & (p["B1"] | p["B2"] | p["node_name"])


def INV_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ INV_X1 gate.

    Args:
        inputs: {"A", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!A".
    """
    p = validate_inputs(inputs, graph, "INV_X1")
    return ((~p["A"] | ~p["node_name"]) & (p["A"] | p["node_name"]))


def AOI21_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AOI21_X1 gate.

    Args:
        inputs: {"A", "B1", "B2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(A | (B1 & B2))".
    """
    p = validate_inputs(inputs, graph, "AOI21_X1")
    return (~p["A"]
            | ~p["node_name"]) & (p["A"] | p["B1"] | p["node_name"]) & (
                p["A"] | p["B2"] | p["node_name"]) & (~p["B1"] | ~p["B2"]
                                                      | ~p["node_name"])


def OAI211_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ OAI211_X1 gate.

    Args:
        inputs: {"A", "B", "C1", "C2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(((C1 | C2) & A) & B)".
    """
    p = validate_inputs(inputs, graph, "OAI211_X1")
    return (~p["A"] | ~p["B"] | ~p["C1"] | ~p["node_name"]) & (
        ~p["A"] | ~p["B"] | ~p["C2"]
        | ~p["node_name"]) & (p["A"] | p["node_name"]) & (
            p["B"] | p["node_name"]) & (p["C1"] | p["C2"] | p["node_name"])


def NAND2_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ NAND2_X1 gate.

    Args:
        inputs: {"A1", "A2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(A1 & A2)".
    """
    p = validate_inputs(inputs, graph, "NAND2_X1")
    return ((~p["A1"] | ~p["A2"] | ~p["node_name"]) &
            (p["A1"] | p["node_name"]) & (p["A2"] | p["node_name"]))


def OAI22_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ OAI22_X1 gate.

    Args:
        inputs: {"A1", "A2", "B1", "B2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!((A1 | A2) & (B1 | B2))".
    """
    p = validate_inputs(inputs, graph, "OAI22_X1")
    return (~p["A1"] | ~p["A1"]
            | ~p["node_name"]) & (~p["A1"] | ~p["B2"] | ~p["node_name"]) & (
                p["A1"] | p["A2"]
                | p["node_name"]) & (~p["A2"] | ~p["B1"] | ~p["node_name"]) & (
                    ~p["A2"] | ~p["B2"] | ~p["node_name"]) & (p["B1"] | p["B2"]
                                                              | p["node_name"])


def OR3_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ OR3_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "((A1 | A2) | A3)".
    """
    p = validate_inputs(inputs, graph, "OR3_X1")
    return (~p["A1"] | p["node_name"]) & (
        p["A1"] | p["A2"] | p["A3"] | ~p["node_name"]) & (
            ~p["A2"] | p["node_name"]) & (~p["A3"] | p["node_name"])


def AND2_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AND2_X1 gate.

    Args:
        inputs: {"A1", "A2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "(A1 & A2)".
    """
    p = validate_inputs(inputs, graph, "AND2_X1")
    return ((~p["A1"] | ~p["A2"] | p["node_name"]) &
            (p["A1"] | ~p["node_name"]) & (p["A2"] | ~p["node_name"]))


def XNOR2_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ XNOR2_X1 gate.

    Args:
        inputs: {"A", "B", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(A ^ B)".
    """
    p = validate_inputs(inputs, graph, "XNOR2_X1")
    return ((~p["A"] | ~p["B"] | p["node_name"]) &
            (p["A"] | p["B"] | p["node_name"]) &
            (p["A"] | ~p["B"] | ~p["node_name"]) &
            (~p["A"] | p["B"] | ~p["node_name"]))


def MUX2_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ MUX2_X1 gate.

    Args:
        inputs: {"A", "B", "S", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        Z = "((S & B) | (A & !S))".
    """
    p = validate_inputs(inputs, graph, "MUX2_X1")
    return (~p["A"] | p["S"]
            | p["node_name"]) & (p["A"] | p["S"] | ~p["node_name"]) & (
                ~p["B"] | ~p["S"] | p["node_name"]) & (p["B"] | ~p["S"]
                                                       | ~p["node_name"])


def AOI211_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AOI211_X1 gate.

    Args:
        inputs: {"A", "B", "C1", "C2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(((C1 & C2) | B) | A)".
    """
    p = validate_inputs(inputs, graph, "AOI211_X1")
    return (~p["A"] | ~p["node_name"]) & (
        p["A"] | p["B"] | p["C1"] | p["node_name"]
    ) & (p["A"] | p["B"] | p["C2"] | p["node_name"]) & (
        ~p["B"] | ~p["node_name"]) & (~p["C1"] | ~p["C2"] | ~p["node_name"])


def AND4_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AND4_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "A4", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "(((A1 & A2) & A3) & A4)".
    """
    p = validate_inputs(inputs, graph, "AND4_X1")
    return (~p["A1"] | ~p["A2"] | ~p["A3"] | ~p["A4"] | p["node_name"]) & (
        p["A1"] | ~p["node_name"]) & (p["A2"] | ~p["node_name"]) & (
            p["A3"] | ~p["node_name"]) & (p["A4"] | ~p["node_name"])


def AND5_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AND5_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "A4", "A5", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "(A1 & A2 & A3 & A4 & A5)".
    """
    p = validate_inputs(inputs, graph, "AND5_X1")
    return (~p["A1"] | ~p["A2"] | ~p["A3"] | ~p["A4"] | ~p["A5"]
            | p["node_name"]) & (p["A1"] | ~p["node_name"]) & (
                p["A2"] | ~p["node_name"]) & (p["A3"] | ~p["node_name"]) & (
                    p["A4"] | ~p["node_name"]) & (p["A5"] | ~p["node_name"])


def AND6_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AND6_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "A4", "A5", "A6", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "(A1 & A2 & A3 & A4 & A5 & A6)".
    """
    p = validate_inputs(inputs, graph, "AND6_X1")
    return (~p["A1"] | ~p["A2"] | ~p["A3"] | ~p["A4"] | ~p["A5"] | ~p["A6"]
            | p["node_name"]
            ) & (p["A1"] | ~p["node_name"]) & (p["A2"] | ~p["node_name"]) & (
                p["A3"] | ~p["node_name"]) & (p["A4"] | ~p["node_name"]) & (
                    p["A5"] | ~p["node_name"]) & (p["A6"] | ~p["node_name"])


def NOR4_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ NOR4_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "A4", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(((A1 | A2) | A3) | A4)".
    """
    p = validate_inputs(inputs, graph, "NOR4_X1")
    return (~p["A1"] | ~p["node_name"]) & (
        p["A1"] | p["A2"] | p["A3"] | p["A4"]
        | p["node_name"]) & (~p["A2"] | ~p["node_name"]) & (
            ~p["A3"] | ~p["node_name"]) & (~p["A4"] | ~p["node_name"])


def NOR2_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ NOR2_X1 gate.

    Args:
        inputs: {"A1", "A2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(A1 | A2)".
    """
    p = validate_inputs(inputs, graph, "NOR2_X1")
    return ((p["A1"] | p["A2"] | p["node_name"]) & (~p["A1"] | ~p["node_name"])
            & (~p["A2"] | ~p["node_name"]))


def OR4_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ OR4_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "A4", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "(((A1 | A2) | A3) | A4)".
    """
    p = validate_inputs(inputs, graph, "OR4_X1")
    return (~p["A1"] | p["node_name"]) & (
        p["A1"] | p["A2"] | p["A3"] | p["A4"]
        | ~p["node_name"]) & (~p["A2"] | p["node_name"]) & (
            ~p["A3"] | p["node_name"]) & (~p["A4"] | p["node_name"])


def NOR3_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ NOR3_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!((A1 | A2) | A3)".
    """
    p = validate_inputs(inputs, graph, "NOR3_X1")
    return (~p["A1"] | ~p["node_name"]) & (
        p["A1"] | p["A2"] | p["A3"] | p["node_name"]) & (
            ~p["A2"] | ~p["node_name"]) & (~p["A3"] | ~p["node_name"])


def register(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ A simplified register.

    Args:
        inputs: {"D", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        Q = "D"
        QN = "!D".
    """
    if graph.in_edges(inputs["node_name"].node):
        p = validate_inputs(inputs, graph, "register")
        return ((~p["D"] | Symbol(inputs["node_name"].node + "_q")) &
                (p["D"] | ~Symbol(inputs["node_name"].node + "_q"))), (
                    (~p["D"] | ~Symbol(inputs["node_name"].node + "_qn")) &
                    (p["D"] | Symbol(inputs["node_name"].node + "_qn")))
    else:
        # Register with no inputs is ignored.
        return true


def OR2_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ OR2_X1 gate.

    Args:
        inputs: {"A1", "A2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "(A1 | A2)".
    """
    p = validate_inputs(inputs, graph, "OR2_X1")
    return ((p["A1"] | p["A2"] | ~p["node_name"]) & (~p["A1"] | p["node_name"])
            & (~p["A2"] | p["node_name"]))


def OAI221_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ OAI221_X1 gate.

    Args:
        inputs: {"A", "B1", "B2", "C1", "C2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(((C1 | C2) & A) & (B1 | B2))".
    """
    p = validate_inputs(inputs, graph, "OAI221_X1")
    return (~p["A"] | ~p["C1"] | ~p["B1"] | ~p["node_name"]) & (
        ~p["A"] | ~p["C1"] | ~p["B2"] | ~p["node_name"]
    ) & (~p["A"] | ~p["C2"] | ~p["B1"] | ~p["node_name"]) & (
        ~p["A"] | ~p["C2"] | ~p["B2"] | ~p["node_name"]) & (
            p["A"] | p["node_name"]) & (p["C1"] | p["C2"] | p["node_name"]) & (
                p["B1"] | p["B2"] | p["node_name"])


def OAI33_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ OAI33_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "B1", "B2", "B3", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(((A1 | A2) | A3) & ((B1 | B2) | B3))".
    """
    p = validate_inputs(inputs, graph, "OAI33_X1")
    return (~p["A1"] | ~p["B1"] | ~p["node_name"]) & (
        ~p["A1"] | ~p["B3"]
        | ~p["node_name"]) & (~p["A1"] | ~p["B2"] | ~p["node_name"]) & (
            p["A1"] | p["A3"] | p["A2"]
            | p["node_name"]) & (~p["B1"] | ~p["A3"] | ~p["node_name"]) & (
                ~p["B1"] | ~p["A2"] | ~p["node_name"]) & (
                    p["B1"] | p["B3"] | p["B2"] | p["node_name"]) & (
                        ~p["A3"] | ~p["B3"] | ~p["node_name"]) & (
                            ~p["A3"] | ~p["B2"] | ~p["node_name"]) & (
                                ~p["B3"] | ~p["A2"] | ~p["node_name"]) & (
                                    ~p["B2"] | ~p["A2"] | ~p["node_name"])


def NAND4_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ NAND4_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "A4", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(((A1 & A2) & A3) & A4)".
    """
    p = validate_inputs(inputs, graph, "NAND4_X1")
    return (~p["A1"] | ~p["A2"] | ~p["A3"] | ~p["A4"] | ~p["node_name"]) & (
        p["A1"] | p["node_name"]) & (p["A2"] | p["node_name"]) & (
            p["A3"] | p["node_name"]) & (p["A4"] | p["node_name"])


def NAND3_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ NAND3_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!((A1 & A2) & A3)".
    """
    p = validate_inputs(inputs, graph, "NAND3_X1")
    return (~p["A1"] | ~p["A2"] | ~p["A3"]
            | ~p["node_name"]) & (p["A1"] | p["node_name"]) & (
                p["A2"] | p["node_name"]) & (p["A3"] | p["node_name"])


def XOR2_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ XOR2_X1 gate.

    Args:
        inputs: {"A", "B", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        Z = "(A ^ B)".
    """

    p = validate_inputs(inputs, graph, "XOR2_X1")

    return ((~p["A"] | ~p["B"] | ~p["node_name"]) &
            (p["A"] | p["B"] | ~p["node_name"]) &
            (p["A"] | ~p["B"] | p["node_name"]) &
            (~p["A"] | p["B"] | p["node_name"]))


def AND3_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AND3_X1 gate.

    Args:
        inputs: {"A1", "A2", "A3", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "((A1 & A2) & A3)".
    """
    p = validate_inputs(inputs, graph, "AND3_X1")
    return (~p["A1"] | ~p["A2"] | ~p["A3"]
            | p["node_name"]) & (p["A1"] | ~p["node_name"]) & (
                p["A2"] | ~p["node_name"]) & (p["A3"] | ~p["node_name"])


def AOI221_X1(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AOI221_X1 gate.

    Args:
        inputs: {"A", "B1", "B2", "C1", "C2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(((C1 & C2) | A) | (B1 & B2))".
    """
    p = validate_inputs(inputs, graph, "AOI221_X1")
    return (~p["A"] | ~p["node_name"]) & (
        p["A"] | p["B1"] | p["C1"]
        | p["node_name"]) & (p["A"] | p["B1"] | p["C2"] | p["node_name"]) & (
            p["A"] | p["B2"] | p["C1"] |
            p["node_name"]) & (p["A"] | p["B2"] | p["C2"] | p["node_name"]) & (
                ~p["B1"] | ~p["B2"] | ~p["node_name"]) & (~p["C1"] | ~p["C2"]
                                                          | ~p["node_name"])


# OTFI specific cells.


def xnor(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ xnor gate.

    Args:
        inputs: {"I1", "I2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "!(I1 ^ I2)".
    """
    p = validate_inputs(inputs, graph, "xnor")

    return ((~p["I1"] | ~p["I2"] | p["node_name"]) &
            (p["I1"] | p["I2"] | p["node_name"]) &
            (p["I1"] | ~p["I2"] | ~p["node_name"]) &
            (~p["I1"] | p["I2"] | ~p["node_name"]))


def xor(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ xor gate.

    Args:
        inputs: {"I1", "I2", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "(I1 ^ I2)".
    """
    p = validate_inputs(inputs, graph, "xor")

    return ((~p["I1"] | ~p["I2"] | ~p["node_name"]) &
            (p["I1"] | p["I2"] | ~p["node_name"]) &
            (p["I1"] | ~p["I2"] | p["node_name"]) &
            (~p["I1"] | p["I2"] | p["node_name"]))


def and_output(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ and gate.

    AND gate for the output logic. As this is the last element of the formula
    the expression "& node_name" is added.

    Args:
        inputs: {"A1", ..., "AN", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = "A1 & ... & AN" & node_name.
    """
    if len(inputs) == 3:
        return AND2_X1(inputs, graph) & Symbol(inputs["node_name"].node + "_" +
                                               inputs["node_name"].out_pin)
    elif len(inputs) == 4:
        return AND3_X1(inputs, graph) & Symbol(inputs["node_name"].node + "_" +
                                               inputs["node_name"].out_pin)
    elif len(inputs) == 5:
        return AND4_X1(inputs, graph) & Symbol(inputs["node_name"].node + "_" +
                                               inputs["node_name"].out_pin)
    elif len(inputs) == 6:
        return AND5_X1(inputs, graph) & Symbol(inputs["node_name"].node + "_" +
                                               inputs["node_name"].out_pin)
    elif len(inputs) == 7:
        return AND6_X1(inputs, graph) & Symbol(inputs["node_name"].node + "_" +
                                               inputs["node_name"].out_pin)
    else:
        raise Exception("Missing and gate for output logic.")


def input_formula(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ Sets a input pin to a predefined (0 or 1) value.

    Args:
        inputs: {"I1", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        0 or 1.
    """

    p = validate_inputs(inputs, graph, "input_formula")
    if inputs["node_name"].out_pin == "QN": invert = True
    else: invert = False

    if inputs["I1"].node == "one":
        # Input is connected to 1.
        if invert:
            # Return a zero.
            return (~false | p["node_name"]) & (false | ~p["node_name"])
        else:
            # Return a one.
            return (~true | p["node_name"]) & (true | ~p["node_name"])
    else:
        # Input ist connected to 0.
        if invert:
            # Return a one.
            return (~true | p["node_name"]) & (true | ~p["node_name"])
        else:
            # Return a zero.
            return (~false | p["node_name"]) & (false | ~p["node_name"])


def in_node(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ In node.

    Args:
        inputs: {"I1", "node_name"}.
        graph: The networkx graph of the circuit.
        
    Returns:
        ZN = I if invert==false or 
        ZN = !I if invert==true
    """
    p = validate_inputs(inputs, graph, "in_node")
    if inputs["node_name"].out_pin == "QN": invert = True
    else: invert = False

    if invert: return (~p["I1"] | ~p["node_name"]) & (p["I1"] | p["node_name"])
    else: return (~p["I1"] | p["node_name"]) & (p["I1"] | ~p["node_name"])


def out_node(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ Out node.

    Args:
        inputs: {"D", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = D.
    """
    p = validate_inputs(inputs, graph, "out_node")
    return (~p["D"] | p["node_name"]) & (p["D"] | ~p["node_name"])


def output(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ Out node.

    Args:
        inputs: {"D", "node_name"}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = I.
    """
    p = validate_inputs(inputs, graph, "output")
    return (~p["I1"] | p["node_name"]) & (p["I1"] | ~p["node_name"])


cell_mapping = {
    "AOI21_X1": AOI21_X1,
    "AOI22_X1": AOI22_X1,
    "AOI211_X1": AOI211_X1,
    "AOI221_X1": AOI221_X1,
    "OAI21_X1": OAI21_X1,
    "OAI22_X1": OAI22_X1,
    "OAI33_X1": OAI33_X1,
    "OAI221_X1": OAI221_X1,
    "OAI211_X1": OAI211_X1,
    "XOR2_X1": XOR2_X1,
    "NAND2_X1": NAND2_X1,
    "NAND3_X1": NAND3_X1,
    "NAND4_X1": NAND4_X1,
    "NOR2_X1": NOR2_X1,
    "NOR3_X1": NOR3_X1,
    "NOR4_X1": NOR4_X1,
    "OR2_X1": OR2_X1,
    "OR3_X1": OR3_X1,
    "OR4_X1": OR4_X1,
    "MUX2_X1": MUX2_X1,
    "XNOR2_X1": XNOR2_X1,
    "INV_X1": INV_X1,
    "AND2_X1": AND2_X1,
    "AND3_X1": AND3_X1,
    "AND4_X1": AND4_X1,
    "DFFS_X1": register,
    "DFFR_X1": register,
    "xnor": xnor,
    "xor": xor,
    "and": and_output,
    "input": input_formula,
    "in_node": in_node,
    "out_node": out_node,
    "output": output
}
