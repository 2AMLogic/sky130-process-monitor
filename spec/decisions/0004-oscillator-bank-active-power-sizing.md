# 0004: Oscillator-bank active-power sizing (osc_wire r004w02, osc_pmos l10)

- Status: **proposed** (not accepted; a human or Champion ratifies)
- Date: 2026-11-21
- Issue: #280 (spec row 7 active power; follows #29's committed power bench and #173's gradability rule)
- Evidence: `sim/power/records/2026-11-21-active-power-iteration.md` and its tables and raw reports
  (`sim/power/records/2026-11-21-*.json`, `sim/power/records/reports/`). **All figures SIMULATED,
  schematic-level, oscillator only** — no counter netlist, no layout, no silicon. ngspice-46/47, sky130A.

## Finding

The committed bank fails row 7's active bounds on `osc_wire` alone: 1740.2 µW worst-cell (ff/1.98 V/−40 °C),
over the 500 µW fallback at every graded cell. The iteration record decomposes each oscillator's power at
its binding cell and sweeps one lever at a time; the load-bearing measured facts:

1. **Stage count is power-neutral** (±0.4 % across wire/nmos/pmos/hd, confirmed on a full 45-cell grid for
   `hd_n061`): first-order ring power ≈ C·V²/(2·t_stage) has no N in it. Stage count is a frequency lever only.
2. **`osc_wire` is RC-delay-dominated**, so its explicit 100 fF capacitors are power-neutral (halving C
   raises f nearly proportionally) and the resistor length is the power lever that *preserves* the wire-RC
   fraction the ring exists to sense (fraction rises 0.51 → 0.90 as L goes 500 → 4000 µm).
3. **`osc_hd`'s power is fixed by the standard cell** (inv_1) at ~396 µW worst-cell, invariant to stage
   count. It alone keeps the bank above the 100 µW target at every stage count tried: **the row-7 target
   (< 100 µW) is infeasible for the committed bank composition**; only the fallback is closable.
4. Candidate 45-cell grids: `wire_r004w02` worst-cell **447.2 µW** (every graded cell under the 500 µW
   fallback; f 14.3–31.7 MHz, counter-covered at all three decision-0003 cells; RC fraction 0.72);
   `pmos_l10` worst-cell **81.7 µW** (under the 100 µW target at every graded cell; sensitivity row
   substantially unchanged); `nmos_l30` worst-cell 102.1 µW but erodes the Pn column that oscillator
   contributes (0.157 → 0.050 at ss/1.62/125) — not proposed.

## Proposal

| Oscillator | Change from the committed point | Worst-cell active power (45-cell grid) | Why |
|---|---|---|---|
| `osc_wire` | per-stage `res_generic_m1` L: 1000 → **4000 µm** (W 0.14 µm unchanged); inverter drivers W 8/4 → **2/1 µm**; stages, 100 fF caps, enable NAND unchanged | 1740.2 → **447.2 µW** (ff/1.98/−40) | Closes the fallback for the bank (worst remaining oscillator: `osc_hd` 396.4 µW) while raising the wire-RC fraction of stage delay (0.69 → 0.72 at the binding cell, 0.90 with the R lever alone) |
| `osc_pmos` | weak pull-up L: 0.5 → **1.0 µm** (W 0.42 µm unchanged); everything else unchanged | 165.6 → **81.7 µW** (ff/1.98/125) | Meets the 100 µW target for this oscillator with the sensitivity row substantially unchanged (V 0.304→0.314, Pp 0.208→0.191 at tt/1.80/27) |
| `osc_nmos` | **no change** | 351.5 µW (under the fallback as committed) | The L lever trades power against the Pn process signature (0.157 → 0.050 at l30); past L ≈ 2 µm the trade stops paying |
| `osc_hd` | **no change** | 396.4 µW | Power is fixed by the library cell and stage-count-invariant; no lever exists without leaving standard cells |
| `osc_subth` | **no change** | 36.6 µW | Under every bound as committed |

Device-count input to #26 (unchanged by this proposal): `osc_wire` keeps **31 capacitors + 31 resistors**;
each resistor is 4× longer (1000 → 4000 µm at W 0.14 µm), so the serpentine's drawn length grows ~4× —
the #75 packing and the §8 area budget re-check are downstream of acceptance, not of this record.

## Downstream re-runs required by acceptance

1. Frequency surfaces (`sim/sensitivity/`) for `osc_wire` and `osc_pmos` over the 45-cell box, including
   the cold-cell complements (`wire_r004w02` already resolves the committed sf/1.62 V/−40 °C convergence
   cell un-relaxed).
2. Mismatch MC and off-nominal MC for the two changed oscillators (same seeds/settings as the committed
   sets), then the solve rows 1-4 re-grade (`sim/solve/`, #277's full-surface re-grade).
3. Row-7 power re-grade under `sim/power/` benches at the new design points (the 2026-11-21 candidate
   grids are the evidence; the committed bank's verdict stays FAIL until this re-run grades otherwise).
4. Readout counter STA re-check against decision 0003 at the three timed cells (candidate frequencies are
   5-18× under the limits; the check is formal).
5. Layout: serpentine re-pack (#75), area re-check against spec §8, LVS device list for #26.

## Bounds and non-goals

- No spec threshold is relaxed or edited by this record; row 7's target/fallback/stretch bounds stand. The
  infeasibility finding for the 100 µW target (item 3 above) is recorded evidence for a future human
  decision, not a change.
- Nothing here covers counter power (no SPICE netlist) or idle power (#279/#295); the active figures
  remain lower bounds on the spec's "one oscillator plus counter".
- The evidence is schematic-level; layout parasitics will move the frequencies (and the RC fractions)
  — re-verified by the PEX path after layout.

No netlist was edited to produce this record; the candidates are bench-side variants
(`sim/power/tb/cand/`, parity-asserted against the committed netlists by
`sim/power/test_gen_candidates.py`).
