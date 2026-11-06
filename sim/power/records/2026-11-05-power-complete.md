# 2026-11-05 — oscillator-bank power (spec row 7), re-run: graded, FAILS target, fallback and stretch

**SIMULATED. Oscillator bank only: COUNTER POWER IS NOT COVERED (no SPICE-level counter netlist).** Schematic-level, no layout.
ngspice-46, sky130A, via `klt sim --batch-set` on the batch fleet (klt 0.9.1.dev155). Supersedes the incomplete
`2026-11-05-power-partial.md` (kept; records are append-only). Tables: `2026-11-05-power-table-complete.json`, `2026-11-05-power-grade-complete.json`.

## Coverage
- Idle: 45/45 cells, all five oscillators present at every cell.
- Active: 219/225 oscillator cells. The 6 missing: osc_subth ss/1.62, ss/1.80, sf/1.62, sf/1.80, sf/1.98 at -40 C (fewer than 8 rising edges in the window; the same cells #8 could not resolve, not separated into dead vs window-too-short) and osc_wire sf/1.62 V/-40 C (`timestep too small` transient abort). Never graded, never filled.
- Fleet loss: several shards were reclaimed (`lost_shard`, `interrupted`). Lost shards were re-submitted with `--resume`; nothing was run locally except one single-unit probe (idle osc_nmos, tt/1.80 V/-40 C) to test the option below.

## Bench change since the partial record
24 `op` units of idle osc_nmos failed (gmin stepping), and 2 each for osc_nmos/osc_wire at -40 C. Cause: with the ring gated off, internal nodes have no DC path. `.options rshunt=1e12` (1 Tohm from every node to ground, ~2 pA/node at 1.8 V) on the osc_nmos and osc_wire benches (active and idle) makes the idle `op` converge on all 45 cells for osc_nmos. It did NOT cure the active osc_wire transient abort. The other three oscillators run without it. This is a bench option, not a model change; the effect is below the nA-scale idle currents but is not zero.

## Verdicts (all FAIL; no bound edited)
| | Target | Fallback | Stretch | Binding cell |
|---|---|---|---|---|
| Active (oscillator only) | < 100 uW FAIL | < 500 uW FAIL | < 20 uW FAIL | osc_wire ff / 1.98 V / -40 C = 1740 uW (219/225 cells) |
| Idle (bank sum) | < 1 uW FAIL | < 10 uW FAIL | < 100 nW FAIL | graded worst sf / 1.62 V / 27 C = 490 uW, SUSPECT (below) |

## Caveats
- The idle binding figure is dominated by one osc_nmos DC point (489 uW at sf/1.62 V/27 C) that is ~30000x its tt value and not monotonic in V or T neighbours; I believe it is a metastable/crowbar `op` solution, not leakage, and did not investigate further. The idle verdict does not depend on it: osc_subth's ungated ~1 uA bias divider alone gives 1.8 uW at tt/1.80 V/27 C (> 1 uW target), and the ff/1.98 V/125 C bank sum is ~53 uW without that point (> 10 uW fallback). Treat 490 uW as an upper-bound artifact until a better `op` is shown.
- Active mean current is over the second half of each tran window (not an integer number of cycles; error <= 1 cycle per window).
- Idle osc_hd came from the earlier fleet run (45/45); the other four idle sets from this one.
Reproduce: `analyze_power.py extract <reports> -o t.json; analyze_power.py grade t.json`.
