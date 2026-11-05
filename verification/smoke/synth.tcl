# Yosys smoke synthesis to sky130_fd_sc_hd, typical Liberty corner.
# Inputs via environment: LIBERTY (tt .lib), RTL (verilog), OUT (netlist).
# A missing Liberty file makes the read fail, and so the run.
set lib $::env(LIBERTY)
yosys read_verilog -sv $::env(RTL)
yosys synth -top smoke -flatten
yosys dfflibmap -liberty $lib
yosys abc -liberty $lib
yosys opt_clean
yosys stat -liberty $lib
yosys write_verilog -noattr $::env(OUT)
