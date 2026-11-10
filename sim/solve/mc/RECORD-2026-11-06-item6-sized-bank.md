# 2026-11-06 (sized full bank) — T1 item 6: osc_hd / osc_nmos / osc_pmos / osc_wire binding-cell MC to n = 200 per row-2/4 cell; `klt yield` re-run (issue #31)

**SIMULATED. Schematic-level netlists (sky130A open_pdks, ngspice-46 on the batch fleet), no layout or parasitics, nothing measured.** Append-only: earlier records and committed reports are not edited. No spec bound or limit is changed. The osc_subth sigma remains UNVALIDATED (#8).

## What was run
- osc_hd, osc_nmos, osc_pmos, osc_wire, `mismatch_scale=1` (`mc_mm_switch=1`), 4 chunks x 50 per cell (requests `requests-sized/`, seeds `20261106 + 1000*chunk`), at the six row-2/4 cells: tt/ss/ff/sf/fs @ 1.98 V / 27 C and ff @ 1.62 V / 27 C. 96 chunks submitted only through `klt sim --batch-set` (fleet; 6 in flight for the first set, 8 for the second); no local ngspice. Reports: `reports-sized/mc_sized_osc_{hd,nmos,pmos,wire}_*.json.gz` (job ids in each report's `environment.remote`).
- 94 of 96 chunks 50/50 passed. Two chunks ended fleet state `failed` / report status `error`, each with **49 valid draws and 1 errored** (nonconvergence / timestep_too_small): `osc_nmos` ss 1.98 V c3 (job klt-sim-5ed586f83cb2) and `osc_wire` ss 1.98 V c3 (job klt-sim-6ca1ed877f51). They were not re-run and not imputed; the ss cell therefore has 2 null draws (`errored: 2` in `klt yield`, n = 208).
- Not run: any osc_* draws at tt 1.62 V / -40 C (row 3 cell stays n = 30; row 3 needs n >= 6147, an operator cost decision, not queued; sigma is not pooled across cells).
- With the earlier osc_subth n = 210, every row-2/4 cell now pairs n = 210 draws (208 valid at ss). `klt yield` 0.9.1 semantics; `klt_yield_native` built from tag v0.9.1 into worktree-local `.venv-yield`.

## Result (`yield-sized-bank.json`, status = fail)
| Row | Cell | n | Empirical yield, 95 % CP CI | Verdict (required n) |
|---|---|---|---|---|
| 2 true tt | 1.98 V / 27 C | 210 | 0.057 [0.030, 0.098] | insufficient (2070) |
| 2 true ff | same | 210 | 0.0 [0.0, 0.017] | sufficient (183) |
| 2 true ss | same | 208 (2 errored) | 1.0 [0.982, 1.0] | insufficient (183; 368 for the target half-width) |
| 2 true sf | same | 210 | 1.0 [0.983, 1.0] | insufficient (183; 368 for target) |
| 2 true fs | same | 210 | 0.181 [0.131, 0.240] | insufficient (5694) |
| 3 dV +-20 mV | tt 1.62 V / -40 C | 30 | 0.20 [0.077, 0.386] | insufficient (6147) |
| 4 dT +-5 C | ff 1.62 V / 27 C | 210 | 0.0 [0.0, 0.017] | sufficient (183) |

Row 4 is `sufficient` at yield 0 (fails its +-5 C limit with confidence). Row 2 tt, fs, row 3 stay `insufficient` with the shortfall stated; row 2 ss/sf report `insufficient` because the tool also requires 368 draws for the target half-width at yield 1.0. Rows 2 (tt, ff, fs), 3 and 4 fail the ratified limits; none is a pass. Pooled estimates above are simulated at the stated corner, testbenches `osc/tb_osc_*.spice`.

## Negative controls (software-injected defect on the same draws, seed 20261105; not a second simulation)
- `yield-sized-bank.json` (+0.05 on ln f of osc_hd): `not_detected` everywhere. The weak control does not register.
- `yield-sized-bank-negctl-hd0.3.json` (`yield_samples.py --defect 0.3 --defect-osc osc_hd`): `detected` for row 2 tt, ss, sf, fs (yield to 0.0, n = 208-210). `not_detected` for row 2 ff (0 -> 1.0, a gross shift lands on the ff centroid), and for row 3 and row 4, which already sit at yield 0 and cannot show degradation. Reported as is.

## Reproduce
```
analyze.py extract sim/sensitivity/records/reports/grid_*.json.gz -o freq.json
analyze.py extract-mc sim/sensitivity/records/reports/mc_osc_*.json.gz -o mcnom.json
analyze.py extract-mc sim/solve/mc/reports/*.json.gz sim/solve/mc/reports-sized/*.json.gz -o mcbind.json
python3 -I sim/solve/yield_samples.py build freq.json mcnom.json mcbind.json -o sim/solve/mc/samples-sized-bank.json
klt yield sim/solve/mc/samples-sized-bank.json --format json > sim/solve/mc/yield-sized-bank.json   # exit 3 = fail
```
`6.analog` now cites `yield-sized-bank.json`. Pinned `klt signoff` 0.9.1 record is unchanged (3 of 22 T1 items met; item 6 analog unmet, digital `not_applicable`).
