# Characterization report — digital partition (T1 item 8, `8.digital`)

**SIMULATED. Every figure below is simulated or a simulated-flow / static-timing
tool output, labelled with its corner and its testbench, and copied from a
committed record — nothing here is measured, and nothing will be until silicon
exists.** This report aggregates; it grades nothing anew. Each verdict is the
verdict the cited record already carries, and no spec bound, limit or recorded
verdict is edited, relaxed or re-derived here. Where a row has no recorded
result it is listed as **not recorded** — never as a pass and never as a fail.

**Numbering convention.** Rows are indexed by **`spec/target-spec.md` section**
("spec §N"), not by T1 checklist item. The two schemes collide: T1 item 5 is
*not* spec §5, T1 item 6 (statistical evidence) is *not* spec §6 (conversion
time), and T1 item 8 (this report) is *not* spec §8 (area). Where a T1 item is
named it is written "T1 item N".

**Partition.** Digital is the enable/select logic, the counter-based frequency
readout against an external reference clock, and the readout interface, per
`manifests/sky130-process-monitor.json`'s `partition_boundary`. The two readout
rows are ratified as the digital subset in `spec/digital-rows.json` (spec §5
Readout, spec §6 Conversion time). The analog rows are in
`characterization/analog.md`. Spec §8 (area) and spec §9 (signoff) bind the
**whole** block, so each appears in **both** reports stating only that
partition's share; neither report claims a whole-block verdict for them.

**Status of this report: `fail`** (`evidence/item8_digital.json`). The counter's
functional behaviour passes every committed check, but the corner-matched static
timing records a **FAIL in all three liberty corners** — the counter does not
cover `osc_hd` in any corner — and spec §6 is now **recorded, and it records
misses**: the target is met only at the nominal cell under the default gate
(0.5153 ms), every longer gate setting exceeds it (up to 10.8118 ms at the
slowest-`osc_subth` cell, past even the fallback), and under the default gate at
that cell the `osc_subth` read does not complete at all. A `pass` would
overclaim on both counts.

Beyond the spec rows, the T1 item-8 checklist asks a digital partition for
**Fmax, area and power across the corner set**, not just functional pass/fail.
Those three are in "Fmax, area and power" below, each with the corner set
actually covered and the gaps in that coverage stated.

---

## Row summary

| Spec row | Target | Fallback | Stretch | Binding corner | Record |
|---|---|---|---|---|---|
| §5 Readout — counter function | **PASS** | — | — | RTL + SDF-annotated gate level, typ | `verification/readout/functional-verification.report.json` |
| §5 Readout — counter timing vs. the selected oscillator | **FAIL** | — | — | `osc_hd`, all three liberty corners (worst ss_100C_1v60) | `sta/readout.osc-corner.sta.report.json` |
| §5 Readout — reference-clock accuracy requirement | **not recorded** | **not recorded** | — | — | requirement on an input; the block does not generate it |
| §6 Conversion time | **FAIL** (0.5153 ms at nominal/default; every longer gate exceeds 1 ms) | **FAIL** (10.8118 ms at sf/1.98 V/−40 °C, k = 14 whole bank) | **FAIL** (best 0.5153 ms) | sf, 1.98 V, −40 °C (`osc_subth`, 945.75 µs; default-gate read does not complete) | `verification/readout/conversion-time.json` |
| §8 Area (digital share) | **not recorded** | **not recorded** | **not recorded** | — | `layout/README.md` |
| §9 Signoff (digital share) | **not recorded** (whole-block) | components recorded below | — | — | `drc/README.md`, `lvs/README.md`, `verification/README.md` |

---

## Spec §5 — Readout

Spec §5 specifies a 24-bit saturating counter, one oscillator selected at a
time, a programmable gate of 2^k reference-clock cycles (default 2^10 =
102.4 µs at 10 MHz), a reference clock that is **an input to the block** (target
10 MHz, ±100 ppm; fallback ±1000 ppm), and raw counts plus a status flag as the
output. It decomposes into three separately-evidenced parts, below.

