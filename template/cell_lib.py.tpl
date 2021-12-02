
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
# "THIS FILE HAS BEEN GENERATED, DO NOT EDIT MANUALLY.
# COMMAND: ./cell_lib_generator.py -l NangateOpenCellLibrary_typical.lib 
#                                  -c examples/config.json 
#                                  -o cell_lib_nangate45_autogen.py

import logging

import networkx as nx

"""Part of the fault injection framework for the OpenTitan.

This library provides the mapping for a gate type of the Nangate45 library to a
boolean formula in CNF.
"""
logger = logging.getLogger(__name__)

# The number is the variable name of a logical 0/1 used by the SAT solver.
one = 1
zero = 2

# Set the clock and reset name and values.
clk_name = ${cell_lib.clk}
clk_value = one

rst_name = ${cell_lib.rst}
rst_value = zero

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
  'output': 'I1',
  'AND19': 'A19',
  'AND15': 'A15',
  'AND10': 'A10',
  'AND9': 'A9',
  'AND8': 'A8',
  'AND7': 'A7',
  'AND6': 'A6',
  'AND5': 'A5',
  'AND4': 'A4',
  'AND3': 'A3',
  'AND2': 'A2',
  'OR10': 'A10',
  'OR9': 'A9',
  'OR8': 'A8',
  'OR7': 'A7',
  'OR6': 'A6',
  'OR5': 'A5',
  'OR4': 'A4',
  'OR3': 'A3',
  'OR2': 'A2',
  'OR1': 'A1'
}

in_type_pins = {
% for in_type, out_pins in cell_lib.type_mapping.in_type_pins.items():
  '${in_type}': ${out_pins},
% endfor
  'D1': {'D', 'node_name'},
  'I1': {'I1', 'node_name'},
  'I2': {'I1', 'I2', 'node_name'},
  'AO1': {'A1', 'node_name'},
  'A2': {'A1', 'A2', 'node_name'},
  'A3': {'A1', 'A2', 'A3', 'node_name'},
  'A4': {'A1', 'A2', 'A3', 'A4', 'node_name'},
  'A5': {'A1', 'A2', 'A3', 'A4', 'A5', 'node_name'},
  'A6': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'node_name'},
  'A7': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'node_name'},
  'A8': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'node_name'},
  'A9': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'node_name'},
  'A10': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'node_name'},
  'A15': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'node_name'},
  'A19': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'node_name'}
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


# The mapping from one input pin type to another used by the injector.
pin_in_mapping = ${cell_lib.pin_in_mapping}

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

def rename_inputs(inputs: dict, type: str) -> dict:
    """ Rename the inputs for the current gate.

    As certain variables (e.g., "I", "S") are predefined by sympy, the cell lib
    generator renamed these pins for all gates in the cell library. Now, rename
    these pins also for the gates handed by the FI injector.

    Args:
        inputs: The list of provided inputs.
        type: The type of the gate.

    Returns:
        The renamed inputs for the gate.
    """
    filter_types = {"in_node", "out_node", "input", "output", "input_formula",
                    "xnor", "xor"}
    inputs_formated = {}
    for input, input_pin in inputs.items():
        if type not in filter_types:
            if "S" in input: input = input.replace("S", "K")
            if "I" in input: input = input.replace("I", "L")
        inputs_formated[input] = input_pin
    return inputs_formated

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

    inputs = rename_inputs(inputs, type)

    if expected_inputs <= inputs.keys():
        input_symbols = {}
        for input_pin, input in inputs.items():
            input_symbols[input_pin] = input.name

        return input_symbols
    else:
        logger.error(inputs)
        raise Exception('Gate ' + type + ' is missing some inputs.')


