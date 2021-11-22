# AES Control FSM
The AES control FSM in the control
[module](https://github.com/lowRISC/opentitan/blob/master/hw/ip/aes/rtl/aes_control.sv)
is responsible for setting control signals for the AES. To protect the state
value from fault-induced hijacks, the state signals are sparsely encoded:
```verilog
  // Hamming distance histogram:
  //
  //  0: --
  //  1: --
  //  2: --
  //  3: |||||||||||||||||||| (57.14%)
  //  4: ||||||||||||||| (42.86%)
  //  5: --
  //  6: --
  //
  // Minimum Hamming distance: 3
  // Maximum Hamming distance: 4
  // Minimum Hamming weight: 1
  // Maximum Hamming weight: 5
  //
  localparam int StateWidth = 6;
  typedef enum logic [StateWidth-1:0] {
    IDLE        = 6'b111100, // 0010001
    LOAD        = 6'b101001, // 0000000
    PRNG_UPDATE = 6'b010000, // 1100010
    PRNG_RESEED = 6'b100010,
    FINISH      = 6'b011011,
    CLEAR       = 6'b110111,
    ERROR       = 6'b001110
  } aes_ctrl_e;
```
## Verification
