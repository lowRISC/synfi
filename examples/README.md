# Examples
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
```sh
$ yosys "write_json circuit.json"
```

## Example Fault Models
To perform the fault experiments with the provided fault models in the
`examples` folder, first run the parser:
```sh
$ cd $REPO_TOP && mkdir output
$ ./parse.py -j examples/circuit.json -m aes_cipher_control -o output/circuit.pickle
```
Then, execute the FI injector for each fault model.
### fault_model_mubi_fl
In this fault model example, the following bits are set and the involved circuit
is analyzed by the framework:
| Name               | Type                  | Input Value | Expected Value |
|--------------------|-----------------------|-------------|----------------|
| rnd_ctr_d/q        | 4-bit internal signal | 4'b0000     | -              |
| rnd_ctr_rem_d/q    | 4-bit internal signal | 4'b1100     | -              |
| key_expand_round_o | 4-bit output signal   | -           | 4'b0001        |
| rnd_ctr_err_sum    | 1-bit error signal    | -           | 1'b0           |

To manually analyze the effect of a fault on the gates specified in the fault
model `fault_locations` field, execute the fault injector with these parameters:
```sh
$ ./fi_injector.py -p output/circuit.pickle -f examples/fault_model_mubi.json \
  -n 1 -c cell_lib_nangate45_autogen.py
```
Two simultaneous faults (`{$16836,$16821}` or `{$16852,$16821}`) into the round
counter and the error logic produces an effective fault (i.e., the round counter
value does not match the expected `4'b0001` value and the `rnd_ctr_err_sum` flag
is not set). As two simultaneous faults (`{$16836,$16852}`) into the round
counter triggers are detected by the error logic, this fault is ineffective.
Hence, the result are four effective and two ineffective faults.

To exhaustively analyze the effects of a fault, the `--auto_fl` command line
argument injects faults into all gates:
```sh
$ ./fi_injector.py -p output/circuit.pickle -f examples/fault_model_mubi.json \
  -n 1 -c cell_lib_nangate45_autogen.py --auto_fl
```
To speed up the analysis process, adapt the number of CPU cores with the `-n`
argument.