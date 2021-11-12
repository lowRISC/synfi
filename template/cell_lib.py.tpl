
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
# "THIS FILE HAS BEEN GENERATED, DO NOT EDIT MANUALLY.
# COMMAND: ./cell_lib_generator.py -l NangateOpenCellLibrary_typical.lib 
#                                  -c examples/config.json 
#                                  -o cell_lib_nangate45_autogen.py

import logging

import networkx as nx
from sympy import Symbol, false, true

"""Part of the fault injection framework for the OpenTitan.

This library provides the mapping for a gate type of the Nangate45 library to a
boolean formula in CNF.
"""
logger = logging.getLogger(__name__)

# Set the clock and reset name and values.
clk_name = ${cell_lib.clk}
clk_value = true

rst_name = ${cell_lib.rst}
rst_value = false

registers = ${cell_lib.reg}

gate_in_type = {
% for cell_name, out_type in cell_lib.type_mapping.gate_in_type.items():
  '${cell_name}': '${out_type}',
% endfor
  'register': 'D1',
  'out_node': 'D1',
  'xnor': 'I2',
  'xor': 'I2',
  'input_formula': 'I1',
  'in_node': 'I1',
  'output': 'I1'
}

gate_in_type_out = {
% for cell_name, out_type in cell_lib.type_mapping.gate_in_type_out.items():
  '${cell_name}': '${out_type}',
% endfor
  'register': 'D1',
  'out_node': 'D1',
  'xnor': 'I2',
  'xor': 'I2',
  'input_formula': 'I1',
  'in_node': 'I1',
  'output': 'I1'
}

in_type_pins = {
% for in_type, out_pins in cell_lib.type_mapping.in_type_pins.items():
  '${in_type}': ${out_pins},
% endfor
  'D1': {'D', 'node_name'},
  'I1': {'I1', 'node_name'},
  'I2': {'I1', 'I2', 'node_name'}
}

gate_out_type = {
% for cell_name, out_type in cell_lib.type_mapping.gate_out_type.items():
  '${cell_name}': '${out_type}',
% endfor
}

out_type_pins = {
% for out_type, out_pins in cell_lib.type_mapping.gate_out_type_pins.items():
  '${out_type}': ${out_pins},
% endfor
}

################################################################################
#                   Adaption needed for a new cell library                     #
################################################################################
# The mapping from one input pin type to another used by the injector.
pin_in_mapping = {
    'A2B2': {
        'A1B1C2': {
            'A1': 'A',
            'A2': 'B',
            'B1': 'C1',
            'B2': 'C2'
        },
        'A4': {
            'A1': 'A1',
            'A2': 'A2',
            'B1': 'A3',
            'B2': 'A4'
        }
    },
    'A1B1C2': {
        'A2B2': {
            'A': 'A1',
            'B': 'A2',
            'C1': 'B1',
            'C2': 'B2'
        },
        'A4': {
            'A': 'A1',
            'B': 'A2',
            'C1': 'A3',
            'C2': 'A4'
        }
    },
    'A4': {
        'A2B2': {
            'A1': 'A1',
            'A2': 'A2',
            'A3': 'B1',
            'A4': 'B2'
        },
        'A1B1C2': {
            'A1': 'A',
            'A2': 'B',
            'A3': 'C1',
            'A4': 'C2'
        }
    },
    'A3': {
        'A1B2': {
            'A1': 'A',
            'A2': 'B1',
            'A3': 'B2'
        },
        'A1B1S1': {
            'A1': 'A',
            'A2': 'B',
            'A3': 'S'
        }
    },
    'A1B2': {
        'A3': {
            'A': 'A1',
            'B1': 'A2',
            'B2': 'A3'
        },
        'A1B1S1': {
            'A': 'A',
            'B1': 'B',
            'B2': 'S'
        }
    },
    'A1B1S1': {
        'A3': {
            'A': 'A1',
            'B': 'A2',
            'S': 'A3'
        },
        'A1B2': {
            'A': 'A',
            'B': 'B1',
            'S': 'B2'
        }
    },
    'A2': {
        'A1B1': {
            'A1': 'A',
            'A2': 'B'
        }
    },
    'A1B1': {
        'A2': {
            'A': 'A1',
            'B': 'A2'
        }
    }
}

# The mapping from one input pin type to another used by the injector.
pin_out_mapping = {
    'ZN1': {
        'Z1': {
            'ZN': 'Z'
        }
    },
    'Z1': {
        'ZN1': {
            'Z': 'ZN'
        }
    }
}

################################################################################
#                                DO NOT EDIT                                   #
################################################################################

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
    type_pins = gate_in_type_out[type]
    expected_inputs = in_type_pins[type_pins]

    if expected_inputs <= inputs.keys():
        input_symbols = {}
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
                input_symbols[input_pin] = Symbol(input.node + '_' +
                                                  input.out_pin)

        return input_symbols
    else:
        logger.error(inputs)
        raise Exception('Gate ' + type + ' is missing some inputs.')

