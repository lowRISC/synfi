# Faulting the AES Round Counter

In this FI experiment, faults are induced into the [aes_cipher_control_fsm](https://github.com/lowRISC/opentitan/blob/097521294cd43a3e059bed8c0cd2a710b4f7f73e/hw/ip/aes/rtl/aes_cipher_control_fsm.sv "aes_cipher_control_fsm.sv") module of the AES core.
By using the ``fault_model_aes_cipher_control_fsm_rnd_cntr.json`` fault description file, SYNFI shows whether it is possible to induce faults into the netlist which arbitrarily change the round counter value generated in the FSM.
In the ``fault_model_aes_cipher_control_fsm_rnd_cntr_target_value.json`` fault description file, SYNFI is used to show if it is possible to manipulate the counter value to 4.
