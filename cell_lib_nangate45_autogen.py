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
clk_name = 'clk_i'
clk_value = true

rst_name = 'rst_ni'
rst_value = false

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
    'register': 'D1',
    'out_node': 'D1',
    'xnor': 'I2',
    'xor': 'I2',
    'input_formula': 'I1',
    'in_node': 'I1',
    'output': 'I1'
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
    'register': 'D1',
    'out_node': 'D1',
    'xnor': 'I2',
    'xor': 'I2',
    'input_formula': 'I1',
    'in_node': 'I1',
    'output': 'I1',
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
    'OR1': 'AO1'
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
    'A10':
    {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'node_name'}
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
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
            (p['node_name'] | ~p['A1'] | ~p['A2']))


def AND2_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AND2_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'AND2_X2_ZN')
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
            (p['node_name'] | ~p['A1'] | ~p['A2']))


def AND2_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AND2_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'AND2_X4_ZN')
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
            (p['node_name'] | ~p['A1'] | ~p['A2']))


def AND3_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AND3_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = ((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'AND3_X1_ZN')
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
            (p['A3'] | ~p['node_name']) &
            (p['node_name'] | ~p['A1'] | ~p['A2'] | ~p['A3']))


def AND3_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AND3_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = ((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'AND3_X2_ZN')
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
            (p['A3'] | ~p['node_name']) &
            (p['node_name'] | ~p['A1'] | ~p['A2'] | ~p['A3']))


def AND3_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AND3_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = ((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'AND3_X4_ZN')
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
            (p['A3'] | ~p['node_name']) &
            (p['node_name'] | ~p['A1'] | ~p['A2'] | ~p['A3']))


def AND4_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AND4_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'AND4_X1_ZN')
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
            (p['A3'] | ~p['node_name']) & (p['A4'] | ~p['node_name']) &
            (p['node_name'] | ~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['A4']))


def AND4_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AND4_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'AND4_X2_ZN')
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
            (p['A3'] | ~p['node_name']) & (p['A4'] | ~p['node_name']) &
            (p['node_name'] | ~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['A4']))


def AND4_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AND4_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'AND4_X4_ZN')
    return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
            (p['A3'] | ~p['node_name']) & (p['A4'] | ~p['node_name']) &
            (p['node_name'] | ~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['A4']))