### §5a — Counter function: PASS

**Verdict: PASS.** Recorded in
`verification/readout/functional-verification.report.json` (the `5.digital`
citation, with `sta/readout.sta.report.json`): `status: "pass"`, **10 of 10
tests**, 0 failed, 0 skipped. **SIMULATED** RTL simulation — Icarus 13.0,
cocotb 2.1.0, testbench `verification/readout/test_readout.py`, random seed 1.
The ten tests are `reset_values`, `count_correctness`, `select_switching`,
`busy_done_sequencing`, `cal_readback`, `reset_mid_gate`,
`saturation_overflow`, `full_read_cycle_count`, `k0_phase_sweep` and
`conversion_time_surfaces`, so gate/count correctness, saturation and select —
exactly what `spec/digital-rows.json` names as this row's testbench — are each
covered by a named passing test.

**Post-layout re-verification (T1 item 7, `7.digital`, graded `met`):**
`verification/readout/functional-verification-sdf.report.json` — `status:
"pass"`, **9 of 9 tests**, SDF-annotated against
`layout/readout/out_sdf/readout_route.sdf` at the **typ** corner. The annotation
is **partial** and its own report says so: Icarus implements IOPATH/INTERCONNECT
annotation but not SDF TIMINGCHECK, so **323 TIMINGCHECK sections are dropped**
and `$setup`/`$hold`/`$width` run against the cell library's placeholder timing
rather than the characterised limits; a further 164 zero-delay INTERCONNECT
entries are removed before annotation (3 alias-port, 160 bus-port-source, 1
physical-only destination). The limits on this run are in
`verification/README.md`. Only the typ corner is annotated — this is not a
corner set.

### §5b — Counter timing against the selected oscillator: FAIL

**Verdict: FAIL in all three liberty corners.** Recorded in
`sta/readout.osc-corner.sta.report.json`, narrated in `sta/README.md`.

**SIMULATED / static timing only.** `klt sta` at `klayout-tools==0.9.1`, 15
requests written and run by `sta/run_osc_sta.py`; geometry
`layout/readout/out/readout.def` (routed, no SPEF); oscillator periods taken
from the committed frequency surfaces (`sim/sensitivity/records/reports/`) at
the grid cell nearest each liberty corner — ss_100C_1v60 ← ss / 1.62 V / 125 °C,
tt_025C_1v80 ← tt / 1.80 V / 27 °C, ff_n40C_1v95 ← ff / 1.98 V / −40 °C. No
assumed periods. Completeness is `complete` in all 15 runs.

| Corner | Oscillator | Period (ns) | Setup slack (ns) | Hold slack (ns) |
|---|---|---|---|---|
| ss_100C_1v60 | `osc_hd` | 2.925 | **−2.921** | 0.678 |
| | `osc_nmos` | 9.075 | 3.229 | 0.678 |
| | `osc_pmos` | 22.550 | 16.704 | 0.678 |
| | `osc_wire` | 19.486 | 13.640 | 0.678 |
| | `osc_subth` | 342.467 | 77.223 | 0.678 |
| tt_025C_1v80 | `osc_hd` | 1.560 | **−1.227** | 0.331 |
| | `osc_nmos` | 4.505 | 1.718 | 0.331 |
| | `osc_pmos` | 12.600 | 9.813 | 0.331 |
| | `osc_wire` | 13.215 | 10.429 | 0.331 |
| | `osc_subth` | 351.994 | 78.580 | 0.331 |
| ff_n40C_1v95 | `osc_hd` | 0.980 | **−0.724** | 0.204 |
| | `osc_nmos` | 2.628 | 0.923 | 0.204 |
| | `osc_pmos` | 7.408 | 5.704 | 0.204 |
| | `osc_wire` | 9.027 | 7.323 | 0.204 |
| | `osc_subth` | 293.293 | 79.115 | 0.204 |

