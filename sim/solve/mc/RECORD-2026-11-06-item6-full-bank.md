# 2026-11-06 (later) — T1 item 6: osc_nmos and osc_wire binding-cell MC completed; `klt yield` re-run on the full 5-oscillator bank (issue #31)

**SIMULATED. Schematic-level netlists (sky130A open_pdks, ngspice-46 on the batch fleet), no layout or parasitics, nothing measured.** Append-only: `RECORD-2026-11-06-item6.md` is not edited; where this record differs, this one supersedes the "Missing" and yield-table sections of that one. No spec bound, limit or decision record is changed.

## What changed
The earlier 7-unit osc_nmos / osc_wire requests ended `failed: job command exited 4` and returned nothing. Exit 4 is a per-unit verdict: a job with any errored draw exits 4 even though the other draws are valid. `sim/solve/gen_binding_mc.py` now emits **one request per binding cell** for those two oscillators (`mc_bind_osc_{nmos,wire}_<corner>_<V>V_<T>C.json`), so one bad draw no longer discards the other cells. Same testbenches, `mismatch_scale=1`, seed 20261105, n = 30 per cell, submitted with `klt sim --batch-set` / `--backend batch` only; no local ngspice grid.

| Cell | osc_nmos | osc_wire |
|---|---|---|
| tt/ss/ff/sf/fs @ 1.98 V, 27 C; tt @ 1.62 V, -40 C; ff @ 1.62 V, 27 C | 7 cells, 6 pass 30/30 | 7 cells, 6 pass 30/30 |
| errored draws | ss @ 1.98 V / 27 C: 29/30 (1 `timestep_too_small`, klt-sim-5e76dc50f7cb) | tt @ 1.62 V / -40 C: 29/30 (klt-sim-9619873e255a) |

Fleet job ids are in each committed report's `environment.remote`. The two errored draws are **not imputed**: they enter `klt yield` as errored samples (conditional yield, flagged by klt).

## Result (recorded failing; `klt yield` 0.9.1 status = fail)
Oscillator bank is now all five (osc_hd, osc_nmos, osc_pmos, osc_wire, osc_subth). The sample count is still capped at **n = 10 for rows 2 and 4 by osc_subth** (its binding-cell MC was run at n = 10; not re-run here). Row 3 uses n = 30.

| Row | Cell | n | Empirical yield, 95 % CP CI | Sample-size verdict |
|---|---|---|---|---|
| 2 margin, true tt | 1.98 V / 27 C | 10 | 0.0 [0.0, 0.31] | insufficient (needs 183) |
| 2 margin, true ff | same | 10 | 0.0 [0.0, 0.31] | insufficient |
| 2 margin, true ss | same | 9 (1 errored) | 1.0 [0.66, 1.0] | insufficient |
| 2 margin, true sf | same | 10 | 1.0 [0.69, 1.0] | insufficient |
| 2 margin, true fs | same | 10 | 0.0 [0.0, 0.31] | insufficient |
| 3 dV, limit ±20 mV | tt @ 1.62 V / -40 C | 30 | 0.20 [0.08, 0.39] | insufficient (needs 6147) |
| 4 dT, limit ±5 C | ff @ 1.62 V / 27 C | 10 | 0.0 [0.0, 0.31] | insufficient |

Compared with the reduced-bank record, row 2 tt now fails (was 1.0 at n = 10): the extra oscillators' own mismatch widens the whitened spread. This is a change in the simulated estimate, not a design improvement or regression. Row 3 yield fell from 0.57 to 0.20. The negative control (+0.05 on ln f of osc_hd, injected in software on the same draws) still did not register for the rows already at yield 0; `klt yield` warns about it. Rows 2-4 remain **failing**; the campaign remains **undersized** (sample-size verdict `insufficient` everywhere). Not a pass in any form.

## Still missing
- n >= 183 (rows 2, 4) and n >= 6147 (row 3) are not reached; a campaign of that size was not run. osc_subth n = 10 is the binding cap for rows 2 and 4 and its sigma is UNVALIDATED (see #8 records).
- The osc_hd 20 ps step artefact is carried as a caveat.

## Reproduce
```
analyze.py extract sim/sensitivity/records/reports/grid_*.json.gz -o freq.json
analyze.py extract-mc sim/sensitivity/records/reports/mc_osc_*.json.gz -o mcnom.json
analyze.py extract-mc sim/solve/mc/reports/*.json.gz -o mcbind.json
python3 -I sim/solve/yield_samples.py build freq.json mcnom.json mcbind.json -o sim/solve/mc/samples-binding-cells.json
klt yield sim/solve/mc/samples-binding-cells.json --format json > sim/solve/mc/yield-binding-cells.json
```
`klt yield` needs `klt_yield_native` (2AMLogic/klayout-tools#5018): built from `native/yield` at tag v0.9.1 into the worktree-local `.venv-yield` (host tools untouched). `klt signoff` (pinned 0.9.1) output is unchanged: item 6 analog `unmet`, digital `not_applicable`; manifest `6.analog` hash updated.
