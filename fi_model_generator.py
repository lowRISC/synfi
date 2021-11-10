#!/usr/bin/env python3
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import logging
import time
from pathlib import Path
from typing import DefaultDict

import helpers

"""Part of the fault injection framework for the OpenTitan.

This module is responsible of automatically creating the fault model based on 
the augmented source code.

Typical usage:
>>> ./fi_model_generator.py -j examples/circuit.json -m aes_cipher_control 
    -s 2 -n rnd_ctr -o examples/fault_model.json
"""


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


def parse_otfi_attr(module: dict) -> dict:
    """ Parses the OTFI annotation values found in the module.

    Args:
        args: The input arguments.

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
            elif "otfi_input" in attr:
                values[netname]["otfi_input"] = attr["otfi_input"]
            elif "bits" in entry:
                values[netname]["bits"] = entry["bits"]

    return values


def parse_otfi_expected_values(attributes: dict, registers: dict) -> dict:
    """ Parses the OTFI expected values found in the module.

    Args:
        attributes: The parsed OTFI attributes.
        registers: The register cellnames with the connected wire.

    Returns:
        The OTFI expected and alert values.
    """
    out_values = DefaultDict(dict)
    alert_values = DefaultDict(dict)
    for netname, entry in attributes.items():
        if "otfi_expected" in entry:
            if entry["otfi_type"] == "output_port":
                bit_length = str(len(entry["bits"]))
                for idx, bit in enumerate(entry["bits"]):
                    name = netname + "(" + bit_length + ")_" + str(bit)
                    out_values[name] = int(entry["otfi_expected"][-(idx + 1)])
            elif entry["otfi_type"] == "alert_port":
                bit_length = str(len(entry["bits"]))
                for idx, bit in enumerate(entry["bits"]):
                    name = netname + "(" + bit_length + ")_" + str(bit)
                    alert_values[name] = int(
                        entry["otfi_expected"][-(idx + 1)])
            elif entry["otfi_type"] == "register_q":
                for idx, cellname in enumerate(registers[netname]):
                    out_values[cellname] = int(
                        entry["otfi_expected"][-(idx + 1)])

    return (out_values, alert_values)


def parse_otfi_in_values(attributes: dict, registers: dict) -> dict:
    """ Parses the OTFI input values found in the module.

    Args:
        attributes: The parsed OTFI attributes.
        registers: The register cellnames with the connected wire.

    Returns:
        The OTFI input values.
    """
    in_values = DefaultDict(dict)
    for netname, entry in attributes.items():
        if "otfi_input" in entry:
            if entry["otfi_type"] == "input_port":
                bit_length = str(len(entry["bits"]))
                for idx, bit in enumerate(entry["bits"]):
                    name = netname + "(" + bit_length + ")_" + str(bit)
                    in_values[name] = int(entry["otfi_input"][-(idx + 1)])
            elif entry["otfi_type"] == "register_q":
                for idx, cellname in enumerate(registers[netname]):
                    in_values[cellname] = int(entry["otfi_input"][-(idx + 1)])

    return in_values


def parse_otfi_registers(attributes: dict, module: dict) -> dict:
    """ Determine the selected registers.

    This function finds the register name a net is connected to.

    Args:
        attributes: The parsed OTFI attributes.
        module: The selected module of the circuit.

    Returns:
        The OTFI registers.
    """
    # The JSON entries.
    nets = module["netnames"]
    cells = module["cells"]

    registers = DefaultDict(list)
    nets_q = DefaultDict(list)
    # Get all netnames and bits for a net connected to a Q port of a register.
    for netname, entry in attributes.items():
        if entry["otfi_type"] == "register_q":
            for bit in nets[netname]["bits"]:
                nets_q[netname].append(bit)

    # Find the register cellname for the corresponding net connected to a
    # Q port of a register.
    for net_q, bits_q in nets_q.items():
        for bit_q in bits_q:
            for cellname, entry in cells.items():
                if "Q" in entry["connections"] and entry["connections"]["Q"][
                        0] == bit_q:
                    registers[net_q].append(cellname)

    return registers


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
    for in_element, in_value in in_values.items():
        for out_element, out_value in in_values.items():
            stage_name = "stage_" + str(num)
            stages[stage_name]["input"] = in_element
            stages[stage_name]["output"] = out_element
            stages[stage_name]["type"] = "input"
            num = num + 1

    for in_element, in_value in in_values.items():
        for out_element, out_value in exp_values.items():
            stage_name = "stage_" + str(num)
            stages[stage_name]["input"] = in_element
            stages[stage_name]["output"] = out_element
            stages[stage_name]["type"] = "output"
            num = num + 1
        for out_element, out_value in alert_values.items():
            stage_name = "stage_" + str(num)
            stages[stage_name]["input"] = in_element
            stages[stage_name]["output"] = out_element
            stages[stage_name]["type"] = "output"
            num = num + 1

    return stages


def write_json_fi_model(args, stages: dict, in_values: dict,
                        exp_values: dict) -> None:
    """ Write fault model to JSON file.
    
    Args:
        args: The input arguments.
        stages: The parsed OTFI attributes.
        in_values: 
        exp_values: 
    
    Returns:
        The OTFI registers.
    """
    json_file = Path(args.outfile)
    data = DefaultDict(dict)
    json_data = DefaultDict(dict)
    fault_name = args.fault_name

    data["simultaneous_faults"] = int(args.simultaneous_faults)
    data["stages"] = stages
    data["input_values"] = in_values
    data["output_values"] = exp_values

    json_data["fimodels"][fault_name] = data

    with open(json_file, 'w') as jfile:
        json.dump(json_data, jfile, indent=4)


def main(argv=None):
    # Configure the logger.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logger.addHandler(console)

    tstp_begin = time.time()
    args = parse_arguments(argv)

    module = open_module(args)
    otfi_attr = parse_otfi_attr(module)

    otfi_registers = parse_otfi_registers(otfi_attr, module)
    otfi_in_values = parse_otfi_in_values(otfi_attr, otfi_registers)
    otfi_exp_values, otfi_alert_values = parse_otfi_expected_values(
        otfi_attr, otfi_registers)
    otfi_stages = create_otfi_stages(otfi_in_values, otfi_exp_values,
                                     otfi_alert_values)
    write_json_fi_model(args, otfi_stages, otfi_in_values, otfi_exp_values)

    tstp_end = time.time()
    logger.info("fi_model_generator.py successful (%.2fs)" %
                (tstp_end - tstp_begin))


if __name__ == "__main__":
    main()
