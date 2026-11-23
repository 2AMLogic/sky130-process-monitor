# 0005: Row-4 yield negative-control semantics (defect on the measurement draw only)

- Status: **proposed** (not accepted; a human or Champion ratifies). The direction is the one recommended in #317's curated enhancement and approved when the issue was promoted to `loom:issue`; it changes no spec bound, limit or target.
- Date: 2026-11-23
- Issue: #317 (found while evaluating PR #296; pre-existing on `main`)
- Evidence: `sim/solve/mc/RECORD-2026-11-23-row4-negative-control.md` and the dated samples files it lists. **All figures SIMULATED**, schematic-level post-processing of recorded MC; nothing measured, nothing re-simulated.

## Background

`sim/solve/yield_samples.py` attaches a software-injected negative control to every emitted
measurement of a row that uses `DEFECT_OSC` (`osc_hd` by default): `+DEFECT` (default 0.05) added to
ln f of that oscillator. For `row4_dT` the
same defect was passed to **both** `draws()` calls — the measurement draw at (ff, 1.62 V, 27 C) and
the one-point calibration draw at (ff, 1.80 V, 27 C). Row 4 grades the calibrated difference
`d = rd - cal`, so the offset subtracted out exactly and the control **could not fail**: with both
RNG streams held fixed, `defect` 0.0 vs 5.0 gave bit-identical calibrated deltas. The recorded
row-4 control arms in the committed `sim/solve/mc/samples-*.json` therefore certified noise
reshuffling (the defect also enters the seed strings), not estimator sensitivity. No row-4 accuracy
figure was wrong; only the control's evidentiary value. Rows 2 (ratio against the baseline) and 3
(un-calibrated) are structurally unaffected and their controls did shift.

## Decision

The row-4 negative control models **post-calibration drift**: the seeded defect is injected on the
**measurement draw only**, and the calibration read stays nominal (defect 0.0, and its RNG stream
does not depend on the defect, so the control's calibration draw is the nominal arm's draw). This is
the reading under which the control is meaningful — a constant ln f offset appearing only after
calibration is exactly what a one-point calibration cannot absorb, and the estimator must notice a
shifted `osc_hd`. The nominal arm (defect 0) is unchanged bit-for-bit, and rows 2 and 3 keep their
existing injection (single draw each) and seeding.

Rejected alternatives:

- **A slope/temperature-coefficient perturbation** instead of a constant offset — a new defect class
  and a new knob, larger than the evidence gap it closes.
- **Keep the injection and label the row-4 control "cancels by construction"** — leaves row 4 with
  no live control, so a genuine row-4 estimator insensitivity would go uncaught.

## Consequences

- `row4_samples` no longer lets the seeded defect cancel; the fixed-noise regression test in
  `sim/solve/test_solve.py` (issue #317) fails on the pre-0005 code.
- The affected evidence is regenerated as **new, dated records**
  (`sim/solve/mc/samples-*-2026-11-23.json`, `RECORD-2026-11-23-row4-negative-control.md`);
  the prior records are not edited in place.
- No spec bound, limit, target, row-4 limit (±5 C) or `TGRID` resolution changes; the solver and
  the row 2/3 controls are untouched.
