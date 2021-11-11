#!/usr/bin/env python3
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import logging
import string
import time
from dataclasses import dataclass
from pathlib import Path

from liberty.parser import parse_liberty
from mako.template import Template
from sympy import Symbol, false, sympify, true
from sympy.logic.boolalg import is_cnf, simplify_logic, to_cnf

import helpers
from template.cell_lib_template import *

"""Part of the fault injection framework for the OpenTitan.

This tool converts a cell library (e.g., the NangateOpenCell library from
https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/\\
flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib) to the format
needed by the FI Injector.

Typical usage:
>>> ./cell_lib_generator.py -l NangateOpenCellLibrary_typical.lib 
                            -c examples/config.json -o cell_lib.py
"""


@dataclass
class TypeMapping:
    """ FI cell in/out type mapping.

    Contains the fields of the cell input and output mappings.

    """
    gate_in_type: dict
    gate_in_type_out: dict
    gate_out_type: dict
    gate_out_type_pins: dict
    in_type_pins: dict


@dataclass
class CellFunction:
    """ FI cell function.

    The function header and body of a cell function.

    """
    name: str
    function: str
    function_cnf: str
    output: str
    inputs: str


@dataclass
class CellLib:
    """ FI cell library class.

    Contains the fields of the cell library.

    """
    clk: str
    rst: str
    reg: str
    type_mapping: TypeMapping
    cell_formulas: list
    cell_mapping: str


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
    formula_cnf: Symbol