def AND2_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ AND2_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (A1 & A2)
    """
    p = validate_inputs(inputs, graph, 'AND2_X1_ZN')
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) & (p['node_name'] | ~p['A1'] | ~p['A2']))

% for cell_function in cell_lib.cell_formulas:
def ${cell_function.name}(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' ${cell_function.name} gate.

    Args:
        inputs: ${cell_function.inputs}
        graph: The networkx graph of the circuit.
    Returns:
        ${cell_function.output} = ${cell_function.function}
    '''
    p = validate_inputs(inputs, graph, '${cell_function.name}')
    return (${cell_function.function_cnf})

% endfor

################################################################################
#                      OTFI SPECIFC CELLS - DO NOT EDIT                        # 
################################################################################
def xnor(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ xnor gate.

    Args:
        inputs: {'I1', 'I2', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = '!(I1 ^ I2)'.
    """
    p = validate_inputs(inputs, graph, 'xnor')

    return ((~p['I1'] | ~p['I2'] | p['node_name']) &
            (p['I1'] | p['I2'] | p['node_name']) &
            (p['I1'] | ~p['I2'] | ~p['node_name']) &
            (~p['I1'] | p['I2'] | ~p['node_name']))


def xor(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ xor gate.

    Args:
        inputs: {'I1', 'I2', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = '(I1 ^ I2)'.
    """
    p = validate_inputs(inputs, graph, 'xor')

    return ((~p['I1'] | ~p['I2'] | ~p['node_name']) &
            (p['I1'] | p['I2'] | ~p['node_name']) &
            (p['I1'] | ~p['I2'] | p['node_name']) &
            (~p['I1'] | p['I2'] | p['node_name']))


def and_output(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ and gate.

    AND gate for the output logic. As this is the last element of the formula
    the expression '& node_name' is added.

    Args:
        inputs: {'A1', ..., 'AN', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = 'A1 & ... & AN' & node_name.
    """
    if len(inputs) == 3:
        return AND2_X1_ZN(inputs, graph) & Symbol(inputs['node_name'].node + '_' +
                                               inputs['node_name'].out_pin)
    elif len(inputs) == 4:
        return AND3_X1_ZN(inputs, graph) & Symbol(inputs['node_name'].node + '_' +
                                               inputs['node_name'].out_pin)
    elif len(inputs) == 5:
        return AND4_X1_ZN(inputs, graph) & Symbol(inputs['node_name'].node + '_' +
                                               inputs['node_name'].out_pin)
    else:
        raise Exception('Missing and gate for output logic.')


def input_formula_Q(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ Sets a input pin to a predefined (0 or 1) value.

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        0 or 1.
    """

    p = validate_inputs(inputs, graph, 'input_formula')

    if inputs['I1'].node == 'one':
        # Input is connected to 1.
        # Return a one.
        return (~true | p['node_name']) & (true | ~p['node_name'])
    else:
        # Input ist connected to 0.
        # Return a zero.
        return (~false | p['node_name']) & (false | ~p['node_name'])


def input_formula_QN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ Sets a input pin to a predefined (0 or 1) value.

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        0 or 1.
    """

    p = validate_inputs(inputs, graph, 'input_formula')

    if inputs['I1'].node == 'one':
        # Input is connected to 1.
        # Return a zero.
        return (~false | p['node_name']) & (false | ~p['node_name'])
    else:
        # Input ist connected to 0.
        # Return a one.
        return (~true | p['node_name']) & (true | ~p['node_name'])

def in_node_Q(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ In node Q

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        Q = I
    """
    p = validate_inputs(inputs, graph, 'in_node')
    return (~p['I1'] | p['node_name']) & (p['I1'] | ~p['node_name'])

def in_node_QN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ In node QN

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        Q = !I
    """
    p = validate_inputs(inputs, graph, 'in_node')
    return (~p['I1'] | ~p['node_name']) & (p['I1'] | p['node_name'])

def out_node(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ Out node.

    Args:
        inputs: {'D', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = D.
    """
    p = validate_inputs(inputs, graph, 'out_node')
    return (~p['D'] | p['node_name']) & (p['D'] | ~p['node_name'])


def output(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ Out node.

    Args:
        inputs: {'D', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = I.
    """
    p = validate_inputs(inputs, graph, 'output')
    return (~p['I1'] | p['node_name']) & (p['I1'] | ~p['node_name'])

def register(inputs: dict, graph: nx.DiGraph) -> Symbol:
    """ A simplified register.

    Args:
        inputs: {'D', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        Q = 'D'
        QN = '!D'.
    """
    if graph.in_edges(inputs['node_name'].node):
        p = validate_inputs(inputs, graph, 'register')
        return ((~p['D'] | Symbol(inputs['node_name'].node + '_q')) &
                (p['D'] | ~Symbol(inputs['node_name'].node + '_q'))), (
                    (~p['D'] | ~Symbol(inputs['node_name'].node + '_qn')) &
                    (p['D'] | Symbol(inputs['node_name'].node + '_qn')))
    else:
        # Register with no inputs is ignored.
        return true

cell_mapping = {
% for mapping in cell_lib.cell_mapping:
  '${mapping}': ${mapping},
% endfor
  'DFFS_X1_Q': register, # Adapt to cell library.
  'DFFS_X1_QN': register, # Adapt to cell library.
  'DFFR_X1_Q': register, # Adapt to cell library.
  'DFFR_X1_QN': register, # Adapt to cell library.
  'xnor_O': xnor,
  'xor_O': xor,
  'and_Q': and_output,
  'input_Q': input_formula_Q,
  'input_QN': input_formula_QN,
  'in_node_Q': in_node_Q,
  'in_node_QN': in_node_QN,
  'out_node_Q': out_node,
  'out_node_QN': out_node,
  'output_O': output
}
