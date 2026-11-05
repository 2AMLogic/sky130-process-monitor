# measurements

Append-only simulation records (JSON Lines). Everything here is **SIMULATED** and names its corner,
testbench, PDK revision and ngspice version; nothing is measured until silicon exists.

- `inv_smoke_records.jsonl` — toolchain smoke (`sim/smoke/run.sh`); no design claim.
- `osc_bank_records.jsonl` — one tt / 1.8 V / 27 °C record per bank oscillator (`sim/osc_bank/run.sh`):
  `f_osc_hz`, `i_avg_ua`. Single corner only: no PVT or accuracy claim.