def parse_arguments(argv):
    """ Command line argument parsing.

    Args:
        argv: The command line arguments.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Parse")
    parser.add_argument("-l",
                        "--cell_lib",
                        dest="cell_lib",
                        type=helpers.ap_check_file_exists,
                        required=True,
                        help="Path of the cell library file")
    parser.add_argument("-c",
                        "--cfg",
                        dest="cfg",
                        type=helpers.ap_check_file_exists,
                        required=True,
                        help="Path of the cell library config file")
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


def open_cfg_file(args) -> dict:
    """ Opens the config JSON file.

    Args:
        args: The input arguments.

    Returns:
        The cell config.
    """
    with open(args.cfg, 'r') as f:
        cfg = json.load(f)
    return cfg


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
    inputs = [in_pin.replace(target_char, replace_char) for in_pin in inputs]
    for out_pin in outputs:
        out_pin.name.replace(target_char, replace_char)

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


def parse_cells(cell_lib) -> list:
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
                if pin_group["function"]:
                    function = pin_group["function"].value
                    out_pin = Output(name=pin_name,
                                     formula=function,
                                     formula_cnf="")
                    outputs.append(out_pin)

        # Ignore cells without outputs or inputs, e.g., filler cells.
        if inputs and outputs:
            cell = Cell(name=name, inputs=inputs, outputs=outputs)
            cells.append(cell)

    return cells


def convert_formula(cells: list):
    """ Converts the boolean function from a string to a clause.

    Args:
        cells: The cells list.

    """
    for cell in cells:
        # "S" is predefined by sympy, replace with K.
        cell.inputs, cell.outputs = replace_pin(cell.inputs, cell.outputs, "S",
                                                "K")
        # "I" is predefined by sympy, replace with L.
        cell.inputs, cell.outputs = replace_pin(cell.inputs, cell.outputs, "I",
                                                "L")
        for output in cell.outputs:
            if output.formula:
                output.formula_cnf = convert_string(output.formula,
                                                    output.name, cell.name)


def build_cell_functions(cells: list) -> list:
    """ Creates the cell functions.

    The cell function consists of the input validation and returns the 
    formula.

    Args:
        cells: The list of cells

    Returns:
        The cell functions list.

    """

    cell_functions = []

    for cell in cells:
        for output in cell.outputs:
            cell_name = cell.name + "_" + output.name
            # Convert sympy formula back to string.
            formula_cnf = str(output.formula_cnf)
            # Use the variables checked with validate_input.
            for in_pin in cell.inputs:
                formula_cnf = formula_cnf.replace(in_pin, f"p['{in_pin}']")
            formula_cnf = formula_cnf.replace(output.name, "p['node_name']")
            # Transform the inputs list to a string.
            inputs_str = "{ " + (", ".join(
                [str("'" + input + "'")
                 for input in cell.inputs])) + ",'node_name' }"
            # Create the cell function.
            cell_function = CellFunction(name=cell_name,
                                         function=output.formula,
                                         function_cnf=formula_cnf,
                                         output=output.name,
                                         inputs=inputs_str)
            cell_functions.append(cell_function)

    return cell_functions


def get_in_out_types(in_outs: str, output: bool):
    """ Determine the in/out types for each cell.

    Args:
        in_outs: The inputs or outputs of the current cell.
        output: Is in_outs an input or an output?

    Returns:
        The in/out_type and the in/out_type_pins.
    """
    # IN/OUT_TYPE:
    # Determine the IN/OUT Type of the current cell. Remove numbers from pins
    # and count the occurence. E.g., "A", "B", "C1", "C2" => "A1B1C2".
    if output: pins = [pins.name.rstrip(string.digits) for pins in in_outs]
    else: pins = [pins.rstrip(string.digits) for pins in in_outs]
    in_out_type = ""
    num_pins = {pin: pins.count(pin) for pin in pins}
    for pin, num_pin in num_pins.items():
        in_out_type += pin + str(num_pin)

    # IN/OUT_TYPE_PINS:
    # Store the corresponding input/outputs to each IN/OUT_TYPE.
    # E.g., "A1B1C2" => "A", "B", "C1", "C2".
    if output:
        in_out_str = "{ " + (", ".join(
            [str("'" + in_out.name + "'")
             for in_out in in_outs])) + ",'node_name' }"
    else:
        in_out_str = "{ " + (", ".join(
            [str("'" + in_out + "'")
             for in_out in in_outs])) + ",'node_name' }"

    return in_out_type, in_out_str


def build_type_mappings(cells: list) -> TypeMapping:
    """ Create the input and output type mappings for each cell.

    Args:
        cells: The list of cells.

    Returns:
        The input and output type mapping string.
    """
    # Create the gate_in/out_type and in/out_type_pins dict.
    # The gate_in/out_type dict contains the mapping <cell>=IN/OUT_TYPE
    # E.g. the IN_TYPE for the cell OAI211_X1 with the inputs
    # "A", "B", "C1", "C2" is "A1B1C2".
    # The in/out_type_pins dict contains the mapping <IN/OUT_TYPE>=in/out_pins
    # E.g. for "A1B1C2" the inputs are "A", "B", "C1", "C2".
    in_types = {}
    in_types_out = {}
    in_types_pins = {}
    out_types = {}
    out_types_pins = {}
    for cell in cells:
        # Inputs.
        in_type, input_str = get_in_out_types(cell.inputs, False)
        in_types[cell.name] = in_type
        in_types_pins[in_type] = input_str
        for output in cell.outputs:
            in_types_out[cell.name + "_" + output.name] = in_type
        # Outputs.
        out_type, out_str = get_in_out_types(cell.outputs, True)
        out_types[cell.name] = out_type
        out_types_pins[in_type] = out_str

    type_mapping = TypeMapping(gate_in_type=in_types,
                               gate_in_type_out=in_types_out,
                               gate_out_type=out_types,
                               gate_out_type_pins=out_types_pins,
                               in_type_pins=in_types_pins)

    return type_mapping


def build_cell_mapping(cells: Cell) -> str:
    """ The cell mapping consists the mapping from the cell name string to
    the corresponding cell function.

    Args:
        cells: The list of cells.

    Returns:
        The dict for each cell name string with its function.
    """
    cell_mapping = []
    for cell in cells:
        for output in cell.outputs:
            cell_mapping.append(
                f"  '{cell.name}_{output.name}': {cell.name}_{output.name},")
    return "\n".join(
        cell_mapping
    )  #CELL_MAPPING.format(cell_mapping="\n".join(cell_mapping))


def build_cell_lib(cells: list, cell_cfg: dict) -> CellLib:
    """ Converts the boolean function from a string to a clause.

    Args:
        cells: The cells list.
        cell_cfg: The configuration parameters of the cell library.

    Returns:
        The cell library used for the template.

    """
    cell_lib = ""

    type_mapping = build_type_mappings(cells)
    cell_formulas = build_cell_functions(cells)
    cell_mapping = build_cell_mapping(cells)

    cell_lib = CellLib(clk=cell_cfg["clk"],
                       rst=cell_cfg["rst"],
                       reg=cell_cfg["reg"],
                       type_mapping=type_mapping,
                       cell_formulas=cell_formulas,
                       cell_mapping=cell_mapping)

    return cell_lib


def write_cell_lib(cell_lib_template: Template, cell_lib_py: str,
                   out_file: Path) -> None:
    """ Write the generated cell library to the out_file path.

    Args:
        cell_lib_py: The string containing the generated cell library.
        out_file: The path of the output file.

    """
    out_file.write_text(cell_lib_template.render(cell_lib=cell_lib_py))
    #with open(out_file, "w") as f:
    #    f.write(cell_lib_py)


def main(argv=None):
    tstp_begin = time.time()
    args = parse_arguments(argv)

    template_file = (Path("template/cell_lib.py.tpl"))
    cell_lib_template = Template(template_file.read_text(),
                                 strict_undefined=True)
    # Open the cell library and config.
    cell_lib = open_cell_lib(args)
    cell_cfg = open_cfg_file(args)
    # Parse the cells of the lib and convert the formulas.
    cells = parse_cells(cell_lib)
    convert_formula(cells)
    # Assemble the output file and write.
    cell_lib_py = build_cell_lib(cells, cell_cfg)
    write_cell_lib(cell_lib_template, cell_lib_py, args.out_lib)

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
