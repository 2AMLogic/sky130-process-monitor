# Readout static timing (T1 item 5, digital)

SIMULATED / static timing only; nothing here is measured silicon.

- `readout.sta.json`: the `klt sta` request. Geometry: `layout/readout/out/readout.def`
  (routed, #24), no SPEF. Constraint: `clk_ref` at 100 ns (10 MHz, spec section 5), ideal clock.
  Corners: `ss_100C_1v60`, `tt_025C_1v80`, `ff_n40C_1v95`.
- `readout.sta.report.json`: its envelope (`klayout-tools==0.9.1`). Every corner is `constrained`;
  setup slack 95.39 / 97.89 / 98.71 ns, hold slack 0.678 / 0.331 / 0.204 ns (ss / tt / ff).
- `readout.sdc`: reference copy of the constraint; klt sta does not read it (see file header).
- `../verification/readout/functional-verification.json` + `.report.json`: 9/9 cocotb tests pass
  (Icarus 13.0, cocotb 2.1.0).

## What this does NOT cover (disclosed, not relaxed)

1. **Corner box.** The pinned hd liberty set has no 125 C file and no 1.62/1.98 V point. The three
   corners above are the nearest installed files; the spec box extremes (125 C, 1.62 V, 1.98 V)
   are not timed. Box coverage is not claimed.
2. **The oscillator-clocked counter is not timed in `readout.sta.json`.** Following the issue
   (SDC defines only the reference clock), the 29 `u_cnt` registers clocked by `osc[4:0]` are
   reported unclocked, and 57 endpoints (outputs, no I/O delays) unconstrained:
   `constraint_completeness.status` is `incomplete` in every corner. The `constrained` verdict
   applies to the reference-clock domain only.
3. **Exploratory result, not cited for 5.digital:** `readout.osc-probe.sta.json` declares `osc[0..4]`
   at 1.0 ns, asynchronous to `clk_ref`. The 1.0 ns figure is an assumption bounded by one local
   SIMULATED ngspice probe (`bench_osc_hd.spice`, ff model, 1.98 V, -40 C: 1.036 GHz, outside the
   liberty set; not appended to `measurements/`). Result: setup slack -4.85 / -1.79 / -0.70 ns
   (ss / tt / ff), hold >= 0.20 ns. The counter does not close at 1 GHz; the real per-corner
   oscillator frequencies (#29) decide whether that is a defect. Slack is bounding, not
   corner-matched (fastest cell frequency applied to every corner). Follow-up filed separately.
