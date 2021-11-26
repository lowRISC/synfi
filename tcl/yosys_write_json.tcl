# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

source ../tcl/flow_utils.tcl
source ../tcl/lr_convert_flow_var.tcl

yosys "read_verilog $lr_convert_netlist"
yosys "read_liberty -lib $lr_convert_cell_library_path"
yosys "write_json $lr_convert_netlist_json_out"