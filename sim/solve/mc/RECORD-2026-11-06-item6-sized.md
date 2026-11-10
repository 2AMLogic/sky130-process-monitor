# 2026-11-06 (sized osc_subth) — T1 item 6: osc_subth binding-cell MC to n = 210 per row-2/4 cell; `klt yield` re-run (issue #31)

**SIMULATED. Schematic-level netlists (sky130A open_pdks, ngspice-46 on the batch fleet), no layout or parasitics, nothing measured.** Append-only: earlier records and committed reports are not edited. No spec bound or limit is changed.

## What was run
- osc_subth, `mismatch_scale=1`, 4 chunks x 50 per cell (seeds `20261106 + 1000*chunk`), at the six row-2/4 cells: tt/ss/ff/sf/fs @ 1.98 V / 27 C and ff @ 1.62 V / 27 C. Only `klt sim --batch-set` (fleet), no local ngspice. 24/24 chunks 50/50 passed, 0 errored (the 2 earlier chunks are in `reports-sized/`; the other 22 collected this pass, job ids in each report's `environment.remote`). With the earlier 10-draw run each cell has **n = 210** for osc_subth (pooled by concatenation, `analyze.py extract-mc`).
- Not run: osc_subth at tt 1.62 V / -40 C (row 3 cell, stays n = 10), and any additional draws for osc_hd / osc_nmos / osc_pmos / osc_wire (stay n = 30, 29 at one cell each). Row 3 campaign (n >= 6147) not funded: operator cost decision, see below.

## Result (`klt yield` 0.9.1 semantics, status = fail; yield_native built from tag v0.9.1 into worktree-local `.venv-yield`)
`yield_samples.py` pairs draws across the whole bank, so n = the smallest per-oscillator count = **30** (29 for ss). Raising osc_subth alone therefore lifts rows 2/4 from n = 10 to n = 30, **not** to 183.

| Row | Cell | n | Empirical yield, 95 % CP CI | Verdict (required n) |
|---|---|---|---|---|
| 2 true tt | 1.98 V / 27 C | 30 | 0.033 [0.001, 0.172] | insufficient (1238) |
| 2 true ff | same | 30 | 0.0 [0.0, 0.116] | insufficient (183) |
| 2 true ss | same | 29 | 1.0 [0.881, 1.0] | insufficient (183) |
| 2 true sf | same | 30 | 1.0 [0.884, 1.0] | insufficient (183) |
| 2 true fs | same | 30 | 0.0 [0.0, 0.116] | insufficient (183) |
| 3 dV +-20 mV | tt 1.62 V / -40 C | 30 | 0.20 [0.077, 0.386] | insufficient (6147) |
| 4 dT +-5 C | ff 1.62 V / 27 C | 30 | 0.0 [0.0, 0.116] | insufficient (183) |

Rows 2 (tt, ff, fs), 3, 4 fail; this is a simulated estimate with an UNVALIDATED osc_subth sigma (#8), not a pass in any form.

## Negative controls
- `yield-sized.json`: seeded +0.05 on ln f of osc_hd (software-injected, same draws). Does **not** register (row 2 yields rise or stay; klt warns).
- `yield-sized-negctl-hd0.3.json` (`yield_samples.py --defect 0.3`): registers for row 2 ss, sf (1.0 -> 0.0), tt and fs (to 0.0) and row 3 (0.2 -> 0.0). Rows already at yield 0 (row 4, row 2 fs) cannot show degradation; row 2 ff moves 0 -> 1.0 (a gross shift lands on the ff centroid), reported as is. Seed 20261105, N = 30.

## Shortfall (stated, not imputed)
- Rows 2/4 need n >= 183 for **every** oscillator at each cell: roughly 4 oscillators x 6 cells of further draws (osc_hd, osc_pmos cheap; osc_nmos/osc_wire one request per cell). Not queued here.
- Row 3 needs n >= 6147 (all five oscillators, ~120+ chunks each): needs an operator cost decision. Sigma is not pooled across cells.
- Verdict stays `insufficient` for all rows; `6.analog` now cites `yield-sized.json`; pinned `klt signoff` (0.9.1) record unchanged (item 6 analog `unmet`, digital `not_applicable`).

## Reproduce
```
analyze.py extract sim/sensitivity/records/reports/grid_*.json.gz -o freq.json
analyze.py extract-mc sim/sensitivity/records/reports/mc_osc_*.json.gz -o mcnom.json
analyze.py extract-mc sim/solve/mc/reports/*.json.gz sim/solve/mc/reports-sized/*.json.gz -o mcbind.json
python3 -I sim/solve/yield_samples.py build freq.json mcnom.json mcbind.json -o sim/solve/mc/samples-sized.json
klt yield sim/solve/mc/samples-sized.json --format json > sim/solve/mc/yield-sized.json   # exit 3 = fail
```
