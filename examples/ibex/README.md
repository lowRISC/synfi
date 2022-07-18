# System Requirements
The tool was tested on Ubuntu 20.04 and requires Python3 and pip3.
# Setup
Clone the repository, switch to the directory, and install the dependencies:
```
git clone https://github.com/lowRISC/synfi.git
cd synfi
pip3 install -r requirements.txt
```
# Usage
Switch to ```examples/ibex``` and adapt the ```N_CPUS``` parameter in ```run.sh``` according to the number of CPU cores you want to utilize.
Then, execute the ```./run.sh``` script to start the fault injection experiment. Depending on the used execution environment, the entire process takes between 5-30min.
# Results
The script instruments SYNFI to inject faults into the netlist (```netlist_ibex_if_stage.json```) of the Ibex instruction fetch module. On this netlist, three different fault injection experiments are performed:
- 1 simultaneous fault into the Ibex instruction fetch module. Effective fault: arbitrarily change the program counter (PC).
  - Result: 78.1% (55.3+22.8) effective faults, as shown in row (1) of Table 7 in the paper.
- 1 simultaneous fault into the Ibex instruction fetch module. Effective fault: change the PC to a specific value.
  - Result: 0% effective faults.
- 2 simultaneous faults into the Ibex instruction fetch module. Effective fault: change the PC to a specific value.
  - Result: Here, we limit the number of injected faults to 10000 avoiding long execution times. As SYNFI randomly injects 10000 faults, the output changes after each execution.