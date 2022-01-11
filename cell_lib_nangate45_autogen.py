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

registers = {'DFFS_X1', 'DFFR_X1'}

gate_in_type = {
    'AND2_X1': 'A2',
    'AND2_X2': 'A2',
    'AND2_X4': 'A2',
    'AND3_X1': 'A3',
    'AND3_X2': 'A3',
    'AND3_X4': 'A3',
    'AND4_X1': 'A4',
    'AND4_X2': 'A4',
    'AND4_X4': 'A4',
    'AOI21_X1': 'A1B2',
    'AOI21_X2': 'A1B2',
    'AOI21_X4': 'A1B2',
    'AOI22_X1': 'A2B2',
    'AOI22_X2': 'A2B2',
    'AOI22_X4': 'A2B2',
    'AOI211_X1': 'A1B1C2',
    'AOI211_X2': 'A1B1C2',
    'AOI211_X4': 'A1B1C2',
    'AOI221_X1': 'A1B2C2',
    'AOI221_X2': 'A1B2C2',
    'AOI221_X4': 'A1B2C2',
    'AOI222_X1': 'A2B2C2',
    'AOI222_X2': 'A2B2C2',
    'AOI222_X4': 'A2B2C2',
    'BUF_X1': 'A1',
    'BUF_X2': 'A1',
    'BUF_X4': 'A1',
    'BUF_X8': 'A1',
    'BUF_X16': 'A1',
    'BUF_X32': 'A1',
    'CLKBUF_X1': 'A1',
    'CLKBUF_X2': 'A1',
    'CLKBUF_X3': 'A1',
    'DFFRS_X1': 'D1RN1KN1CK1',
    'DFFRS_X2': 'D1RN1KN1CK1',
    'DFFR_X1': 'D1RN1CK1',
    'DFFR_X2': 'D1RN1CK1',
    'DFFS_X1': 'D1KN1CK1',
    'DFFS_X2': 'D1KN1CK1',
    'DFF_X1': 'D1CK1',
    'DFF_X2': 'D1CK1',
    'DLH_X1': 'D1G1',
    'DLH_X2': 'D1G1',
    'DLL_X1': 'D1GN1',
    'DLL_X2': 'D1GN1',
    'FA_X1': 'A1B1CL1',
    'HA_X1': 'A1B1',
    'INV_X1': 'A1',
    'INV_X2': 'A1',
    'INV_X4': 'A1',
    'INV_X8': 'A1',
    'INV_X16': 'A1',
    'INV_X32': 'A1',
    'MUX2_X1': 'A1B1K1',
    'MUX2_X2': 'A1B1K1',
    'NAND2_X1': 'A2',
    'NAND2_X2': 'A2',
    'NAND2_X4': 'A2',
    'NAND3_X1': 'A3',
    'NAND3_X2': 'A3',
    'NAND3_X4': 'A3',
    'NAND4_X1': 'A4',
    'NAND4_X2': 'A4',
    'NAND4_X4': 'A4',
    'NOR2_X1': 'A2',
    'NOR2_X2': 'A2',
    'NOR2_X4': 'A2',
    'NOR3_X1': 'A3',
    'NOR3_X2': 'A3',
    'NOR3_X4': 'A3',
    'NOR4_X1': 'A4',
    'NOR4_X2': 'A4',
    'NOR4_X4': 'A4',
    'OAI21_X1': 'A1B2',
    'OAI21_X2': 'A1B2',
    'OAI21_X4': 'A1B2',
    'OAI22_X1': 'A2B2',
    'OAI22_X2': 'A2B2',
    'OAI22_X4': 'A2B2',
    'OAI33_X1': 'A3B3',
    'OAI211_X1': 'A1B1C2',
    'OAI211_X2': 'A1B1C2',
    'OAI211_X4': 'A1B1C2',
    'OAI221_X1': 'A1B2C2',
    'OAI221_X2': 'A1B2C2',
    'OAI221_X4': 'A1B2C2',
    'OAI222_X1': 'A2B2C2',
    'OAI222_X2': 'A2B2C2',
    'OAI222_X4': 'A2B2C2',
    'OR2_X1': 'A2',
    'OR2_X2': 'A2',
    'OR2_X4': 'A2',
    'OR3_X1': 'A3',
    'OR3_X2': 'A3',
    'OR3_X4': 'A3',
    'OR4_X1': 'A4',
    'OR4_X2': 'A4',
    'OR4_X4': 'A4',
    'SDFFRS_X1': 'D1RN1KE1KL1KN1CK1',
    'SDFFRS_X2': 'D1RN1KE1KL1KN1CK1',
    'SDFFR_X1': 'D1RN1KE1KL1CK1',
    'SDFFR_X2': 'D1RN1KE1KL1CK1',
    'SDFFS_X1': 'D1KE1KL1KN1CK1',
    'SDFFS_X2': 'D1KE1KL1KN1CK1',
    'SDFF_X1': 'D1KE1KL1CK1',
    'SDFF_X2': 'D1KE1KL1CK1',
    'TBUF_X1': 'A1EN1',
    'TBUF_X2': 'A1EN1',
    'TBUF_X4': 'A1EN1',
    'TBUF_X8': 'A1EN1',
    'TBUF_X16': 'A1EN1',
    'TINV_X1': 'EN1L1',
    'TLAT_X1': 'D1G1OE1',
    'XNOR2_X1': 'A1B1',
    'XNOR2_X2': 'A1B1',
    'XOR2_X1': 'A1B1',
    'XOR2_X2': 'A1B1',
    'register': 'OTFI_D1',
    'out_node': 'OTFI_D1',
    'xnor': 'OTFI_I2',
    'xor': 'OTFI_I2',
    'in_node': 'OTFI_I1',
    'output': 'OTFI_I1',
    'input': 'OTFI_I1',
    'input_fault': 'OTFI_I1'
}

