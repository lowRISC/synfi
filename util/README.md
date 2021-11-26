# OpenTitan FI Utils
## Convert Netlist to JSON
To convert a verilog netlist synthesized with any synthesis tool of choice to a
JSON netlist, the `convert_netlist.sh` can be used. Copy and adapt the setup
file and invoke the netlist converter:
```console
$ cp convert_setup_example.sh convert_setup.sh # Adapt this file.
$ ./convert_netlist.sh
```