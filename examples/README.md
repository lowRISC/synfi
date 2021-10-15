# Example
The JSON netlist provided in this directory was created with the 
[pre_syn](https://github.com/lowRISC/opentitan/tree/master/hw/ip/aes/pre_syn)
Yosys flow using the Nangate45 library.
To reproduce the netlist, change the following variables in the
`syn_setup.sh` script:
```sh
export LR_SYNTH_TOP_MODULE=aes_cipher_control

# Setup module parameters.
#export LR_SYNTH_AES_192_ENABLE=0
export LR_SYNTH_MASKING=0
export LR_SYNTH_S_BOX_IMPL=1
```
To convert the Verilog netlist to the JSON format, use the Yosys command:
```console
yosys "write_json circuit.json"
```