% for cell_function in cell_lib.cell_formulas:
def ${cell_function.name}(inputs: dict, graph: nx.DiGraph, solver):
    ''' ${cell_function.name} gate.

    Args:
        inputs: ${cell_function.inputs}
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ${cell_function.output} = ${cell_function.function}
    '''
    p = validate_inputs(inputs, graph, '${cell_function.name}')
    % for clause in cell_function.clauses:
    solver.add_clause(${clause})
    % endfor

% endfor

################################################################################
#                      OTFI SPECIFC CELLS - DO NOT EDIT                        # 
################################################################################
def xnor(inputs: dict, graph: nx.DiGraph, solver):
    """ xnor gate.

    Args:
        inputs: {'I1', 'I2', 'node_name'}.
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = '!(I1 ^ I2)'.
    """
    p = validate_inputs(inputs, graph, 'xnor')
    solver.add_clause([-p['I1'], -p['I2'], p['node_name']])
    solver.add_clause([p['I1'], p['I2'], p['node_name']])
    solver.add_clause([p['I1'], -p['I2'], -p['node_name']])
    solver.add_clause([-p['I1'], p['I2'], -p['node_name']])


def xor(inputs: dict, graph: nx.DiGraph, solver):
    """ xor gate.

    Args:
        inputs: {'I1', 'I2', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = '(I1 ^ I2)'.
    """
    p = validate_inputs(inputs, graph, 'xor')
    solver.add_clause([-p['I1'], -p['I2'], -p['node_name']])
    solver.add_clause([p['I1'], p['I2'], -p['node_name']])
    solver.add_clause([p['I1'], -p['I2'], p['node_name']])
    solver.add_clause([-p['I1'], p['I2'], p['node_name']])


