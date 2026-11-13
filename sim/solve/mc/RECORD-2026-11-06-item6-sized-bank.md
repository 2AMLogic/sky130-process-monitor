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

## Inputs pinned 2026-11-13 (#140) — appended; nothing above this line is edited

The Reproduce block above globs four directories. All four still resolve to this record's input set
today (checked 2026-11-13 against `17d4279`: no report matching those globs has landed since
`6d7a431`), so unlike the three sibling records this block still reproduces as written — by luck,
not by pinning, which is what #140 is about. The next
report to land in any of `sim/sensitivity/records/reports/`, `sim/solve/mc/reports/` or
`sim/solve/mc/reports-sized/` moves it. Nothing above is edited and no committed JSON is regenerated;
this note pins the set so that cannot happen silently.

Note in particular that `reports-sized/*.json.gz` here is all **120** chunks (5 oscillators x 6
row-2/4 cells x 4 chunks of n = 50), where the identical-looking glob in
`RECORD-2026-11-06-item6-sized.md` denoted only the 24 osc_subth chunks that existed at its commit.

**Pinned input set** (8 grid + 6 nominal-MC + 18 binding-cell + 120 sized chunks, in this order —
order is part of the pin, because `analyze.py extract-mc` pools same-cell samples by concatenation
and the chunks `c0..c3` pool onto the same cells). The brace forms below name exactly those files and
contain no wildcard, so nothing new in those directories can join them:

```
R=sim/sensitivity/records/reports
B=sim/solve/mc/reports
Z=sim/solve/mc/reports-sized
BIND=ff_1.62V_27C,ff_1.98V_27C,fs_1.98V_27C,sf_1.98V_27C,ss_1.98V_27C,tt_1.62V_-40C,tt_1.98V_27C
CELL=ff_1.62V_27C,ff_1.98V_27C,fs_1.98V_27C,sf_1.98V_27C,ss_1.98V_27C,tt_1.98V_27C

python3 -I sim/sensitivity/analyze.py extract \
  $R/grid_osc_hd.json.gz $R/grid_osc_hd_5p.json.gz $R/grid_osc_nmos.json.gz \
  $R/grid_osc_pmos.json.gz $R/grid_osc_subth.json.gz $R/grid_osc_subth_sf_cold.json.gz \
  $R/grid_osc_wire.json.gz $R/grid_osc_wire_sf_cold.json.gz -o freq.json
python3 -I sim/sensitivity/analyze.py extract-mc \
  $R/mc_osc_hd.json.gz $R/mc_osc_hd_5p.json.gz $R/mc_osc_nmos.json.gz \
  $R/mc_osc_pmos.json.gz $R/mc_osc_subth.json.gz $R/mc_osc_wire.json.gz -o mcnom.json
python3 -I sim/sensitivity/analyze.py extract-mc \
  $B/mc_bind_osc_hd.json.gz $B/mc_bind_osc_nmos_{$BIND}.json.gz $B/mc_bind_osc_pmos.json.gz \
  $B/mc_bind_osc_subth_-40C.json.gz $B/mc_bind_osc_subth_27C.json.gz \
  $B/mc_bind_osc_wire_{$BIND}.json.gz \
  $Z/mc_sized_osc_{hd,nmos,pmos,subth,wire}_{$CELL}_c{0,1,2,3}.json.gz -o mcbind.json   # 18 + 120
python3 -I sim/solve/yield_samples.py build freq.json mcnom.json mcbind.json -o samples.json
cmp samples.json sim/solve/mc/samples-sized-bank.json                      # identical

# the registering negative control of the section above, same draws, same inputs:
python3 -I sim/solve/yield_samples.py build freq.json mcnom.json mcbind.json \
  --defect 0.3 --defect-osc osc_hd -o negctl.json
cmp negctl.json sim/solve/mc/samples-sized-bank-negctl-hd0.3.json          # identical
```

Checked 2026-11-13 against `17d4279`: both byte-identical, on CPython 3.10.22, 3.11.17, 3.12.3 and
3.13.16. `sim/solve/test_records_reproduce.py` asserts both on every `npm test` run from the same
literal 152-path list (8 + 6 + 18 + 120), reading no glob. The `klt yield` step of the block above is not covered: no
released klt runs it (2AMLogic/klayout-tools#5018).