def AOI21_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI21_X1_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI21_X1_ZN')
    return ((p['A'] | p['B1'] | p['node_name']) &
            (p['A'] | p['B2'] | p['node_name']) & (~p['A'] | ~p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']))


def AOI21_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI21_X2_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI21_X2_ZN')
    return ((p['A'] | p['B1'] | p['node_name']) &
            (p['A'] | p['B2'] | p['node_name']) & (~p['A'] | ~p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']))


def AOI21_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI21_X4_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI21_X4_ZN')
    return ((p['A'] | p['B1'] | p['node_name']) &
            (p['A'] | p['B2'] | p['node_name']) & (~p['A'] | ~p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']))


def AOI22_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI22_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 & A2) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI22_X1_ZN')
    return ((p['A1'] | p['B1'] | p['node_name']) &
            (p['A1'] | p['B2'] | p['node_name']) &
            (p['A2'] | p['B1'] | p['node_name']) &
            (p['A2'] | p['B2'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']))


def AOI22_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI22_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 & A2) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI22_X2_ZN')
    return ((p['A1'] | p['B1'] | p['node_name']) &
            (p['A1'] | p['B2'] | p['node_name']) &
            (p['A2'] | p['B1'] | p['node_name']) &
            (p['A2'] | p['B2'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']))


def AOI22_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI22_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 & A2) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI22_X4_ZN')
    return ((p['A1'] | p['B1'] | p['node_name']) &
            (p['A1'] | p['B2'] | p['node_name']) &
            (p['A2'] | p['B1'] | p['node_name']) &
            (p['A2'] | p['B2'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']))


def AOI211_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI211_X1_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((C1 & C2) | B) | A)
    '''
    p = validate_inputs(inputs, graph, 'AOI211_X1_ZN')
    return ((~p['A'] | ~p['node_name']) & (~p['B'] | ~p['node_name']) &
            (p['A'] | p['B'] | p['C1'] | p['node_name']) &
            (p['A'] | p['B'] | p['C2'] | p['node_name']) &
            (~p['C1'] | ~p['C2'] | ~p['node_name']))


def AOI211_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI211_X2_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((C1 & C2) | B) | A)
    '''
    p = validate_inputs(inputs, graph, 'AOI211_X2_ZN')
    return ((~p['A'] | ~p['node_name']) & (~p['B'] | ~p['node_name']) &
            (p['A'] | p['B'] | p['C1'] | p['node_name']) &
            (p['A'] | p['B'] | p['C2'] | p['node_name']) &
            (~p['C1'] | ~p['C2'] | ~p['node_name']))


def AOI211_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI211_X4_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(!(!(((C1 & C2) | B) | A)))
    '''
    p = validate_inputs(inputs, graph, 'AOI211_X4_ZN')
    return ((~p['A'] | ~p['node_name']) & (~p['B'] | ~p['node_name']) &
            (p['A'] | p['B'] | p['C1'] | p['node_name']) &
            (p['A'] | p['B'] | p['C2'] | p['node_name']) &
            (~p['C1'] | ~p['C2'] | ~p['node_name']))


def AOI221_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI221_X1_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((C1 & C2) | A) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI221_X1_ZN')
    return ((~p['A'] | ~p['node_name']) &
            (p['A'] | p['B1'] | p['C1'] | p['node_name']) &
            (p['A'] | p['B1'] | p['C2'] | p['node_name']) &
            (p['A'] | p['B2'] | p['C1'] | p['node_name']) &
            (p['A'] | p['B2'] | p['C2'] | p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']) &
            (~p['C1'] | ~p['C2'] | ~p['node_name']))


def AOI221_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI221_X2_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((C1 & C2) | A) | (B1 & B2))
    '''
    p = validate_inputs(inputs, graph, 'AOI221_X2_ZN')
    return ((~p['A'] | ~p['node_name']) &
            (p['A'] | p['B1'] | p['C1'] | p['node_name']) &
            (p['A'] | p['B1'] | p['C2'] | p['node_name']) &
            (p['A'] | p['B2'] | p['C1'] | p['node_name']) &
            (p['A'] | p['B2'] | p['C2'] | p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']) &
            (~p['C1'] | ~p['C2'] | ~p['node_name']))


def AOI221_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI221_X4_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(!(!(((C1 & C2) | A) | (B1 & B2))))
    '''
    p = validate_inputs(inputs, graph, 'AOI221_X4_ZN')
    return ((~p['A'] | ~p['node_name']) &
            (p['A'] | p['B1'] | p['C1'] | p['node_name']) &
            (p['A'] | p['B1'] | p['C2'] | p['node_name']) &
            (p['A'] | p['B2'] | p['C1'] | p['node_name']) &
            (p['A'] | p['B2'] | p['C2'] | p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']) &
            (~p['C1'] | ~p['C2'] | ~p['node_name']))


def AOI222_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI222_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 & A2) | (B1 & B2)) | (C1 & C2))
    '''
    p = validate_inputs(inputs, graph, 'AOI222_X1_ZN')
    return ((p['A1'] | p['B1'] | p['C1'] | p['node_name']) &
            (p['A1'] | p['B1'] | p['C2'] | p['node_name']) &
            (p['A1'] | p['B2'] | p['C1'] | p['node_name']) &
            (p['A1'] | p['B2'] | p['C2'] | p['node_name']) &
            (p['A2'] | p['B1'] | p['C1'] | p['node_name']) &
            (p['A2'] | p['B1'] | p['C2'] | p['node_name']) &
            (p['A2'] | p['B2'] | p['C1'] | p['node_name']) &
            (p['A2'] | p['B2'] | p['C2'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']) &
            (~p['C1'] | ~p['C2'] | ~p['node_name']))


def AOI222_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI222_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 & A2) | (B1 & B2)) | (C1 & C2))
    '''
    p = validate_inputs(inputs, graph, 'AOI222_X2_ZN')
    return ((p['A1'] | p['B1'] | p['C1'] | p['node_name']) &
            (p['A1'] | p['B1'] | p['C2'] | p['node_name']) &
            (p['A1'] | p['B2'] | p['C1'] | p['node_name']) &
            (p['A1'] | p['B2'] | p['C2'] | p['node_name']) &
            (p['A2'] | p['B1'] | p['C1'] | p['node_name']) &
            (p['A2'] | p['B1'] | p['C2'] | p['node_name']) &
            (p['A2'] | p['B2'] | p['C1'] | p['node_name']) &
            (p['A2'] | p['B2'] | p['C2'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']) &
            (~p['C1'] | ~p['C2'] | ~p['node_name']))


def AOI222_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' AOI222_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(!(!(((A1 & A2) | (B1 & B2)) | (C1 & C2))))
    '''
    p = validate_inputs(inputs, graph, 'AOI222_X4_ZN')
    return ((p['A1'] | p['B1'] | p['C1'] | p['node_name']) &
            (p['A1'] | p['B1'] | p['C2'] | p['node_name']) &
            (p['A1'] | p['B2'] | p['C1'] | p['node_name']) &
            (p['A1'] | p['B2'] | p['C2'] | p['node_name']) &
            (p['A2'] | p['B1'] | p['C1'] | p['node_name']) &
            (p['A2'] | p['B1'] | p['C2'] | p['node_name']) &
            (p['A2'] | p['B2'] | p['C1'] | p['node_name']) &
            (p['A2'] | p['B2'] | p['C2'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['node_name']) &
            (~p['B1'] | ~p['B2'] | ~p['node_name']) &
            (~p['C1'] | ~p['C2'] | ~p['node_name']))


def BUF_X1_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' BUF_X1_Z gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X1_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def BUF_X2_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' BUF_X2_Z gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X2_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def BUF_X4_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' BUF_X4_Z gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X4_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def BUF_X8_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' BUF_X8_Z gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X8_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def BUF_X16_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' BUF_X16_Z gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X16_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def BUF_X32_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' BUF_X32_Z gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'BUF_X32_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def CLKBUF_X1_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' CLKBUF_X1_Z gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'CLKBUF_X1_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def CLKBUF_X2_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' CLKBUF_X2_Z gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'CLKBUF_X2_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def CLKBUF_X3_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' CLKBUF_X3_Z gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'CLKBUF_X3_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def FA_X1_CO(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' FA_X1_CO gate.

    Args:
        inputs: { 'A', 'B', 'CL', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        CO = ((A & B) | (CI & (A | B)))
    '''
    p = validate_inputs(inputs, graph, 'FA_X1_CO')
    return ((p['A'] | p['B'] | ~p['node_name']) &
            (p['A'] | p['CL'] | ~p['node_name']) &
            (p['B'] | p['CL'] | ~p['node_name']) &
            (p['node_name'] | ~p['A'] | ~p['B']) &
            (p['node_name'] | ~p['A'] | ~p['CL']) &
            (p['node_name'] | ~p['B'] | ~p['CL']))


def FA_X1_S(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' FA_X1_S gate.

    Args:
        inputs: { 'A', 'B', 'CL', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        S = (CI ^ (A ^ B))
    '''
    p = validate_inputs(inputs, graph, 'FA_X1_S')
    return ((p['A'] | p['B'] | p['CL'] | ~p['node_name']) &
            (p['A'] | p['B'] | p['node_name'] | ~p['CL']) &
            (p['A'] | p['CL'] | p['node_name'] | ~p['B']) &
            (p['B'] | p['CL'] | p['node_name'] | ~p['A']) &
            (p['A'] | ~p['B'] | ~p['CL'] | ~p['node_name']) &
            (p['B'] | ~p['A'] | ~p['CL'] | ~p['node_name']) &
            (p['CL'] | ~p['A'] | ~p['B'] | ~p['node_name']) &
            (p['node_name'] | ~p['A'] | ~p['B'] | ~p['CL']))


def HA_X1_CO(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' HA_X1_CO gate.

    Args:
        inputs: { 'A', 'B', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        CO = (A & B)
    '''
    p = validate_inputs(inputs, graph, 'HA_X1_CO')
    return ((p['A'] | ~p['node_name']) & (p['B'] | ~p['node_name']) &
            (p['node_name'] | ~p['A'] | ~p['B']))


def HA_X1_S(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' HA_X1_S gate.

    Args:
        inputs: { 'A', 'B', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        S = (A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'HA_X1_S')
    return ((p['A'] | p['B'] | ~p['node_name']) &
            (p['A'] | p['node_name'] | ~p['B']) &
            (p['B'] | p['node_name'] | ~p['A']) &
            (~p['A'] | ~p['B'] | ~p['node_name']))


def INV_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' INV_X1_ZN gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X1_ZN')
    return ((p['A'] | p['node_name']) & (~p['A'] | ~p['node_name']))


def INV_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' INV_X2_ZN gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X2_ZN')
    return ((p['A'] | p['node_name']) & (~p['A'] | ~p['node_name']))


def INV_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' INV_X4_ZN gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X4_ZN')
    return ((p['A'] | p['node_name']) & (~p['A'] | ~p['node_name']))


def INV_X8_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' INV_X8_ZN gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X8_ZN')
    return ((p['A'] | p['node_name']) & (~p['A'] | ~p['node_name']))


def INV_X16_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' INV_X16_ZN gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X16_ZN')
    return ((p['A'] | p['node_name']) & (~p['A'] | ~p['node_name']))


def INV_X32_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' INV_X32_ZN gate.

    Args:
        inputs: { 'A', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !A
    '''
    p = validate_inputs(inputs, graph, 'INV_X32_ZN')
    return ((p['A'] | p['node_name']) & (~p['A'] | ~p['node_name']))


def MUX2_X1_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' MUX2_X1_Z gate.

    Args:
        inputs: { 'A', 'B', 'K', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = ((S & B) | (A & !S))
    '''
    p = validate_inputs(inputs, graph, 'MUX2_X1_Z')
    return ((p['A'] | p['K'] | ~p['node_name']) &
            (p['K'] | p['node_name'] | ~p['A']) &
            (p['B'] | ~p['K'] | ~p['node_name']) &
            (p['node_name'] | ~p['B'] | ~p['K']))


def MUX2_X2_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' MUX2_X2_Z gate.

    Args:
        inputs: { 'A', 'B', 'K', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = ((S & B) | (A & !S))
    '''
    p = validate_inputs(inputs, graph, 'MUX2_X2_Z')
    return ((p['A'] | p['K'] | ~p['node_name']) &
            (p['K'] | p['node_name'] | ~p['A']) &
            (p['B'] | ~p['K'] | ~p['node_name']) &
            (p['node_name'] | ~p['B'] | ~p['K']))


def NAND2_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NAND2_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'NAND2_X1_ZN')
    return ((p['A1'] | p['node_name']) & (p['A2'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['node_name']))


def NAND2_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NAND2_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'NAND2_X2_ZN')
    return ((p['A1'] | p['node_name']) & (p['A2'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['node_name']))


def NAND2_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NAND2_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A1 & A2)
    '''
    p = validate_inputs(inputs, graph, 'NAND2_X4_ZN')
    return ((p['A1'] | p['node_name']) & (p['A2'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['node_name']))


def NAND3_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NAND3_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'NAND3_X1_ZN')
    return ((p['A1'] | p['node_name']) & (p['A2'] | p['node_name']) &
            (p['A3'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['node_name']))


def NAND3_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NAND3_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'NAND3_X2_ZN')
    return ((p['A1'] | p['node_name']) & (p['A2'] | p['node_name']) &
            (p['A3'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['node_name']))


def NAND3_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NAND3_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 & A2) & A3)
    '''
    p = validate_inputs(inputs, graph, 'NAND3_X4_ZN')
    return ((p['A1'] | p['node_name']) & (p['A2'] | p['node_name']) &
            (p['A3'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['node_name']))


def NAND4_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NAND4_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'NAND4_X1_ZN')
    return ((p['A1'] | p['node_name']) & (p['A2'] | p['node_name']) &
            (p['A3'] | p['node_name']) & (p['A4'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['A4'] | ~p['node_name']))


def NAND4_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NAND4_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'NAND4_X2_ZN')
    return ((p['A1'] | p['node_name']) & (p['A2'] | p['node_name']) &
            (p['A3'] | p['node_name']) & (p['A4'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['A4'] | ~p['node_name']))


def NAND4_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NAND4_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 & A2) & A3) & A4)
    '''
    p = validate_inputs(inputs, graph, 'NAND4_X4_ZN')
    return ((p['A1'] | p['node_name']) & (p['A2'] | p['node_name']) &
            (p['A3'] | p['node_name']) & (p['A4'] | p['node_name']) &
            (~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['A4'] | ~p['node_name']))


def NOR2_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NOR2_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'NOR2_X1_ZN')
    return ((p['A1'] | p['A2'] | p['node_name']) & (~p['A1'] | ~p['node_name'])
            & (~p['A2'] | ~p['node_name']))


def NOR2_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NOR2_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'NOR2_X2_ZN')
    return ((p['A1'] | p['A2'] | p['node_name']) & (~p['A1'] | ~p['node_name'])
            & (~p['A2'] | ~p['node_name']))


def NOR2_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NOR2_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'NOR2_X4_ZN')
    return ((p['A1'] | p['A2'] | p['node_name']) & (~p['A1'] | ~p['node_name'])
            & (~p['A2'] | ~p['node_name']))


def NOR3_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NOR3_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'NOR3_X1_ZN')
    return ((~p['A1'] | ~p['node_name']) & (~p['A2'] | ~p['node_name']) &
            (~p['A3'] | ~p['node_name']) &
            (p['A1'] | p['A2'] | p['A3'] | p['node_name']))


def NOR3_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NOR3_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'NOR3_X2_ZN')
    return ((~p['A1'] | ~p['node_name']) & (~p['A2'] | ~p['node_name']) &
            (~p['A3'] | ~p['node_name']) &
            (p['A1'] | p['A2'] | p['A3'] | p['node_name']))


def NOR3_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NOR3_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'NOR3_X4_ZN')
    return ((~p['A1'] | ~p['node_name']) & (~p['A2'] | ~p['node_name']) &
            (~p['A3'] | ~p['node_name']) &
            (p['A1'] | p['A2'] | p['A3'] | p['node_name']))


def NOR4_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NOR4_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'NOR4_X1_ZN')
    return ((~p['A1'] | ~p['node_name']) & (~p['A2'] | ~p['node_name']) &
            (~p['A3'] | ~p['node_name']) & (~p['A4'] | ~p['node_name']) &
            (p['A1'] | p['A2'] | p['A3'] | p['A4'] | p['node_name']))


def NOR4_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NOR4_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'NOR4_X2_ZN')
    return ((~p['A1'] | ~p['node_name']) & (~p['A2'] | ~p['node_name']) &
            (~p['A3'] | ~p['node_name']) & (~p['A4'] | ~p['node_name']) &
            (p['A1'] | p['A2'] | p['A3'] | p['A4'] | p['node_name']))


def NOR4_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' NOR4_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'NOR4_X4_ZN')
    return ((~p['A1'] | ~p['node_name']) & (~p['A2'] | ~p['node_name']) &
            (~p['A3'] | ~p['node_name']) & (~p['A4'] | ~p['node_name']) &
            (p['A1'] | p['A2'] | p['A3'] | p['A4'] | p['node_name']))


def OAI21_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI21_X1_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI21_X1_ZN')
    return ((p['A'] | p['node_name']) & (p['B1'] | p['B2'] | p['node_name']) &
            (~p['A'] | ~p['B1'] | ~p['node_name']) &
            (~p['A'] | ~p['B2'] | ~p['node_name']))


def OAI21_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI21_X2_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI21_X2_ZN')
    return ((p['A'] | p['node_name']) & (p['B1'] | p['B2'] | p['node_name']) &
            (~p['A'] | ~p['B1'] | ~p['node_name']) &
            (~p['A'] | ~p['B2'] | ~p['node_name']))


def OAI21_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI21_X4_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI21_X4_ZN')
    return ((p['A'] | p['node_name']) & (p['B1'] | p['B2'] | p['node_name']) &
            (~p['A'] | ~p['B1'] | ~p['node_name']) &
            (~p['A'] | ~p['B2'] | ~p['node_name']))


def OAI22_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI22_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 | A2) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI22_X1_ZN')
    return ((p['A1'] | p['A2'] | p['node_name']) &
            (p['B1'] | p['B2'] | p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['node_name']))


def OAI22_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI22_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 | A2) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI22_X2_ZN')
    return ((p['A1'] | p['A2'] | p['node_name']) &
            (p['B1'] | p['B2'] | p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['node_name']))


def OAI22_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI22_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !((A1 | A2) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI22_X4_ZN')
    return ((p['A1'] | p['A2'] | p['node_name']) &
            (p['B1'] | p['B2'] | p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['node_name']))


def OAI33_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI33_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 | A2) | A3) & ((B1 | B2) | B3))
    '''
    p = validate_inputs(inputs, graph, 'OAI33_X1_ZN')
    return ((p['A1'] | p['A2'] | p['A3'] | p['node_name']) &
            (p['B1'] | p['B2'] | p['B3'] | p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['node_name']) &
            (~p['A1'] | ~p['B3'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B3'] | ~p['node_name']) &
            (~p['A3'] | ~p['B1'] | ~p['node_name']) &
            (~p['A3'] | ~p['B2'] | ~p['node_name']) &
            (~p['A3'] | ~p['B3'] | ~p['node_name']))


def OAI211_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI211_X1_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((C1 | C2) & A) & B)
    '''
    p = validate_inputs(inputs, graph, 'OAI211_X1_ZN')
    return ((p['A'] | p['node_name']) & (p['B'] | p['node_name']) &
            (p['C1'] | p['C2'] | p['node_name']) &
            (~p['A'] | ~p['B'] | ~p['C1'] | ~p['node_name']) &
            (~p['A'] | ~p['B'] | ~p['C2'] | ~p['node_name']))


def OAI211_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI211_X2_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((C1 | C2) & A) & B)
    '''
    p = validate_inputs(inputs, graph, 'OAI211_X2_ZN')
    return ((p['A'] | p['node_name']) & (p['B'] | p['node_name']) &
            (p['C1'] | p['C2'] | p['node_name']) &
            (~p['A'] | ~p['B'] | ~p['C1'] | ~p['node_name']) &
            (~p['A'] | ~p['B'] | ~p['C2'] | ~p['node_name']))


def OAI211_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI211_X4_ZN gate.

    Args:
        inputs: { 'A', 'B', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((C1 | C2) & A) & B)
    '''
    p = validate_inputs(inputs, graph, 'OAI211_X4_ZN')
    return ((p['A'] | p['node_name']) & (p['B'] | p['node_name']) &
            (p['C1'] | p['C2'] | p['node_name']) &
            (~p['A'] | ~p['B'] | ~p['C1'] | ~p['node_name']) &
            (~p['A'] | ~p['B'] | ~p['C2'] | ~p['node_name']))


def OAI221_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI221_X1_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((C1 | C2) & A) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI221_X1_ZN')
    return ((p['A'] | p['node_name']) & (p['B1'] | p['B2'] | p['node_name']) &
            (p['C1'] | p['C2'] | p['node_name']) &
            (~p['A'] | ~p['B1'] | ~p['C1'] | ~p['node_name']) &
            (~p['A'] | ~p['B1'] | ~p['C2'] | ~p['node_name']) &
            (~p['A'] | ~p['B2'] | ~p['C1'] | ~p['node_name']) &
            (~p['A'] | ~p['B2'] | ~p['C2'] | ~p['node_name']))


def OAI221_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI221_X2_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((C1 | C2) & A) & (B1 | B2))
    '''
    p = validate_inputs(inputs, graph, 'OAI221_X2_ZN')
    return ((p['A'] | p['node_name']) & (p['B1'] | p['B2'] | p['node_name']) &
            (p['C1'] | p['C2'] | p['node_name']) &
            (~p['A'] | ~p['B1'] | ~p['C1'] | ~p['node_name']) &
            (~p['A'] | ~p['B1'] | ~p['C2'] | ~p['node_name']) &
            (~p['A'] | ~p['B2'] | ~p['C1'] | ~p['node_name']) &
            (~p['A'] | ~p['B2'] | ~p['C2'] | ~p['node_name']))


def OAI221_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI221_X4_ZN gate.

    Args:
        inputs: { 'A', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(!(!(((C1 | C2) & A) & (B1 | B2))))
    '''
    p = validate_inputs(inputs, graph, 'OAI221_X4_ZN')
    return ((p['A'] | p['node_name']) & (p['B1'] | p['B2'] | p['node_name']) &
            (p['C1'] | p['C2'] | p['node_name']) &
            (~p['A'] | ~p['B1'] | ~p['C1'] | ~p['node_name']) &
            (~p['A'] | ~p['B1'] | ~p['C2'] | ~p['node_name']) &
            (~p['A'] | ~p['B2'] | ~p['C1'] | ~p['node_name']) &
            (~p['A'] | ~p['B2'] | ~p['C2'] | ~p['node_name']))


def OAI222_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI222_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 | A2) & (B1 | B2)) & (C1 | C2))
    '''
    p = validate_inputs(inputs, graph, 'OAI222_X1_ZN')
    return ((p['A1'] | p['A2'] | p['node_name']) &
            (p['B1'] | p['B2'] | p['node_name']) &
            (p['C1'] | p['C2'] | p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['C1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['C2'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['C1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['C2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['C1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['C2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['C1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['C2'] | ~p['node_name']))


def OAI222_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI222_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(((A1 | A2) & (B1 | B2)) & (C1 | C2))
    '''
    p = validate_inputs(inputs, graph, 'OAI222_X2_ZN')
    return ((p['A1'] | p['A2'] | p['node_name']) &
            (p['B1'] | p['B2'] | p['node_name']) &
            (p['C1'] | p['C2'] | p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['C1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['C2'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['C1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['C2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['C1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['C2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['C1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['C2'] | ~p['node_name']))


def OAI222_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OAI222_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(!(!(((A1 | A2) & (B1 | B2)) & (C1 | C2))))
    '''
    p = validate_inputs(inputs, graph, 'OAI222_X4_ZN')
    return ((p['A1'] | p['A2'] | p['node_name']) &
            (p['B1'] | p['B2'] | p['node_name']) &
            (p['C1'] | p['C2'] | p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['C1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B1'] | ~p['C2'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['C1'] | ~p['node_name']) &
            (~p['A1'] | ~p['B2'] | ~p['C2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['C1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B1'] | ~p['C2'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['C1'] | ~p['node_name']) &
            (~p['A2'] | ~p['B2'] | ~p['C2'] | ~p['node_name']))


def OR2_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OR2_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'OR2_X1_ZN')
    return ((p['node_name'] | ~p['A1']) & (p['node_name'] | ~p['A2']) &
            (p['A1'] | p['A2'] | ~p['node_name']))


def OR2_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OR2_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'OR2_X2_ZN')
    return ((p['node_name'] | ~p['A1']) & (p['node_name'] | ~p['A2']) &
            (p['A1'] | p['A2'] | ~p['node_name']))


def OR2_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OR2_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (A1 | A2)
    '''
    p = validate_inputs(inputs, graph, 'OR2_X4_ZN')
    return ((p['node_name'] | ~p['A1']) & (p['node_name'] | ~p['A2']) &
            (p['A1'] | p['A2'] | ~p['node_name']))


def OR3_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OR3_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = ((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'OR3_X1_ZN')
    return ((p['node_name'] | ~p['A1']) & (p['node_name'] | ~p['A2']) &
            (p['node_name'] | ~p['A3']) &
            (p['A1'] | p['A2'] | p['A3'] | ~p['node_name']))


def OR3_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OR3_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = ((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'OR3_X2_ZN')
    return ((p['node_name'] | ~p['A1']) & (p['node_name'] | ~p['A2']) &
            (p['node_name'] | ~p['A3']) &
            (p['A1'] | p['A2'] | p['A3'] | ~p['node_name']))


def OR3_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OR3_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = ((A1 | A2) | A3)
    '''
    p = validate_inputs(inputs, graph, 'OR3_X4_ZN')
    return ((p['node_name'] | ~p['A1']) & (p['node_name'] | ~p['A2']) &
            (p['node_name'] | ~p['A3']) &
            (p['A1'] | p['A2'] | p['A3'] | ~p['node_name']))


def OR4_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OR4_X1_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'OR4_X1_ZN')
    return ((p['node_name'] | ~p['A1']) & (p['node_name'] | ~p['A2']) &
            (p['node_name'] | ~p['A3']) & (p['node_name'] | ~p['A4']) &
            (p['A1'] | p['A2'] | p['A3'] | p['A4'] | ~p['node_name']))


def OR4_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OR4_X2_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'OR4_X2_ZN')
    return ((p['node_name'] | ~p['A1']) & (p['node_name'] | ~p['A2']) &
            (p['node_name'] | ~p['A3']) & (p['node_name'] | ~p['A4']) &
            (p['A1'] | p['A2'] | p['A3'] | p['A4'] | ~p['node_name']))


def OR4_X4_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' OR4_X4_ZN gate.

    Args:
        inputs: { 'A1', 'A2', 'A3', 'A4', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = (((A1 | A2) | A3) | A4)
    '''
    p = validate_inputs(inputs, graph, 'OR4_X4_ZN')
    return ((p['node_name'] | ~p['A1']) & (p['node_name'] | ~p['A2']) &
            (p['node_name'] | ~p['A3']) & (p['node_name'] | ~p['A4']) &
            (p['A1'] | p['A2'] | p['A3'] | p['A4'] | ~p['node_name']))


def TBUF_X1_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' TBUF_X1_Z gate.

    Args:
        inputs: { 'A', 'EN', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X1_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def TBUF_X2_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' TBUF_X2_Z gate.

    Args:
        inputs: { 'A', 'EN', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X2_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def TBUF_X4_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' TBUF_X4_Z gate.

    Args:
        inputs: { 'A', 'EN', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X4_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def TBUF_X8_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' TBUF_X8_Z gate.

    Args:
        inputs: { 'A', 'EN', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X8_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def TBUF_X16_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' TBUF_X16_Z gate.

    Args:
        inputs: { 'A', 'EN', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = A
    '''
    p = validate_inputs(inputs, graph, 'TBUF_X16_Z')
    return ((p['A'] | ~p['node_name']) & (p['node_name'] | ~p['A']))


def TINV_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' TINV_X1_ZN gate.

    Args:
        inputs: { 'EN', 'L', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !I
    '''
    p = validate_inputs(inputs, graph, 'TINV_X1_ZN')
    return ((p['L'] | p['node_name']) & (~p['L'] | ~p['node_name']))


def XNOR2_X1_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' XNOR2_X1_ZN gate.

    Args:
        inputs: { 'A', 'B', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'XNOR2_X1_ZN')
    return ((p['A'] | p['B'] | p['node_name']) &
            (p['A'] | ~p['B'] | ~p['node_name']) &
            (p['B'] | ~p['A'] | ~p['node_name']) &
            (p['node_name'] | ~p['A'] | ~p['B']))


def XNOR2_X2_ZN(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' XNOR2_X2_ZN gate.

    Args:
        inputs: { 'A', 'B', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        ZN = !(A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'XNOR2_X2_ZN')
    return ((p['A'] | p['B'] | p['node_name']) &
            (p['A'] | ~p['B'] | ~p['node_name']) &
            (p['B'] | ~p['A'] | ~p['node_name']) &
            (p['node_name'] | ~p['A'] | ~p['B']))


def XOR2_X1_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' XOR2_X1_Z gate.

    Args:
        inputs: { 'A', 'B', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = (A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'XOR2_X1_Z')
    return ((p['A'] | p['B'] | ~p['node_name']) &
            (p['A'] | p['node_name'] | ~p['B']) &
            (p['B'] | p['node_name'] | ~p['A']) &
            (~p['A'] | ~p['B'] | ~p['node_name']))


def XOR2_X2_Z(inputs: dict, graph: nx.DiGraph) -> Symbol:
    ''' XOR2_X2_Z gate.

    Args:
        inputs: { 'A', 'B', 'node_name' }
        graph: The networkx graph of the circuit.
    Returns:
        Z = (A ^ B)
    '''
    p = validate_inputs(inputs, graph, 'XOR2_X2_Z')
    return ((p['A'] | p['B'] | ~p['node_name']) &
            (p['A'] | p['node_name'] | ~p['B']) &
            (p['B'] | p['node_name'] | ~p['A']) &
            (~p['A'] | ~p['B'] | ~p['node_name']))


#                      OTFI SPECIFC CELLS - DO NOT EDIT                        #
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
        p = validate_inputs(inputs, graph, 'AND2')
        return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
                (p['node_name'] | ~p['A1']
                 | ~p['A2'])) & Symbol(inputs['node_name'].node + '_' +
                                       inputs['node_name'].out_pin)
    elif len(inputs) == 4:
        p = validate_inputs(inputs, graph, 'AND3')
        return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
                (p['A3'] | ~p['node_name']) &
                (p['node_name'] | ~p['A1'] | ~p['A2']
                 | ~p['A3'])) & Symbol(inputs['node_name'].node + '_' +
                                       inputs['node_name'].out_pin)
    elif len(inputs) == 5:
        p = validate_inputs(inputs, graph, 'AND4')
        return ((p['A1'] | ~p['node_name']) & (p['A2'] | ~p['node_name']) &
                (p['A3'] | ~p['node_name']) & (p['A4'] | ~p['node_name']) &
                (p['node_name'] | ~p['A1'] | ~p['A2'] | ~p['A3']
                 | ~p['A4'])) & Symbol(inputs['node_name'].node + '_' +
                                       inputs['node_name'].out_pin)
    elif len(inputs) == 6:
        p = validate_inputs(inputs, graph, 'AND5')
        return (
            (~p['A1'] | ~p['A2'] | ~p['A3'] | ~p['A4'] | ~p['A5']
             | p['node_name']) & (p['A1'] | ~p['node_name']) &
            (p['A2'] | ~p['node_name']) & (p['A3'] | ~p['node_name']) &
            (p['A4'] | ~p['node_name']) &
            (p['A5'] | ~p['node_name'])) & Symbol(inputs['node_name'].node +
                                                  '_' +
                                                  inputs['node_name'].out_pin)
    elif len(inputs) == 7:
        p = validate_inputs(inputs, graph, 'AND6')
        return (
            (~p["A1"] | ~p["A2"] | ~p["A3"] | ~p["A4"] | ~p["A5"] | ~p["A6"]
             | p["node_name"]) & (p["A1"] | ~p["node_name"]) &
            (p["A2"] | ~p["node_name"]) & (p["A3"] | ~p["node_name"]) &
            (p["A4"] | ~p["node_name"]) & (p["A5"] | ~p["node_name"]) &
            (p["A6"] | ~p["node_name"])) & Symbol(inputs['node_name'].node +
                                                  '_' +
                                                  inputs['node_name'].out_pin)
    elif len(inputs) == 8:
        p = validate_inputs(inputs, graph, 'AND7')
        return (
            (~p["A1"] | ~p["A2"] | ~p["A3"] | ~p["A4"] | ~p["A5"] | ~p["A6"]
             | ~p["A7"] | p["node_name"]) & (p["A1"] | ~p["node_name"]) &
            (p["A2"] | ~p["node_name"]) & (p["A3"] | ~p["node_name"]) &
            (p["A4"] | ~p["node_name"]) & (p["A5"] | ~p["node_name"]) &
            (p["A6"] | ~p["node_name"]) &
            (p["A7"] | ~p["node_name"])) & Symbol(inputs['node_name'].node +
                                                  '_' +
                                                  inputs['node_name'].out_pin)
    elif len(inputs) == 9:
        p = validate_inputs(inputs, graph, 'AND8')
        return (
            (~p["A1"] | ~p["A2"] | ~p["A3"] | ~p["A4"] | ~p["A5"] | ~p["A6"]
             | ~p["A7"] | ~p["A8"] | p["node_name"]) &
            (p["A1"] | ~p["node_name"]) & (p["A2"] | ~p["node_name"]) &
            (p["A3"] | ~p["node_name"]) & (p["A4"] | ~p["node_name"]) &
            (p["A5"] | ~p["node_name"]) & (p["A6"] | ~p["node_name"]) &
            (p["A7"] | ~p["node_name"]) &
            (p["A8"] | ~p["node_name"])) & Symbol(inputs['node_name'].node +
                                                  '_' +
                                                  inputs['node_name'].out_pin)
    elif len(inputs) == 10:
        p = validate_inputs(inputs, graph, 'AND9')
        return (
            (~p["A1"] | ~p["A2"] | ~p["A3"] | ~p["A4"] | ~p["A5"] | ~p["A6"]
             | ~p["A7"] | ~p["A8"] | ~p["A9"] | p["node_name"]) &
            (p["A1"] | ~p["node_name"]) & (p["A2"] | ~p["node_name"]) &
            (p["A3"] | ~p["node_name"]) & (p["A4"] | ~p["node_name"]) &
            (p["A5"] | ~p["node_name"]) & (p["A6"] | ~p["node_name"]) &
            (p["A7"] | ~p["node_name"]) & (p["A8"] | ~p["node_name"]) &
            (p["A9"] | ~p["node_name"])) & Symbol(inputs['node_name'].node +
                                                  '_' +
                                                  inputs['node_name'].out_pin)
    elif len(inputs) == 11:
        p = validate_inputs(inputs, graph, 'AND10')
        return (
            (~p["A1"] | ~p["A10"] | ~p["A2"] | ~p["A3"] | ~p["A4"] | ~p["A5"]
             | ~p["A6"] | ~p["A7"] | ~p["A8"] | ~p["A9"] | p["node_name"]) &
            (p["A1"] | ~p["node_name"]) & (p["A10"] | ~p["node_name"]) &
            (p["A2"] | ~p["node_name"]) & (p["A3"] | ~p["node_name"]) &
            (p["A4"] | ~p["node_name"]) & (p["A5"] | ~p["node_name"]) &
            (p["A6"] | ~p["node_name"]) & (p["A7"] | ~p["node_name"]) &
            (p["A8"] | ~p["node_name"]) &
            (p["A9"] | ~p["node_name"])) & Symbol(inputs['node_name'].node +
                                                  '_' +
                                                  inputs['node_name'].out_pin)
    else:
        raise Exception('Missing and gate for output logic.')


def or_output(inputs: dict, graph: nx.DiGraph) -> Symbol:
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
        return ((~p["A1"]  | p["node_name"]) & (p["A1"] | ~p["node_name"]))
    elif len(inputs) == 3:
        p = validate_inputs(inputs, graph, 'OR2')
        return ((~p["A1"] | p["node_name"]) &
                (p["A1"] | p["A2"] | ~p["node_name"]) &
                (~p["A2"] | p["node_name"]))
    elif len(inputs) == 4:
        p = validate_inputs(inputs, graph, 'OR3')
        return ((~p["A1"] | p["node_name"]) &
                (p["A1"] | p["A2"] | p["A3"] | ~p["node_name"]) &
                (~p["A2"] | p["node_name"]) & (~p["A3"] | p["node_name"]))
    elif len(inputs) == 5:
        p = validate_inputs(inputs, graph, 'OR4')
        return ((~p["A1"] | p["node_name"]) &
                (p["A1"] | p["A2"] | p["A3"] | p["A4"] | ~p["node_name"]) &
                (~p["A2"] | p["node_name"]) & (~p["A3"] | p["node_name"]) &
                (~p["A4"] | p["node_name"]))
    elif len(inputs) == 6:
        p = validate_inputs(inputs, graph, 'OR5')
        return (
            (~p["A1"] | p["node_name"]) &
            (p["A1"] | p["A2"] | p["A3"] | p["A4"] | p["A5"] | ~p["node_name"])
            & (~p["A2"] | p["node_name"]) & (~p["A3"] | p["node_name"]) &
            (~p["A4"] | p["node_name"]) & (~p["A5"] | p["node_name"]))
    elif len(inputs) == 7:
        p = validate_inputs(inputs, graph, 'OR6')
        return ((~p["A1"] | p["node_name"]) &
                (p["A1"] | p["A2"] | p["A3"] | p["A4"] | p["A5"] | p["A6"]
                 | ~p["node_name"]) & (~p["A2"] | p["node_name"]) &
                (~p["A3"] | p["node_name"]) & (~p["A4"] | p["node_name"]) &
                (~p["A5"] | p["node_name"]) & (~p["A6"] | p["node_name"]))
    elif len(inputs) == 8:
        p = validate_inputs(inputs, graph, 'OR7')
        return ((~p["A1"] | p["node_name"]) &
                (p["A1"] | p["A2"] | p["A3"] | p["A4"] | p["A5"] | p["A6"]
                 | p["A7"] | ~p["node_name"]) & (~p["A2"] | p["node_name"]) &
                (~p["A3"] | p["node_name"]) & (~p["A4"] | p["node_name"]) &
                (~p["A5"] | p["node_name"]) & (~p["A6"] | p["node_name"]) &
                (~p["A7"] | p["node_name"]))
    elif len(inputs) == 9:
        p = validate_inputs(inputs, graph, 'OR8')
        return ((~p["A1"] | p["node_name"]) &
                (p["A1"] | p["A2"] | p["A3"] | p["A4"] | p["A5"] | p["A6"]
                 | p["A7"] | p["A8"] | ~p["node_name"]) &
                (~p["A2"] | p["node_name"]) & (~p["A3"] | p["node_name"]) &
                (~p["A4"] | p["node_name"]) & (~p["A5"] | p["node_name"]) &
                (~p["A6"] | p["node_name"]) & (~p["A7"] | p["node_name"]) &
                (~p["A8"] | p["node_name"]))
    elif len(inputs) == 10:
        p = validate_inputs(inputs, graph, 'OR9')
        return ((~p["A1"] | p["node_name"]) &
                (p["A1"] | p["A2"] | p["A3"] | p["A4"] | p["A5"] | p["A6"]
                 | p["A7"] | p["A8"] | p["A9"] | ~p["node_name"]) &
                (~p["A2"] | p["node_name"]) & (~p["A3"] | p["node_name"]) &
                (~p["A4"] | p["node_name"]) & (~p["A5"] | p["node_name"]) &
                (~p["A6"] | p["node_name"]) & (~p["A7"] | p["node_name"]) &
                (~p["A8"] | p["node_name"]) & (~p["A9"] | p["node_name"]))
    elif len(inputs) == 11:
        p = validate_inputs(inputs, graph, 'OR10')
        return ((~p["A1"] | p["node_name"]) &
                (p["A1"] | p["A2"] | p["A3"] | p["A4"] | p["A5"] | p["A6"]
                 | p["A7"] | p["A8"] | p["A9"] | p["A10"] | ~p["node_name"]) &
                (~p["A2"] | p["node_name"]) & (~p["A3"] | p["node_name"]) &
                (~p["A4"] | p["node_name"]) & (~p["A5"] | p["node_name"]) &
                (~p["A6"] | p["node_name"]) & (~p["A7"] | p["node_name"]) &
                (~p["A8"] | p["node_name"]) & (~p["A9"] | p["node_name"]) &
                (~p["A10"] | p["node_name"]))
    else:
        raise Exception('Missing or gate for output logic.')


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
    'in_node_Q': in_node_Q,
    'in_node_QN': in_node_QN,
    'out_node_Q': out_node,
    'out_node_QN': out_node,
    'output_O': output
}
