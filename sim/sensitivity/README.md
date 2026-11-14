# sim/sensitivity

Sensitivity matrix, conditioning and discrimination margin for the five-oscillator bank
(spec §2, decision 0001 Q1). **Everything here is SIMULATED**: schematic-level netlists
(`design/osc_bank/`), no layout, no parasitics, ngspice on the sky130A models. Each recorded figure names
its corner, testbench, PDK pin and ngspice version. Nothing is measured, and **no estimate accuracy is
quoted**: the margin below is a discrimination statistic, not an accuracy.

## Files

| Path | What |
|---|---|
| `osc/tb_<osc>.spice` | testbench body per oscillator (circuit body only; `klt sim` owns `.control`/`.end`). The oscillators are the committed `design/osc_bank/` netlists, reused, not copied. The enable is a behavioural source following `v(vdd)`, so it swings rail to rail at every supply |
| `gen_requests.py` | writes `requests/*.json` deterministically |
| `requests/grid_<osc>.json` | 5 corners × 3 V × 3 T = the 45-cell box, one request per oscillator (225 units) |
| `requests/mc_<osc>.json` | mismatch Monte Carlo at the nominal cell only: 5 corners × 1.80 V/27 °C × 50 samples (osc_subth: 20), `mc_mm_switch=1` via `monte_carlo.mismatch_scale` |
| `requests/mc_offnom_*.json` | mismatch Monte Carlo at the off-nominal cells: 5 corners × {1.62 V/125 °C, 1.98 V/−40 °C}, per-oscillator N from `OFFNOM_N` in `gen_requests.py` (osc_subth: one request per cell). Coverage status is recorded in `records/2026-11-05-mc-offnom-partial.md` and the later `records/2026-11-06-mc-offnominal-*.md`; this table makes no completeness claim |
| `requests/*_osc_hd_5p.json` | osc_hd re-run with a 5 ps max step (grid, nominal MC, off-nominal MC); results in `records/2026-11-05-osc-hd-step-refined.md` |
| `analyze.py` | frequency extraction, sensitivity matrix, SVD / κ / rank, margin, counter-gate sweep (stdlib only) |
| `test_analyze.py` | unit tests on synthetic data: `python3 -I sim/sensitivity/test_analyze.py` |
| `records/` | dated, append-only result records (never edited; a re-run is a new dated file). `2026-11-14-osc-subth-gate-sizing.md` sizes the `osc_subth` counter gate: counts and cold-cell (1.98 V / −40 °C) margin versus gate exponent `k`, and the result against spec §6 conversion time |

## Running

Multi-unit runs go to the batch fleet through `klt sim` (never hand-launched ngspice):

    klt sim --batch-set sim/sensitivity/requests/grid_*.json --report-out <dir>/grid.json.gz -o <dir>
    python3 -I sim/sensitivity/analyze.py extract <grid reports> -o freq_table.json
    python3 -I sim/sensitivity/analyze.py extract-mc <mc reports> -o mc_table.json
    python3 -I sim/sensitivity/analyze.py report freq_table.json mc_table.json

The counter gate defaults to spec §5's 2^10 reference cycles at 10 MHz (`GATE_S`). `report --gate-exp K`
re-runs the same analysis at a gate of 2^K cycles, and `gate-sweep FREQ MC --vdd V --temp T` tabulates
counts and margin over a range of `K` at one (V,T) cell; both label the gate they used, and neither
changes the default. Extraction takes no gate option — it records `f_osc`, not counts.

`--pdk-root` cannot be combined with the batch backend; the runner uses its own PDK, and the PDK stamp it
reports (`environment.remote.worker_environment.pdk`) is what the record cites. The client-side
`provenance.pdk` in a report is the *submitting* host's search result and may name a different install.

## Measurement

`f_osc` is read from the rising-edge crossing times of `v(out)` at VDD/2 (`crossings`), skipping the first
3 edges (start-up); at least 5 cycles must remain or the cell is reported MISSING, never interpolated.
Process coordinates, column scaling and the P contrasts are stated in the `analyze.py` docstring and
repeated in every report.
