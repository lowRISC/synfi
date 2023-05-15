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
from random import shuffle

import numpy
import ray
from liberty.parser import parse_liberty
from mako.template import Template
from sympy import Symbol

import helpers
from formula_converter_class import FormulaConverter

"""Part of the fault injection framework for the OpenTitan.

This tool converts a cell library (e.g., the NangateOpenCell library from
https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/\\
flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib) to the format
needed by the FI Injector.

Typical usage:
>>> ./cell_lib_generator.py -l NangateOpenCellLibrary_typical.lib -n 16
                            -c examples/config.json 
                            -o cell_lib_nangate45_autogen.py
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
    clauses: list
    output: str
    inputs: str


@dataclass
class CellLib:
    """ FI cell library class.

    Contains the fields of the cell library.

    """
    reg: str
    port_in_mapping: dict
    port_out_mapping: dict
    type_mapping: TypeMapping
    cell_formulas: list
    cell_mapping: list
    ge: dict


@dataclass
class Cell:
    """ Cell data class.

    A cell consists of a list of input and output pins and a boolean formula.

    """
    name: str
    inputs: list
    outputs: list
    area: float
    ge: float


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
    parser.add_argument("-j",
                        "--json",
                        dest="netlist",
                        type=helpers.ap_check_file_exists,
                        required=False,
                        help="Only parse cells which are also in the netlist")
    parser.add_argument("-n",
                        "--num_cores",
                        dest="num_cores",
                        type=int,
                        required=True,
                        help="Number of cores to use")
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
        helpers.show_and_exit(__file__, ["sympy", "ray", "numpy"])

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


def open_netlist(args) -> list:
    """ Opens the JSON netlist and parses all cell types.

    Args:
        args: The input arguments.

    Returns:
        The cell types.
    """
    modules = None
    cell_types = []
    if args.netlist:
        with open(args.netlist, "r") as circuit_json_file:
            circuit_json = json.load(circuit_json_file)
            modules = circuit_json["modules"]
        # Iterate over netlist and add all cell types to the list.
        for module, module_value in modules.items():
            for cell, cell_value in module_value["cells"].items():
                cell_types.append(cell_value["type"])
        # Remove duplicates from the list.
        cell_types = list(dict.fromkeys(cell_types))
    return cell_types


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


def parse_cells(cell_lib: dict, cell_types: list, cell_cfg: dict) -> list:
    """ Parse the cells in the cell library.

    Args:
        cell_lib: The opened cell library.
        cell_types: The cell black list.
        cell_cfg: The cell configuration dict provided by the user.

    Returns:
        The cells list.
    """
    cells = []
    area_nand2 = 0
    for cell_group in cell_lib.get_groups("cell"):
        name = str(cell_group.args[0])
        area = cell_group["area"]
        if (not cell_types) or (name in cell_types):
            if not helpers.match(name, cell_cfg["exclude_cells"]):
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
                    cell = Cell(name=name.replace('"', ''), inputs=inputs, outputs=outputs, area=area, ge=1)
                    cells.append(cell)
                    if name == cell_cfg["ref_nand"]:
                        area_nand2 = area
    # Calculate kGE (area/area_NAND2).
    if area_nand2:
        for cell in cells:
            cell.ge = round(cell.area / area_nand2, 4)
    else:
        logger.info(f"Could not find area for NAND2 ({cell_cfg['ref_nand']})")
    return cells

def create_clauses(formula: str) -> str:
    """ Convert the formula string to clauses.

    This function converts the formula string to clauses needed by the SAT
    solver. For this, characters in the string are replaced.

    Args:
        formula: The formula as a string.

    Returns:
        The clauses.

    """
    clauses_ret = []
    clause_list = formula.split("&")
    for clause in clause_list:
        clause = clause.replace("|", ",")
        clause = clause.replace("~", "-")
        clause = clause.replace("(", "[")
        clause = clause.replace(")", "]")
        clauses_ret.append(clause)

    return clauses_ret

def build_cell_functions(cells: list) -> list:
    """ Creates the cell functions.

    The cell function consists of the input validation and returns the 
    formula.

    Args:
        cells: The list of cells.

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
            clauses = create_clauses(formula_cnf)
            # Transform the inputs list to a string.
            inputs_str = "{ " + (", ".join(
                [str("'" + input + "'")
                 for input in cell.inputs])) + ",'node_name' }"
            # Create the cell function.
            cell_function = CellFunction(name=cell_name,
                                         function=output.formula,
                                         clauses=clauses,
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


def build_cell_mapping(cells: Cell) -> list:
    """ The cell mapping consists the mapping from the cell name string to
    the corresponding cell function.

    Args:
        cells: The list of cells.

    Returns:
        The list for each cell name string with its function.
    """
    cell_mapping = []
    for cell in cells:
        for output in cell.outputs:
            cell_mapping.append(cell.name + "_" + output.name)

    return cell_mapping

def extract_cell_ge(cells: list) -> dict:
    """ Extract all kGE and store in dict.

    Args:
        cells: The cells list.

    Returns:
        Dict containing all kGE.

    """
    cell_ge = {}
    for cell in cells:
        cell_ge[cell.name] = cell.ge
    return cell_ge

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
    cell_ge = extract_cell_ge(cells)

    cell_lib = CellLib(reg=cell_cfg["reg"],
                       port_in_mapping=cell_cfg["port_in_mapping"],
                       port_out_mapping=cell_cfg["port_out_mapping"],
                       type_mapping=type_mapping,
                       cell_formulas=cell_formulas,
                       cell_mapping=cell_mapping,
                       ge=cell_ge)

    return cell_lib


def write_cell_lib(cell_lib_template: Template, cell_lib_py: str,
                   out_file: Path) -> None:
    """ Write the generated cell library to the out_file path.

    Args:
        cell_lib_py: The string containing the generated cell library.
        out_file: The path of the output file.

    """
    out_file.write_text(cell_lib_template.render(cell_lib=cell_lib_py))


def handle_cells(cells: dict, num_cores: int) -> list:
    """ Convert the cell formulas to sympy formulas using ray.

    Args:
        cells: The cells of the library.
        num_cores: The number of ray processes.
    Returns:
        The list of cells with the sympy formulas.
    """
    # Shuffle the list as some cell types take longer.
    shuffle(cells)
    # Split cells into num_core shares.
    cell_shares = numpy.array_split(numpy.array(cells), num_cores)
    # Use ray to distribute fault injection to num_cores processes.
    workers = [
        FormulaConverter.remote(cell_share) for cell_share in cell_shares
    ]

    # Perform the cell parsing and collect the results.
    tasks = [worker.convert_formulas.remote() for worker in workers]
    results = ray.get(tasks)
    cell_formulas = [item for sublist in results for item in sublist]

    return cell_formulas


def main(argv=None):
    tstp_begin = time.time()
    args = parse_arguments(argv)

    num_cores = args.num_cores
    ray.init(num_cpus=num_cores)

    template_file = (Path("template/cell_lib.py.tpl"))
    cell_lib_template = Template(template_file.read_text(),
                                 strict_undefined=True)
    # Open the cell library and config.
    cell_lib = open_cell_lib(args)
    cell_cfg = open_cfg_file(args)
    # If provided, open the netlist. Only cells used in the netlist are parsed.
    cell_types = open_netlist(args)
    # Parse the cells of the lib and convert the formulas.
    cells = parse_cells(cell_lib, cell_types, cell_cfg)
    # Distribute formula conversion to ray.
    cells = handle_cells(cells, num_cores)
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
