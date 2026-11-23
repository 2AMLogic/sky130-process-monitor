# Characterization report — analog partition (T1 item 8, `8.analog`)

**SIMULATED. Every figure below is simulated, labelled with its corner and its
testbench, and copied from a committed record — nothing here is measured, and
nothing will be until silicon exists.** This report aggregates; it grades
nothing anew. Each verdict is the verdict the cited record already carries, and
no spec bound, limit or recorded verdict is edited, relaxed or re-derived here.
Where a row has no recorded result it is listed as **not recorded** — never as a
pass and never as a fail.

**Numbering convention.** Rows are indexed by **`spec/target-spec.md` section**
("spec §N"), not by T1 checklist item. The two schemes collide: T1 item 6
(statistical evidence) is *not* spec §6 (conversion time), and T1 item 8 (this
report) is *not* spec §8 (area). Where a T1 item is named it is written "T1
item N".

**Partition.** Analog is the ring-oscillator bank (standard-cell and
custom-cell variants, including the leakage-starved subthreshold oscillator) and
the subthreshold sensing path, per `manifests/sky130-process-monitor.json`'s
`partition_boundary`. The readout rows are in
`characterization/digital.md`. Spec §8 (area) and spec §9 (signoff) bind the
**whole** block, so each appears in **both** reports stating only that
partition's share; neither report claims a whole-block verdict for them.

**Status of this report: `fail`** (`evidence/item8_analog.json`). Spec §1, §3
and §4 fail both target and fallback; spec §2 fails its five-corner target and
passes the slow/fast fallback; spec §7 fails at all three levels on both the
active and the idle figure; the analog share of spec §9 fails target and
fallback. No row here passes its target.

**No estimate accuracy is quoted anywhere in this report.** The worst-case
errors recorded for spec §3 and §4 below are the *graded failures* the solve
procedure produced against those rows' limits — they are recorded results, not
an accuracy claim for the block. Per `CLAUDE.md`, no accuracy is quoted that the
solve procedure has not been run against, and the sensitivity matrix and its
conditioning are shown (spec §2) before any of those rows is discussed.

---

## Row summary

| Spec row | Target | Fallback | Stretch | Binding corner | Record |
|---|---|---|---|---|---|
| §1 Oscillator bank composition | **FAIL** | **FAIL** | not recorded | 7 of 225 oscillator cells, all at −40 °C | `sim/solve/records/2026-11-05-rows1-4.md` |
| §2 Process discrimination | **FAIL** (8 of 9 (V,T) cells) | **PASS** (slow/fast, 9 of 9) | not recorded | 1.98 V / 27 °C | `sim/solve/records/2026-11-05-rows1-4.md` |
| §3 Supply estimate | **FAIL** | **FAIL** | not recorded | tt / 1.62 V / −40 °C | `sim/solve/records/2026-11-05-rows1-4.md` |
| §4 Temperature estimate | **FAIL** | **FAIL** | not recorded | ff / 1.62 V / 27 °C | `sim/solve/records/2026-11-05-rows1-4.md` |
| §7 Active power | **FAIL** | **FAIL** | **FAIL** | osc_wire / ff / 1.98 V / −40 °C | `sim/power/records/2026-11-05-power-complete.md` |
| §7 Idle power | **FAIL** | **FAIL** | **FAIL** | sf / 1.62 V / 27 °C (figure SUSPECT; verdict holds without it) | `sim/power/records/2026-11-05-power-complete.md` |
| §8 Area (analog share) | **not recorded** | **not recorded** | **not recorded** | — | `layout/README.md` |
| §9 Signoff (analog share) | **FAIL** | **FAIL** | — | — | `lvs/README.md`, `sim/pex/README.md` |

Spec §5 (readout) and §6 (conversion time) are the digital partition's rows and
are in `characterization/digital.md`; the partition split for those two is
ratified in `spec/digital-rows.json`.

---

## Spec §1 — Oscillator bank composition

**Verdict: target FAIL, fallback FAIL.** Recorded in
`sim/solve/records/2026-11-05-rows1-4.md` (per-cell output
`sim/solve/records/2026-11-05-rows1-4.json`).

