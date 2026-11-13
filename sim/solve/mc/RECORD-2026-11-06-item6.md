# 2026-11-06 — T1 item 6: `klt yield` at the binding cells of rows 2-4, and the digital not-applicable statement (issue #31)

**SIMULATED. Schematic-level netlists (sky130A open_pdks, ngspice-46 on the batch fleet), no layout or parasitics, nothing measured.** Append-only: `sim/solve/records/2026-11-05-rows1-4.*` is not edited. No spec bound, limit or decision record is changed.

## Verdict (recorded as failing / incomplete, not hidden)
`klt signoff` (klayout-tools 0.9.1): item 6 **analog = unmet (`check_failed`)**, **digital = `not_applicable`**. Rows 2, 3, 4 fail their limits in every measurement that can fail, and the campaign is undersized and partly missing:

| Row | Cell (corner @ V / T) | Samples (n) | Empirical yield, 95 % CP CI | Sample-size verdict | Negative control |
|---|---|---|---|---|---|
| 2 margin, true tt | 1.98 V / 27 C | 10 | 1.0 [0.69, 1.0] | insufficient (needs 183) | not detected |
| 2 margin, true ff | same | 10 | 0.0 [0.0, 0.31] | insufficient | not detected (nominal already 0) |
| 2 margin, true ss | same | 10 | 1.0 [0.69, 1.0] | insufficient | not detected |
| 2 margin, true sf | same | 10 | 1.0 [0.69, 1.0] | insufficient | not detected |
| 2 margin, true fs | same | 10 | 0.0 [0.0, 0.31] | insufficient | not detected (nominal already 0) |
| 3 dV, limit ±20 mV | tt @ 1.62 V / -40 C | 30 | 0.57 [0.37, 0.75] | insufficient (needs 9433) | detected |
| 4 dT, limit ±5 C | ff @ 1.62 V / 27 C (cal 1.80 V / 27 C) | 10 | 0.0 [0.0, 0.31] | insufficient | not detected (nominal already 0) |

Row 2 margin = whitened d² to the nearest wrong centroid minus d² to the true centroid (> 0 = correct); this convention is a grading choice made here. Row 2 ff and fs are all-wrong at 1.98 V / 27 C, i.e. worse than the single-error 2000-draw result in the rows 1-4 record, because here the draws are real per-cell mismatch samples with the oscillator set below, not the pooled sigma. The negative control (+0.05 on ln f of osc_hd, injected in software on the same draws, not a second simulation) cannot show degradation where the nominal yield is already 0; for the rows that pass in some draws it also did not register at n = 10. Neither is a pass: signoff would grade them `negative_control_not_detected` / `undersized_sample` if the yield itself were not already failing.

## What ran
Requests `sim/solve/mc/requests/mc_bind_*.json` (generator `sim/solve/gen_binding_mc.py`): `klt sim --batch-set` on the batch fleet, mismatch MC (`mismatch_scale=1`, i.e. `mc_mm_switch=1`), seed 20261105, `seed_scope: point`, same testbenches/windows as the #8 nominal MC. n = 30 per cell (osc_subth: 10). Committed reports: `sim/solve/mc/reports/`. Fleet jobs: osc_hd klt-sim-e6ff53edad9c, osc_pmos klt-sim-6010922adfb8, osc_subth 27 C klt-sim-78a575c94999, osc_subth -40 C klt-sim-6d4ef7df76e9. No local ngspice was used.

