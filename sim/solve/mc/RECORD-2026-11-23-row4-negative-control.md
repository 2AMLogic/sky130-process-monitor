# 2026-11-23 — T1 item 6: row-4 yield negative control no longer cancels in the one-point calibration (issue #317, decision 0005)

**SIMULATED. Post-processing only: pure stdlib re-derivation of the committed yield samples from the
recorded MC reports; no simulator, no PDK, no new draws, nothing measured.** Append-only: the five
prior `samples-*.json` outputs, the `RECORD-2026-11-06-*` records and every committed report are not
edited. No spec bound, limit, target or grid is changed. Rows 2 and 3 controls are untouched.

## What changed and why

`yield_samples.py` `row4_samples` passed the same seeded `defect` to both `draws()` calls — the
measurement draw at (ff, 1.62 V, 27 C) and the one-point calibration draw at (ff, 1.80 V, 27 C) —
and row 4 grades the calibrated difference `d = rd - cal`, so the offset subtracted out **exactly**
and the control could not fail (#317). Per [`spec/decisions/0005`](../../../spec/decisions/0005-row4-negative-control.md)
the defect is now injected on the **measurement draw only** (post-calibration drift); the calibration
read stays nominal, and its RNG stream no longer depends on the defect (seed string keeps the literal
`0.0` tail), so the control's calibration draw is the nominal arm's draw. The `build()` description
of the row-4 control states where the defect is injected. Rows 2 and 3 keep their existing injection
and seeding. A fixed-noise regression test in `sim/solve/test_solve.py`
(`test_row4_negative_control_moves_with_the_defect`) fails on the pre-0005 code.

## Fixed-RNG verification (the issue's measurement method, `TY.fake_mc(1e-4)`, row-4 grading loop,
both RNG streams held fixed so the deltas differ only through the defect)

| defect | row-4 calibrated deltas (n = 20, first/most-common value) |
|---|---|
| 0.0 | all `0.0` |
| 0.05 (committed `DEFECT`) | all `-1.0` — every draw moves ≥ one `TGRID` step |
| 0.5 | all `-8.5` — outside the ±5 C row-4 limit |
| 5.0 (the issue's 100x probe) | all `-72.0` |

The same four defects were then run through `row4_samples` itself (its own seeding) on the merged
code and give the same four results; on pre-0005 `origin/main` (`7eb4daa`) all four give **all `0.0`,
bit-identical to defect 0.0** (the vacuous control), which is the `assertNotEqual(fn_nom, fn_ctl)`
failure of the regression test on that code.

## Regenerated evidence (new, dated; prior files untouched)

Each new file is built from **the same pinned inputs, order and seed (20261105)** as its predecessor;
apart from `row4_dT.negative_control` the JSON is identical to the committed predecessor (checked as
data, see the foot of this record), so only the row-4 control arm differs. "nc moved" counts samples
whose value changed against the predecessor's control arm (grid snapping at 0.5 C absorbs sub-step
shifts; the sensitivity itself is the fixed-RNG table above):

| new file (this record) | supersedes | row-4 n | nc moved | \|nc\| > 5 C |
|---|---|---|---|---|
| `samples-binding-cells-2026-11-23.json` | `samples-binding-cells.json` | 10 | 1/10 | 10/10 |
| `samples-sized-2026-11-23.json` | `samples-sized.json` | 30 | 3/30 | 30/30 |
| `samples-sized-negctl-hd0.3-2026-11-23.json` | `samples-sized-negctl-hd0.3.json` | 30 | 7/30 | 30/30 |
| `samples-sized-bank-2026-11-23.json` | `samples-sized-bank.json` | 210 | 18/210 | 210/210 |
| `samples-sized-bank-negctl-hd0.3-2026-11-23.json` | `samples-sized-bank-negctl-hd0.3.json` | 210 | 98/210 | 210/210 |

At the committed `DEFECT` (0.05) the row-4 control therefore **grades as failing** on the recorded
evidence: 0 of 210 control samples fall inside the ±5 C limit (the nominal arm is also 0/210 — row 4
already fails its limit outright, so the control's job here is to stay sensitive, not to flip a
verdict).

The committed `yield-*.json` (`klt yield` outputs) are **not** regenerated: they grade the nominal
arms, which are identical in the dated files, so every recorded item-6 yield figure is unchanged, and
the row-4 control yield inside them stays 0.0 (already failing at nominal). Re-running `klt yield` on
the dated files needs `klt_yield_native` (2AMLogic/klayout-tools#5018, built from tag v0.9.1 into a
worktree-local `.venv-yield`); it is the last step of the reproduce block and is not covered by
`sim/solve/test_records_reproduce.py`, which pins the samples files only.

## Reproduce (pinned input sets, no globs; the same literal lists as `sim/solve/test_records_reproduce.py`)