The row binds all 45 cells of the PVT box (5 corners × 3 V × 3 T) for frequency
surfaces, five oscillators, so 225 oscillator cells.

**SIMULATED**, schematic-level netlists, no layout and no parasitics.
Testbenches `sim/sensitivity/osc/` (reusing `design/osc_bank/`), requests
`sim/sensitivity/requests/`, run as `klt sim --batch-set` on the batch fleet;
ngspice-46, sky130A from open_pdks `c6d73a35` (`sim/pdk.json`).

- **7 of 225 oscillator cells have no oscillation or too few edges** — reported
  missing, never interpolated
  (`sim/sensitivity/records/2026-11-05-grid-sensitivity-partial.md`):
  `osc_nmos` tt / 1.80 V / −40 °C; `osc_subth` ss / 1.62 V / −40 °C, ss /
  1.80 V / −40 °C, sf / 1.62 V / −40 °C, sf / 1.80 V / −40 °C, sf / 1.98 V /
  −40 °C; `osc_wire` sf / 1.98 V / −40 °C.
- **Fallback bank** (`osc_hd`, `osc_nmos`, `osc_pmos`) fails on the `osc_nmos`
  tt / 1.80 V / −40 °C cell, so the fallback does not rescue the row.
- Disclosed in the record, not relaxed: some of the seven may be
  window-too-short rather than dead; the grid run did not separate the two.