def and_output(inputs: dict, graph: nx.DiGraph, solver):
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
        p = validate_inputs(inputs, graph, 'AND2')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['node_name'], -p['A1'], -p['A2']])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 4:
        p = validate_inputs(inputs, graph, 'AND3')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['node_name'], -p['A1'], -p['A2'], -p['A3']])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 5:
        p = validate_inputs(inputs, graph, 'AND4')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['A4'], -p['node_name']])
        solver.add_clause(
            [p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4']])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 6:
        p = validate_inputs(inputs, graph, 'AND5')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['A4'], -p['node_name']])
        solver.add_clause([p['A5'], -p['node_name']])
        solver.add_clause(
            [p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['A5']])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 7:
        p = validate_inputs(inputs, graph, 'AND6')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['A4'], -p['node_name']])
        solver.add_clause([p['A5'], -p['node_name']])
        solver.add_clause([p['A6'], -p['node_name']])
        solver.add_clause([
            p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['A5'],
            -p['A6']
        ])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 8:
        p = validate_inputs(inputs, graph, 'AND7')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['A4'], -p['node_name']])
        solver.add_clause([p['A5'], -p['node_name']])
        solver.add_clause([p['A6'], -p['node_name']])
        solver.add_clause([p['A7'], -p['node_name']])
        solver.add_clause([
            p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['A5'],
            -p['A6'], -p['A7']
        ])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 9:
        p = validate_inputs(inputs, graph, 'AND8')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['A4'], -p['node_name']])
        solver.add_clause([p['A5'], -p['node_name']])
        solver.add_clause([p['A6'], -p['node_name']])
        solver.add_clause([p['A7'], -p['node_name']])
        solver.add_clause([p['A8'], -p['node_name']])
        solver.add_clause([
            p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['A5'],
            -p['A6'], -p['A7'], -p['A8']
        ])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 10:
        p = validate_inputs(inputs, graph, 'AND9')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['A4'], -p['node_name']])
        solver.add_clause([p['A5'], -p['node_name']])
        solver.add_clause([p['A6'], -p['node_name']])
        solver.add_clause([p['A7'], -p['node_name']])
        solver.add_clause([p['A8'], -p['node_name']])
        solver.add_clause([p['A9'], -p['node_name']])
        solver.add_clause([
            p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['A5'],
            -p['A6'], -p['A7'], -p['A8'], -p['A9']
        ])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 11:
        p = validate_inputs(inputs, graph, 'AND10')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['A4'], -p['node_name']])
        solver.add_clause([p['A5'], -p['node_name']])
        solver.add_clause([p['A6'], -p['node_name']])
        solver.add_clause([p['A7'], -p['node_name']])
        solver.add_clause([p['A8'], -p['node_name']])
        solver.add_clause([p['A9'], -p['node_name']])
        solver.add_clause([p['A10'], -p['node_name']])
        solver.add_clause([
            p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['A5'],
            -p['A6'], -p['A7'], -p['A8'], -p['A9'], -p['A10']
        ])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 16:
        p = validate_inputs(inputs, graph, 'AND15')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['A4'], -p['node_name']])
        solver.add_clause([p['A5'], -p['node_name']])
        solver.add_clause([p['A6'], -p['node_name']])
        solver.add_clause([p['A7'], -p['node_name']])
        solver.add_clause([p['A8'], -p['node_name']])
        solver.add_clause([p['A9'], -p['node_name']])
        solver.add_clause([p['A10'], -p['node_name']])
        solver.add_clause([p['A11'], -p['node_name']])
        solver.add_clause([p['A12'], -p['node_name']])
        solver.add_clause([p['A13'], -p['node_name']])
        solver.add_clause([p['A14'], -p['node_name']])
        solver.add_clause([p['A15'], -p['node_name']])
        solver.add_clause([
            p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['A5'],
            -p['A6'], -p['A7'], -p['A8'], -p['A9'], -p['A10'], -p['A11'],
            -p['A12'], -p['A13'], -p['A14'], -p['A15']
        ])
        solver.add_clause([p['node_name']])
    elif len(inputs) == 20:
        p = validate_inputs(inputs, graph, 'AND19')
        solver.add_clause([p['A1'], -p['node_name']])
        solver.add_clause([p['A2'], -p['node_name']])
        solver.add_clause([p['A3'], -p['node_name']])
        solver.add_clause([p['A4'], -p['node_name']])
        solver.add_clause([p['A5'], -p['node_name']])
        solver.add_clause([p['A6'], -p['node_name']])
        solver.add_clause([p['A7'], -p['node_name']])
        solver.add_clause([p['A8'], -p['node_name']])
        solver.add_clause([p['A9'], -p['node_name']])
        solver.add_clause([p['A10'], -p['node_name']])
        solver.add_clause([p['A11'], -p['node_name']])
        solver.add_clause([p['A12'], -p['node_name']])
        solver.add_clause([p['A13'], -p['node_name']])
        solver.add_clause([p['A14'], -p['node_name']])
        solver.add_clause([p['A15'], -p['node_name']])
        solver.add_clause([p['A16'], -p['node_name']])
        solver.add_clause([p['A17'], -p['node_name']])
        solver.add_clause([p['A18'], -p['node_name']])
        solver.add_clause([p['A19'], -p['node_name']])
        solver.add_clause([
            p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['A5'],
            -p['A6'], -p['A7'], -p['A8'], -p['A9'], -p['A10'], -p['A11'],
            -p['A12'], -p['A13'], -p['A14'], -p['A15'], -p['A16'], -p['A17'],
            -p['A18'], -p['A19']
        ])
        solver.add_clause([p['node_name']])
    else:
        print(len(inputs))
        raise Exception('Missing and gate for output logic.')


