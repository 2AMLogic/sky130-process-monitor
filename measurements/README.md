# measurements

Append-only simulation records (JSON Lines). Everything here is **SIMULATED** and names its corner,
testbench, PDK revision and ngspice version; nothing is measured until silicon exists.

- `inv_smoke_records.jsonl` — toolchain smoke (`sim/smoke/run.sh`); no design claim.
- `osc_bank_records.jsonl` — one tt / 1.8 V / 27 °C record per bank oscillator (`sim/osc_bank/run.sh`):
  `f_osc_hz`, `i_avg_ua`. Single corner only: no PVT or accuracy claim.
- `subthreshold_records.jsonl` — spec Q2 evidence (`sim/subthreshold/`): oscillator 45-cell grid, device probe, `mc_mm_switch` Monte Carlo; `record` names the kind, `tran_step_window` the transient step/window. Appended by `sim/subthreshold/analyze.py --append`.