**Post-layout (extracted) side**, from
`sim/pex/records/2026-11-11-grade-extracted-values.json` and
`sim/pex/records/2026-11-20-grade-extracted-values-osc_subth-dev2493.json`:
`osc_hd`, `osc_nmos`, `osc_pmos` and `osc_wire` meet the row-1 "oscillates"
criterion (≥ 9 rising edges per cell, counted over each request's own
observation window — 300 ns for `osc_hd`, 800 ns for `osc_nmos`, 2.5 µs for
`osc_pmos` and `osc_wire`) at **45 of 45 cells each**. The extracted
`osc_subth` starts on the net-split-fixed extractor (klayout-tools#5311): its
2026-11-20 dev2493 report
(`sim/pex/records/2026-11-20-osc_subth-dev2493.pex.report.json`) has status
`pass` with 45/45 cells compared, and in the 2 ms window **40 of 45** extracted
cells meet the nine-edge minimum. The five below (ss and sf corners at −40 °C,
where the schematic leg is marginal too) are the remaining §1 failures on the
extracted side. The extracted `osc_wire` is not a like-for-like netlist. See
`sim/pex/README.md`. The extracted side therefore does not close this row
either. The 2026-11-22 frequency pass (issue #282,
`sim/pex/records/2026-11-22-grade-extracted-frequencies.json`) confirms this on
measured frequencies: 220 of 225 extracted cells resolve, the same five
`osc_subth` ss/sf −40 °C cells do not.

**Stretch** (a second oscillator on a second standard-cell library): **not
recorded** — no such oscillator exists in `design/osc_bank/` and no record
grades it.

---

## Spec §2 — Process discrimination

**Verdict: five-corner target FAIL (8 of 9 (V,T) cells identified); slow/fast
fallback PASS (9 of 9).** Recorded in
`sim/solve/records/2026-11-05-rows1-4.md`. This is a **split verdict** and is
rendered as such: the row is not a plain failure and it is not a pass.

- **Binding cell for the target failure**: 1.98 V / 27 °C — one fs→tt
  misclassification in 2000 draws (**SIMULATED**, seed 20261105, post-processing
  of the committed grid and mismatch-MC reports by `sim/solve/solve.py`).
- The three −40 °C (V,T) cells are graded on a **reduced bank** (3–4
  oscillators) because of the §1 missing cells above; the other six use all
  five.

### Sensitivity matrix and its conditioning (shown before any estimate is discussed)

Per `CLAUDE.md`, the matrix and its conditioning are stated before the §3/§4
estimate rows. Recorded in
`sim/sensitivity/records/2026-11-05-grid-sensitivity-partial.md`
(**SIMULATED**, schematic-level; testbenches `sim/sensitivity/osc/`; columns
scaled by box half-range V × 0.18, T × 82.5, Pn/Pp = corner extent ±1):

| Quantity | Recorded value |
|---|---|
| (V,T) cells where the full 5×4 absolute matrix forms | **5 of 9** |
| (V,T) cells where the 4×4 ratio-only matrix forms | **5 of 9** |
| Absolute-matrix condition number κ | **27.8 to 67.9** |
| Ratio-only κ | **19.8 to 67.9** |
| Rank | **4 / 4** in every formed cell |

The four (V,T) cells that cannot be formed are the three −40 °C cells and
1.80 V / 27 °C — exactly the cells with oscillators missing from §1; they are
never interpolated. The record also resolves the spec's open sf/fs question from
a local single-corner DC operating-point probe (`probe_skew.sh`, tt/sf/fs,
27 °C, |Vgs| = |Vds| = 0.9 V): **sf = NMOS-fast / PMOS-slow, fs = NMOS-slow /
PMOS-fast.**

Disclosed in the same record, not relaxed: `osc_subth` has **fewer than 100
counts** in the default 2^10-at-10 MHz gate in 10 cells (as low as 0.77 counts
at ss / 1.98 V / −40 °C), so counter quantization dominates there; and the
mismatch Monte Carlo the discrimination margin needs was **not** run in that
record (77 spot-instance interruptions), so no Q1 verdict is proposed in it.

### Mismatch-Monte-Carlo yield (T1 item 6, `6.analog`)

Recorded in `sim/solve/mc/yield-sized-bank.json` (`status = fail`, the
`6.analog` citation), narrated in
`sim/solve/mc/RECORD-2026-11-06-item6-sized-bank.md`. **SIMULATED**,
`mismatch_scale = 1` (`mc_mm_switch=1`), ngspice-46 on the batch fleet,
testbenches `sim/sensitivity/osc/`; graded with `klt yield` 0.9.1; 95 %
Clopper-Pearson intervals:

| Measurement | Cell | n | Empirical yield [95 % CI] | Sample-size verdict |
|---|---|---|---|---|
| §2 margin, true tt | 1.98 V / 27 °C | 210 | 0.057 [0.030, 0.098] | insufficient (needs 2070) |
| §2 margin, true ff | 1.98 V / 27 °C | 210 | 0.000 [0.000, 0.017] | sufficient (183) |
| §2 margin, true ss | 1.98 V / 27 °C | 208 (2 errored) | 1.000 [0.982, 1.000] | insufficient (183; 368 for the target half-width) |
| §2 margin, true sf | 1.98 V / 27 °C | 210 | 1.000 [0.983, 1.000] | insufficient (183; 368 for the target half-width) |
| §2 margin, true fs | 1.98 V / 27 °C | 210 | 0.181 [0.131, 0.240] | insufficient (needs 5694) |

As the record states: spec rows 2 (tt, ff, fs), 3 and 4 fail the ratified
limits; **none is a pass**. The `osc_subth` σ(ln f) = 0.27 remains
**UNVALIDATED** and dominates every solve it enters
(`sim/solve/records/2026-11-05-rows1-4.md`).

**Stretch** (continuous NMOS/PMOS skew as values): **not recorded**. No record
grades it, and per `CLAUDE.md` the stretch does not drive the bank architecture
before the target closes.

---

## Spec §3 — Supply estimate

**Verdict: target FAIL (±20 mV), fallback FAIL (±50 mV).** Recorded in
`sim/solve/records/2026-11-05-rows1-4.md`.

- **Recorded worst-case graded error: p99 |ΔV| = 62 mV**, binding cell
  **tt / 1.62 V / −40 °C** (**SIMULATED**; post-processing of the committed grid
  and MC reports by `sim/solve/solve.py`; the bank at −40 °C is reduced per §1).
  This is the failure the grader recorded against the row's limits, not a quoted
  accuracy for the block.
- Yield half, `sim/solve/mc/yield-sized-bank.json`: at tt / 1.62 V / −40 °C,
  n = 30, empirical yield 0.200 [0.077, 0.386], verdict **insufficient** (needs
  6147 draws). The record states the shortfall rather than imputing it; σ is not
  pooled across cells.
- Disclosed, not relaxed: only the 1.80 V cells are held out — the 1.62 V and
  1.98 V cells are in-sample (noise-only). Grading is on the 3×3 (V,T) grid
  points only; no off-grid truth was simulated, so **no accuracy between grid
  points is quoted** anywhere.
- Conditioning that bears on this row is in §2 above (absolute κ 27.8–67.9,
  rank 4/4, matrix formed in 5 of 9 (V,T) cells).

**Stretch** (±10 mV, and the joint P/V/T solve): **not recorded** — the record
states the row-4 joint V+T solve was not run.

---

## Spec §4 — Temperature estimate

**Verdict: target FAIL (±5 °C), fallback FAIL (±10 °C).** Recorded in
`sim/solve/records/2026-11-05-rows1-4.md`.

- **Recorded worst-case graded error: p99 |ΔT| = 19.0 °C**, binding cell
  **ff / 1.62 V / 27 °C** (**SIMULATED**; one-point calibration at 27 °C /
  1.80 V, V known; tt-model and corner-agnostic; `sim/solve/solve.py`).
- Coverage disclosed in the record: `osc_nmos` is excluded (missing tt cell),
  corners lacking a full four-oscillator surface are not graded, so **29 of 45
  cells are graded**; the tt die is in-sample.
- Yield half, `sim/solve/mc/yield-sized-bank.json`: at ff / 1.62 V / 27 °C,
  n = 210, empirical yield **0.000** [0.000, 0.017], verdict **sufficient**
  (183) — i.e. the row fails its ±5 °C limit *with confidence*, which is the
  one place in that record where the sample size is adequate to the conclusion.
- This estimate is **not** `sky130-temp-por`. Per `spec/target-spec.md` §4 and
  `CLAUDE.md`, the sibling block builds a PTAT/CTAT sensor; this row is an
  oscillator-frequency-derived estimate and nothing here is copied from or
  depends on that sibling.

**Stretch** (±2 °C): **not recorded**.

---

## Spec §7 — Active and idle power

**Verdict: active FAIL at target, fallback and stretch; idle FAIL at target,
fallback and stretch.** Recorded in
`sim/power/records/2026-11-05-power-complete.md` (tables
`sim/power/records/2026-11-05-power-table-complete.json` and
`sim/power/records/2026-11-05-power-grade-complete.json`; also carried in the
`5.analog` envelope `evidence/item5_analog.json`).

**SIMULATED**, oscillator bank only, schematic-level, no layout. Testbenches
under `sim/power/`, run as `klt sim --batch-set` on the batch fleet; ngspice-46,
sky130A. Graded by `sim/power/analyze_power.py`.

| | Target | Fallback | Stretch | Binding cell, recorded value |
|---|---|---|---|---|
| Active (oscillator only) | < 100 µW **FAIL** | < 500 µW **FAIL** | < 20 µW **FAIL** | `osc_wire` / ff / 1.98 V / −40 °C = **1740 µW** |
| Idle (bank sum) | < 1 µW **FAIL** | < 10 µW **FAIL** | < 100 nW **FAIL** | sf / 1.62 V / 27 °C = **490 µW**, SUSPECT (below) |

**Coverage, as the record discloses it:** idle 45 of 45 cells, all five
oscillators at every cell; active **219 of 225** oscillator cells. The six not
graded and never filled: `osc_subth` ss / 1.62 V, ss / 1.80 V, sf / 1.62 V,
sf / 1.80 V, sf / 1.98 V at −40 °C (fewer than 8 rising edges in the window —
the same cells §1 could not resolve) and `osc_wire` sf / 1.62 V / −40 °C
(`timestep too small` transient abort).

**The counter's power is NOT covered** by this row's evidence — there is no
SPICE-level counter netlist. Spec §7 binds "one oscillator running plus
counter"; only the oscillator half is recorded, so the recorded figures are a
**lower bound** on the block's active power. The flow-estimated readout power is
in `characterization/digital.md`, and it is a different basis that cannot be
added to these numbers to form a block figure; this report forms none.

**The idle binding figure is flagged SUSPECT in its own record and is quoted
with that flag.** The 490 µW is dominated by one `osc_nmos` DC operating point
(489 µW at sf / 1.62 V / 27 °C) about 30 000× its tt value and not monotonic in
its V or T neighbours; the record's author judged it a metastable/crowbar `op`
solution rather than leakage and did not investigate further. **The idle verdict
does not depend on it**: `osc_subth`'s ungated ~1 µA bias divider alone gives
1.8 µW at tt / 1.80 V / 27 °C (over the 1 µW target), and the
ff / 1.98 V / 125 °C bank sum is ~53 µW without that point (over the 10 µW
fallback). Treat 490 µW as an upper-bound artifact until a better `op` is shown.

Two further disclosures carried from the record: a bench option
`.options rshunt=1e12` was added on the `osc_nmos` and `osc_wire` benches to
make the gated-off idle `op` converge (a bench option, not a model change;
below the nA-scale idle currents but not zero), and active mean current is taken
over the second half of each transient window, not an integer number of cycles
(error ≤ 1 cycle per window).

**What sets each oscillator's power, and the over-target iteration, are recorded
in `sim/power/records/2026-11-21-active-power-iteration.md`** (issue #280;
SIMULATED, same scope — oscillator only, counter not covered). It decomposes
each oscillator's active power at its binding cell (the wire ring's explicit
31 × 100 fF load explains 77.6 % of its 1740 µW; the residual is slope-driven
overlap current), sweeps the levers one at a time (stage count measured
power-neutral on all four ring families; the capacitor value power-neutral in
the wire ring's RC-dominated regime; resistor length and driver size the real
levers), and carries 45-cell candidate grids: `osc_wire` r004w02 at 447.2 µW
worst-cell (under the fallback everywhere, wire-RC fraction preserved at 0.72)
and `osc_pmos` l10 at 81.7 µW (under the target everywhere). It also grades the
six cells this section lists as not graded — union coverage 225/225 — with the
`osc_wire` sf/1.62 V/−40 °C cell coming from a disclosed relaxed bench
(`reltol`/`gmin`/`method=gear`, #8's precedent) after two `timestep too small`
aborts, and the five cold `osc_subth` cells from ms-scale windows. **No verdict
above changes**: row 7 stays FAIL at every bound for the committed bank; the
sizing changes are [decision 0004](../spec/decisions/0004-oscillator-bank-active-power-sizing.md),
status proposed, with the downstream re-runs listed there. The record's §5 also
states the measured infeasibility of the 100 µW target for the committed bank
composition (`osc_hd`'s power is fixed by the library cell at ~396 µW and
stage-count-invariant).

---

## Spec §8 — Area budget (analog share)

**Verdict: not recorded.** Spec §8 binds the **whole** block (oscillators,
counter and register file, ≤ 0.02 mm² target / ≤ 0.05 mm² fallback / ≤ 0.01 mm²
stretch, all *proposed*). **No committed record carries a whole-block area
verdict**, and this report does not compute one — summing the analog and digital
figures below would be a new figure, not a recorded one.

What *is* recorded, for the analog share only, in `layout/README.md`
(**SIMULATED-flow output**, derived from the committed stream
`layout/osc_bank.gds` by `klt stats --top <cell>` and summed by hand; footprint
= cell bounding box, including port stubs and, for `osc_wire`, the serpentine
band):

| Cell | Footprint (µm) | Footprint (µm²) |
|---|---|---|
| `osc_hd` | 45.5 × 3.2 | 145 |
| `osc_nmos` | 84.8 × 8.8 | 742 |
| `osc_pmos` | 84.8 × 11.3 | 961 |
| `osc_wire` | 83.9 × 146.1 | 12 257 |
| `osc_subth` | 96.4 × 27.1 | 2 613 |
| **Sum of footprints** | | **16 720 µm² = 0.0167 mm²** |

Against the spec §8 whole-block target, the oscillators alone are **84 % of the
target budget and 33 % of the fallback**, before any readout. `layout/README.md`
states verbatim that *"this issue does not pass/fail §8"* — it records the
oscillator share only. None of these figures is DRC- or LVS-checked as an area
claim, and none is measured.

---

## Spec §9 — Signoff (analog share)

**Verdict: target FAIL, fallback FAIL — for the analog share.** Spec §9 binds
the whole block ("DRC + LVS clean, and post-layout re-verification of every row
above"; fallback "DRC + LVS clean"), and **no committed record carries a
whole-block §9 verdict**; this report records only the analog share, whose
recorded components are negative.

**DRC (T1 item 3, `3.analog`) — clean, with disclosure.**
`drc/osc_bank.report.json`: `klt drc --deck sky130` (curated engine) on
`layout/osc_bank.gds`, `klayout-tools==0.9.1`, PDK sky130A — **clean, 0
violations**. `drc/README.md` discloses what that does not mean: the curated
deck leaves 13 stream layers without rules and skips a long rule list, and the
**PDK-native deck disagrees on the same stream, reporting 562 violations**
(`ct.4` ×220, `li.5` ×342) in the hand-drawn cells. That cross-check is not
cited as evidence. DRC covers drawn geometry only.

**LVS (T1 item 4) — `4.analog` is NOT cited and stays `unmet`.** Per
`lvs/README.md`: `osc_nmos`, `osc_pmos` and `osc_hd` match against their item-1
netlists (`osc_hd` with a `topology.flattened` warning), but `osc_wire` and
`osc_subth` match only against **reduced** references — `osc_wire`'s 31 ideal
100 fF shunt caps are dropped and each wire resistor shorted; `osc_subth`'s
reference swaps the item-1 ideal 300 kΩ/1.5 MΩ for PDK `res_high_po_0p35`
devices. Against the unreduced item-1 netlists `osc_wire` cannot match, because
no capacitor or wire resistor is drawn (`layout/README.md`). So the fallback
("DRC + LVS clean") is **not** met for this partition.

Also disclosed, because `manifests/design-evidence-tiers.md` item 4 says an
`"unchecked"` body verification "is not `verified`": each report's
`body_verification.status` is **`unchecked`** for `osc_hd`, `osc_nmos`,
`osc_pmos` and `osc_wire` (`lvs/osc_hd.report.json`,
`lvs/osc_nmos.report.json`, `lvs/osc_pmos.report.json`,
`lvs/osc_wire.report.json`) and `verified` only for `osc_subth`
(`lvs/osc_subth.report.json`). So on four of the five cells the compare did not
verify the body ties at all, independently of the reduced-reference problem
above. `klt lvs` also does not compare resistor L/W
(`device.geometry_not_compared`), so the `osc_subth` divider lengths agree by a
hand check against `klt extract`, not by LVS.

**Post-layout re-verification (T1 item 7) — `7.analog` is NOT met**
(`unmet` / `check_failed` in `manifests/sky130-process-monitor.signoff.json`).
Per `sim/pex/README.md`: the extracted side meets the §1 "oscillates" criterion
for four oscillators at 45/45 cells and for `osc_subth` at 40/45 (2026-11-20
dev2493 grade), and **spec rows 2–4 are now re-graded on measured frequencies**
(2026-11-22 frequency pass, issue #282:
`sim/pex/records/2026-11-22-grade-extracted-frequencies.json`, **SIMULATED**,
`klt pex --measure-command` reports under `sim/pex/records/`): the same
`f_osc = (n-1)/(t_last - t_first)` estimator as the schematic record, measured
per corner on the schematic and the extracted netlist of all five oscillators
over the 45-cell box, with both legs graded by the same `sim/solve/solve.py`
replay (seed 20261105, 2000 row-2 draws; the pooled mismatch model is
schematic-side MC data applied unchanged to both legs, disclosed in the
record). On the **extracted leg**, row 2 identifies 9/9 cells (the schematic
leg reproduces the 2026-11-05 result: 8/9, the same `1.98 V/27 °C` `fs->tt`
error), row 3's worst p99 voltage error is 30 mV at 125 °C ff 1.80 V
(fallback PASS, target FAIL) and row 4's worst p99 temperature error is
31.0 °C at ff 1.80 V 125 C (FAIL) — rows 3 and 4 stay FAIL at the target
tiers on both legs, and the `osc_wire` extraction is not like-for-like. The
§2 ratio coordinates shift by a median −7.6 % (`osc_nmos`), −11.2 %
(`osc_pmos`), −1.7 % (`osc_wire`) and −26.3 % (`osc_subth`). All 225
oscillator/corner pairs per leg are accounted for with unresolved cells as
null plus cause (the two known schematic cold cells and `osc_subth`'s ss/sf
−40 °C cells). The item-7 citation for `osc_subth`
(`sim/pex/records/2026-11-20-osc_subth-dev2493.pex.report.json`) grades `met`;
the overall `unmet` / `check_failed` verdict is still solely the 2026-11-10
`osc_nmos` and `osc_wire` count reports at status `error` — one schematic-side
cold cell each (tracked in #264; the 2026-11-22 frequency reports hit the same
two cells on the schematic leg and record them as null with cause, and which
citations close item 7 stays #264's decision).

**Body bias, stated because item 7 requires the claimant to state it.**
`manifests/design-evidence-tiers.md` item 7 says `klt signoff` surfaces a
citation's `body_bias` verbatim but does **not** grade on it, so a claim citing
item 7 must read the field and say whether its post-layout numbers came from a
properly-biased netlist. They did: `sim/pex/README.md` records
`body_bias.status = biased` (0 unbiased devices) **for all five extractions**,
and the four committed reports confirm it individually. The extraction model is
disclosed in the same place and is a lumped RC one (net-to-ground
area/perimeter, vertical-overlap coupling, one lumped series R per net as a
star, quasi-static; **no lateral coupling**, because no `--critical-net` was
named).

Two further disclosures from `sim/pex/README.md`, carried rather than left out:
the `klt pex` report status is **`error` for `osc_nmos` and `osc_wire`** and
`pass` for `osc_hd` and `osc_pmos` — the two errors are *schematic*-side
non-convergence at one cell each (`osc_nmos` tt / 1.80 V / −40 °C and
`osc_wire` sf / 1.98 V / −40 °C, `timestep_too_small`), so those two
oscillators have a schematic-vs-extracted delta at 44 of 45 cells rather than
45; the **extracted** leg converged at both, which is why the extracted-side
row-1 count above is 45 of 45. The 2026-11-10 reported quantity is a
**quantised frequency proxy** (rising crossings in a fixed window), which is
why rows 2–4 could not be re-graded from those reports; the 2026-11-22
frequency pass superseded the proxy with the measured `f_osc` itself (the
proxy is retained and labelled as such wherever the historical records are
discussed). The §9 target's "post-layout re-verification of every row above"
is still not met on this partition: rows 3 and 4 fail on the extracted
frequencies.

---

## What this report does not establish

- **Nothing here is measured.** Every figure is simulated or a
  simulated-flow/tool output, at the corner and testbench named beside it.
- **No estimate accuracy is quoted.** The §3 and §4 numbers are recorded graded
  failures against those rows' limits, on the 3×3 (V,T) grid points only; no
  off-grid truth was simulated and no between-grid accuracy exists.
- **No whole-block verdict** is formed for spec §8 or §9; each is recorded as a
  partition share, and §8 has no recorded verdict at all.
- **No new simulation, extraction or Monte Carlo was run for this report.** It
  is an aggregation of already-committed records; the T1 item-8 checklist is
  satisfied by a hand-assembled record because no `klt` aggregation verb exists
  (`manifests/design-evidence-tiers.md` item 8; upstream tracker
  klayout-tools#309).
- Open proposals touching these rows are cited as proposals, not resolutions:
  the `spec/decisions/` records that are `draft` do not grade any row here.

**Reproduce the per-row evidence**: the `README.md` "Reproduce" table names the
cheapest command for each result class cited above (commands 1, 3, 4, 6, 7 and
8). The citation-existence check for this report is
`characterization/test_citations.py`, run from `npm test`.
