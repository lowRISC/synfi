# AES Round Counter

The AES cipher control [module](https://github.com/lowRISC/opentitan/blob/master/hw/ip/aes/rtl/aes_cipher_control.sv)
is responsible for creating the AES round counter value. As a fault on this
counter value could enable an adversary to conduct round-reduced attacks on the
AES, the generation of the round counter value is protected by dedicated fault
countermeasures.
```verilog
module aes_cipher_control (
  ...
  output logic                    alert_o,
  output logic [3:0]              key_expand_round_o,
  ...
);
  ...
  assign key_expand_round_o = rnd_ctr_q;
  ...
  // Generate parity bits and sum.
  assign rnd_ctr_parity_d = ^rnd_ctr_d;
  assign rnd_ctr_parity   = ^rnd_ctr_q;
  assign rnd_ctr_sum      = rnd_ctr_q + rnd_ctr_rem_q;

  // Detect faults.
  assign rnd_ctr_err_sum    = (rnd_ctr_sum != num_rounds_q)        ? 1'b1 : 1'b0;
  assign rnd_ctr_err_parity = (rnd_ctr_parity != rnd_ctr_parity_q) ? 1'b1 : 1'b0;

  assign rnd_ctr_err = rnd_ctr_err_sum | rnd_ctr_err_parity;
  ...
```
The `rnd_ctr` variable, which is forwarded to the output port, is the up counter
incrementing the value from 0 to `num_rounds` (e.g., 12 for AES192) and the
`rnd_rem` variable counts from `num_rounds` to 0. To detect a fault manipulating
the round counter, `rnd_ctr` and `rnd_rem` are added and compared to
`num_rounds`. On a mismatch, the `rnd_ctr_err_sum` flag is raised. In addition
to this comparison, a parity bit is computed and compared. If either the parity
comparison or the sum comparison fails, the `rnd_ctr_err` flag is raised and the
FSM of the module enters the error state. In this error state, the error flag
is forwarded to the output with the `alert_o` signal.

## Verification
The goal of a fault attacker targeting the round counter is to manipulate the
round counter (i.e., `key_expand_round_o != expected_value`) but to not trigger
the error logic (i.e., `rnd_ctr_err = 0`). To show the effectiveness of the
FI countermeasure and find potential weaknesses, the OTFI framework can be used.

<img src="./images/aes_rnd_cntr.png" width="66%">

The first step when using the OTFI framework is to identify the circuit involved
in the computation of the security critical variables. The counter values
`rnd_ctr` and `rnd_ctr_rem` are computed in the combinational circuit between
the `u_rnd_ctr_regs` and `u_rnd_ctr_rem_regs` registers (stage 1). The value of
the `rnd_ctr` variable then is directly forwarded to the `key_expand_round_o` 
output port (stage 2). In stage 3, the `rnd_ctr` and `rnd_ctr_rem` values are
used to compute the `rnd_ctr_err_sum` and `rnd_ctr_err_parity` signals, which
are then used to generate the `rnd_ctr_err` flag.

Then, the next step is to define the input and expected values:

| Name               | Type                  | Input Value | Expected Value |
|--------------------|-----------------------|-------------|----------------|
| rnd_ctr            | 4-bit internal signal | 4'b0000     | -              |
| rnd_ctr_rem        | 4-bit internal signal | 4'b1100     | -              |
| key_expand_round_o | 4-bit output signal   | -           | 4'b0001        |
| rnd_ctr_err        | 1-bit error signal    | -           | 1'b0           |

For the AES192, the input value for the round counter is set to 0 and for the
down counting counter to 12. The expected value for the output counter value is
1 and the error flag should be 0.

## Verification Flow
### 0. Preparation
By default, the OTFI framework uses the
[Nangate45](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/tree/master/flow/platforms/nangate45/lib)
cell library. When switching to a different (e.g., proprietary) library, the
following adaptions are required:
- `examples/config.json`: Define the names of common signals (e.g., the clock).
- `examples/fault_mapping_cfg.json`: The fault mapping specifies to which gate a
    target gate is replaced during the FI process.

Then, convert the used cell library using the cell library generator script:
```console
$ ./cell_lib_generator.py -l NangateOpenCellLibrary_typical.lib \
                          -c examples/config.json \
                          -o cell_lib_nangate45_autogen.py
```
The resulting `cell_lib_nangate45_autogen.py` cell library is laster used by the
FI injector in step 3.

### 1. Annotation and Synthesis

To start the verification for the circuit shown in the Figure above, the
SystemVerilog code needs to be annotated:
```verilog
module aes_cipher_control (
  ...
  (* otfi_type = "output_port", otfi_expected = 1 *) output logic [3:0] key_expand_round_o,
  ...
);
  ...
  // Signals
  (* keep, otfi_type = "register_d", otfi_input = 0, otfi_stage = "2" *)     logic [3:0] rnd_ctr_d;
  (* keep, otfi_type = "register_q", otfi_input = 0, otfi_stage = "1"  *)    logic [3:0] rnd_ctr_q;
  (* keep, otfi_type = "register_d", otfi_input = 12, otfi_stage = "1"  *)   logic [3:0] rnd_ctr_rem_d;
  (* keep, otfi_type = "register_q", otfi_input = 12, otfi_stage = "1"  *)   logic [3:0] rnd_ctr_rem_q;
  (* keep, otfi_type = "alert_port", otfi_expected, otfi_stage = "3"  = 0 *) logic rnd_ctr_err;
  ...
```
To synthesize the annotated AES cipher control module, use the 
[pre_syn](https://github.com/lowRISC/opentitan/tree/master/hw/ip/aes/pre_syn)
Yosys synthesis flow. Modify the following parameters in the `syn_setup.sh`
script to only synthesize the cipher control module:
```sh
export LR_SYNTH_TOP_MODULE=aes_cipher_control

export LR_SYNTH_MASKING=0
export LR_SYNTH_S_BOX_IMPL=1
```
Finally, convert the Verilog netlist to JSON with:
```console
$ yosys "write_json circuit_rnd_cntr.json"
```
Note that this JSON file and all other files described in this example can be
found in the `$REPO_TOP/examples` directory.
### 2. Fault Model Generation
The fault model is used by the OTFI framework to identify the security sensitive
circuit and to perform the fault analysis. To automatically generate the fault
model, run the fault model generator with the following parameters:
```console
$ ./fi_model_generator.py -j examples/circuit_rnd_cntr.json \
                          -m aes_cipher_control -s 2 -n rnd_ctr \
                          -c examples/fault_mapping_cfg.json \
                          -o fault_model_rnd_cntr.json
```
The resulting fault model file contains the stages depicted in the circuit above
and sets the input and expected values according to the annotated SystemVerilog
code.
### 3. Fault Evaluation
To start the fault evaluation of the circuit, first convert the JSON netlist
into a directed graph using the parser script:
```console
$ ./parse.py -j examples/circuit_rnd_cntr.json  -m aes_cipher_control \
             -o output/circuit_rnd_cntr.pickle
```
The fault injector extracts the target circuit according to the fault model and
injects faults into the gates of the circuit. The attacked gates are either
manually specified by the user or automatically determined by the framework. To
start the automatic approach, use the `--auto_fl` command line argument:
```console
$ ./fi_injector.py -p output/circuit_rnd_cntr.pickle \
                   -f examples/fault_model_rnd_cntr.json \
                   -n 4 -c cell_lib_nangate45_autogen.py --auto_fl
```
As the automatic approach exhaustively induces faults into all gates in the
target circuit, this step could take some time. Make sure to adapt the number of
cores with the `-n` argument to your machine. 

To analyze the effects of faults on specific gates, remove the `--auto_fl`
argument and add the following fault location entry to the fault model:
```json
"fault_locations": {
  "$abc$16618$auto$blifparse.cc:381:parse_blif$16802": "stage_1_1",
  "$abc$16618$auto$blifparse.cc:381:parse_blif$16815": "stage_1_1",
  "$abc$16618$auto$blifparse.cc:381:parse_blif$16775": "stage_1_3"
}
```
The first entry (`$16802`) is the OAI21 gate directly at the register for the
`rnd_ctr[0]` value and the second entry (`$16815`) is the AOI21 gate directly at
the register for the `rnd_ctr[2]` value. The last entry (`$16775`) is the OR3
gate responsible for setting the `rnd_ctr_err` flag. When starting the fault
injector without the `--auto_fl` option, these manually specified gates are
targeted:
```console
$ ./fi_injector.py -p output/circuit_rnd_cntr.pickle \
                   -f examples/fault_model_rnd_cntr.json \
                   -n 4 -c cell_lib_nangate45_autogen.py
```
As the number of simultaneous faults is set to 2, 3*2 faults are induced into
the circuit. Although faults into `$16802` and `$16815` change the round
counter values (`rnd_ctr[0]` and `rnd_ctr[1]`), the faults are also detected by
the fault countermeasure (`rnd_ctr_err=1`). Hence, an ineffective fault is
reported. However, when injecting faults into `$16802` and `$16775` or `$16815`
and `$16775`, the round counter value is changed and the error flag is disarmed.
Now, two effective faults are reported by the OTFI framework.