gate_in_type_out = {
    'AND2_X1_ZN': 'A2',
    'AND2_X2_ZN': 'A2',
    'AND2_X4_ZN': 'A2',
    'AND3_X1_ZN': 'A3',
    'AND3_X2_ZN': 'A3',
    'AND3_X4_ZN': 'A3',
    'AND4_X1_ZN': 'A4',
    'AND4_X2_ZN': 'A4',
    'AND4_X4_ZN': 'A4',
    'AOI21_X1_ZN': 'A1B2',
    'AOI21_X2_ZN': 'A1B2',
    'AOI21_X4_ZN': 'A1B2',
    'AOI22_X1_ZN': 'A2B2',
    'AOI22_X2_ZN': 'A2B2',
    'AOI22_X4_ZN': 'A2B2',
    'AOI211_X1_ZN': 'A1B1C2',
    'AOI211_X2_ZN': 'A1B1C2',
    'AOI211_X4_ZN': 'A1B1C2',
    'AOI221_X1_ZN': 'A1B2C2',
    'AOI221_X2_ZN': 'A1B2C2',
    'AOI221_X4_ZN': 'A1B2C2',
    'AOI222_X1_ZN': 'A2B2C2',
    'AOI222_X2_ZN': 'A2B2C2',
    'AOI222_X4_ZN': 'A2B2C2',
    'BUF_X1_Z': 'A1',
    'BUF_X2_Z': 'A1',
    'BUF_X4_Z': 'A1',
    'BUF_X8_Z': 'A1',
    'BUF_X16_Z': 'A1',
    'BUF_X32_Z': 'A1',
    'CLKBUF_X1_Z': 'A1',
    'CLKBUF_X2_Z': 'A1',
    'CLKBUF_X3_Z': 'A1',
    'DFFRS_X1_Q': 'D1RN1KN1CK1',
    'DFFRS_X1_QN': 'D1RN1KN1CK1',
    'DFFR_X1_Q': 'D1RN1CK1',
    'DFFR_X1_QN': 'D1RN1CK1',
    'DFFS_X1_Q': 'D1KN1CK1',
    'DFFS_X1_QN': 'D1KN1CK1',
    'FA_X1_CO': 'A1B1CL1',
    'FA_X1_S': 'A1B1CL1',
    'HA_X1_CO': 'A1B1',
    'HA_X1_S': 'A1B1',
    'INV_X1_ZN': 'A1',
    'INV_X2_ZN': 'A1',
    'INV_X4_ZN': 'A1',
    'INV_X8_ZN': 'A1',
    'INV_X16_ZN': 'A1',
    'INV_X32_ZN': 'A1',
    'MUX2_X1_Z': 'A1B1K1',
    'MUX2_X2_Z': 'A1B1K1',
    'NAND2_X1_ZN': 'A2',
    'NAND2_X2_ZN': 'A2',
    'NAND2_X4_ZN': 'A2',
    'NAND3_X1_ZN': 'A3',
    'NAND3_X2_ZN': 'A3',
    'NAND3_X4_ZN': 'A3',
    'NAND4_X1_ZN': 'A4',
    'NAND4_X2_ZN': 'A4',
    'NAND4_X4_ZN': 'A4',
    'NOR2_X1_ZN': 'A2',
    'NOR2_X2_ZN': 'A2',
    'NOR2_X4_ZN': 'A2',
    'NOR3_X1_ZN': 'A3',
    'NOR3_X2_ZN': 'A3',
    'NOR3_X4_ZN': 'A3',
    'NOR4_X1_ZN': 'A4',
    'NOR4_X2_ZN': 'A4',
    'NOR4_X4_ZN': 'A4',
    'OAI21_X1_ZN': 'A1B2',
    'OAI21_X2_ZN': 'A1B2',
    'OAI21_X4_ZN': 'A1B2',
    'OAI22_X1_ZN': 'A2B2',
    'OAI22_X2_ZN': 'A2B2',
    'OAI22_X4_ZN': 'A2B2',
    'OAI33_X1_ZN': 'A3B3',
    'OAI211_X1_ZN': 'A1B1C2',
    'OAI211_X2_ZN': 'A1B1C2',
    'OAI211_X4_ZN': 'A1B1C2',
    'OAI221_X1_ZN': 'A1B2C2',
    'OAI221_X2_ZN': 'A1B2C2',
    'OAI221_X4_ZN': 'A1B2C2',
    'OAI222_X1_ZN': 'A2B2C2',
    'OAI222_X2_ZN': 'A2B2C2',
    'OAI222_X4_ZN': 'A2B2C2',
    'OR2_X1_ZN': 'A2',
    'OR2_X2_ZN': 'A2',
    'OR2_X4_ZN': 'A2',
    'OR3_X1_ZN': 'A3',
    'OR3_X2_ZN': 'A3',
    'OR3_X4_ZN': 'A3',
    'OR4_X1_ZN': 'A4',
    'OR4_X2_ZN': 'A4',
    'OR4_X4_ZN': 'A4',
    'TBUF_X1_Z': 'A1EN1',
    'TBUF_X2_Z': 'A1EN1',
    'TBUF_X4_Z': 'A1EN1',
    'TBUF_X8_Z': 'A1EN1',
    'TBUF_X16_Z': 'A1EN1',
    'TINV_X1_ZN': 'EN1L1',
    'XNOR2_X1_ZN': 'A1B1',
    'XNOR2_X2_ZN': 'A1B1',
    'XOR2_X1_Z': 'A1B1',
    'XOR2_X2_Z': 'A1B1',
    'register': 'OTFI_D1',
    'out_node': 'OTFI_D1',
    'xnor': 'OTFI_I2',
    'xor': 'OTFI_I2',
    'in_node': 'OTFI_I1',
    'output': 'OTFI_I1',
    'AND19': 'OTFI_A19',
    'AND15': 'OTFI_A15',
    'AND10': 'OTFI_A10',
    'AND9': 'OTFI_A9',
    'AND8': 'OTFI_A8',
    'AND7': 'OTFI_A7',
    'AND6': 'OTFI_A6',
    'AND5': 'OTFI_A5',
    'AND4': 'OTFI_A4',
    'AND3': 'OTFI_A3',
    'AND2': 'OTFI_A2',
    'OR10': 'OTFI_A10',
    'OR9': 'OTFI_A9',
    'OR8': 'OTFI_A8',
    'OR7': 'OTFI_A7',
    'OR6': 'OTFI_A6',
    'OR5': 'OTFI_A5',
    'OR4': 'OTFI_A4',
    'OR3': 'OTFI_A3',
    'OR2': 'OTFI_A2',
    'OR1': 'OTFI_A1'
}

in_type_pins = {
    'A2': {'A1', 'A2', 'node_name'},
    'A3': {'A1', 'A2', 'A3', 'node_name'},
    'A4': {'A1', 'A2', 'A3', 'A4', 'node_name'},
    'A1B2': {'A', 'B1', 'B2', 'node_name'},
    'A2B2': {'A1', 'A2', 'B1', 'B2', 'node_name'},
    'A1B1C2': {'A', 'B', 'C1', 'C2', 'node_name'},
    'A1B2C2': {'A', 'B1', 'B2', 'C1', 'C2', 'node_name'},
    'A2B2C2': {'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'node_name'},
    'A1': {'A', 'node_name'},
    'D1RN1KN1CK1': {'D', 'RN', 'KN', 'CK', 'node_name'},
    'D1RN1CK1': {'D', 'RN', 'CK', 'node_name'},
    'D1KN1CK1': {'D', 'KN', 'CK', 'node_name'},
    'D1CK1': {'D', 'CK', 'node_name'},
    'D1G1': {'D', 'G', 'node_name'},
    'D1GN1': {'D', 'GN', 'node_name'},
    'A1B1CL1': {'A', 'B', 'CL', 'node_name'},
    'A1B1': {'A', 'B', 'node_name'},
    'A1B1K1': {'A', 'B', 'K', 'node_name'},
    'A3B3': {'A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'node_name'},
    'D1RN1KE1KL1KN1CK1': {'D', 'RN', 'KE', 'KL', 'KN', 'CK', 'node_name'},
    'D1RN1KE1KL1CK1': {'D', 'RN', 'KE', 'KL', 'CK', 'node_name'},
    'D1KE1KL1KN1CK1': {'D', 'KE', 'KL', 'KN', 'CK', 'node_name'},
    'D1KE1KL1CK1': {'D', 'KE', 'KL', 'CK', 'node_name'},
    'A1EN1': {'A', 'EN', 'node_name'},
    'EN1L1': {'EN', 'L', 'node_name'},
    'D1G1OE1': {'D', 'G', 'OE', 'node_name'},
    'OTFI_D1': {'D', 'node_name'},
    'OTFI_I1': {'I1', 'node_name'},
    'OTFI_I2': {'I1', 'I2', 'node_name'},
    'OTFI_A1': {'A1', 'node_name'},
    'OTFI_A2': {'A1', 'A2', 'node_name'},
    'OTFI_A3': {'A1', 'A2', 'A3', 'node_name'},
    'OTFI_A4': {'A1', 'A2', 'A3', 'A4', 'node_name'},
    'OTFI_A5': {'A1', 'A2', 'A3', 'A4', 'A5', 'node_name'},
    'OTFI_A6': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'node_name'},
    'OTFI_A7': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'node_name'},
    'OTFI_A8': {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'node_name'},
    'OTFI_A9':
    {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'node_name'},
    'OTFI_A10':
    {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'node_name'},
    'OTFI_A15': {
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11',
        'A12', 'A13', 'A14', 'A15', 'node_name'
    },
    'OTFI_A19': {
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11',
        'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'node_name'
    }
}