**Recorded verdict, quoted: "the counter does not cover `osc_hd` in any
corner"** — 1.74× short at ff, 2.0× at ss. The other four oscillators close
everywhere. Setup slack at the `osc_hd` period is negative in all three
corners; hold slack is positive everywhere.

This bears directly on spec §5's "one oscillator selected at a time, counted
against the reference clock": the fastest oscillator in the ratified
five-oscillator bank cannot be counted at the corner-matched frequency.
`spec/decisions/0003-counter-max-input-frequency.md` proposes a resolution and
is cited here **as an open proposal only** — its `Status` is
*draft / proposed (not accepted)*, it resolves nothing, and neither this report
nor the PR that adds it ratifies it. RTL and spec are unchanged.

### §5c — Reference-clock accuracy requirement: not recorded

**Verdict: not recorded.** Spec §5 requires the reference clock at 10 MHz with
±100 ppm (fallback ±1000 ppm), and states explicitly that it is **an input to
the block; no on-die reference clock**. The block neither generates nor varies
it (`verification/readout/not-statistical.json`), so there is nothing on-die to
measure and no committed record grades the row. Every timing and functional run
above constrains `clk_ref` at exactly 100 ns (10 MHz) with an **ideal** clock,
which assumes the requirement rather than testing it.

### §5 reference-clock-domain static timing (supporting, `5.digital`)

`sta/readout.sta.report.json` — `klt sta` at `klayout-tools==0.9.1`, geometry
`layout/readout/out/readout.def`, no SPEF, `clk_ref` at 100 ns, ideal clock.
Every corner is `constrained`:

| Corner | Setup slack (ns) | Hold slack (ns) |
|---|---|---|
| ss_100C_1v60 | 95.39 | 0.678 |
| tt_025C_1v80 | 97.89 | 0.331 |
| ff_n40C_1v95 | 98.71 | 0.204 |

**What that `constrained` verdict does not cover, carried from `sta/README.md`
rather than left out:**

1. **Corner box.** The pinned `sky130_fd_sc_hd` liberty set has no 125 °C file
   and no 1.62 V or 1.98 V point. These three corners are the nearest installed
   files; the spec box extremes (125 °C, 1.62 V, 1.98 V) are **not timed** and
   box coverage is not claimed.
2. **`constraint_completeness` is `incomplete` in every corner** of this run:
   the SDC defines only the reference clock, so the **29 `u_cnt` registers
   clocked by `osc[4:0]` are reported unclocked** and **57 endpoints** (outputs,
   no I/O delays) unconstrained. The `constrained` verdict applies to the
   reference-clock domain only. The oscillator-clocked counter is timed in the
   corner-matched runs of §5b above.
3. **Clocks are ideal** (no propagation through the select mux), there is **no
   SPEF**, the oscillator frequencies are schematic-level, the liberty corners
   differ from the grid cells by up to 25 °C / 0.03 V, and `klt sta` reports **no
   minimum-pulse-width check**, so that edge case is unassessed. Tool gaps filed
   upstream: klayout-tools#5240, #5241.
4. `sta/readout.sdc` is a reference copy of the constraint; `klt sta` does not
   read it.

---

## Spec §6 — Conversion time

**Verdict: recorded, FAIL against target and fallback and stretch** (the target
is met at exactly one of the six recorded cell × gate-setting combinations).
Recorded in `verification/readout/conversion-time.json`, written by the bench
itself (`verification/readout/test_readout.py::conversion_time_surfaces`);
the gate-level leg is `verification/readout/conversion-time-sdf.json`.
**SIMULATED** — Icarus 13.0, cocotb 2.1.0, RTL pre-layout plus one
SDF-annotated gate-level leg, random seed 1, reference clock exactly 10 MHz.
This section quotes the record's verdicts; it derives none.