## Missing (not filled, not interpolated)
- **osc_nmos and osc_wire at all binding cells**: batch jobs klt-sim-3088fc5273ba and klt-sim-1be9ae9b5158 (nmos, submitted twice) and klt-sim-e1806ca95d7b (wire) ended `failed: job command exited 4` after 10-20 min with no per-unit diagnostics (generic tool gap filed: 2AMLogic/klayout-tools#5019). No retry loop beyond one resubmission; no local fallback.
- Consequently the oscillator bank in the yield samples is osc_hd, osc_pmos (+ osc_subth where it has data): row 2 uses {osc_hd, osc_pmos, osc_subth}, row 3 {osc_hd, osc_pmos}, row 4 {osc_hd, osc_pmos, osc_subth}. This is a REDUCED bank; the 5-oscillator figures are not available.
- osc_subth has n = 10, which also caps n for rows 2 and 4 (draw k pairs the k-th sample of every oscillator). Its sigma is UNVALIDATED (see the #8 records). The osc_hd 20 ps step artefact is carried as a caveat, not fixed.
- Row 4's calibration read is drawn from the #8 nominal-cell MC independently of the measurement draw (a real die would correlate them): conservative.

## Reproduce
```
analyze.py extract sim/sensitivity/records/reports/grid_*.json.gz -o freq.json
analyze.py extract-mc sim/sensitivity/records/reports/mc_osc_*.json.gz -o mcnom.json
analyze.py extract-mc sim/solve/mc/reports/*.json.gz -o mcbind.json
python3 -I sim/solve/yield_samples.py build freq.json mcnom.json mcbind.json -o sim/solve/mc/samples-binding-cells.json
klt yield sim/solve/mc/samples-binding-cells.json --format json > sim/solve/mc/yield-binding-cells.json
```
`klt yield` is not runnable on any released klt (2AMLogic/klayout-tools#5018, a recurrence). The report was produced with `klt_yield_native` built from the `native/yield` tree at tag v0.9.1 into a worktree-local venv (`maturin develop --release`, CARGO_BUILD_JOBS=2); host tools untouched.

## Digital (`6.digital`)
`spec/digital-rows.json` (rows 5 and 6 only; reference-clock wording is "tolerance", an input requirement) and `verification/readout/not-statistical.json`, hash-bound in the manifest; `klt signoff` grades `not_applicable`. This is a classification of the rows, not a result: the readout testbench behind them (`verification/readout/`) is not yet built.

## Inputs pinned 2026-11-13 (#140) — appended; nothing above this line is edited

The Reproduce block above globs three directories. At this record's commit (`63392bd`) they resolved
to a set that no longer exists, and **the output this record produced is no longer in the tree**:
`sim/solve/mc/samples-binding-cells.json` was overwritten at `f1026ec` by the full-bank run of
`RECORD-2026-11-06-item6-full-bank.md`, which is the record that supersedes this one's "Missing" and
yield-table sections. So there is no committed file to diff this record against, and it is
deliberately **left out of `sim/solve/test_records_reproduce.py`** rather than being made to pass
against someone else's output. Nothing here is edited and nothing is regenerated.

The input set is still identified. Measured 2026-11-13 against `17d4279`: with today's code, the list
below reproduces `samples-binding-cells.json` **as committed at `63392bd`**
(`git show 63392bd:sim/solve/mc/samples-binding-cells.json`) byte-identically — so the post-processing
refactors since (`0930916`, `ff1ce1c`) did not change this record's numbers. It is out of the test
only because a shallow CI checkout has no `63392bd` blob to compare against.

```
R=sim/sensitivity/records/reports
B=sim/solve/mc/reports
python3 -I sim/sensitivity/analyze.py extract \
  $R/grid_osc_hd.json.gz $R/grid_osc_nmos.json.gz $R/grid_osc_pmos.json.gz \
  $R/grid_osc_wire.json.gz $R/grid_osc_subth.json.gz -o freq.json
python3 -I sim/sensitivity/analyze.py extract-mc \
  $R/mc_osc_hd.json.gz $R/mc_osc_nmos.json.gz $R/mc_osc_pmos.json.gz \
  $R/mc_osc_wire.json.gz $R/mc_osc_subth.json.gz -o mcnom.json
python3 -I sim/sensitivity/analyze.py extract-mc \
  $B/mc_bind_osc_hd.json.gz $B/mc_bind_osc_pmos.json.gz \
  $B/mc_bind_osc_subth_-40C.json.gz $B/mc_bind_osc_subth_27C.json.gz -o mcbind.json
python3 -I sim/solve/yield_samples.py build freq.json mcnom.json mcbind.json -o samples.json
git show 63392bd:sim/solve/mc/samples-binding-cells.json > at-63392bd.json
cmp samples.json at-63392bd.json      # identical
```

Two things the Reproduce block above does not say, both found by running it (#140):

- **`grid_*.json.gz` / `mc_osc_*.json.gz` were already wider than the input set when this record was
  written.** `grid_osc_hd_5p.json.gz` and `mc_osc_hd_5p.json.gz` were in `reports/` at `63392bd` and
  match those globs, but including them does not reproduce this record; the five per-oscillator
  reports above do. The `_5p` reports *are* part of the full-bank record's input set, which is why
  that record's pinned list has six of each — the two records' globs look identical and denote
  different sets.
- **`sim/solve/mc/reports/*.json.gz` was four files here, eighteen from `f1026ec` onwards** (the
  per-cell osc_nmos / osc_wire resubmission). That is the reduced bank this record reports, and it is
  what makes the glob reading of this block return the full-bank numbers today.
