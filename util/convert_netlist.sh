#!/bin/bash

# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

# This script converts a verilog netlist to JSON using yosys.

set -e
set -o pipefail

error () {
    echo >&2 "$@"
    exit 1
}

if [ ! -f convert_setup.sh ]; then
    error "No convert_setup.sh file: see README.md for instructions"
fi

source convert_setup.sh

if [ -z "$LR_CONVERT_NETLIST" ]; then
    echo >&2 "You forgot to set LR_CONVERT_NETLIST!";
    exit 1;
fi
if [ -z "$LR_CONVERT_NETLIST_JSON_OUT" ]; then
    echo >&2 "You forgot to set LR_CONVERT_NETLIST_JSON_OUT!";
    exit 1;
fi
if [ -z "$LR_CONVERT_CELL_LIBRARY_PATH" ]; then
    echo >&2 "You forgot to set LR_CONVERT_CELL_LIBRARY_PATH!";
    exit 1;
fi

teelog () {
    tee "$1.log"
}

echo "run yosys to convert netlist"
#-------------------------------------------------------------------------
# run Yosys netlist convertion.
#-------------------------------------------------------------------------
yosys -c ../tcl/yosys_write_json.tcl |& teelog convert_netlist || {
    error "Failed to convert the netlist to JSON with Yosys"
}
echo "end yosys"