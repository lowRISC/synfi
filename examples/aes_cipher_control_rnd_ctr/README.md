# Faulting the AES Round Counter

In this FI experiment, faults are induced into the [aes_cipher_control](https://github.com/lowRISC/opentitan/blob/097521294cd43a3e059bed8c0cd2a710b4f7f73e/hw/ip/aes/rtl/aes_cipher_control.sv "aes_cipher_control.sv") module of the AES core.
This module instantiates the [aes_cipher_control_fsm](https://github.com/lowRISC/opentitan/blob/097521294cd43a3e059bed8c0cd2a710b4f7f73e/hw/ip/aes/rtl/aes_cipher_control_fsm.sv "aes_cipher_control_fsm.sv") module redundantly to protect the module against faults.

The target circuit, which is described in the ``fault_model_aes_cipher_control_rnd_cntr.json`` fault specification file, comprises the logic in between the registers storing the up and down counting counter value (c.f., ``stage_1``).
Moreover, the target circuit consists of the logic between these registers and the ``key_expand_round_o`` port (c.f., ``stage_2``) and the register storing the error signal (c.f., ``stage_3``).
The error signal is triggered, when a fault is detected.

The ``run.sh`` script injects faults into the netlist in three different configurations:
- 1 simultaneous faults: no effective fault
- 2 simultaneous faults into the ``fault_locations`` specified in the fault specification file: effective faults found
- 2 simultaneous faults exhaustively into all available gates: effective faults found
