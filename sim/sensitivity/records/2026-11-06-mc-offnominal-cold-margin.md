# 2026-11-06 — cold-cell (1.98 V / -40 C) margin with all five oscillators (issue #48)

**SIMULATED. Schematic-level netlists, no layout/parasitics. Nothing measured. No estimate accuracy is quoted** (the solve procedure has not been run); the margin below is a corner-discrimination figure from `analyze.margin`, not an estimate error. Append-only: no existing record is edited. No spec change. The osc_subth mismatch model is still UNVALIDATED.

## 1. The last missing nominal cell: osc_wire sf, 1.98 V / -40 C
The 2026-11-06 cold-sf record showed `timestep_too_small` for this cell with the default solver settings. New request `requests/probe_wire_sf.json` runs the same `tran 50p 2.5u 0 20p` on `osc/tb_osc_wire_probe.spice`, which is `tb_osc_wire.spice` plus one added line, `.options reltol=0.01 gmin=1e-10 method=gear` (original testbench untouched).
- One unit, run **locally** as a single-corner debug probe (ngspice 46): converged, 212 edges, **f = 84.99 MHz** (`reports/probe_wire_sf_relaxed.json.gz`).
- Bias check of the relaxed options, fleet job **klt-sim-3dc552387883** (`requests/probe_wire_val.json`, 3 units, `--backend batch`, done) against the original default-option grid at cells that did converge:

| cell | relaxed f (Hz) | default-option grid f (Hz) | ratio |
|---|---|---|---|
| tt 1.98 V -40 C | 94.558e6 | 94.372e6 | 1.0020 |
| sf 1.80 V -40 C | 72.916e6 | 72.855e6 | 1.0008 |
| ss 1.98 V -40 C | 77.233e6 | 77.138e6 | 1.0012 |

The options shift f by up to +0.2 % at these three cells. Three cells do not bound the bias at the sf/1.98 V/-40 C point, which is the one that failed under default options, so the 84.99 MHz value carries that caveat. The cause of the default-option failure was not investigated. The 8 `timestep too small` MC samples at this cell (2026-11-06-mc-offnominal-complete.md) were not re-run.

## 2. Cold-cell MC sigma(ln f) (existing reports, no new MC)
osc_hd 0.00479 (n=30/corner), osc_nmos 0.00247 (20), osc_pmos 0.00541 (30), osc_wire 0.00130 (29/23/30 usable), osc_subth 0.1858 (ff/fs/tt n=10; ss 6/10; sf 6/10, truncated: the slowest draws are the ones lost, so sigma is biased low). Per-cell sigma = RMS over the five process corners at that cell. Fast-oscillator step bias (#54) not checked.

## 3. Margin at 1.98 V / -40 C (`analyze.margin`, reproduced by script from the committed reports)
Frequency table: grid reports + `grid_osc_subth_sf_cold` + the osc_wire sf value above (no other cell at this (V,T) is missing). Minimum over corner pairs, sigma of noise, quantization (2^10 ref cycles at 10 MHz) and MC in quadrature:

| form | nominal pooled sigma everywhere | same, osc_hd ff=0 artefact excluded | per-cell sigma at 1.98 V/-40 C | quantization only |
|---|---|---|---|---|
| absolute | 0.759 (ss,sf) | 0.759 | 0.763 (ss,sf) | 0.766 |
| ratio-only | 0.822 (ss,sf) | 0.822 | 0.826 (ss,sf) | 0.830 |

Per-cell sigma changes the margin by about +0.5 %. The margin is **below 1 sigma and is set by counter quantization, not by MC**: in the default gate osc_subth gets 0.11 counts (sf), 0.77 (ss), 31.9 (tt), 349 (ff). That is a property of the 2^10 @ 10 MHz gate at ~1 kHz, so a longer osc_subth gate is the lever; this record does not size it. Hot-cell result (abs 2.57 -> 3.12) is in the 2026-11-06 complete record and stands.

## 4. Status of #48
Collected: off-nominal MC for all five oscillators at the hot cell and, with the caveats above, the cold cell; margins at both. Not done: the other seven (V,T) cells have no off-nominal MC; truncated osc_subth sf/ss cold samples; the osc_wire default-solver failure cause.