Spec §6 binds "< 1 ms for a full read of all oscillators" (target), "< 10 ms"
(fallback) and "< 100 µs" (stretch), at the target reference frequency with
**all oscillator frequencies from the surfaces**. The bench therefore drives
the five oscillators at their committed surface periods — nominal cell
(tt, 1.80 V, 27 °C) and the cell with the slowest `osc_subth`
(sf, 1.98 V, −40 °C; 1057.37 Hz, T = 945.75 µs), each period naming its source
report and grid cell in the record (`osc_wire` at the sf cell is the
relaxed-solver probe value, 84.986 MHz, carrying its recorded bias caveat) —
and reads the bank at the three gate settings the gate-sizing record
(`sim/sensitivity/records/2026-11-14-osc-subth-gate-sizing.md`) tabulates:
the spec default 2^10 on all five, 2^14 on all five, and 2^14 on `osc_subth`
only. No gate is picked and no RTL default is changed by the record.

Full-read conversion time, first CTRL start write to the fifth `STATUS.done`
(the record also carries per-oscillator times, counts unasserted, phase
evidence and host overhead):

| Cell / gate setting | Full read | §6 verdict (quoted) |
|---|---|---|
| nominal, 2^10 × 5 (default) | 5153 cycles = **0.5153 ms** | target **PASS**, fallback PASS, stretch FAIL |
| nominal, 2^14 × 5 | 81 954 cycles = 8.1954 ms | target FAIL, fallback PASS, stretch FAIL |
| nominal, 2^14 `osc_subth` only | 20 514 cycles = 2.0514 ms | target FAIL, fallback PASS, stretch FAIL |
| sf 1.98 V −40 °C, 2^10 × 5 (default) | **did not complete** (`osc_subth`) | no time, no grade |
| sf, 2^14 × 5 | 108 118 cycles = **10.8118 ms** | target FAIL, **fallback FAIL**, stretch FAIL |
| sf, 2^14 `osc_subth` only | 46 678 cycles = 4.6678 ms | target FAIL, fallback PASS, stretch FAIL |

Reads that do not complete are recorded as such, with gate and period, never
asserted away, lengthened or dropped:

- **sf cell, default gate, `osc_subth`: the read hangs.** The gate window
  (1024 clk_ref cycles = 102.4 µs) is shorter than one oscillator period
  (945.75 µs; window/period 0.108), and at the bench's recorded deterministic
  phase (first `osc_subth` rising edge half a period after the gate rise) no
  rising edge lands inside the window — the condition under which
  `test_readout.py::k0_phase_sweep` established busy never clears (issue #82;
  the RTL documents the minimum-k rule 2^k·T_ref ≥ T_osc). The record carries
  the phase evidence; completion at this cell and gate is phase-dependent, so
  **no full-read time exists at the default gate** and no §6 bound is graded
  for it. This is the recorded input to the gate / readout design iteration
  and to draft `spec/decisions/0003-counter-max-input-frequency.md`, which
  remains draft and resolves nothing.
- **Gate level (SDF typ, nominal cell only): `osc_hd` reads did not complete
  at any of the three gate settings**, so no gate-level §6 time is recorded at
  all. `osc_hd`'s surface frequency at nominal (641.0 MHz) exceeds what the
  §5b STA already fails (counter Fmax 358.9 MHz at tt); with SDF delays
  annotated the read never completes — the timing FAIL made visible in
  simulation, not a new verdict. The record states this per read and cites
  `sta/readout.osc-corner.sta.report.json` rather than silently substituting
  a slower period; the surface period was driven as-is. `conversion-time-sdf.json`
  carries the leg's limits: typ corner only, partial annotation (323
  TIMINGCHECK sections dropped by Icarus, so neither completion nor
  non-completion is timing-certified), ideal bench-driven `osc` inputs.

What the record adds beyond the planning figure: the 5 × 102.4 µs ≈ 0.5 ms
arithmetic in `spec/target-spec.md` §6 (quoted there as unverified planning)
is confirmed only at the nominal cell — 0.5153 ms including 33 cycles of
handshake and host overhead. At the sf cell the `osc_subth` handshake alone
(the oscillator-domain synchroniser at a 945.75 µs period) costs more than the
gate: the k = 14 `osc_subth` read is 42 561 cycles (4.2561 ms) against a
16 384-cycle gate, which is why the whole-bank k = 14 read (10.8118 ms)
exceeds even the 10 ms fallback while the `osc_subth`-only-k = 14 reading
stays under it (4.6678 ms).

