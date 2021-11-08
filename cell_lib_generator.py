#!/usr/bin/env python3
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import time
from dataclasses import dataclass

import sympy
from liberty.parser import parse_liberty
from sympy import Symbol, false, solve, sympify, true
from sympy.logic.boolalg import is_cnf, simplify_logic, to_cnf

import helpers

"""Part of the fault injection framework for the OpenTitan.

This tool converts a cell library (e.g., the NangateOpenCell library from 
https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/\\
flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib) to the format
needed by the FI Injector.

Typical usage:
>>> ./cell_lib_generator.py -c NangateOpenCellLibrary_typical.lib 
                            -o nangate45_cell_lib.py
"""


@dataclass
class Cell:
    """ Cell data class.

    A cell consists of a list of input and output pins and a boolean formula.

    """
    name: str
    inputs: list
    outputs: list

@dataclass
class Output:
    """ An output of a cell.

    A cell consists of one or multiple outputs with an associated formula.

    """
    name: str
    formula: str

def parse_arguments(argv):
    """ Command line argument parsing.

    Args:
        argv: The command line arguments.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Parse")
    parser.add_argument("-c",
                        "--cell_lib",
                        dest="cell_lib",
                        type=helpers.ap_check_file_exists,
                        required=True,
                        help="Path of the cell library file")
    parser.add_argument("-o",
                        "--output",
                        dest="out_lib",
                        type=helpers.ap_check_dir_exists,
                        required=True,
                        help="Path of the output library file")
    parser.add_argument("--version",
                        action="store_true",
                        help="Show version and exit")
    args = parser.parse_args(argv)

    if args.version:
        helpers.show_and_exit(__file__, ["sympy"])

    return args


def open_cell_lib(args) -> dict:
    """ Opens the cell library in the liberty format.
    
    Args:
        args: The input arguments.

    Returns:
        The cell library.
    """
    try:
        cell_lib = parse_liberty(open(args.cell_lib).read())
    except:
        raise Exception(f"Failed to parse the {args.cell_lib} library.")

    return cell_lib


def simplify_expression(expr: Symbol) -> Symbol:
    """ Simplify the CNF expression.

    The simplify_logic functionality of sympy is used to simplify the given 
    expression. As the output needs to be in CNF, a check is conducted.

    Args:
        expr: The boolean expression to simplify.

    Returns:
        The simplified boolean expression in CNF.
    """
    simplified = simplify_logic(expr, 'cnf', True)
    if is_cnf(simplified):
        return simplified
    else:
        return expr


def convert_cnf(expr: Symbol, out_symbol: Symbol, gate: str) -> Symbol:
    """ Convert the given boolean expression to CNF.

    The logical biconditional of the boolean expression of the gate is converted
    to CNF using the sympy library.

    Args:
        expr: The boolean expression to convert.
        out_symbol: The output variable of the boolean expression.
        gate: The name of the current gate.

    Returns:
        The boolean expression in CNF.
    """
    cnf = to_cnf((out_symbol & expr) | (~out_symbol & ~expr))
    if not is_cnf(cnf):
        raise Exception(f"Failed to convert {gate} to CNF.")
    return cnf


def replace_pin(inputs: list, outputs: list, target_char: str,
replace_char: str) -> str:
    """ Replace a pin name.

    Sympy uses some predefined symbols (I, S), which need to be replaced in the
    input and output pins.

    Args:
        inputs: The inputs of the cell.
        outputs: The outputs of the cell.
        target_char: The char to replace.
        replace_char: The rename char.

    Returns:
        The formula, input, and output with the replaced pin name.
    """
    inputs=[in_pin.replace(target_char, replace_char) for in_pin in inputs]
    for out_pin in outputs:
        out_pin.name.replace(target_char, replace_char)
    #outputs=[out_pin.name.replace(target_char, replace_char) for out_pin in outputs]
    return inputs, outputs


def convert_string(formula: str, output: str, gate: str) -> Symbol:
    """ Convert the formula string to a sympy Symbol.

    Args:
        formula: The boolean formula.
        output: The output in name of the boolean expression.
        gate: The current gate.

    Returns:
        The boolean expression in CNF.
    """
    # As sympy requires ~ as a NOT, replace !.
    formula = formula.replace("!", "~")
    # "S" is predefined by sympy, replace with K.
    formula = formula.replace("S", "K")
    # "I" is predefined by sympy, replace with L.
    formula = formula.replace("I", "L")
    # Set 1/0 formula to true/false
    if formula == "1": formula = true
    if formula == "0": formula = false
    try:
        # Convert the string to sympy using sympify. The convert_xor=False
        # converts a ^ to a XOR.
        formula = sympify(formula, convert_xor=False)
        # Use the logical biconditional to induce the output.
        formula = convert_cnf(formula, Symbol(output), gate)
        # Simplify CNF formula.
        formula = simplify_expression(formula)
    except:
        raise Exception(f"Failed to convert formula for {gate}.")

    return formula

def parse_cells(cell_lib):
    """ Parse the cells in the cell library.

    Args:
        cell_lib: The opened cell library.

    Returns:
        The cells list.
    """
    cells = []
    for cell_group in cell_lib.get_groups("cell"):
        name = cell_group.args[0]
        inputs = []
        outputs = []
        for pin_group in cell_group.get_groups("pin"):
            pin_name = pin_group.args[0]
            if pin_group["direction"] == "input":
                inputs.append(pin_name)
            else:
                if pin_group["function"]: function = pin_group["function"].value
                else: function = ""
                out_pin = Output(name=pin_name, formula=function)
                outputs.append(out_pin)

        cell = Cell(name=name,
                    inputs=inputs,
                    outputs=outputs)
        cells.append(cell)

    return cells


def convert_formula(cells):
    """ Converts the boolean function from a string to a clause.

    Args:
        cells: The cells list.
    
    """
    for cell in cells:
        # "S" is predefined by sympy, replace with K.
        cell.inputs, cell.outputs = replace_pin(cell.inputs, cell.outputs, "S", "K")
        # "I" is predefined by sympy, replace with L.
        cell.inputs, cell.outputs = replace_pin(cell.inputs, cell.outputs, "I", "L")
        for output in cell.outputs:
            if output.formula:
                output.formula = convert_string(output.formula, output.name, cell.name)

def main(argv=None):
    tstp_begin = time.time()
    args = parse_arguments(argv)

    cell_lib = open_cell_lib(args)
    cells = parse_cells(cell_lib)
    convert_formula(cells)

    tstp_end = time.time()
    logger.info("cell_lib_generator.py successful (%.2fs)" %
                (tstp_end - tstp_begin))


if __name__ == "__main__":
    # Configure the logger.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logger.addHandler(console)
    main()