gate_out_type = {
    'AND2_X1': 'ZN1',
    'AND2_X2': 'ZN1',
    'AND2_X4': 'ZN1',
    'AND3_X1': 'ZN1',
    'AND3_X2': 'ZN1',
    'AND3_X4': 'ZN1',
    'AND4_X1': 'ZN1',
    'AND4_X2': 'ZN1',
    'AND4_X4': 'ZN1',
    'AOI21_X1': 'ZN1',
    'AOI21_X2': 'ZN1',
    'AOI21_X4': 'ZN1',
    'AOI22_X1': 'ZN1',
    'AOI22_X2': 'ZN1',
    'AOI22_X4': 'ZN1',
    'AOI211_X1': 'ZN1',
    'AOI211_X2': 'ZN1',
    'AOI211_X4': 'ZN1',
    'AOI221_X1': 'ZN1',
    'AOI221_X2': 'ZN1',
    'AOI221_X4': 'ZN1',
    'AOI222_X1': 'ZN1',
    'AOI222_X2': 'ZN1',
    'AOI222_X4': 'ZN1',
    'BUF_X1': 'Z1',
    'BUF_X2': 'Z1',
    'BUF_X4': 'Z1',
    'BUF_X8': 'Z1',
    'BUF_X16': 'Z1',
    'BUF_X32': 'Z1',
    'CLKBUF_X1': 'Z1',
    'CLKBUF_X2': 'Z1',
    'CLKBUF_X3': 'Z1',
    'DFFRS_X1': 'Q1QN1',
    'DFFRS_X2': 'Q1QN1',
    'DFFR_X1': 'Q1QN1',
    'DFFR_X2': 'Q1QN1',
    'DFFS_X1': 'Q1QN1',
    'DFFS_X2': 'Q1QN1',
    'DFF_X1': 'Q1QN1',
    'DFF_X2': 'Q1QN1',
    'DLH_X1': 'Q1',
    'DLH_X2': 'Q1',
    'DLL_X1': 'Q1',
    'DLL_X2': 'Q1',
    'FA_X1': 'CO1S1',
    'HA_X1': 'CO1S1',
    'INV_X1': 'ZN1',
    'INV_X2': 'ZN1',
    'INV_X4': 'ZN1',
    'INV_X8': 'ZN1',
    'INV_X16': 'ZN1',
    'INV_X32': 'ZN1',
    'MUX2_X1': 'Z1',
    'MUX2_X2': 'Z1',
    'NAND2_X1': 'ZN1',
    'NAND2_X2': 'ZN1',
    'NAND2_X4': 'ZN1',
    'NAND3_X1': 'ZN1',
    'NAND3_X2': 'ZN1',
    'NAND3_X4': 'ZN1',
    'NAND4_X1': 'ZN1',
    'NAND4_X2': 'ZN1',
    'NAND4_X4': 'ZN1',
    'NOR2_X1': 'ZN1',
    'NOR2_X2': 'ZN1',
    'NOR2_X4': 'ZN1',
    'NOR3_X1': 'ZN1',
    'NOR3_X2': 'ZN1',
    'NOR3_X4': 'ZN1',
    'NOR4_X1': 'ZN1',
    'NOR4_X2': 'ZN1',
    'NOR4_X4': 'ZN1',
    'OAI21_X1': 'ZN1',
    'OAI21_X2': 'ZN1',
    'OAI21_X4': 'ZN1',
    'OAI22_X1': 'ZN1',
    'OAI22_X2': 'ZN1',
    'OAI22_X4': 'ZN1',
    'OAI33_X1': 'ZN1',
    'OAI211_X1': 'ZN1',
    'OAI211_X2': 'ZN1',
    'OAI211_X4': 'ZN1',
    'OAI221_X1': 'ZN1',
    'OAI221_X2': 'ZN1',
    'OAI221_X4': 'ZN1',
    'OAI222_X1': 'ZN1',
    'OAI222_X2': 'ZN1',
    'OAI222_X4': 'ZN1',
    'OR2_X1': 'ZN1',
    'OR2_X2': 'ZN1',
    'OR2_X4': 'ZN1',
    'OR3_X1': 'ZN1',
    'OR3_X2': 'ZN1',
    'OR3_X4': 'ZN1',
    'OR4_X1': 'ZN1',
    'OR4_X2': 'ZN1',
    'OR4_X4': 'ZN1',
    'SDFFRS_X1': 'Q1QN1',
    'SDFFRS_X2': 'Q1QN1',
    'SDFFR_X1': 'Q1QN1',
    'SDFFR_X2': 'Q1QN1',
    'SDFFS_X1': 'Q1QN1',
    'SDFFS_X2': 'Q1QN1',
    'SDFF_X1': 'Q1QN1',
    'SDFF_X2': 'Q1QN1',
    'TBUF_X1': 'Z1',
    'TBUF_X2': 'Z1',
    'TBUF_X4': 'Z1',
    'TBUF_X8': 'Z1',
    'TBUF_X16': 'Z1',
    'TINV_X1': 'ZN1',
    'TLAT_X1': 'Q1',
    'XNOR2_X1': 'ZN1',
    'XNOR2_X2': 'ZN1',
    'XOR2_X1': 'Z1',
    'XOR2_X2': 'Z1',
    'input': 'OTFI_I1',
    'input_fault': 'OTFI_I1'
}

out_type_pins = {
    'A2': {'ZN', 'node_name'},
    'A3': {'ZN', 'node_name'},
    'A4': {'ZN', 'node_name'},
    'A1B2': {'ZN', 'node_name'},
    'A2B2': {'ZN', 'node_name'},
    'A1B1C2': {'ZN', 'node_name'},
    'A1B2C2': {'ZN', 'node_name'},
    'A2B2C2': {'ZN', 'node_name'},
    'A1': {'ZN', 'node_name'},
    'D1RN1KN1CK1': {'Q', 'QN', 'node_name'},
    'D1RN1CK1': {'Q', 'QN', 'node_name'},
    'D1KN1CK1': {'Q', 'QN', 'node_name'},
    'D1CK1': {'Q', 'QN', 'node_name'},
    'D1G1': {'Q', 'node_name'},
    'D1GN1': {'Q', 'node_name'},
    'A1B1CL1': {'CO', 'S', 'node_name'},
    'A1B1': {'Z', 'node_name'},
    'A1B1K1': {'Z', 'node_name'},
    'A3B3': {'ZN', 'node_name'},
    'D1RN1KE1KL1KN1CK1': {'Q', 'QN', 'node_name'},
    'D1RN1KE1KL1CK1': {'Q', 'QN', 'node_name'},
    'D1KE1KL1KN1CK1': {'Q', 'QN', 'node_name'},
    'D1KE1KL1CK1': {'Q', 'QN', 'node_name'},
    'A1EN1': {'Z', 'node_name'},
    'EN1L1': {'ZN', 'node_name'},
    'D1G1OE1': {'Q', 'node_name'},
}

#                   Adaption needed for a new cell library                     #
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
pin_out_mapping = {'ZN1': {'Z1': {'ZN': 'Z'}}, 'Z1': {'ZN1': {'Z': 'ZN'}}}

#                                DO NOT EDIT                                   #


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
    filter_types = {
        "in_node", "out_node", "input", "output", "input_formula", "xnor",
        "xor"
    }
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

def validate_generic_inputs(inputs: dict, num_inputs: int, type: str) -> dict:
    """ Validates the provided input of a generic gate.

    Generic gates, such as inputs, have generic input ports. Rename them to
    input + counter.

    Args:
        inputs: The list of provided inputs.
        num_inputs: The number of expected inputs.
        type: The type of the gate.

    Returns:
        The inputs for the generic gate.
    """
    if len(inputs) != num_inputs:
        logger.error(inputs)
        raise Exception('Gate ' + type + ' is missing some inputs.')
    input_symbols = {}
    in_count = 0
    for input_pin, input in inputs.items():
        if input_pin == "node_name":
            input_symbols[input_pin] = input.name
        else:
            input_symbols["input_" + str(in_count)] = input.name
            in_count += 1
    return input_symbols