def or_output(inputs: dict, graph: nx.DiGraph, solver):
    """ or gate.

    OR gate for the output logic.

    Args:
        inputs: {'A1', ..., 'AN', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = 'A1 | ... | AN' | node_name.
    """
    if len(inputs) == 2:
        p = validate_inputs(inputs, graph, 'OR1')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([p["A1"], -p["node_name"]])
    elif len(inputs) == 3:
        p = validate_inputs(inputs, graph, 'OR2')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([-p["A2"], p["node_name"]])
        solver.add_clause([p["A1"], p["A2"], -p["node_name"]])
    elif len(inputs) == 4:
        p = validate_inputs(inputs, graph, 'OR3')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([-p["A2"], p["node_name"]])
        solver.add_clause([-p["A3"], p["node_name"]])
        solver.add_clause([p["A1"], p["A2"], p["A3"], -p["node_name"]])
    elif len(inputs) == 5:
        p = validate_inputs(inputs, graph, 'OR4')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([-p["A2"], p["node_name"]])
        solver.add_clause([-p["A3"], p["node_name"]])
        solver.add_clause([-p["A4"], p["node_name"]])
        solver.add_clause(
            [p["A1"], p["A2"], p["A3"], p["A4"], -p["node_name"]])
    elif len(inputs) == 6:
        p = validate_inputs(inputs, graph, 'OR5')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([-p["A2"], p["node_name"]])
        solver.add_clause([-p["A3"], p["node_name"]])
        solver.add_clause([-p["A4"], p["node_name"]])
        solver.add_clause([-p["A5"], p["node_name"]])
        solver.add_clause(
            [p["A1"], p["A2"], p["A3"], p["A4"], p["A5"], -p["node_name"]])
    elif len(inputs) == 7:
        p = validate_inputs(inputs, graph, 'OR6')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([-p["A2"], p["node_name"]])
        solver.add_clause([-p["A3"], p["node_name"]])
        solver.add_clause([-p["A4"], p["node_name"]])
        solver.add_clause([-p["A5"], p["node_name"]])
        solver.add_clause([-p["A6"], p["node_name"]])
        solver.add_clause([
            p["A1"], p["A2"], p["A3"], p["A4"], p["A5"], p["A6"],
            -p["node_name"]
        ])
    elif len(inputs) == 8:
        p = validate_inputs(inputs, graph, 'OR7')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([-p["A2"], p["node_name"]])
        solver.add_clause([-p["A3"], p["node_name"]])
        solver.add_clause([-p["A4"], p["node_name"]])
        solver.add_clause([-p["A5"], p["node_name"]])
        solver.add_clause([-p["A6"], p["node_name"]])
        solver.add_clause([-p["A7"], p["node_name"]])
        solver.add_clause([
            p["A1"], p["A2"], p["A3"], p["A4"], p["A5"], p["A6"], p["A7"],
            -p["node_name"]
        ])
    elif len(inputs) == 9:
        p = validate_inputs(inputs, graph, 'OR8')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([-p["A2"], p["node_name"]])
        solver.add_clause([-p["A3"], p["node_name"]])
        solver.add_clause([-p["A4"], p["node_name"]])
        solver.add_clause([-p["A5"], p["node_name"]])
        solver.add_clause([-p["A6"], p["node_name"]])
        solver.add_clause([-p["A7"], p["node_name"]])
        solver.add_clause([-p["A8"], p["node_name"]])
        solver.add_clause([
            p["A1"], p["A2"], p["A3"], p["A4"], p["A5"], p["A6"], p["A7"],
            p["A8"], -p["node_name"]
        ])
    elif len(inputs) == 10:
        p = validate_inputs(inputs, graph, 'OR9')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([-p["A2"], p["node_name"]])
        solver.add_clause([-p["A3"], p["node_name"]])
        solver.add_clause([-p["A4"], p["node_name"]])
        solver.add_clause([-p["A5"], p["node_name"]])
        solver.add_clause([-p["A6"], p["node_name"]])
        solver.add_clause([-p["A7"], p["node_name"]])
        solver.add_clause([-p["A8"], p["node_name"]])
        solver.add_clause([-p["A9"], p["node_name"]])
        solver.add_clause([
            p["A1"], p["A2"], p["A3"], p["A4"], p["A5"], p["A6"], p["A7"],
            p["A8"], p["A9"], -p["node_name"]
        ])
    elif len(inputs) == 11:
        p = validate_inputs(inputs, graph, 'OR10')
        solver.add_clause([-p["A1"], p["node_name"]])
        solver.add_clause([-p["A2"], p["node_name"]])
        solver.add_clause([-p["A3"], p["node_name"]])
        solver.add_clause([-p["A4"], p["node_name"]])
        solver.add_clause([-p["A5"], p["node_name"]])
        solver.add_clause([-p["A6"], p["node_name"]])
        solver.add_clause([-p["A7"], p["node_name"]])
        solver.add_clause([-p["A8"], p["node_name"]])
        solver.add_clause([-p["A9"], p["node_name"]])
        solver.add_clause([-p["A10"], p["node_name"]])
        solver.add_clause([
            p["A1"], p["A2"], p["A3"], p["A4"], p["A5"], p["A6"], p["A7"],
            p["A8"], p["A9"], p["A10"], -p["node_name"]
        ])
    else:
        raise Exception('Missing or gate for output logic.')

