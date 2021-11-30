#!/usr/bin/env python3
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import logging
import sys
import time
from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from typing import DefaultDict

import helpers

"""Part of the fault injection framework for the OpenTitan.

This module is responsible of automatically creating the fault model based on 
the augmented source code.

Typical usage:
>>> ./fi_model_generator.py -j examples/circuit.json -m aes_cipher_control 
    -s 2 -n rnd_ctr -c examples/fault_mapping_cfg.json 
    -o examples/fault_model.json
"""

logger = logging.getLogger()


@dataclass
class StageEntry:
    """ An entry of a OTFI stage.

    """
    cell: str
    value: int


def parse_arguments(argv):
    """ Command line argument parsing.
    
    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Parse")
    parser.add_argument("-j",
                        "--json",
                        dest="netlist",
                        type=helpers.ap_check_file_exists,
                        required=True,
                        help="Path of the json netlist")
    parser.add_argument("-o",
                        "--output",
                        dest="outfile",
                        type=helpers.ap_check_dir_exists,
                        required=True,
                        help="The output fault model file")
    parser.add_argument("-c",
                        "--cfg",
                        dest="cfg",
                        type=helpers.ap_check_file_exists,
                        required=True,
                        help="Path of the fault mapping config file")
    parser.add_argument("-m",
                        "--module",
                        dest="module",
                        required=True,
                        help="The module to analyze")
    parser.add_argument("-s",
                        "--simultaneous",
                        dest="simultaneous_faults",
                        required=True,
                        help="The number of simultaneous faults")
    parser.add_argument("-n",
                        "--name",
                        dest="fault_name",
                        required=True,
                        help="The name of the fault model")
    parser.add_argument("--version",
                        action="store_true",
                        help="Show version and exit")
    args = parser.parse_args(argv)

    if args.version:
        helpers.show_and_exit(__file__, [])

    return args


def open_module(args):
    """ Opens the JSON netlist.

    Args:
        args: The input arguments.

    Returns:
        The selected module of the netlist.
    """
    module = None
    with open(args.netlist, "r") as circuit_json_file:
        circuit_json = json.load(circuit_json_file)
        module = circuit_json["modules"][args.module]
    return module


def open_fault_mapping(args):
    """ Opens the user-specified fault mapping.

    Args:
        args: The input arguments.

    Returns:
        The configured fault mapping.
    """
    fault_mapping = None
    with open(args.cfg, "r") as fault_mapping_json_file:
        fault_mapping = json.load(fault_mapping_json_file)
    return fault_mapping["node_fault_mapping"]


def parse_otfi_attr(module: dict) -> dict:
    """ Parses the OTFI annotation values found in the module.

    Args:
        module: The loaded Verilog module.

    Returns:
        The OTFI attributes.
    """
    values = DefaultDict(dict)
    for netname, entry in module["netnames"].items():
        attr = entry["attributes"]
        if "otfi_type" in attr:
            otfi_type = attr["otfi_type"]
            values[netname]["otfi_type"] = otfi_type
            if "otfi_expected" in attr:
                values[netname]["otfi_expected"] = attr["otfi_expected"]
            if "otfi_expected" in attr:
                values[netname]["otfi_expected"] = attr["otfi_expected"]
            if "otfi_input" in attr:
                values[netname]["otfi_input"] = attr["otfi_input"]
            if "otfi_stage" in attr:
                values[netname]["otfi_stage"] = attr["otfi_stage"]
            if "bits" in entry:
                values[netname]["bits"] = entry["bits"]
                values[netname]["bits_len"] = str(len(entry["bits"]))
    return values


def parse_otfi_expected_values(attributes: dict, registers: dict,
                               module: dict) -> dict:
    """ Parses the OTFI expected values found in the module.

    Args:
        attributes: The parsed OTFI attributes.
        registers: The register cellnames with the connected wire.
        module: The loaded Verilog module.

    Returns:
        The OTFI expected and alert values.
    """

    out_values = DefaultDict(lambda: DefaultDict(list))
    alert_values = DefaultDict(lambda: DefaultDict(list))
    for netname, entry in attributes.items():
        if "otfi_expected" in entry:
            if entry["otfi_type"] == "output_port":
                for idx, bit in enumerate(entry["bits"]):
                    name = netname + "(" + entry["bits_len"] + ")_" + str(bit)
                    stage = StageEntry(cell=name,
                                       value=int(
                                           entry["otfi_expected"][-(idx + 1)]))
                    out_values[entry["otfi_stage"]]["stage"].append(stage)
                    out_values[
                        entry["otfi_stage"]]["type"] = entry["otfi_type"]
            elif entry["otfi_type"] == "alert_port":
                for idx, bit in enumerate(entry["bits"]):
                    name = netname + "(" + entry["bits_len"] + ")_" + str(bit)
                    stage = StageEntry(cell=name,
                                       value=int(
                                           entry["otfi_expected"][-(idx + 1)]))
                    alert_values[entry["otfi_stage"]]["stage"].append(stage)
                    alert_values[
                        entry["otfi_stage"]]["type"] = entry["otfi_type"]
            elif entry["otfi_type"] == "alert_signal":
                for idx, bit in enumerate(entry["bits"]):
                    name = get_connected_cell(str(bit), module)
                    stage = StageEntry(cell=name,
                                       value=int(
                                           entry["otfi_expected"][-(idx + 1)]))
                    alert_values[entry["otfi_stage"]]["stage"].append(stage)
                    alert_values[
                        entry["otfi_stage"]]["type"] = entry["otfi_type"]
            elif entry["otfi_type"] == "register_q":
                for idx, cellname in enumerate(registers[netname]):
                    stage = StageEntry(cell=cellname,
                                       value=int(
                                           entry["otfi_expected"][-(idx + 1)]))
                    alert_values[entry["otfi_stage"]]["stage"].append(stage)
                    alert_values[
                        entry["otfi_stage"]]["type"] = entry["otfi_type"]
    return (out_values, alert_values)


def parse_otfi_in_values(attributes: dict, registers: dict) -> dict:
    """ Parses the OTFI input values found in the Verilog module.

    Args:
        attributes: The parsed OTFI attributes.
        registers: The register cellnames with the connected wire.

    Returns:
        The OTFI input values.
    """
    in_values = DefaultDict(lambda: DefaultDict(list))
    for netname, entry in attributes.items():
        if "otfi_input" in entry:
            if entry["otfi_type"] == "input_port":
                for idx, bit in enumerate(entry["bits"]):
                    name = netname + "(" + entry["bits_len"] + ")_" + str(bit)
                    stage = StageEntry(cell=name,
                                       value=int(
                                           entry["otfi_input"][-(idx + 1)]))
                    in_values[entry["otfi_stage"]]["stage"].append(stage)
                    in_values[entry["otfi_stage"]]["type"] = entry["otfi_type"]
            elif entry["otfi_type"] == "register_q":
                for idx, cellname in enumerate(
                        registers[netname]["registers"]):
                    stage = StageEntry(cell=cellname,
                                       value=int(
                                           entry["otfi_input"][-(idx + 1)]))
                    in_values[entry["otfi_stage"]]["stage"].append(stage)
                    in_values[entry["otfi_stage"]]["type"] = entry["otfi_type"]
    return in_values


def parse_otfi_registers(attributes: dict, module: dict) -> dict:
    """ Determine the selected registers.

    This function finds the register name a net is connected to.

    Args:
        attributes: The parsed OTFI attributes.
        module: The selected Verilog module of the circuit.

    Returns:
        The OTFI registers.
    """
    # The JSON entries.
    nets = module["netnames"]
    cells = module["cells"]

    registers = DefaultDict(dict)
    nets_q = DefaultDict(dict)
    # Get all netnames and bits for a net connected to a Q port of a register.
    for netname, entry in attributes.items():
        if entry["otfi_type"] == "register_q":
            nets_q[netname]["nets"] = []
            for bit in nets[netname]["bits"]:
                nets_q[netname]["nets"].append(bit)
                nets_q[netname]["stage"] = entry["otfi_stage"]

    # Find the register cellname for the corresponding net connected to a
    # Q port of a register.
    for net_q, net_entry in nets_q.items():
        registers[net_q]["registers"] = []
        for bit_q in net_entry["nets"]:
            for cellname, entry in cells.items():
                if "Q" in entry["connections"] and entry["connections"]["Q"][
                        0] == bit_q:
                    registers[net_q]["registers"].append(cellname)
                    registers[net_q]["stage"] = net_entry["stage"]

    return registers


def get_connected_cell(wire_name: str, module: dict) -> str:
    """ Determine the selected registers.

    This function finds the cell connected to a wire.

    Args:
        wire_name: The name of the wire.
        module: The selected Verilog module of the circuit.

    Returns:
        The cell connected with a wire.
    """
    # The JSON entries.

    cells = module["cells"]
    cell = ""
    for cell_name, entry in cells.items():
        for port, wire in entry["connections"].items():
            if wire_name in str(
                    wire[0]) and entry["port_directions"][port] == "output":
                cell = cell_name
    if cell == "":
        logger.error("Alert signal gate not found.")
        sys.exit()
    return cell


def create_otfi_stages(in_values: dict, exp_values: dict,
                       alert_values: dict) -> dict:
    """ Determine the stages to analyze.

    The stages define the sensitive parts of the circuit which are analyzed by
    the OTFI framework. A stage includes all nodes in the nx.DiGraph between the 
    input and output node.

    Args:
        in_values: The parsed OTFI input values.
        exp_values: The parsed OTFI expected values.
        alert_values: The parsed OTFI alert values.

    Returns:
        The OTFI stages.
    """
    stages = DefaultDict(dict)
    num = 1

    for in_stage_name, in_stage in in_values.items():
        if "register_q" in in_stage["type"]:
            stage_name = "stage_" + str(in_stage_name) + "_" + str(
                in_stage_name)
            stages[stage_name]["type"] = "input"
            stages[stage_name]["inputs"] = [
                stage.cell for stage in in_stage["stage"]
            ]
            stages[stage_name]["outputs"] = stages[stage_name]["inputs"]
    # Join the expected and output values dict.
    out_values = exp_values | alert_values
    for in_stage_name, in_stage in in_values.items():
        for out_stage_name, out_stage in out_values.items():
            stage_name = "stage_" + str(in_stage_name) + "_" + str(
                out_stage_name)
            stages[stage_name]["type"] = "output"
            if len(in_stage["stage"]) == len(out_stage["stage"]):
                stages[stage_name]["inputs"] = [
                    stage.cell for stage in in_stage["stage"]
                ]
                stages[stage_name]["outputs"] = [
                    stage.cell for stage in out_stage["stage"]
                ]
            elif len(in_stage["stage"]) > len(out_stage["stage"]):
                stages[stage_name]["inputs"] = [
                    stage.cell for stage in in_stage["stage"]
                ]
                flatten_outputs = [stage.cell for stage in out_stage["stage"]]
                # Fill up the output.
                out_stage_cycle = cycle(flatten_outputs)
                stages[stage_name]["outputs"] = [
                    next(out_stage_cycle) for i in in_stage["stage"]
                ]
            else:
                stages[stage_name]["outputs"] = [
                    stage.cell for stage in out_stage["stage"]
                ]
                flatten_inputs = [stage.cell for stage in in_stage["stage"]]
                # Fill up the input.
                in_stage_cycle = cycle(flatten_inputs)
                stages[stage_name]["inputs"] = [
                    next(in_stage_cycle) for i in out_stage["stage"]
                ]

    return stages


def write_json_fi_model(args, stages: dict, fault_mapping: dict,
                        in_values: dict, exp_values: dict,
                        alert_values: dict) -> None:
    """ Write fault model to JSON file.
    
    Args:
        args: The input arguments.
        stages: The parsed OTFI attributes.
        fault_mapping: The user-specified fault mapping.
        in_values: The input values.
        exp_values: The expected output values.
        alert_values: The expected alert output values.
    
    Returns:
        The OTFI registers.
    """
    json_file = Path(args.outfile)
    data = DefaultDict(dict)
    json_data = DefaultDict(dict)
    fault_name = args.fault_name

    data["simultaneous_faults"] = int(args.simultaneous_faults)
    data["stages"] = stages
    data["node_fault_mapping"] = fault_mapping
    data["input_values"] = DefaultDict()
    for stage_name, in_stage in in_values.items():
        for stage in in_stage["stage"]:
            data["input_values"][stage.cell] = stage.value
    data["output_values"] = DefaultDict()
    for stage_name, out_stage in exp_values.items():
        for stage in out_stage["stage"]:
            data["output_values"][stage.cell] = stage.value
    data["alert_values"] = DefaultDict()
    for stage_name, alert_stage in alert_values.items():
        for stage in alert_stage["stage"]:
            data["alert_values"][stage.cell] = stage.value
    json_data["fimodels"][fault_name] = data

    with open(json_file, 'w') as jfile:
        json.dump(json_data, jfile, indent=4)


def main(argv=None):
    # Configure the logger.
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logger.addHandler(console)

    tstp_begin = time.time()
    args = parse_arguments(argv)

    module = open_module(args)
    fault_mapping = open_fault_mapping(args)
    otfi_attr = parse_otfi_attr(module)

    otfi_registers = parse_otfi_registers(otfi_attr, module)
    otfi_in_values = parse_otfi_in_values(otfi_attr, otfi_registers)
    otfi_exp_values, otfi_alert_values = parse_otfi_expected_values(
        otfi_attr, otfi_registers, module)
    otfi_stages = create_otfi_stages(otfi_in_values, otfi_exp_values,
                                     otfi_alert_values)
    write_json_fi_model(args, otfi_stages, fault_mapping, otfi_in_values,
                        otfi_exp_values, otfi_alert_values)

    tstp_end = time.time()
    logger.info("fi_model_generator.py successful (%.2fs)" %
                (tstp_end - tstp_begin))


if __name__ == "__main__":
    main()