- `verification/readout/not-statistical.json` still classifies the row
  `deterministic-cycle-count` (the `6.digital` `not_applicable` citation):
  conversion time is an exact arithmetic result of the design with no spread
  to estimate. That classification is unchanged; this record now supplies the
  measured figures it lacked.

---

## Fmax, area and power (T1 item-8 digital requirement)

T1 item 8 asks a digital partition for Fmax, area and power **across the corner
set**. All three figures below are **SIMULATED / simulated-flow outputs** from
committed records, and the corner coverage each one actually has is stated with
it. None is a spec verdict: spec §8 is addressed below, spec §7 (power) is an
analog-partition row whose evidence explicitly excludes the counter, and no spec
row sets an Fmax bound on this block.

### Fmax

| Figure | Value | Corner / basis | Record |
|---|---|---|---|
| Counter Fmax | **171.1 MHz** | ss_100C_1v60 | `sta/readout.osc-corner.sta.report.json` |
| Counter Fmax | **358.9 MHz** | tt_025C_1v80 | same |
| Counter Fmax | **586.8 MHz** | ff_n40C_1v95 | same |
| Flow-reported Fmax | **375.404 MHz** | nominal corner, OpenROAD after route | `layout/readout/report.json` |

The three corner-matched figures are the counter's maximum input frequency as
`klt sta` reports it at each liberty corner (`klayout-tools==0.9.1`, routed DEF,
no SPEF, ideal clocks). Read against §5b: the same report records
`osc_hd`'s own frequency at those corners as **341.9 / 641.0 / 1020.3 MHz**
(`f_osc_hz`, periods 2.925 / 1.560 / 0.980 ns), each above that corner's counter
Fmax, which is why that oscillator fails everywhere while the other four close. The
flow-reported 375.404 MHz is a single nominal-corner number from the P&R run and
is **not** corner-swept; the corner set for Fmax is the three liberty corners
only, and the spec box extremes (125 °C, 1.62 V, 1.98 V) are not timed.

### Area

From `layout/readout/report.json` and `layout/README.md` — the routed `readout`
block from `klt place-and-route` (OpenROAD, `sky130_fd_sc_hd`,
`power.preset: sky130hd`, 40 % target utilization, `clk_ref` at 100 ns,
`target_stage: route`, seed 1), regenerated from the gate-level netlist
`synth/readout/readout.gl.v`:

| Figure | Value |
|---|---|
| Die area | **39 970 µm² = 0.040 mm²** |
| Core area | **36 434.9 µm²** |
| Utilization | **42.943 %** |
| Components | **5 341** (468 tapcells, 3 620 fillers) |
| Routed wirelength | **39 612 µm** |
| Synthesis cell area | **14 734 µm²** |

Area is a geometric result of one P&R run, not a corner-dependent quantity, so
there is no corner set to sweep. The die includes the floorplan margin and the
40 % utilization headroom. `layout/README.md` states that this is a
simulated-flow output, **not DRC-, LVS- or extraction-checked at the time it was
written**, and that spec §8 is *not judged* by it — see §8 below.

### Power

| Figure | Value | Basis | Record |
|---|---|---|---|
| Flow-estimated total power | **0.2688 mW = 268.8 µW** | nominal interconnect corner | `layout/readout/report.json` |

**This is a flow estimate, and its own record says on what basis.**
`power_basis.activity_source` is `engine_default` (no switching activity was
supplied, so the engine's default activity is assumed), `power_basis.activity`
and `power_basis.duty` are both null, and `power_basis.parasitics` is
`estimate_only` — there is no SPEF-backed power run (`spef_sta` is null).
`interconnect_corner` is `nom`. **It is a single-corner figure: there is no
per-corner power in any committed record**, so the corner set for power is one
point, and power across the corner set is **not recorded**.

It is also **not** a spec §7 result and must not be read as one. Spec §7 binds
"one oscillator running plus counter"; the §7 evidence
(`sim/power/records/2026-11-05-power-complete.md`) is a SPICE oscillator-bank
run that states *"COUNTER POWER IS NOT COVERED (no SPICE-level counter
netlist)"*. This 268.8 µW is a different basis (gate-level flow estimate with
default activity) and **cannot be added to those figures** to form a block
power. Neither report forms one.

