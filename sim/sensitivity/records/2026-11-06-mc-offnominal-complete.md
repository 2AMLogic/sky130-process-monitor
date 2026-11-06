# 2026-11-06 — off-nominal mismatch Monte Carlo, remainder (PARTIAL: cold osc_subth not collected) (issue #48)

**SIMULATED. Schematic-level netlists, no layout/parasitics. Nothing measured. No estimate accuracy is quoted** (the solve procedure has not been run). Append-only: no existing record is edited, including `2026-11-05-mc-offnom-partial.md`. No spec change.

Despite the file name suggested by the issue revision, this record is **not complete**: osc_subth at 1.98 V / -40 C did not finish on the fleet, so the cold-cell margin is **not computed** (a margin with a missing oscillator is a different quantity). Issue #48 stays open (`Part of #48`).

## 1. What ran
Requests `requests/mc_offnom_osc_{nmos,wire}.json` and `mc_offnom_osc_subth_1.98V_-40C.json` (unchanged), submitted with `klt sim --batch-set ... --resume --wait-for-capacity 600 --max-units-per-job 75`, backend `batch`; no local ngspice. Runner ngspice-46, open_pdks c6d73a35, klt client 0.9.2.dev25, runner klt 0.9.0. Cells: 1.62 V/125 C and 1.98 V/-40 C, 5 corners, mismatch MC.

| oscillator | cells | n per corner | result | fleet job ids |
|---|---|---|---|---|
| osc_nmos | both | 20 | 200/200 pass | klt-sim-00ce50c98331, klt-sim-1b78d6e62477, klt-sim-2adf0f93fa6f |
| osc_wire | both | 30 | 292/300 pass, **8 errored** (counted missing, not filled) | klt-sim-6cfcfcb0fcc7, klt-sim-eef5d6e16a0e, klt-sim-0fdbe74748a6 (failed: errors), klt-sim-fc5298dfcfc5 (failed: errors) |
| osc_subth | 1.98 V/-40 C | 10 (window 2 ms) | **not collected**: spot reclaim twice (klt-sim-0f28851980b6 at 421 s; klt-sim-5daaef14ce43 at ~950 s) | — |

The "failed" wire shards are klt's verdict exit code 4 (errored units), not runner crashes; their reports were merged. Reports: `records/reports/mc_offnom_osc_nmos.json.gz`, `mc_offnom_osc_wire.json.gz`.

osc_wire errors (all at 1.98 V/-40 C): tt 1 of 30, ss 7 of 30 (sigma uses 29 and 23 samples) — ngspice `timestep too small` / dynamic gmin stepping failed, no output. Cause not investigated; the ss n=23/30 sigma is from a truncated sample and could be biased if failures correlate with mismatch draw.

## 2. sigma(ln f) per corner (simulated)
| oscillator | cell | ff | fs | sf | ss | tt | pooled (RMS of five) |
|---|---|---|---|---|---|---|---|
| osc_nmos | 1.62 V/125 C | 0.00151 | 0.00241 | 0.00225 | 0.00226 | 0.00174 | 0.00206 |
| osc_nmos | 1.98 V/-40 C | 0.00165 | 0.00376 | 0.00226 | 0.00229 | 0.00180 | 0.00247 |
| osc_wire | 1.62 V/125 C | 0.00102 | 0.00101 | 0.00126 | 0.00115 | 0.00127 | 0.00115 |
| osc_wire | 1.98 V/-40 C | 0.00119 | 0.00107 | 0.00138 | 0.00131 (23/30) | 0.00151 (29/30) | 0.00130 |

Versus nominal pooled (2026-11-05): osc_nmos 0.00308 -> 0.67x (hot), 0.80x (cold); osc_wire 0.00146 -> 0.79x, 0.89x. With n = 20-30 the sampling error is about 13-17 %, so these are mostly within noise; no sign of a larger off-nominal spread. Fast-oscillator step bias (20 ps-style, issue #54) applies to these requests too and is not checked.

## 3. Margin re-run (hot cell only; `analyze.margin`, grid from `records/reports/grid_osc_*.json.gz`)
Per-cell sigma available for all five oscillators only at 1.62 V/125 C (osc_subth n=10, UNVALIDATED mismatch). Minimum discrimination margin over corner pairs, in sigma of noise, quantization + MC in quadrature:

| form | nominal pooled sigma everywhere | same, osc_hd ff=0 artefact excluded | per-cell sigma at 1.62 V/125 C |
|---|---|---|---|
| absolute | 2.57 (ss,sf) | 2.57 | 3.12 (ss,sf) |
| ratio-only | 1.62 (tt,ss) | 1.62 | 1.96 (tt,ss) |

The margin at this cell rises (about +21 %) because every oscillator's off-nominal hot sigma is below its nominal pool except osc_pmos (1.13x). osc_subth dominates the noise; its hot sigma has n=10. The osc_hd ff artefact exclusion (PR #52 finding) changes the margin in the fourth digit only. **1.98 V/-40 C: not computed (osc_subth missing). The other seven (V,T) grid cells have no off-nominal MC and are unchanged.** The margin is a discrimination figure from the existing tool, not an estimate accuracy.

## 4. Run notes and tool friction
- Both `--batch-set` and single-request polling kept polling a shard in terminal `interrupted` state (spot reclaim) until killed; it never reports or resubmits itself. To be filed generically at `2AMLogic/klayout-tools` (tool gap: wait loop on a terminal-interrupted job).
- Remainder: osc_subth 1.98 V/-40 C (10 samples/corner), then the cold-cell margin.
