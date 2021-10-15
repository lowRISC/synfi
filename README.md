# OpenTitan FI Formal Verification Framework
Note: This tool is currently a work-in-progress.
## Introduction
This framework formally verifies the functionality of the fault countermeasure
building blocks of the OpenTitan. By annotating the SystemVerilog code, the tool
is capable of extracting sensitive parts of the circuit and to inject multiple 
faults into these parts. The effectiveness of the injected faults are
evaluated and the tool verifies that the installed fault countermeasures detect 
the faults.

## Usage
The framework consists of a preprocessing phase and a fault injection and 
evaluation phase. 

The `examples` directory contains the netlist for the 
[aes_cipher_control](https://github.com/lowRISC/opentitan/blob/master/hw/ip/aes/rtl/aes_cipher_control.sv) 
module synthesized with the 
[provided](https://github.com/lowRISC/opentitan/tree/master/hw/ip/aes/pre_syn) 
Yosys flow. To start the preprocessing phase for this  example netlist, create 
the `output` directory and invoke the parser:
```console
$ ./parse.py -j examples/circuit.json -m aes_cipher_control -o output
```
The parser preprocesses the provided netlist and creates a directed graph, which
is then used by the fault injector to evaluate the effects of the induced 
faults.