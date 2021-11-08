# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

cell_header = """
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import logging

import networkx as nx
from sympy import Symbol, false, true

'''Part of the fault injection framework for the OpenTitan.

This library provides the mapping for a gate type of the Nangate45 library to a 
boolean formula in CNF.
'''
logger = logging.getLogger(__name__)

# Set the clock and reset name and values.
clk_name = 'clk_i'
clk_value = true

rst_name = 'rst_ni'
rst_value = false

registers = {'DFFS_X1', 'DFFR_X1'}
"""

cell_in_validation = """
def validate_inputs(inputs: dict, graph: nx.DiGraph, type: str) -> dict:
    ''' Validates the provided input of the gate.

    This function verifies that all inputs are present for the selected gate. 

    Args:
        inputs: The list of provided inputs.
        graph: The networkx graph of the circuit.
        type: The type of the gate.    
    
    Returns:
        The inputs for the gate.
    '''
    type_pins = gate_in_type[type]
    expected_inputs = in_type_pins[type_pins]

    if expected_inputs <= inputs.keys():
        input_symbols = {{}}
        for input_pin, input in inputs.items():
            if graph.nodes[input.node][
                    'node'].type == 'input' and clk_name in input.node:
                input_symbols[input_pin] = clk_value
            elif graph.nodes[input.node][
                    'node'].type == 'input' and rst_name in input.node:
                input_symbols[input_pin] = rst_value
            elif graph.nodes[input.node]['node'].type == 'null_node':
                input_symbols[input_pin] = false
            elif graph.nodes[input.node]['node'].type == 'one_node':
                input_symbols[input_pin] = true
            else:
                if input_pin == 'node_name':
                    input_symbols[input_pin] = Symbol(input.node + '_' +
                                                      input.out_pin)
                else:
                    input_symbols[input_pin] = Symbol(input.node + '_' +
                                                      input.out_pin)
        return input_symbols
    else:
        logger.error(inputs)
        raise Exception(f'Gate {{type}} is missing some inputs.')
"""

otfi_cells = """
# OTFI specific cells.
def xnor(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' xnor gate.

    Args:
        inputs: {'I1', 'I2', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = '!(I1 ^ I2)'.
    '''
    p = validate_inputs(inputs, graph, 'xnor')

    return ((~p['I1'] | ~p['I2'] | p['node_name']) &
            (p['I1'] | p['I2'] | p['node_name']) &
            (p['I1'] | ~p['I2'] | ~p['node_name']) &
            (~p['I1'] | p['I2'] | ~p['node_name']))


def xor(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' xor gate.

    Args:
        inputs: {'I1', 'I2', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = '(I1 ^ I2)'.
    '''
    p = validate_inputs(inputs, graph, 'xor')

    return ((~p['I1'] | ~p['I2'] | ~p['node_name']) &
            (p['I1'] | p['I2'] | ~p['node_name']) &
            (p['I1'] | ~p['I2'] | p['node_name']) &
            (~p['I1'] | p['I2'] | p['node_name']))


def and_output(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' and gate.

    AND gate for the output logic. As this is the last element of the formula
    the expression '& node_name' is added.

    Args:
        inputs: {'A1', ..., 'AN', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = 'A1 & ... & AN' & node_name.
    '''
    if len(inputs) == 3:
        return AND2_X1(inputs, graph) & Symbol(inputs['node_name'].node + '_' +
                                               inputs['node_name'].out_pin)
    elif len(inputs) == 4:
        return AND3_X1(inputs, graph) & Symbol(inputs['node_name'].node + '_' +
                                               inputs['node_name'].out_pin)
    elif len(inputs) == 5:
        return AND4_X1(inputs, graph) & Symbol(inputs['node_name'].node + '_' +
                                               inputs['node_name'].out_pin)
    elif len(inputs) == 6:
        return AND5_X1(inputs, graph) & Symbol(inputs['node_name'].node + '_' +
                                               inputs['node_name'].out_pin)
    elif len(inputs) == 7:
        return AND6_X1(inputs, graph) & Symbol(inputs['node_name'].node + '_' +
                                               inputs['node_name'].out_pin)
    else:
        raise Exception('Missing and gate for output logic.')


def input_formula(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' Sets a input pin to a predefined (0 or 1) value.

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        0 or 1.
    '''

    p = validate_inputs(inputs, graph, 'input_formula')
    if inputs['node_name'].out_pin == 'QN': invert = True
    else: invert = False

    if inputs['I1'].node == 'one':
        # Input is connected to 1.
        if invert:
            # Return a zero.
            return (~false | p['node_name']) & (false | ~p['node_name'])
        else:
            # Return a one.
            return (~true | p['node_name']) & (true | ~p['node_name'])
    else:
        # Input ist connected to 0.
        if invert:
            # Return a one.
            return (~true | p['node_name']) & (true | ~p['node_name'])
        else:
            # Return a zero.
            return (~false | p['node_name']) & (false | ~p['node_name'])


def in_node(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' In node.

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.
        
    Returns:
        ZN = I if invert==false or 
        ZN = !I if invert==true
    '''
    p = validate_inputs(inputs, graph, 'in_node')
    if inputs['node_name'].out_pin == 'QN': invert = True
    else: invert = False

    if invert: return (~p['I1'] | ~p['node_name']) & (p['I1'] | p['node_name'])
    else: return (~p['I1'] | p['node_name']) & (p['I1'] | ~p['node_name'])


def out_node(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' Out node.

    Args:
        inputs: {'D', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = D.
    '''
    p = validate_inputs(inputs, graph, 'out_node')
    return (~p['D'] | p['node_name']) & (p['D'] | ~p['node_name'])


def output(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' Out node.

    Args:
        inputs: {'D', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = I.
    '''
    p = validate_inputs(inputs, graph, 'output')
    return (~p['I1'] | p['node_name']) & (p['I1'] | ~p['node_name'])
"""