### Static-timing coverage across the P&R corner set (supporting)

`layout/readout/report.json` sweeps **16 corners**, all `timing_status:
constrained`, with 0 setup and 0 hold violations, 0 route-DRC and 0 antenna
violations as counted by the flow:

- Worst setup slack across the 16: **82.0592 ns** at `ss_n40C_1v28` (against the
  100 ns `clk_ref` period).
- Worst hold slack across the 16: **0.22313 ns** at `ff_n40C_1v95`.
- Nominal-corner clock skew **0.02815 ns**.
- Corners swept: `ff_100C_1v65`, `ff_100C_1v95`, `ff_n40C_1v56`,
  `ff_n40C_1v65`, `ff_n40C_1v76`, `ff_n40C_1v95`, `ss_100C_1v40`,
  `ss_100C_1v60`, `ss_n40C_1v28`, `ss_n40C_1v35`, `ss_n40C_1v40`,
  `ss_n40C_1v44`, `ss_n40C_1v60`, `ss_n40C_1v76`, `tt_025C_1v80`,
  `tt_100C_1v80`.

This sweep constrains the **reference-clock domain only**, like
`sta/readout.sta.report.json`: the oscillator-clocked counter registers are not
in it. The flow's own `coverage` block records that no metal-density fill is
inserted and density rules are not evaluated, so a zero route-DRC count does not
imply density compliance.

---

## Spec §8 — Area budget (digital share)

**Verdict: not recorded.** Spec §8 binds the **whole** block (oscillators,
counter and register file, ≤ 0.02 mm² target / ≤ 0.05 mm² fallback / ≤ 0.01 mm²
stretch, all *proposed*). **No committed record carries a whole-block area
verdict**, and this report does not compute one — adding the readout die area to
the analog oscillator-footprint sum in `characterization/analog.md` would be a
new figure, not a recorded one, and the two are not measured on a comparable
basis (one is a routed die including floorplan margin and utilization headroom,
the other a sum of cell bounding boxes).

The recorded digital share is the area block above: die **39 970 µm² =
0.040 mm²**, core 36 434.9 µm², 42.943 % utilization, synthesis cell area
14 734 µm². `layout/README.md` states verbatim that *"spec §8 (≤ 0.02 mm²,
proposed) is not judged here"*. The recorded die figure is numerically larger
than the §8 target figure, but no committed record grades the row and this
report does not either: a §8 judgement would have to account for the floorplan
margin and the 40 % utilization headroom in that die number, and for the
register file, and nothing recorded does that. The row stays **not recorded**.

---

## Spec §9 — Signoff (digital share)

**Verdict: no whole-block verdict is recorded.** Spec §9 binds the whole block
("DRC + LVS clean, and post-layout re-verification of every row above";
fallback "DRC + LVS clean"), and **no committed record carries a whole-block §9
verdict**. The digital partition's own components are each recorded, and are
listed here as components — not as a §9 pass:

- **DRC (T1 item 3, `3.digital`, graded `met`)** — `drc/readout.report.json`:
  `klt drc --deck sky130` on `layout/readout/out/readout.gds`,
  `klayout-tools==0.9.1`, PDK sky130A — **clean, 0 violations**.
  `drc/README.md` discloses that the curated deck leaves 18 stream layers
  without rules and skips a rule list, and that the **PDK-native deck run on the
  same readout stream ends `coverage_unknown` (exit 4), which is not a clean
  verdict either**. DRC covers drawn geometry only.
