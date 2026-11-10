# 0003: Readout counter maximum input frequency vs the fastest oscillator (draft)

- Status: **draft / proposed** (not accepted; a human or Champion ratifies)
- Date: 2026-11-10
- Issue: #89 (follows #29 oscillator frequency surfaces and #30 readout STA)
- Evidence: `sta/readout.osc-corner.sta.report.json` (15 `klt sta` runs, `klayout-tools==0.9.1`, requests in `sta/osc/`), periods from `sim/sensitivity/records/reports/grid_*.json.gz`. **All figures SIMULATED / static timing**: schematic-level oscillator frequencies, routed DEF with no SPEF, ideal clocks, no silicon.

## Finding

With each `osc[i]` clock at its corner-matched #29 period, the oscillator-domain registers are all clocked and every endpoint is constrained (`constraint_completeness: complete` in all 15 runs). The counter's setup-limited maximum clock rate (`fmax_mhz`) against the fastest oscillator, `osc_hd`:

| Liberty corner | Nearest #29 cell | counter fmax (MHz) | `osc_hd` f (MHz) | setup slack at `osc_hd` period (ns) |
|---|---|---|---|---|
| ss_100C_1v60 | ss / 1.62 V / 125 C | 171.1 | 341.9 | -2.92 |
| tt_025C_1v80 | tt / 1.80 V / 27 C | 358.9 | 641.0 | -1.23 |
| ff_n40C_1v95 | ff / 1.98 V / -40 C | 586.8 | 1020.3 | -0.72 |

**The counter does not cover `osc_hd` in any corner**, including the issue's named worst case (ff, 1.98 V, -40 C): it needs about 2.0x (ss), 1.79x (tt) and 1.74x (ff) more speed. All four other oscillators close in every corner (smallest setup slack +0.92 ns, `osc_nmos` at ff). Hold slack is 0.20 to 0.68 ns everywhere and does not depend on the oscillator. Per-oscillator numbers are in the report.

Bounds on this finding: the oscillator frequencies are schematic-level (layout parasitics will slow them), and the STA is without SPEF, so both sides of the comparison are optimistic and the gap could narrow or widen. The liberty corners differ from the grid cells (see `sta/README.md`), the spec-box extremes are not timed, and minimum-pulse-width checks are not reported by the tool. The size of the gap (about 2x) is well outside those effects, so the direction of the finding is not expected to change.

## Options for the human decision (best to worst)
1. **Add a divide-by-N prescaler (N >= 2, e.g. toggle flop) between the oscillator mux and the counter**, with the readout register and the gate-length rule (`2^k * T_ref >= T_osc`) adjusted for N. Fixes `osc_hd` with no spec change; costs a few cells and halves count resolution for that oscillator (the 24-bit width and +-1 count quantisation then apply per N osc cycles). Needs an RTL decision and re-verification.
2. **Slow `osc_hd` down** (more stages) so its fastest corner stays under about 500 MHz, with margin. A change to spec section 1 (stage counts are planning figures that change only through a decision record) and to the #8/#29 surfaces, which would then need re-running.
3. **Restrict `osc_hd` to a lower-voltage / lower-speed use** or drop it from the target bank. Changes the five-oscillator target to a fallback-like bank; not supported by this evidence alone.
4. **Accept as is** and treat `osc_hd` counts as unreliable in the fast corners. Not recommended: the count would be wrong exactly where the estimate is needed.

No bound was relaxed and no RTL was edited to produce this record. The spec is unchanged by it.
