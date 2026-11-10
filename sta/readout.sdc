# Readout reference-clock constraint (spec/target-spec.md section 5: 10 MHz target).
# REFERENCE COPY: klt sta 0.9.1 has no read_sdc passthrough; it builds the equivalent
# create_clock from constraints.clock_port/clock_period_ns in sta/readout.sta.json.
# If you change the period here, change it there and re-run.
create_clock -name clk_ref -period 100.0 [get_ports clk_ref]
