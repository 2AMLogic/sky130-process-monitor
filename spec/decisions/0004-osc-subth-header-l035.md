# 0004: osc_subth header channel length 0.5 → 0.35 µm (proposal)

- Status: **proposed** (not accepted; a human or Champion ratifies)
- Date: 2026-11-21
- Issue: #278 (osc_subth cold-corner design iteration; follows [0002](0002-q1-verdict-proposal.md) item 3 and
  the gate-sizing record of 2026-11-14)
- Evidence: `sim/sensitivity/records/2026-11-21-osc-subth-cold-iteration.md` and the committed reports under
  `sim/subthreshold/variants/reports/`. **All figures SIMULATED**, schematic-level, sky130A / open_pdks
  `f6eeac7dad08…` (fleet runners) / ngspice 47; nothing measured.

## Proposal

Change the `osc_subth` starved-stage header (`pfet_01v8_lvt`, 14 instances in
`design/osc_bank/osc_subth.spice`) from **L = 0.5 µm to L = 0.35 µm** (W = 0.42 µm unchanged). 0.35 µm is the
model bin floor: the `pfet_01v8_lvt` discrete bins in this open_pdks install have no L below it (ngspice
"could not find a valid modelname" at L = 0.25 / 0.15, verified on the pinned models). Everything else in the
schematic stays byte-identical.

Why: the cold (−40 °C) slow-corner cells of `osc_subth` run at 437–3044 Hz on the committed schematic — under
one counter count at the spec-default 2^10 gate (0.045–0.312 expected counts), so the five-corner target's
estimate needs either a longer gate (k = 15, a 3.686 ms five-oscillator read against spec §6's <1 ms target) or
a faster oscillator. The L = 0.35 header lifts the five cold cells to 12.4–277 kHz (**1.271 expected counts at
k = 10 at the worst cold cell, sf / 1.62 V / −40 °C**), keeps all 45 PVT cells oscillating (row 1), and leaves
the full read at 512 µs — inside §6's target with **no readout change**. The mechanism is Vth roll-off: at the
baseline 0.30 V header drive the L = 0.35 device carries 120× the baseline current at sf / −40 °C but only
8.8× at tt / 27 °C, so the correction lands exactly where the starvation is.

## Costs, stated (all simulated; the record's section 5 tables are the source)

- The 27 °C dT slope of ln f drops 10–27 % (scaled 1.68–1.77 vs 1.86–2.44); the 125 °C slope roughly doubles.
- Nominal mismatch σ(ln f) rises 0.266 → 0.316 (30 draws, seed 20261105, tt / 1.80 V / 27 °C).
- The 1.62 V / 125 °C corner-discrimination margin drops 2.574 → 0.627 (the variant's new minimum);
  1.98 V / −40 °C improves 0.759 → 1.327.
- The fastest cell rises 151 → 351 MHz (ff / 1.98 V / 125 °C): still inside decision 0003's corner-matched
  counter fmax, but the unmapped hot cells need the re-STA below.
- The frequency window moves up: min 12.4 kHz (vs 437 Hz), max 351 MHz (vs 151 MHz); the max/min ratio
  narrows from 3.5·10^5 to 2.8·10^4.

Alternatives carried by the same record: header **W×3** is the better discriminator (margins 2.7–8.3× better
at every shared cell, σ(ln f) 0.091) but leaves the cold cells under one count at k = 10 (needs k = 14,
2.048 ms read); the divider-ratio levers (vbp at 2/3 or 1/2 VDD) clear any count bar but collapse the dT slope
to 0.49–1.73 and push the fastest cell to 586–795 MHz; 15→11 stages moves the cold cells only ×1.5–1.8.

## Downstream re-runs an acceptance triggers (not done here)

1. `design/osc_bank/osc_subth.spice` + `.sch` edit and `design/osc_bank/gen_schematics.py` regeneration; the
   layout is untouched here on purpose (#117's extraction re-check needs the current layout).
2. Layout generator run for `osc_subth`; then DRC, LVS, `klt pex` and the #117/#275 extraction re-check on the
   new geometry.
3. The full sensitivity grid + MC re-run for `osc_subth` (`sim/sensitivity/`) and every record that consumes
   its surface: rows 1–4 re-grade (`sim/solve/`), the gate-sizing record's k-sweep, the row-7 idle power
   bench, and the #277 225-cell table.
4. Per-oscillator re-STA against decision 0003's counter fmax at the new hot cells (351 MHz max).
5. #281's conversion-time re-grade if any gate default changes (none is proposed here).

No bound is relaxed and no RTL is edited by this proposal. Decision 0002 is untouched.