def input_formula_Q(inputs: dict, graph: nx.DiGraph, solver):
    """ Sets a input pin to a predefined (0 or 1) value.

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        0 or 1.
    """

    p = validate_inputs(inputs, graph, 'input_formula')

    if 'one' in inputs['I1'].node:
        # Input is connected to 1.
        # Return a one.
        solver.add_clause([-one, p['node_name']])
        solver.add_clause([one, -p['node_name']])
    else:
        # Input ist connected to 0.
        # Return a zero.
        solver.add_clause([-zero, p['node_name']])
        solver.add_clause([zero, -p['node_name']])


def input_formula_QN(inputs: dict, graph: nx.DiGraph, solver):
    """ Sets a input pin to a predefined (0 or 1) value.

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        0 or 1.
    """

    p = validate_inputs(inputs, graph, 'input_formula')

    if 'one' in inputs['I1'].node:
        # Input is connected to 1.
        # Return a zero.
        solver.add_clause([-zero, p['node_name']])
        solver.add_clause([zero, -p['node_name']])
    else:
        # Input ist connected to 0.
        # Return a one.
        solver.add_clause([-one, p['node_name']])


def in_node_Q(inputs: dict, graph: nx.DiGraph, solver):
    """ In node Q

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        Q = I
    """
    p = validate_inputs(inputs, graph, 'in_node')
    solver.add_clause([-p['I1'], p['node_name']])
    solver.add_clause([p['I1'], -p['node_name']])


def in_node_QN(inputs: dict, graph: nx.DiGraph, solver):
    """ In node QN

    Args:
        inputs: {'I1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        Q = !I
    """
    p = validate_inputs(inputs, graph, 'in_node')
    solver.add_clause([-p['I1'], -p['node_name']])
    solver.add_clause([p['I1'], p['node_name']])


def out_node(inputs: dict, graph: nx.DiGraph, solver):
    """ Out node.

    Args:
        inputs: {'D', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = D.
    """
    p = validate_inputs(inputs, graph, 'out_node')
    solver.add_clause([-p['D'], p['node_name']])
    solver.add_clause([p['D'], -p['node_name']])


def output(inputs: dict, graph: nx.DiGraph, solver):
    """ Out node.

    Args:
        inputs: {'D', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = I.
    """
    p = validate_inputs(inputs, graph, 'output')
    solver.add_clause([-p['I1'], p['node_name']])
    solver.add_clause([p['I1'], -p['node_name']])

cell_mapping = {
% for mapping in cell_lib.cell_mapping:
  '${mapping}': ${mapping},
% endfor
  'xnor_O': xnor,
  'xor_O': xor,
  'and_O': and_output,
  'or_O': or_output,
  'input_Q': input_formula_Q,
  'input_QN': input_formula_QN,
  'in_node_Q': in_node_Q,
  'in_node_QN': in_node_QN,
  'out_node_Q': out_node,
  'out_node_QN': out_node,
  'output_O': output
}
