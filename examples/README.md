# Example
The JSON netlist provided in this directory was created with the 
[pre_syn](https://github.com/lowRISC/opentitan/tree/master/hw/ip/aes/pre_syn)
Yosys flow using the Nangate45 library.
To reproduce the netlist, change the `LR_SYNTH_TOP_MODULE` variable in the
`syn_setup.sh` script:
```sh
export LR_SYNTH_TOP_MODULE=aes_cipher_control
```
To convert the Verilog netlist to the JSON format, use the Yosys command:
```console
yosys "write_json circuit.json"
```