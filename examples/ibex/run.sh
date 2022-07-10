#!/bin/bash

# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

# OpenTitan repository: 097521294cd43a3e059bed8c0cd2a710b4f7f73e
# Design flow: Yosys with Nangate45 cell lib
# Module: ibex_if_stage.sv
# Experiment: glitch the PC in the ibex_if_stage module


export N_CPUS=16
export REPO_TOP=../../

export PARSER=$REPO_TOP/parse.py
export FI_INJECTOR=$REPO_TOP/fi_injector.py
export CELL_LIB=$REPO_TOP/cell_lib_nangate45_autogen.py

mkdir -p output

$PARSER -j netlist_ibex_if_stage.json \
        -m ibex_if_stage \
        -o output/netlist_ibex_if_stage.pickle

$FI_INJECTOR    -p output/netlist_ibex_if_stage.pickle \
                -f fault_model_ibex_if_stage_pc.json -n $N_CPUS \
                -c $CELL_LIB --auto_fl \
                -s 1 2>&1 | tee -a output/fault_model_ibex_if_stage_pc.log

$FI_INJECTOR    -p output/netlist_ibex_if_stage.pickle \
                -f fault_model_ibex_if_stage_pc_target.json -n $N_CPUS \
                -c $CELL_LIB --auto_fl \
                -s 1 2>&1 | tee -a output/fault_model_ibex_if_stage_pc_target.log

$FI_INJECTOR    -p output/netlist_ibex_if_stage.pickle \
                -f fault_model_ibex_if_stage_pc_target.json -n $N_CPUS \
                -c $CELL_LIB --auto_fl \
                -s 2 -l 10000 2>&1 | tee -a output/fault_model_ibex_if_stage_pc_target.log
