# OpenTitan FI Formal Verification Framework
Note: This tool is currently a work-in-progress.
## Introduction
This framework formally verifies the functionality of the fault countermeasure
building blocks of the OpenTitan SoC. By annotating the SystemVerilog code, the 
tool can extract sensitive parts of the circuit, and inject multiple faults into 
these parts. The effectiveness of the injected faults are
evaluated and the tool verifies that the installed fault countermeasures detect 
the faults.

The framework is broken into three phases:

1. a preprocessing phase,
2. a fault injection phase, and
3. an evaluation phase.

## Usage
Install python3 and the corresponding packages:
```console
$ pip3 install -r requirements.txt
```

The `examples/circuit.json` file contains the netlist for the 
[aes_cipher_control](https://github.com/lowRISC/opentitan/blob/master/hw/ip/aes/rtl/aes_cipher_control.sv) 
module synthesized with the 
[provided](https://github.com/lowRISC/opentitan/tree/master/hw/ip/aes/pre_syn) 
Yosys flow.

The convert a cell library (e.g., the 
[NANGATE45](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/tree/master/flow/platforms/nangate45/lib) library), 
adapt the `examples/config.json` file and start the cell library generator:
```console
$ ./cell_lib_generator.py -l NangateOpenCellLibrary_typical.lib -n 16 \
    -c examples/config.json -o cell_lib_nangate45_autogen.py
```
To start the preprocessing phase for this  example netlist, create 
the `output` directory and invoke the parser:
```console
$ ./parse.py -j examples/circuit.json -m aes_cipher_control \
    -o output/circuit.pickle
```
The parser preprocesses the provided netlist and creates a directed graph, which
is then used by the fault injector to evaluate the effects of the induced 
faults. To run the fault injector with the example netlist and the example fault
model, execute the fi_injector tool:
```console
$ ./fi_injector.py -p output/circuit.pickle -f examples/fault_model.json -n 16 \
    -c cell_lib_nangate45_autogen.py
```

## Licensing

Unless otherwise noted, everything in this repository is covered by the Apache
License, Version 2.0 (see [LICENSE](./LICENSE) for full text).