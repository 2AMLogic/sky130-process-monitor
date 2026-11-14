# 2026-11-14 — correction to the row-7 active-power gradability threshold (issue #173). No recorded verdict changes.

**Not a re-run and not a re-grade.** No simulation was performed for this note and nothing in this directory
was edited; records here are append-only. This records a correction to the *grader*, made after
`2026-11-05-power-grade-complete.json` was produced, and states exactly what it does and does not touch.

## What was wrong

`analyze_power.py` decided which active cells are gradable with its own literal, `len(cr) >= 5 + 3`, commented
"`>= 5 edges inside the run (3 start-up edges skipped as in #8)`". The #8 rule it cites is
`sim/sensitivity/analyze.py:freq_from_crossings`, which drops `SKIP_EDGES = 3` start-up edges and then requires
`MIN_CYCLES + 1 = 6` further crossings — **9 rising crossings**, not 8. `sim/pex/grade_pex.py` computed 9
correctly; the power grader was one count low. The file's docstring carried the same off-by-one in prose
("fewer than 5 rising crossings in the window").

Net effect: a cell with **exactly 8** rising crossings was graded for power — its mean supply current folded
into the "worst oscillator, worst cell" active binding figure — while the #8 frequency surface records the same
cell as MISSING. A cell at that boundary is a barely-starting ring, whose mean supply current is the least
trustworthy number in the set. The window is exactly one count wide: 8 was the only crossing count at which the
two graders disagreed.

The threshold is now read from the module `analyze_power.py` already loads
(`MIN_EDGES = _SENS.SKIP_EDGES + _SENS.MIN_CYCLES + 1`), so there is one definition of the rule, not three.

## Effect on the recorded row-7 verdicts: none

- `2026-11-05-power-grade-complete.json` re-grades **byte-identically** from the committed
  `2026-11-05-power-table-complete.json` under the corrected grader. The threshold is applied in `extract`
  (reports -> table), and `grade` (table -> verdicts) reads `i_a` only, so the committed grade cannot move.
  This byte-identity is asserted in `sim/power/test_analyze_power.py`.
- The active verdict is FAIL at target (< 100 uW), fallback (< 500 uW) and stretch (< 20 uW), binding on
  `osc_wire|ff|1.98|-40` at 1740.2 uW — a fast corner three orders of magnitude above the loosest bound and
  nowhere near the start-up boundary. Tightening the gradability rule cannot flip it.
- The idle verdict is unaffected: idle is an `op` analysis with the ring gated off, so the oscillation rule
  never applied to it.

## What cannot be restated, and is therefore not claimed

**Whether any of the 219 graded active cells sat at exactly 8 crossings is not recoverable from this
directory.** The power raw `klt sim` reports are not committed (only the extracted table and the grade), and
`2026-11-05-power-table-complete.json` carries `i_a` per cell with no crossing count. So the corrected grader
cannot be re-run against the 2026-11-05 data, and the cell count `cells_graded: 219 / 225` in that record is
**not revised here** — it is the number the grader of the day produced. If a future power run re-extracts from
fresh reports, its coverage line may legitimately differ by the cells at 8 crossings, and that is a new record,
not a correction to this one.

Relatedly, `2026-11-05-power-complete.md` describes the 6 ungraded active cells as having "fewer than 8 rising
edges in the window". That prose reflects the grader as it then stood and is left as written (append-only); the
rule in force from this date is 9. The 6 cells (5 `osc_subth` at -40 C, 1 `osc_wire` sf/1.62 V/-40 C) are
ungraded under either threshold, so their status is unchanged.

## Verification

Stdlib `unittest`, no simulator: `python3 -I sim/power/test_analyze_power.py` (wired into `npm test`). It pins
the boundary as an invariant rather than a number — a cell is gradable for power **iff**
`sensitivity/analyze.py:freq_from_crossings` yields a frequency for it — checks 8 MISSING / 9 graded directly,
and proves the grader tracks the source constants by loading an unmodified copy of `analyze_power.py` beside a
sensitivity module with `SKIP_EDGES, MIN_CYCLES = 4, 7` and asserting the boundary moves to 12.
