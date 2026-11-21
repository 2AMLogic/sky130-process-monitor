# 2026-11-21 — spec rows 1-4 re-graded on the fullest frequency table main supports (issue #277)

**SIMULATED. Schematic-level netlists, no layout/parasitics, nothing measured.** Post-processing only: no
simulation is run for the grade itself; every input is a committed `klt sim` report. This record supersedes
`2026-11-05-rows1-4.md` for T1 item 5 (analog) — that record graded with 7 of 225 oscillator cells missing and
**is not edited** (append-only; it remains the grading of the reduced table). The difference here: the seven
cold cells now carry frequencies from five new single-cell fleet runs plus the two 2026-11-06 cold fills, so the
table has 225 of 225 coordinates resolved and rows 1-4 are graded on the full five-oscillator bank at every
(V,T) cell. Reproduce (byte-identical, CPython >= 3.12 — same `sum()` caveat as the 2026-11-05 record, identical
`mc_pooled_sigma_lnf` values): the pinned commands in `sim/solve/test_records_reproduce.py`
(`test_full_table_grade`); `solve.py grade` takes ~27 s.

## Inputs — explicit, ordered, no glob

`analyze.table()` is last-wins, so the input order decides the frequency table (the #140 lesson). The list is
the nine reports of `records/2026-11-14-osc-subth-gate-sizing.md` §1 — which keeps `grid_osc_hd_5p` before
`grid_osc_hd` so the default-step `osc_hd` value wins, and carries `probe_wire_sf_relaxed` after both
`grid_osc_wire*` — followed by the five new single-cell reports of this issue:

```
records/reports/grid_osc_hd_5p.json.gz
records/reports/grid_osc_hd.json.gz
records/reports/grid_osc_nmos.json.gz
records/reports/grid_osc_pmos.json.gz
records/reports/grid_osc_subth.json.gz
records/reports/grid_osc_subth_sf_cold.json.gz
records/reports/grid_osc_wire.json.gz
records/reports/grid_osc_wire_sf_cold.json.gz
records/reports/probe_wire_sf_relaxed.json.gz
records/reports/grid_osc_subth_ss_1.8V_-40C.json.gz
records/reports/grid_osc_subth_ss_1.62V_-40C.json.gz
records/reports/grid_osc_subth_sf_1.8V_-40C.json.gz
records/reports/grid_osc_subth_sf_1.62V_-40C.json.gz
records/reports/probe_nmos_tt_relaxed.json.gz
```

MC table: the five nominal MC reports only (`mc_osc_{hd,nmos,pmos,wire,subth}`), **not** `mc_osc_hd_5p` — the
2026-11-05 grading convention, so the pooled sigmas, seed (20261105) and draw count (2000) are unchanged from
that record and the diff below is attributable to the filled cells alone. Checked: the nine-report prefix
resolves 220/225 with all 218 originally resolved frequencies identical to `GRID_5` and only the two known fills
added (`osc_subth` sf/1.98 V/-40 C = 1057.366 Hz, `osc_wire` sf/1.98 V/-40 C = 84.9858 MHz); the five new
reports take coverage to 225/225.

## The seven previously missing cells — where each frequency comes from

| Cell | Filled by | Value | Caveat |
|---|---|---|---|
| `osc_subth` sf / 1.98 V / -40 C | `grid_osc_subth_sf_cold` (2026-11-06 fill) | 1057.37 Hz | longer window (10 ms), later open_pdks stamp than the base grid |
| `osc_wire` sf / 1.98 V / -40 C | `probe_wire_sf_relaxed` (2026-11-06 fill) | 84.986 MHz | **relaxed solver** (reltol=0.01 gmin=1e-10 method=gear), local probe run; bias up to +0.2 % at three converging cells (2026-11-06 record §1) |
| `osc_nmos` tt / 1.80 V / -40 C | `probe_nmos_tt_relaxed` (this issue) | 253.23 MHz | **relaxed solver** (same option set on `tb_osc_nmos_probe.spice`), fleet job; the same bias caveat as the wire probe is carried — the relaxed bias at this cell itself is not bounded |
| `osc_subth` ss / 1.80 V / -40 C | `grid_osc_subth_ss_1.8V_-40C` (this issue) | 3043.81 Hz | longer window (10 ms, 10 ns max step), fleet job klt-sim-2a87a76bfba6 |
| `osc_subth` ss / 1.62 V / -40 C | `grid_osc_subth_ss_1.62V_-40C` (this issue) | 1251.87 Hz | longer window (20 ms, 20 ns max step), fleet job klt-sim-20fe1964e087 |
| `osc_subth` sf / 1.80 V / -40 C | `grid_osc_subth_sf_1.8V_-40C` (this issue) | 586.21 Hz | longer window (40 ms, 40 ns max step), fleet job klt-sim-2b166cd03834 |
| `osc_subth` sf / 1.62 V / -40 C | `grid_osc_subth_sf_1.62V_-40C` (this issue) | 436.93 Hz | longer window (80 ms, 80 ns max step), fleet job klt-sim-a8f52ea96150 |

The five new runs are ngspice 47 on open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (the runner's own
install), submitted as single-cell `klt sim` batch jobs (`--wait-for-capacity 600`, no hand-launched ngspice).
Window sizes follow the #44 2 ms edge-spacing runs (`sim/subthreshold/README.md`) with >= 2x margin over the
nine edges the estimator needs; the max step is sized per window so each job stays ~1M internal steps, inside
the fleet whole-job ceiling. Edge counts: 202 / 30 / 25 / 23 / 38 rising edges — all well above the five-cycle
minimum. The ss/1.62 V and sf/1.80 V frequencies agree with the #44 spacings (~1.25 kHz, one edge at 1.94 ms);
nothing is interpolated or taken from edge spacing.

## Verdicts (target / fallback)

| Row | Target | Fallback | Binding / why |
|---|---|---|---|
| 1 oscillates at all 45 cells | **PASS** (225/225) | **PASS** (135/135) | was FAIL/FAIL with 7 missing cells; the full bank oscillates everywhere. Lowest f is the new `osc_subth` sf / 1.62 V / -40 C cell, 436.93 Hz |
| 2 five-corner ID at known V,T (ratio space) | **FAIL** (8 of 9 (V,T) cells identified) | **PASS** (slow/fast, 9 of 9) | 1.98 V / 27 C: 1 fs->tt error in 2000 draws — unchanged from the reduced-table grade. **Every (V,T) cell now grades on the full 5-oscillator bank** (the three -40 C cells used 3-4 oscillators before) |
| 3 V solve, T known, corner unknown | **FAIL** | **PASS** | worst p99 \|dV\| = 34 mV at 125 C, ff, 1.80 V (the held-out interior cell; systematic 28 mV). Was FAIL/FAIL with 62 mV at -40 C, tt, 1.62 V on the reduced -40 C bank. 45/45 cells graded, five oscillators everywhere |
| 4 T solve, one-point cal at 27 C/1.80 V, V known | **FAIL** | **FAIL** | worst p99 \|dT\| = 36.0 C at sf, 1.62 V, 125 C (systematic -31.5 C). **Worse than the recorded 19.0 C** because 45/45 cells are now graded with all five oscillators (was 29/45, `osc_nmos` excluded): the previously ungradable cells fail harder than the old binding cell (ff, 1.62 V, 27 C). tt-model, corner-agnostic; the tt die is in-sample |

Row 2's five-corner target remains limited by the 1.98 V / 27 C fs/tt confusion, not by cold-cell coverage. Rows
3 and 4 remain limited by the model shape (row 3: corner-unknown quadratic; row 4: corner-agnostic tt
tensor-product), now exposed at the hot cells rather than masked by missing -40 C data. What limits each failing
row, as input to follow-on design iteration: row 2 target — `osc_hd`/`osc_subth` ratio separation between fs and
tt at 1.98 V / 27 C under the pooled noise; row 3 target — the ff quadratic in V at 125 C (systematic, not
noise); row 4 — the single-point-cal tt model's systematic error at sf / 1.62 V / 125 C.

## Caveats (not hidden)

- Two of the seven fills (`osc_wire` sf/1.98 V/-40 C, `osc_nmos` tt/1.80 V/-40 C) rest on **relaxed-solver**
  values whose bias at the filled cell itself is not bounded (the 2026-11-06 caveat, carried unchanged); the
  other five rest on longer-window runs with the default solver. Row 1's PASS therefore rests on two
  relaxed-solver cells.
- Noise = counter quantization + the pooled MC sigma applied to every cell; MC exists only at 1.80 V/27 C.
  `osc_subth`'s sigma(ln f)=0.27 is UNVALIDATED and dominates every solve it is in — unchanged from the
  2026-11-05 record (the MC inputs are byte-identical).
- Rows 3 and 4 are graded on the 3x3 (V,T) grid points only; no off-grid truth was simulated, so no accuracy
  between grid points is quoted, and **no estimate accuracy is quoted anywhere here**: the row 3/4 figures are
  graded failures against those rows' limits, not an accuracy claim.
- Row 4 joint V+T solve: not run. Row 2 absolute-ln f variant: not run. Mismatch MC beyond the pooled noise
  term is #31.
- The synthetic negative controls (`test_solve.py`) still show the estimators recover a known V/T and fail under
  excess noise.
