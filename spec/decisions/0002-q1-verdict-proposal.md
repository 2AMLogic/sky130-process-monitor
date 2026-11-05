# 0002: Q1 verdict (proposal) — are frequency ratios alone enough?

- Status: **proposed** (not accepted; a human or Champion ratifies)
- Date: 2026-11-05
- Issue: #8 (answers Q1 of [0001](0001-ratify-target-spec.md))
- Evidence: `sim/sensitivity/records/2026-11-05-grid-sensitivity-partial.md` and `sim/sensitivity/records/2026-11-05-mc-margin.md`. **All figures SIMULATED**, schematic-level, sky130A / open_pdks c6d73a35 / ngspice-46; nothing measured.

## Proposal

Q1 is **not answered in favour of ratios alone, and not shown to need a better bank either**. The evidence supports three statements:

1. **Conditioning of the five-oscillator bank is moderate where it can be computed**: 5 of 9 (V,T) cells form a 5x4 matrix, absolute kappa 27.8 to 67.9, ratio-only 19.8 to 67.9, rank 4/4. Four cells (the -40 C column and V=1.8/27 C) cannot be formed because 7 grid cells did not oscillate; those cells are unanswered, not interpolated.
2. **Ratio-only is worse than absolute on margin**: minimum discrimination margin 0.46 (ratio-only, V=1.98/T=125, tt vs sf) against 1.13 (absolute, V=1.98/T=27, tt vs fs), over the formed cells. The spec's decision rule has no numeric threshold, so neither is called sufficient here. A threshold needs its own decision.
3. **The result hangs on the subthreshold oscillator, whose MC is unvalidated.** With it, margins are as above. Without it, margins rise (min 8.02 absolute, 4.22 ratio-only) but 6 of 10 formed matrices drop to rank 3 of 4. Its mismatch sigma(ln f) is 0.27 against 0.0015 to 0.0067 for the others; whether that is a real mismatch spread or a model artefact is Q2 (#10).

Caveats that bound this proposal: MC exists only at 1.80 V / 27 C and is applied to every cell; osc_hd shows zero mismatch spread at the ff corner (unexplained); the solve procedure (`sim/solve/`) has not been run. **No estimate accuracy follows from this record.**

## Options for the human decision (best to worst)
1. **Hold Q1 open** until (a) a margin threshold is ratified, (b) MC is run at the two off-nominal (V,T) cells, (c) #10 bounds the subthreshold MC. Cheapest, and nothing is concluded beyond the evidence.
2. Ratify "ratios alone are insufficient on the current bank" and open the better-bank / reference-input follow-up. Premature while the dominant noise term is unvalidated.
3. Ratify "ratios alone are sufficient". Not supported: the minimum margins are about 1 sigma or below.

The spec is unchanged by this record.