def AND2_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AND2_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'AND2_X1_ZN')
    solver.add_clause([p['A1'], -p['node_name']])
    solver.add_clause([p['A2'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A1'], -p['A2']])


def AND2_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AND2_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'AND2_X2_ZN')
    solver.add_clause([p['A1'], -p['node_name']])
    solver.add_clause([p['A2'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A1'], -p['A2']])


def AND2_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AND2_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'AND2_X4_ZN')
    solver.add_clause([p['A1'], -p['node_name']])
    solver.add_clause([p['A2'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A1'], -p['A2']])


def AND3_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AND3_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = ((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'AND3_X1_ZN')
    solver.add_clause([p['A1'], -p['node_name']])
    solver.add_clause([p['A2'], -p['node_name']])
    solver.add_clause([p['A3'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A1'], -p['A2'], -p['A3']])


def AND3_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AND3_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = ((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'AND3_X2_ZN')
    solver.add_clause([p['A1'], -p['node_name']])
    solver.add_clause([p['A2'], -p['node_name']])
    solver.add_clause([p['A3'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A1'], -p['A2'], -p['A3']])


def AND3_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AND3_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = ((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'AND3_X4_ZN')
    solver.add_clause([p['A1'], -p['node_name']])
    solver.add_clause([p['A2'], -p['node_name']])
    solver.add_clause([p['A3'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A1'], -p['A2'], -p['A3']])


def AND4_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AND4_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'AND4_X1_ZN')
    solver.add_clause([p['A1'], -p['node_name']])
    solver.add_clause([p['A2'], -p['node_name']])
    solver.add_clause([p['A3'], -p['node_name']])
    solver.add_clause([p['A4'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4']])


def AND4_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AND4_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'AND4_X2_ZN')
    solver.add_clause([p['A1'], -p['node_name']])
    solver.add_clause([p['A2'], -p['node_name']])
    solver.add_clause([p['A3'], -p['node_name']])
    solver.add_clause([p['A4'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4']])


def AND4_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AND4_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'AND4_X4_ZN')
    solver.add_clause([p['A1'], -p['node_name']])
    solver.add_clause([p['A2'], -p['node_name']])
    solver.add_clause([p['A3'], -p['node_name']])
    solver.add_clause([p['A4'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A1'], -p['A2'], -p['A3'], -p['A4']])


def AOI21_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI21_X1_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI21_X1_ZN')
    solver.add_clause([p['A'], p['B1'], p['node_name']])
    solver.add_clause([p['A'], p['B2'], p['node_name']])
    solver.add_clause([-p['A'], -p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])


def AOI21_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI21_X2_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI21_X2_ZN')
    solver.add_clause([p['A'], p['B1'], p['node_name']])
    solver.add_clause([p['A'], p['B2'], p['node_name']])
    solver.add_clause([-p['A'], -p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])


def AOI21_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI21_X4_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI21_X4_ZN')
    solver.add_clause([p['A'], p['B1'], p['node_name']])
    solver.add_clause([p['A'], p['B2'], p['node_name']])
    solver.add_clause([-p['A'], -p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])


def AOI22_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI22_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 & A2) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI22_X1_ZN')
    solver.add_clause([p['A1'], p['B1'], p['node_name']])
    solver.add_clause([p['A1'], p['B2'], p['node_name']])
    solver.add_clause([p['A2'], p['B1'], p['node_name']])
    solver.add_clause([p['A2'], p['B2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])


def AOI22_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI22_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 & A2) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI22_X2_ZN')
    solver.add_clause([p['A1'], p['B1'], p['node_name']])
    solver.add_clause([p['A1'], p['B2'], p['node_name']])
    solver.add_clause([p['A2'], p['B1'], p['node_name']])
    solver.add_clause([p['A2'], p['B2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])


def AOI22_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI22_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 & A2) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI22_X4_ZN')
    solver.add_clause([p['A1'], p['B1'], p['node_name']])
    solver.add_clause([p['A1'], p['B2'], p['node_name']])
    solver.add_clause([p['A2'], p['B1'], p['node_name']])
    solver.add_clause([p['A2'], p['B2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])


def AOI211_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI211_X1_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((C1 & C2) | B) | A)
    '''
    p = validate_inputs(inputs, graph, 'AOI211_X1_ZN')
    solver.add_clause([-p['A'], -p['node_name']])
    solver.add_clause([-p['B'], -p['node_name']])
    solver.add_clause([p['A'], p['B'], p['C1'], p['node_name']])
    solver.add_clause([p['A'], p['B'], p['C2'], p['node_name']])
    solver.add_clause([-p['C1'], -p['C2'], -p['node_name']])


def AOI211_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI211_X2_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((C1 & C2) | B) | A)
    '''
    p = validate_inputs(inputs, graph, 'AOI211_X2_ZN')
    solver.add_clause([-p['A'], -p['node_name']])
    solver.add_clause([-p['B'], -p['node_name']])
    solver.add_clause([p['A'], p['B'], p['C1'], p['node_name']])
    solver.add_clause([p['A'], p['B'], p['C2'], p['node_name']])
    solver.add_clause([-p['C1'], -p['C2'], -p['node_name']])


def AOI211_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI211_X4_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(!(!(((C1 & C2) | B) | A)))
    '''
    p = validate_inputs(inputs, graph, 'AOI211_X4_ZN')
    solver.add_clause([-p['A'], -p['node_name']])
    solver.add_clause([-p['B'], -p['node_name']])
    solver.add_clause([p['A'], p['B'], p['C1'], p['node_name']])
    solver.add_clause([p['A'], p['B'], p['C2'], p['node_name']])
    solver.add_clause([-p['C1'], -p['C2'], -p['node_name']])


def AOI221_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI221_X1_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((C1 & C2) | A) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI221_X1_ZN')
    solver.add_clause([-p['A'], -p['node_name']])
    solver.add_clause([p['A'], p['B1'], p['C1'], p['node_name']])
    solver.add_clause([p['A'], p['B1'], p['C2'], p['node_name']])
    solver.add_clause([p['A'], p['B2'], p['C1'], p['node_name']])
    solver.add_clause([p['A'], p['B2'], p['C2'], p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['C1'], -p['C2'], -p['node_name']])


def AOI221_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI221_X2_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((C1 & C2) | A) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI221_X2_ZN')
    solver.add_clause([-p['A'], -p['node_name']])
    solver.add_clause([p['A'], p['B1'], p['C1'], p['node_name']])
    solver.add_clause([p['A'], p['B1'], p['C2'], p['node_name']])
    solver.add_clause([p['A'], p['B2'], p['C1'], p['node_name']])
    solver.add_clause([p['A'], p['B2'], p['C2'], p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['C1'], -p['C2'], -p['node_name']])


def AOI221_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI221_X4_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(!(!(((C1 & C2) | A) | (B1 & B2))))
    '''
    p = validate_inputs(inputs, graph, 'AOI221_X4_ZN')
    solver.add_clause([-p['A'], -p['node_name']])
    solver.add_clause([p['A'], p['B1'], p['C1'], p['node_name']])
    solver.add_clause([p['A'], p['B1'], p['C2'], p['node_name']])
    solver.add_clause([p['A'], p['B2'], p['C1'], p['node_name']])
    solver.add_clause([p['A'], p['B2'], p['C2'], p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['C1'], -p['C2'], -p['node_name']])


def AOI222_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI222_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 & A2) | (B1 & B2)) | (C1 & C2))
    '''
    p = validate_inputs(inputs, graph, 'AOI222_X1_ZN')
    solver.add_clause([p['A1'], p['B1'], p['C1'], p['node_name']])
    solver.add_clause([p['A1'], p['B1'], p['C2'], p['node_name']])
    solver.add_clause([p['A1'], p['B2'], p['C1'], p['node_name']])
    solver.add_clause([p['A1'], p['B2'], p['C2'], p['node_name']])
    solver.add_clause([p['A2'], p['B1'], p['C1'], p['node_name']])
    solver.add_clause([p['A2'], p['B1'], p['C2'], p['node_name']])
    solver.add_clause([p['A2'], p['B2'], p['C1'], p['node_name']])
    solver.add_clause([p['A2'], p['B2'], p['C2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['C1'], -p['C2'], -p['node_name']])


def AOI222_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI222_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 & A2) | (B1 & B2)) | (C1 & C2))
    '''
    p = validate_inputs(inputs, graph, 'AOI222_X2_ZN')
    solver.add_clause([p['A1'], p['B1'], p['C1'], p['node_name']])
    solver.add_clause([p['A1'], p['B1'], p['C2'], p['node_name']])
    solver.add_clause([p['A1'], p['B2'], p['C1'], p['node_name']])
    solver.add_clause([p['A1'], p['B2'], p['C2'], p['node_name']])
    solver.add_clause([p['A2'], p['B1'], p['C1'], p['node_name']])
    solver.add_clause([p['A2'], p['B1'], p['C2'], p['node_name']])
    solver.add_clause([p['A2'], p['B2'], p['C1'], p['node_name']])
    solver.add_clause([p['A2'], p['B2'], p['C2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['C1'], -p['C2'], -p['node_name']])


def AOI222_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' AOI222_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(!(!(((A1 & A2) | (B1 & B2)) | (C1 & C2))))
    '''
    p = validate_inputs(inputs, graph, 'AOI222_X4_ZN')
    solver.add_clause([p['A1'], p['B1'], p['C1'], p['node_name']])
    solver.add_clause([p['A1'], p['B1'], p['C2'], p['node_name']])
    solver.add_clause([p['A1'], p['B2'], p['C1'], p['node_name']])
    solver.add_clause([p['A1'], p['B2'], p['C2'], p['node_name']])
    solver.add_clause([p['A2'], p['B1'], p['C1'], p['node_name']])
    solver.add_clause([p['A2'], p['B1'], p['C2'], p['node_name']])
    solver.add_clause([p['A2'], p['B2'], p['C1'], p['node_name']])
    solver.add_clause([p['A2'], p['B2'], p['C2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['node_name']])
    solver.add_clause([-p['B1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['C1'], -p['C2'], -p['node_name']])


def BUF_X1_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' BUF_X1_Z gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X1_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def BUF_X2_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' BUF_X2_Z gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X2_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def BUF_X4_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' BUF_X4_Z gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X4_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def BUF_X8_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' BUF_X8_Z gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X8_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def BUF_X16_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' BUF_X16_Z gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X16_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def BUF_X32_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' BUF_X32_Z gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X32_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def CLKBUF_X1_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' CLKBUF_X1_Z gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'CLKBUF_X1_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def CLKBUF_X2_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' CLKBUF_X2_Z gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'CLKBUF_X2_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def CLKBUF_X3_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' CLKBUF_X3_Z gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'CLKBUF_X3_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def FA_X1_CO(inputs: dict, graph: nx.DiGraph, solver):
    ''' FA_X1_CO gate.

    Args:
        inputs: { 'A', 'B', 'CL','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        CO = ((A & B) | (CI & (A | B)))
    '''
    p = validate_inputs(inputs, graph, 'FA_X1_CO')
    solver.add_clause([p['A'], p['B'], -p['node_name']])
    solver.add_clause([p['A'], p['CL'], -p['node_name']])
    solver.add_clause([p['B'], p['CL'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A'], -p['B']])
    solver.add_clause([p['node_name'], -p['A'], -p['CL']])
    solver.add_clause([p['node_name'], -p['B'], -p['CL']])


def FA_X1_S(inputs: dict, graph: nx.DiGraph, solver):
    ''' FA_X1_S gate.

    Args:
        inputs: { 'A', 'B', 'CL','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        S = (CI ^ (A ^ B))
    '''
    p = validate_inputs(inputs, graph, 'FA_X1_S')
    solver.add_clause([p['A'], p['B'], p['CL'], -p['node_name']])
    solver.add_clause([p['A'], p['B'], p['node_name'], -p['CL']])
    solver.add_clause([p['A'], p['CL'], p['node_name'], -p['B']])
    solver.add_clause([p['B'], p['CL'], p['node_name'], -p['A']])
    solver.add_clause([p['A'], -p['B'], -p['CL'], -p['node_name']])
    solver.add_clause([p['B'], -p['A'], -p['CL'], -p['node_name']])
    solver.add_clause([p['CL'], -p['A'], -p['B'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A'], -p['B'], -p['CL']])


def HA_X1_CO(inputs: dict, graph: nx.DiGraph, solver):
    ''' HA_X1_CO gate.

    Args:
        inputs: { 'A', 'B','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        CO = (A & B)
    '''
    p = validate_inputs(inputs, graph, 'HA_X1_CO')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['B'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A'], -p['B']])


def HA_X1_S(inputs: dict, graph: nx.DiGraph, solver):
    ''' HA_X1_S gate.

    Args:
        inputs: { 'A', 'B','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        S = (A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'HA_X1_S')
    solver.add_clause([p['A'], p['B'], -p['node_name']])
    solver.add_clause([p['A'], p['node_name'], -p['B']])
    solver.add_clause([p['B'], p['node_name'], -p['A']])
    solver.add_clause([-p['A'], -p['B'], -p['node_name']])


def INV_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' INV_X1_ZN gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X1_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([-p['A'], -p['node_name']])


def INV_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' INV_X2_ZN gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X2_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([-p['A'], -p['node_name']])


def INV_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' INV_X4_ZN gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X4_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([-p['A'], -p['node_name']])


def INV_X8_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' INV_X8_ZN gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X8_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([-p['A'], -p['node_name']])


def INV_X16_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' INV_X16_ZN gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X16_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([-p['A'], -p['node_name']])


def INV_X32_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' INV_X32_ZN gate.

    Args:
        inputs: { 'A','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X32_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([-p['A'], -p['node_name']])


def MUX2_X1_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' MUX2_X1_Z gate.

    Args:
        inputs: { 'A', 'B', 'K','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = ((S & B) | (A & !S))
    '''
    p = validate_inputs(inputs, graph, 'MUX2_X1_Z')
    solver.add_clause([p['A'], p['K'], -p['node_name']])
    solver.add_clause([p['K'], p['node_name'], -p['A']])
    solver.add_clause([p['B'], -p['K'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['B'], -p['K']])


def MUX2_X2_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' MUX2_X2_Z gate.

    Args:
        inputs: { 'A', 'B', 'K','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = ((S & B) | (A & !S))
    '''
    p = validate_inputs(inputs, graph, 'MUX2_X2_Z')
    solver.add_clause([p['A'], p['K'], -p['node_name']])
    solver.add_clause([p['K'], p['node_name'], -p['A']])
    solver.add_clause([p['B'], -p['K'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['B'], -p['K']])


def NAND2_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NAND2_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'NAND2_X1_ZN')
    solver.add_clause([p['A1'], p['node_name']])
    solver.add_clause([p['A2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['node_name']])


def NAND2_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NAND2_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'NAND2_X2_ZN')
    solver.add_clause([p['A1'], p['node_name']])
    solver.add_clause([p['A2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['node_name']])


def NAND2_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NAND2_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'NAND2_X4_ZN')
    solver.add_clause([p['A1'], p['node_name']])
    solver.add_clause([p['A2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['node_name']])


def NAND3_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NAND3_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'NAND3_X1_ZN')
    solver.add_clause([p['A1'], p['node_name']])
    solver.add_clause([p['A2'], p['node_name']])
    solver.add_clause([p['A3'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['A3'], -p['node_name']])


def NAND3_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NAND3_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'NAND3_X2_ZN')
    solver.add_clause([p['A1'], p['node_name']])
    solver.add_clause([p['A2'], p['node_name']])
    solver.add_clause([p['A3'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['A3'], -p['node_name']])


def NAND3_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NAND3_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'NAND3_X4_ZN')
    solver.add_clause([p['A1'], p['node_name']])
    solver.add_clause([p['A2'], p['node_name']])
    solver.add_clause([p['A3'], p['node_name']])
    solver.add_clause([-p['A1'], -p['A2'], -p['A3'], -p['node_name']])


def NAND4_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NAND4_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'NAND4_X1_ZN')
    solver.add_clause([p['A1'], p['node_name']])
    solver.add_clause([p['A2'], p['node_name']])
    solver.add_clause([p['A3'], p['node_name']])
    solver.add_clause([p['A4'], p['node_name']])
    solver.add_clause(
        [-p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['node_name']])


def NAND4_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NAND4_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'NAND4_X2_ZN')
    solver.add_clause([p['A1'], p['node_name']])
    solver.add_clause([p['A2'], p['node_name']])
    solver.add_clause([p['A3'], p['node_name']])
    solver.add_clause([p['A4'], p['node_name']])
    solver.add_clause(
        [-p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['node_name']])


def NAND4_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NAND4_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'NAND4_X4_ZN')
    solver.add_clause([p['A1'], p['node_name']])
    solver.add_clause([p['A2'], p['node_name']])
    solver.add_clause([p['A3'], p['node_name']])
    solver.add_clause([p['A4'], p['node_name']])
    solver.add_clause(
        [-p['A1'], -p['A2'], -p['A3'], -p['A4'], -p['node_name']])


def NOR2_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NOR2_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'NOR2_X1_ZN')
    solver.add_clause([p['A1'], p['A2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['node_name']])


def NOR2_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NOR2_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'NOR2_X2_ZN')
    solver.add_clause([p['A1'], p['A2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['node_name']])


def NOR2_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NOR2_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'NOR2_X4_ZN')
    solver.add_clause([p['A1'], p['A2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['node_name']])


def NOR3_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NOR3_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'NOR3_X1_ZN')
    solver.add_clause([-p['A1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['node_name']])
    solver.add_clause([-p['A3'], -p['node_name']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['node_name']])


def NOR3_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NOR3_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'NOR3_X2_ZN')
    solver.add_clause([-p['A1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['node_name']])
    solver.add_clause([-p['A3'], -p['node_name']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['node_name']])


def NOR3_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NOR3_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'NOR3_X4_ZN')
    solver.add_clause([-p['A1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['node_name']])
    solver.add_clause([-p['A3'], -p['node_name']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['node_name']])


def NOR4_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NOR4_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'NOR4_X1_ZN')
    solver.add_clause([-p['A1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['node_name']])
    solver.add_clause([-p['A3'], -p['node_name']])
    solver.add_clause([-p['A4'], -p['node_name']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['A4'], p['node_name']])


def NOR4_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NOR4_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'NOR4_X2_ZN')
    solver.add_clause([-p['A1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['node_name']])
    solver.add_clause([-p['A3'], -p['node_name']])
    solver.add_clause([-p['A4'], -p['node_name']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['A4'], p['node_name']])


def NOR4_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' NOR4_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'NOR4_X4_ZN')
    solver.add_clause([-p['A1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['node_name']])
    solver.add_clause([-p['A3'], -p['node_name']])
    solver.add_clause([-p['A4'], -p['node_name']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['A4'], p['node_name']])


def OAI21_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI21_X1_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI21_X1_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([-p['A'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B2'], -p['node_name']])


def OAI21_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI21_X2_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI21_X2_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([-p['A'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B2'], -p['node_name']])


def OAI21_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI21_X4_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI21_X4_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([-p['A'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B2'], -p['node_name']])


def OAI22_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI22_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 | A2) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI22_X1_ZN')
    solver.add_clause([p['A1'], p['A2'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['node_name']])


def OAI22_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI22_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 | A2) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI22_X2_ZN')
    solver.add_clause([p['A1'], p['A2'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['node_name']])


def OAI22_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI22_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !((A1 | A2) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI22_X4_ZN')
    solver.add_clause([p['A1'], p['A2'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['node_name']])


def OAI33_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI33_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'B1', 'B2', 'B3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 | A2) | A3) & ((B1 | B2) | B3))
    '''
    p = validate_inputs(inputs, graph, 'OAI33_X1_ZN')
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['B3'], p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B3'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B3'], -p['node_name']])
    solver.add_clause([-p['A3'], -p['B1'], -p['node_name']])
    solver.add_clause([-p['A3'], -p['B2'], -p['node_name']])
    solver.add_clause([-p['A3'], -p['B3'], -p['node_name']])


def OAI211_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI211_X1_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((C1 | C2) & A) & B)
    '''
    p = validate_inputs(inputs, graph, 'OAI211_X1_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([p['B'], p['node_name']])
    solver.add_clause([p['C1'], p['C2'], p['node_name']])
    solver.add_clause([-p['A'], -p['B'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B'], -p['C2'], -p['node_name']])


def OAI211_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI211_X2_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((C1 | C2) & A) & B)
    '''
    p = validate_inputs(inputs, graph, 'OAI211_X2_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([p['B'], p['node_name']])
    solver.add_clause([p['C1'], p['C2'], p['node_name']])
    solver.add_clause([-p['A'], -p['B'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B'], -p['C2'], -p['node_name']])


def OAI211_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI211_X4_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((C1 | C2) & A) & B)
    '''
    p = validate_inputs(inputs, graph, 'OAI211_X4_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([p['B'], p['node_name']])
    solver.add_clause([p['C1'], p['C2'], p['node_name']])
    solver.add_clause([-p['A'], -p['B'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B'], -p['C2'], -p['node_name']])


def OAI221_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI221_X1_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((C1 | C2) & A) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI221_X1_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([p['C1'], p['C2'], p['node_name']])
    solver.add_clause([-p['A'], -p['B1'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B1'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B2'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B2'], -p['C2'], -p['node_name']])


def OAI221_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI221_X2_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((C1 | C2) & A) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI221_X2_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([p['C1'], p['C2'], p['node_name']])
    solver.add_clause([-p['A'], -p['B1'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B1'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B2'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B2'], -p['C2'], -p['node_name']])


def OAI221_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI221_X4_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(!(!(((C1 | C2) & A) & (B1 | B2))))
    '''
    p = validate_inputs(inputs, graph, 'OAI221_X4_ZN')
    solver.add_clause([p['A'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([p['C1'], p['C2'], p['node_name']])
    solver.add_clause([-p['A'], -p['B1'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B1'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B2'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A'], -p['B2'], -p['C2'], -p['node_name']])


def OAI222_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI222_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 | A2) & (B1 | B2)) & (C1 | C2))
    '''
    p = validate_inputs(inputs, graph, 'OAI222_X1_ZN')
    solver.add_clause([p['A1'], p['A2'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([p['C1'], p['C2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['C2'], -p['node_name']])


def OAI222_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI222_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(((A1 | A2) & (B1 | B2)) & (C1 | C2))
    '''
    p = validate_inputs(inputs, graph, 'OAI222_X2_ZN')
    solver.add_clause([p['A1'], p['A2'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([p['C1'], p['C2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['C2'], -p['node_name']])


def OAI222_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OAI222_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(!(!(((A1 | A2) & (B1 | B2)) & (C1 | C2))))
    '''
    p = validate_inputs(inputs, graph, 'OAI222_X4_ZN')
    solver.add_clause([p['A1'], p['A2'], p['node_name']])
    solver.add_clause([p['B1'], p['B2'], p['node_name']])
    solver.add_clause([p['C1'], p['C2'], p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B1'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A1'], -p['B2'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B1'], -p['C2'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['C1'], -p['node_name']])
    solver.add_clause([-p['A2'], -p['B2'], -p['C2'], -p['node_name']])


def OR2_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OR2_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'OR2_X1_ZN')
    solver.add_clause([p['node_name'], -p['A1']])
    solver.add_clause([p['node_name'], -p['A2']])
    solver.add_clause([p['A1'], p['A2'], -p['node_name']])


def OR2_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OR2_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'OR2_X2_ZN')
    solver.add_clause([p['node_name'], -p['A1']])
    solver.add_clause([p['node_name'], -p['A2']])
    solver.add_clause([p['A1'], p['A2'], -p['node_name']])


def OR2_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OR2_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'OR2_X4_ZN')
    solver.add_clause([p['node_name'], -p['A1']])
    solver.add_clause([p['node_name'], -p['A2']])
    solver.add_clause([p['A1'], p['A2'], -p['node_name']])


def OR3_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OR3_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = ((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'OR3_X1_ZN')
    solver.add_clause([p['node_name'], -p['A1']])
    solver.add_clause([p['node_name'], -p['A2']])
    solver.add_clause([p['node_name'], -p['A3']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], -p['node_name']])


def OR3_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OR3_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = ((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'OR3_X2_ZN')
    solver.add_clause([p['node_name'], -p['A1']])
    solver.add_clause([p['node_name'], -p['A2']])
    solver.add_clause([p['node_name'], -p['A3']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], -p['node_name']])


def OR3_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OR3_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = ((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'OR3_X4_ZN')
    solver.add_clause([p['node_name'], -p['A1']])
    solver.add_clause([p['node_name'], -p['A2']])
    solver.add_clause([p['node_name'], -p['A3']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], -p['node_name']])


def OR4_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OR4_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'OR4_X1_ZN')
    solver.add_clause([p['node_name'], -p['A1']])
    solver.add_clause([p['node_name'], -p['A2']])
    solver.add_clause([p['node_name'], -p['A3']])
    solver.add_clause([p['node_name'], -p['A4']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['A4'], -p['node_name']])


def OR4_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OR4_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'OR4_X2_ZN')
    solver.add_clause([p['node_name'], -p['A1']])
    solver.add_clause([p['node_name'], -p['A2']])
    solver.add_clause([p['node_name'], -p['A3']])
    solver.add_clause([p['node_name'], -p['A4']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['A4'], -p['node_name']])


def OR4_X4_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' OR4_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = (((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'OR4_X4_ZN')
    solver.add_clause([p['node_name'], -p['A1']])
    solver.add_clause([p['node_name'], -p['A2']])
    solver.add_clause([p['node_name'], -p['A3']])
    solver.add_clause([p['node_name'], -p['A4']])
    solver.add_clause([p['A1'], p['A2'], p['A3'], p['A4'], -p['node_name']])


def TBUF_X1_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' TBUF_X1_Z gate.

    Args:
        inputs: { 'A', 'EN','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X1_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def TBUF_X2_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' TBUF_X2_Z gate.

    Args:
        inputs: { 'A', 'EN','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X2_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def TBUF_X4_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' TBUF_X4_Z gate.

    Args:
        inputs: { 'A', 'EN','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X4_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def TBUF_X8_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' TBUF_X8_Z gate.

    Args:
        inputs: { 'A', 'EN','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X8_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def TBUF_X16_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' TBUF_X16_Z gate.

    Args:
        inputs: { 'A', 'EN','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X16_Z')
    solver.add_clause([p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A']])


def TINV_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' TINV_X1_ZN gate.

    Args:
        inputs: { 'EN', 'L','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !I
    '''
    p = validate_inputs(inputs, graph, 'TINV_X1_ZN')
    solver.add_clause([p['L'], p['node_name']])
    solver.add_clause([-p['L'], -p['node_name']])


def XNOR2_X1_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' XNOR2_X1_ZN gate.

    Args:
        inputs: { 'A', 'B','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'XNOR2_X1_ZN')
    solver.add_clause([p['A'], p['B'], p['node_name']])
    solver.add_clause([p['A'], -p['B'], -p['node_name']])
    solver.add_clause([p['B'], -p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A'], -p['B']])


def XNOR2_X2_ZN(inputs: dict, graph: nx.DiGraph, solver):
    ''' XNOR2_X2_ZN gate.

    Args:
        inputs: { 'A', 'B','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = !(A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'XNOR2_X2_ZN')
    solver.add_clause([p['A'], p['B'], p['node_name']])
    solver.add_clause([p['A'], -p['B'], -p['node_name']])
    solver.add_clause([p['B'], -p['A'], -p['node_name']])
    solver.add_clause([p['node_name'], -p['A'], -p['B']])


def XOR2_X1_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' XOR2_X1_Z gate.

    Args:
        inputs: { 'A', 'B','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = (A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'XOR2_X1_Z')
    solver.add_clause([p['A'], p['B'], -p['node_name']])
    solver.add_clause([p['A'], p['node_name'], -p['B']])
    solver.add_clause([p['B'], p['node_name'], -p['A']])
    solver.add_clause([-p['A'], -p['B'], -p['node_name']])


def XOR2_X2_Z(inputs: dict, graph: nx.DiGraph, solver):
    ''' XOR2_X2_Z gate.

    Args:
        inputs: { 'A', 'B','node_name' }
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        Z = (A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'XOR2_X2_Z')
    solver.add_clause([p['A'], p['B'], -p['node_name']])
    solver.add_clause([p['A'], p['node_name'], -p['B']])
    solver.add_clause([p['B'], p['node_name'], -p['A']])
    solver.add_clause([-p['A'], -p['B'], -p['node_name']])


#                      OTFI SPECIFC CELLS - DO NOT EDIT                        #
def xnor(inputs: dict, graph: nx.DiGraph, solver):
    """ xnor gate.

    Args:
        inputs: {'input_0', 'input_1', 'node_name'}.
        graph: The networkx graph of the circuit.
        solver: The SAT solver instance.

    Returns:
        ZN = '!(input_0 ^ input_1)'.
    """
    p = validate_generic_inputs(inputs, 3, 'xnor')
    solver.add_clause([-p['input_0'], -p['input_1'], p['node_name']])
    solver.add_clause([p['input_0'], p['input_1'], p['node_name']])
    solver.add_clause([p['input_0'], -p['input_1'], -p['node_name']])
    solver.add_clause([-p['input_0'], p['input_1'], -p['node_name']])


def xor(inputs: dict, graph: nx.DiGraph, solver):
    """ xor gate.

    Args:
        inputs: {'input_0', 'input_1', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = '(input_0 ^ input_1)'.
    """
    p = validate_generic_inputs(inputs, 3, 'xor')
    solver.add_clause([-p['input_0'], -p['input_1'], -p['node_name']])
    solver.add_clause([p['input_0'], p['input_1'], -p['node_name']])
    solver.add_clause([p['input_0'], -p['input_1'], p['node_name']])
    solver.add_clause([-p['input_0'], p['input_1'], p['node_name']])


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
        inputs: {'input_0', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        0 or 1.
    """
    p = validate_generic_inputs(inputs, 2, "input_formula_Q")

    if one == p['input_0']:
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
        inputs: {'input_0', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        0 or 1.
    """
    p = validate_generic_inputs(inputs, 2, "input_formula_QN")

    if one == p['input_0']:
        # Input is connected to 1.
        # Return a zero.
        solver.add_clause([-zero, p['node_name']])
        solver.add_clause([zero, -p['node_name']])
    else:
        # Input ist connected to 0.
        # Return a one.
        solver.add_clause([-one, p['node_name']])
        solver.add_clause([one, -p['node_name']])


def in_node_Q(inputs: dict, graph: nx.DiGraph, solver):
    """ In node Q

    Args:
        inputs: {'input_0', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        Q = input_0
    """
    p = validate_generic_inputs(inputs, 2, "in_node_Q")
    solver.add_clause([-p['input_0'], p['node_name']])
    solver.add_clause([p['input_0'], -p['node_name']])


def in_node_QN(inputs: dict, graph: nx.DiGraph, solver):
    """ In node QN

    Args:
        inputs: {'input_0', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        Q = !input_0
    """
    p = validate_generic_inputs(inputs, 2, "in_node_QN")
    solver.add_clause([-p['I1'], -p['node_name']])
    solver.add_clause([p['I1'], p['node_name']])


def out_node(inputs: dict, graph: nx.DiGraph, solver):
    """ Out node.

    Args:
        inputs: {'input_0', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = input_0.
    """
    p = validate_generic_inputs(inputs, 2, "out_node")
    solver.add_clause([-p['input_0'], p['node_name']])
    solver.add_clause([p['input_0'], -p['node_name']])


def output(inputs: dict, graph: nx.DiGraph, solver):
    """ Out node.

    Args:
        inputs: {'D', 'node_name'}.
        graph: The networkx graph of the circuit.

    Returns:
        ZN = I.
    """
    p = validate_generic_inputs(inputs, 2, "output")
    solver.add_clause([-p['input_0'], p['node_name']])
    solver.add_clause([p['input_0'], -p['node_name']])


cell_mapping = {
    'AND2_X1_ZN': AND2_X1_ZN,
    'AND2_X2_ZN': AND2_X2_ZN,
    'AND2_X4_ZN': AND2_X4_ZN,
    'AND3_X1_ZN': AND3_X1_ZN,
    'AND3_X2_ZN': AND3_X2_ZN,
    'AND3_X4_ZN': AND3_X4_ZN,
    'AND4_X1_ZN': AND4_X1_ZN,
    'AND4_X2_ZN': AND4_X2_ZN,
    'AND4_X4_ZN': AND4_X4_ZN,
    'AOI21_X1_ZN': AOI21_X1_ZN,
    'AOI21_X2_ZN': AOI21_X2_ZN,
    'AOI21_X4_ZN': AOI21_X4_ZN,
    'AOI22_X1_ZN': AOI22_X1_ZN,
    'AOI22_X2_ZN': AOI22_X2_ZN,
    'AOI22_X4_ZN': AOI22_X4_ZN,
    'AOI211_X1_ZN': AOI211_X1_ZN,
    'AOI211_X2_ZN': AOI211_X2_ZN,
    'AOI211_X4_ZN': AOI211_X4_ZN,
    'AOI221_X1_ZN': AOI221_X1_ZN,
    'AOI221_X2_ZN': AOI221_X2_ZN,
    'AOI221_X4_ZN': AOI221_X4_ZN,
    'AOI222_X1_ZN': AOI222_X1_ZN,
    'AOI222_X2_ZN': AOI222_X2_ZN,
    'AOI222_X4_ZN': AOI222_X4_ZN,
    'BUF_X1_Z': BUF_X1_Z,
    'BUF_X2_Z': BUF_X2_Z,
    'BUF_X4_Z': BUF_X4_Z,
    'BUF_X8_Z': BUF_X8_Z,
    'BUF_X16_Z': BUF_X16_Z,
    'BUF_X32_Z': BUF_X32_Z,
    'CLKBUF_X1_Z': CLKBUF_X1_Z,
    'CLKBUF_X2_Z': CLKBUF_X2_Z,
    'CLKBUF_X3_Z': CLKBUF_X3_Z,
    'FA_X1_CO': FA_X1_CO,
    'FA_X1_S': FA_X1_S,
    'HA_X1_CO': HA_X1_CO,
    'HA_X1_S': HA_X1_S,
    'INV_X1_ZN': INV_X1_ZN,
    'INV_X2_ZN': INV_X2_ZN,
    'INV_X4_ZN': INV_X4_ZN,
    'INV_X8_ZN': INV_X8_ZN,
    'INV_X16_ZN': INV_X16_ZN,
    'INV_X32_ZN': INV_X32_ZN,
    'MUX2_X1_Z': MUX2_X1_Z,
    'MUX2_X2_Z': MUX2_X2_Z,
    'NAND2_X1_ZN': NAND2_X1_ZN,
    'NAND2_X2_ZN': NAND2_X2_ZN,
    'NAND2_X4_ZN': NAND2_X4_ZN,
    'NAND3_X1_ZN': NAND3_X1_ZN,
    'NAND3_X2_ZN': NAND3_X2_ZN,
    'NAND3_X4_ZN': NAND3_X4_ZN,
    'NAND4_X1_ZN': NAND4_X1_ZN,
    'NAND4_X2_ZN': NAND4_X2_ZN,
    'NAND4_X4_ZN': NAND4_X4_ZN,
    'NOR2_X1_ZN': NOR2_X1_ZN,
    'NOR2_X2_ZN': NOR2_X2_ZN,
    'NOR2_X4_ZN': NOR2_X4_ZN,
    'NOR3_X1_ZN': NOR3_X1_ZN,
    'NOR3_X2_ZN': NOR3_X2_ZN,
    'NOR3_X4_ZN': NOR3_X4_ZN,
    'NOR4_X1_ZN': NOR4_X1_ZN,
    'NOR4_X2_ZN': NOR4_X2_ZN,
    'NOR4_X4_ZN': NOR4_X4_ZN,
    'OAI21_X1_ZN': OAI21_X1_ZN,
    'OAI21_X2_ZN': OAI21_X2_ZN,
    'OAI21_X4_ZN': OAI21_X4_ZN,
    'OAI22_X1_ZN': OAI22_X1_ZN,
    'OAI22_X2_ZN': OAI22_X2_ZN,
    'OAI22_X4_ZN': OAI22_X4_ZN,
    'OAI33_X1_ZN': OAI33_X1_ZN,
    'OAI211_X1_ZN': OAI211_X1_ZN,
    'OAI211_X2_ZN': OAI211_X2_ZN,
    'OAI211_X4_ZN': OAI211_X4_ZN,
    'OAI221_X1_ZN': OAI221_X1_ZN,
    'OAI221_X2_ZN': OAI221_X2_ZN,
    'OAI221_X4_ZN': OAI221_X4_ZN,
    'OAI222_X1_ZN': OAI222_X1_ZN,
    'OAI222_X2_ZN': OAI222_X2_ZN,
    'OAI222_X4_ZN': OAI222_X4_ZN,
    'OR2_X1_ZN': OR2_X1_ZN,
    'OR2_X2_ZN': OR2_X2_ZN,
    'OR2_X4_ZN': OR2_X4_ZN,
    'OR3_X1_ZN': OR3_X1_ZN,
    'OR3_X2_ZN': OR3_X2_ZN,
    'OR3_X4_ZN': OR3_X4_ZN,
    'OR4_X1_ZN': OR4_X1_ZN,
    'OR4_X2_ZN': OR4_X2_ZN,
    'OR4_X4_ZN': OR4_X4_ZN,
    'TBUF_X1_Z': TBUF_X1_Z,
    'TBUF_X2_Z': TBUF_X2_Z,
    'TBUF_X4_Z': TBUF_X4_Z,
    'TBUF_X8_Z': TBUF_X8_Z,
    'TBUF_X16_Z': TBUF_X16_Z,
    'TINV_X1_ZN': TINV_X1_ZN,
    'XNOR2_X1_ZN': XNOR2_X1_ZN,
    'XNOR2_X2_ZN': XNOR2_X2_ZN,
    'XOR2_X1_Z': XOR2_X1_Z,
    'XOR2_X2_Z': XOR2_X2_Z,
    'xnor_O': xnor,
    'xor_O': xor,
    'and_O': and_output,
    'or_O': or_output,
    'input_Q': input_formula_Q,
    'input_QN': input_formula_QN,
    'input_fault_Q': input_formula_Q,
    'input_fault_QN': input_formula_QN,
    'in_node_Q': in_node_Q,
    'in_node_QN': in_node_QN,
    'out_node_Q': out_node,
    'out_node_QN': out_node,
    'output_O': output
}