```
R=sim/sensitivity/records/reports
B=sim/solve/mc/reports
Z=sim/solve/mc/reports-sized

# freq_8 / mcnom_6 / mcbind_18 (the RECORD-2026-11-06-item6-sized-bank pinned sets):
python3 -I sim/sensitivity/analyze.py extract \
  $R/grid_osc_hd.json.gz $R/grid_osc_hd_5p.json.gz $R/grid_osc_nmos.json.gz \
  $R/grid_osc_pmos.json.gz $R/grid_osc_subth.json.gz $R/grid_osc_subth_sf_cold.json.gz \
  $R/grid_osc_wire.json.gz $R/grid_osc_wire_sf_cold.json.gz -o freq_8.json
python3 -I sim/sensitivity/analyze.py extract-mc \
  $R/mc_osc_hd.json.gz $R/mc_osc_hd_5p.json.gz $R/mc_osc_nmos.json.gz \
  $R/mc_osc_pmos.json.gz $R/mc_osc_subth.json.gz $R/mc_osc_wire.json.gz -o mcnom_6.json
python3 -I sim/sensitivity/analyze.py extract-mc \
  $B/mc_bind_osc_hd.json.gz \
  $B/mc_bind_osc_nmos_{ff_1.62V_27C,ff_1.98V_27C,fs_1.98V_27C,sf_1.98V_27C,ss_1.98V_27C,tt_1.62V_-40C,tt_1.98V_27C}.json.gz \
  $B/mc_bind_osc_pmos.json.gz \
  $B/mc_bind_osc_subth_-40C.json.gz $B/mc_bind_osc_subth_27C.json.gz \
  $B/mc_bind_osc_wire_{ff_1.62V_27C,ff_1.98V_27C,fs_1.98V_27C,sf_1.98V_27C,ss_1.98V_27C,tt_1.62V_-40C,tt_1.98V_27C}.json.gz \
  -o mcbind_18.json
# freq_6 (the full-bank set): same extract step without the two *_sf_cold grids.
# mcbind_sized: mcbind_18's 18 reports + the 24 osc_subth sized chunks;
# mcbind_sized_bank: mcbind_18's 18 + all 120 sized chunks
#   ($Z/mc_sized_osc_{hd,nmos,pmos,subth,wire}_{ff_1.62V_27C,ff_1.98V_27C,fs_1.98V_27C,sf_1.98V_27C,ss_1.98V_27C,tt_1.98V_27C}_c{0,1,2,3}.json.gz);
#   the exact literal 152-path lists are sim/solve/test_records_reproduce.py's GRID_6/GRID_8/MCNOM_6/
#   MCBIND_18/MCSIZED_SUBTH_24/MCSIZED_ALL_120, which this record incorporates by reference.

python3 -I sim/solve/yield_samples.py build freq_6.json  mcnom_6.json mcbind_18.json          -o sim/solve/mc/samples-binding-cells-2026-11-23.json
python3 -I sim/solve/yield_samples.py build freq_8.json  mcnom_6.json mcbind_sized.json       -o sim/solve/mc/samples-sized-2026-11-23.json
python3 -I sim/solve/yield_samples.py build freq_8.json  mcnom_6.json mcbind_sized.json  --defect 0.3 -o sim/solve/mc/samples-sized-negctl-hd0.3-2026-11-23.json
python3 -I sim/solve/yield_samples.py build freq_8.json  mcnom_6.json mcbind_sized_bank.json  -o sim/solve/mc/samples-sized-bank-2026-11-23.json
python3 -I sim/solve/yield_samples.py build freq_8.json  mcnom_6.json mcbind_sized_bank.json  --defect 0.3 --defect-osc osc_hd -o sim/solve/mc/samples-sized-bank-negctl-hd0.3-2026-11-23.json
# klt yield <each dated samples file> --format json   # needs klt_yield_native (2AMLogic/klayout-tools#5018)
```

Byte-identity of the five predecessor files against these input sets was re-measured on the pre-0005
`yield_samples.py` (`origin/main` at `7eb4daa`, i.e. after #296 merged) by running the pre-0005
`sim/solve/test_records_reproduce.py` against them: its five predecessor checks pass byte-for-byte, so
the input pins above are exactly the sets the prior records were built from. The dated files were
built before #296 merged and were **not** rebuilt afterwards: on the merged tree (#296 plus this
change) the five dated outputs regenerate byte-identically from the same lists
(`sim/solve/test_records_reproduce.py`, 10 of 10 tests), because #296's per-cell sigma
(`analyze.mc_sigmas`) is the same estimate the former `sigma_cell` computed for every eligible cell.
Compared as data, each dated file equals its predecessor with `row4_dT.negative_control` removed: the
nominal arms and the rows 2/3 control arms are identical, and only the row-4 control arm differs.
Checked 2026-11-23 on CPython 3.12.3, post-processing only.