- **LVS (T1 item 4, `4.digital`, graded `met`)** — `lvs/readout.report.json`:
  layout side `readout.gate.spice` from `klt extract --abstract-cells
  'sky130_fd_sc_hd__*' --def-net-names`, reference the **as-built**
  `layout/readout/out/readout.v` (`gate-level-verilog`), **match**, with
  `power_connectivity` **match**. Counts from the report: nets 1290 layout /
  1270 reference / 1784 matched, pins 1255 / 63 / 1767, and **0 devices on
  either side** — the standard cells are black boxes in this compare, per
  `lvs/README.md`, so no device-level topology was compared at all.
  `error_count` is 0 with `mismatch_count` 5 (the report's `status` is still
  `match`). Disclosed because `manifests/design-evidence-tiers.md` item 4 says
  an `"unchecked"` body verification "is not `verified`":
  `body_verification.status` on this report is **`unchecked`**, i.e. the compare
  did not verify the body ties.
- **Post-layout re-verification (T1 item 7, `7.digital`, graded `met`)** — the
  SDF-annotated functional run of §5a:
  `verification/readout/functional-verification-sdf.report.json`, 9/9 pass,
  **typ corner only**, annotation **partial** (323 TIMINGCHECK sections
  dropped). See `verification/README.md`.

**Why that is not a §9 pass for this partition.** The §9 target additionally
requires post-layout re-verification of **every row above**: spec §6's
post-layout leg records no conversion time at all (the `osc_hd` reads did not
complete at gate level, §6 above); the post-layout
functional run covers one corner, not the box; and there is **no SPEF-backed
post-layout timing run** on this block (`spef_sta` is null in
`layout/readout/report.json`, and both `klt sta` runs are DEF-only). The
fallback ("DRC + LVS clean") binds the whole block, whose analog half does not
meet it (`4.analog` is `unmet`; see `characterization/analog.md` §9). So this
report records the digital components above and **no §9 verdict**.

---

## What this report does not establish

- **Nothing here is measured.** Every figure is simulated, a static-timing
  result, or a simulated-flow output, at the corner and testbench named beside
  it.
- **Spec §6 is recorded only as far as the committed record reaches**: two
  cells (nominal; sf 1.98 V / −40 °C) × three gate settings, pre-layout, at
  the bench's single recorded deterministic phase — completion under a
  sub-period gate is phase-dependent, so the sf/default non-completion is the
  recorded phase's outcome, with `k0_phase_sweep` characterizing the law. The
  gate-level leg records no §6 time at all (`osc_hd` reads did not complete;
  typ corner, partial annotation). The planning arithmetic in
  `spec/target-spec.md` §6 is still quoted only as a planning figure.
- **No whole-block verdict** is formed for spec §8 or §9, and no cross-partition
  area or power figure is computed from the two reports' numbers.
- **Power and Fmax are not swept across the spec PVT box.** Power is one nominal
  flow estimate with `engine_default` activity and `estimate_only` parasitics;
  Fmax is the three installed liberty corners. The box extremes (125 °C,
  1.62 V, 1.98 V) have no liberty files in the pinned set and are not timed.
- **`spec/decisions/0003-counter-max-input-frequency.md` is cited as a draft
  proposal only.** The §5b FAIL stands as recorded; nothing here ratifies or
  acts on that draft.
- **No new simulation, synthesis, place-and-route, extraction or Monte Carlo was
  run for this report.** It is an aggregation of committed records — including
  `verification/readout/conversion-time.json` and
  `verification/readout/conversion-time-sdf.json`, which the readout bench
  itself wrote and which were committed before this report quoted them; the
  T1 item-8 checklist is satisfied by a hand-assembled record because no `klt`
  aggregation verb exists (`manifests/design-evidence-tiers.md` item 8;
  upstream tracker klayout-tools#309).

**Reproduce the per-row evidence**: the `README.md` "Reproduce" table names the
cheapest command for each result class cited above (commands 5, 6 and 7). The
citation-existence check for this report is
`characterization/test_citations.py`, run from `npm test`.
