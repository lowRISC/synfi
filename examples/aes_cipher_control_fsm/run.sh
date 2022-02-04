#!/bin/bash

# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

# OpenTitan repository: 097521294cd43a3e059bed8c0cd2a710b4f7f73e
# Design flow: Yosys with Nangate45 cell lib
# Module: aes_cipher_control_fsm.sv
# Experiment: fault the rnd_ctr generated in this FSM

export N_CPUS=16
export REPO_TOP=../../

export PARSER=$REPO_TOP/parse.py
export FI_INJECTOR=$REPO_TOP/fi_injector.py
export CELL_LIB=$REPO_TOP/cell_lib_nangate45_autogen.py

mkdir -p output

$PARSER -j netlist_aes_cipher_control_fsm.json \
        -m aes_cipher_control_fsm \
        -o output/netlist_aes_cipher_control_fsm.pickle


$FI_INJECTOR    -p output/netlist_aes_cipher_control_fsm.pickle \
                -f fault_model_aes_cipher_control_fsm_rnd_cntr.json -n $N_CPUS \
                -c $CELL_LIB --auto_fl \
                -s 1 2>&1 | tee -a output/aes_cipher_control_fsm.log

$FI_INJECTOR    -p output/netlist_aes_cipher_control_fsm.pickle \
                -f fault_model_aes_cipher_control_fsm_rnd_cntr_target_value.json \
                -n $N_CPUS -c $CELL_LIB --auto_fl \
                -s 1 2>&1 | tee -a output/aes_cipher_control_fsm.log

$FI_INJECTOR    -p output/netlist_aes_cipher_control_fsm.pickle \
                -f fault_model_aes_cipher_control_fsm_rnd_cntr_target_value.json \
                -n $N_CPUS -c $CELL_LIB --auto_fl \
                -s 2 2>&1 | tee -a output/aes_cipher_control_fsm.log