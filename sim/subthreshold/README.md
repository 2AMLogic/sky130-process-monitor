# sim/subthreshold — spec Q2: are the open sky130 models good enough in subthreshold?

**Everything here is SIMULATED** (ngspice 46 on the batch fleet, sky130A models, `models_lib_sha256`
`17c208a6…`, identical to the pinned open_pdks `c6d73a35…` file on this host). Nothing is measured.
Each result names its corner, supply, temperature and testbench. Records: `measurements/subthreshold_records.jsonl`
(append-only). Raw `klt sim` reports: `runs/` (gzip). Reduction: `python3 -I analyze.py` (prints every table below;
`--append` writes the records, once).

## What is here

| File | Role |
|---|---|
| `osc_subth_tb.spice` | circuit body: `design/osc_bank/osc_subth.spice` (15 stages, read-only) with the same enable drive as `sim/osc_bank` |
| `osc_grid.request.json` | 45 cells: tt/ff/ss/sf/fs × 1.62/1.80/1.98 V × −40/27/125 °C. `.tran 2n 80u`; f = 8 cycles between rising edges 3 and 11 (the `sim/osc_bank` method) |
| `osc_grid_long`/`osc_grid_fast.request.json` | explicit re-runs of cells the first grid could not resolve (`5n 400u`) or under-resolved (`0.2n 3u`) — see "Method findings" |
| `gen_probe.py` → `probe_tb.spice`, `probe.request.json` | device probe: Id vs \|Vgs\| for the oscillator's devices and W-bin neighbours; 15 cells (5 corners × 3 T), `gmin=1e-15` |
| `osc_mc*.request.json` | `mc_mm_switch` Monte Carlo (`monte_carlo.vary: mismatch, mismatch_scale: 1`, N=30, seed 20261105), tt 1.80 V × −40/27/125 °C; `osc_mc_control0` is `mismatch_scale 0` (N=5) |
| `negative_controls.sh` | a wrong model path / corner name must fail with no frequency (both pass) |

Grid, probe and Monte Carlo ran through `klt sim --backend batch`; none ran locally. The only local runs were single-unit
debug probes (tt/1.8 V/27 °C, one probe corner, ff/1.8 V/125 °C at fine step) and the negative controls.
The batch worker's PDK cannot be pinned from the request (`models.pdk_root` is refused for batch); the worker's
`models_lib_sha256` equals the pinned local file's, and the tt/1.8 V/27 °C cell (1 706 830 Hz) is identical local vs batch.

## Results (simulated, tt 1.80 V unless stated)

Oscillator frequency, kHz, with the transient step/window that produced it (`2n/80u` = first grid; only cells ≤ ~7 MHz keep it):

```
            -40 C            27 C            125 C
tt 1.62V     50.9 (5n/400u)   1039.7 (2n/80u)   9781.5 (0.2n/3u)
tt 1.80V    109.0 (5n/400u)   1706.8 (2n/80u)  12658.3 (0.2n/3u)
tt 1.98V    218.1 (2n/80u)    2668.9 (2n/80u)  16045.1 (0.2n/3u)
ff 1.62V   1156.6             8230.2           31112.7
ff 1.80V   2093.2            11264.3           35971.2
ff 1.98V   3323.0            14881.0           41495.1
ss 1.62V     none             84.9 (5n/400u)    2077.3
ss 1.80V     none            159.3              3052.0
ss 1.98V     none            289.6              4299.0
sf 1.62V     none             none               963.4
sf 1.80V     none             37.4 (5n/400u)    1463.1
sf 1.98V     none             73.0 (5n/400u)    2206.0
fs 1.62V   3209.3            12500.1           32051.1
fs 1.80V   5194.6            15997.1           36493.4
fs 1.98V   7366.3            19920.1           41319.1
```

**38 of 45 cells resolved.** The 7 `none` cells (ss −40 °C × 3 V, sf −40 °C × 3 V, sf 1.62 V/27 °C) did not give 11 rising
edges in 400 µs (so f < ~27.5 kHz, or no oscillation). The runs cannot tell those two apart: **no-oscillation vs. too slow is
unresolved** for these 7 (not extended silently; one explicit 400 µs re-run was done and reported).

### Non-physicality checks

| # | Check | Result |
|---|---|---|
| 1 | f increasing with T, each (corner, V), resolved pairs | **PASS**, 23 pairs, 0 violations |
| 2 | Ioff (Vgs=0) and Id(0.30 V) increasing with T, 26 devices × 5 corners × 2 biases | **PASS**, 260 series, 0 violations |
| 3 | Subthreshold slope S rises with T, S(125)/S(−40) in 1.2–2.2 (ideal ∝ T: 1.71) | **FAIL**, 5 of 14 evaluable series out of band: pfet W=0.42 tt 2.24; pfet_lvt tt 2.55, ff 2.62, ss 2.27, fs 2.76. 11 of 25 series not evaluable (Id at 0.15 V under 1.1e-13 A at some T) |
| 4 | Id/W continuity across W-bin edges at 0.42 and 0.84 µm (0.01 µm steps, tt 27 °C, Vgs 0/0.15/0.30) | **PASS**, no step > 25 % |
| 5 | f(125 °C)/f(27 °C) tracks the header pfet_lvt Id(125)/Id(27) at \|Vsg\| = 0.30 V | **consistent**: f ratio / Id ratio = 0.81–0.85 in all five corners (tt 7.42/9.11, ff 3.19/3.84, ss 19.2/22.6, sf 39.1/46.5, fs 2.28/2.67) |

Other observations (all simulated):

- **Flat leakage floor.** Every device and corner bottoms at the same ~1.09e-14 A at Vgs=0 (cold ss/fs/sf), independent of
  width and type: a numerical/model floor, not device leakage. With ngspice's default `gmin` the floor was ~9.1e-13 A and
  corrupted the cold slopes (e.g. S = 62 874 mV/dec); the first probe run is kept as `runs/probe_gmin1e-12.report.json.gz`.
- **Slope.** S at tt 27 °C is 84 (nfet) / 137–154 (pfet) / 118 (pfet_lvt) mV/dec; the pfet and pfet_lvt slopes grow ×2.2–2.8 from
  −40 to 125 °C, faster than T. Whether that is a model artefact needs a reference not available here.
- **Width dependence.** Ioff/W at W 0.84–0.86 µm vs 0.42–0.44 µm (tt, 27 °C): nfet 0.90, pfet 4.27, pfet_lvt 1.60. The pfet
  has no model bin below W=0.42 µm (a W=0.40 instance fails with "could not find a valid modelname"), and the oscillator's
  W=0.42 and 0.84 devices sit exactly on bin edges.
- **Supply.** f(1.98 V)/f(1.62 V) = 2.57 at tt 27 °C (the header bias divider tracks Vdd). Input for #8, not judged here.
- **Mismatch (`mc_mm_switch`=1, N=30 each, tt 1.80 V).** Frequency spread σ/mean: 29.1 % at −40 °C (5n/400u, 30/30 oscillate),
  13.4 % at 27 °C (2n/80u), 10.0 % at 125 °C (0.2n/3u). Mean is below the no-mismatch value (−19 %, −13 %, −3 %).
  Control `mismatch_scale 0` (N=5): all five samples identical (1 706 830 Hz), so the spread is the switch, not noise.
  The first N=30 at −40 °C with `2n/80u` had 1/30 samples complete the measurement: window, not mismatch.
  `mc_pr_switch` was not used.

### Method findings (change how `sim/osc_bank` numbers above a few MHz should be read)

- **The `.tran 2n 80u` bench is unreliable above ~5 MHz.** ff/1.80 V/125 °C gave 142.6 MHz at 2 ns step and 36.0–36.3 MHz at
  0.2 ns / 0.1 ns (local 0.1n 1u vs batch 0.2n 3u agree to 1 %). tt/1.8 V/125 °C: 19.1 MHz vs 12.7 MHz. Fine-step values
  replace the coarse ones in the table; the first-grid record is kept (append-only), flagged by `tran_step_window`. Cells still
  at 2n step are ≤ 5.2 MHz; the 7.4 MHz cell moved by 6 %, so their error is not quantified here but is bounded by that order.
- The 80 µs window is too short for f < ~140 kHz (11 periods): 12 first-grid cells failed that way, 5 resolved at 400 µs.

## Verdict: INCONCLUSIVE (model-usable at tt/ff/fs ≥ 27 °C; not established at the cold slow corners)

- Supports "model is self-consistent": checks 1, 2, 4, 5 pass; frequency follows the header current's temperature
  dependence uniformly across five corners; the mismatch switch acts in subthreshold with a clean control.
- Supports "model is suspect": check 3 fails (subthreshold ideality grows with T faster than the model's own 1/T scaling would
  suggest for the pfet devices that set the oscillator current) and a device-independent leakage floor of ~1.1e-14 A exists.
- Supports neither: 7 of 45 spec-box cells are unresolved at the slow/cold end, which is exactly where the spec's
  temperature row needs the oscillator.
- Not "design-limited": the oscillator runs and is monotonic in T and V wherever it resolves; its T sensitivity (×7.4 over
  27→125 °C at tt) is large. Supply sensitivity is also large (×2.57 for ±10 % V) — a #8 matter.

**Evidence that would settle it:** (1) re-run the 7 cells with ≥ 2 ms window to see whether they oscillate (and a faster-start
enable); (2) a reference for subthreshold S(T) of the sky130 pfet / pfet_lvt (foundry data or silicon) to judge check 3;
(3) the origin of the 1.09e-14 A floor (model parameter vs ngspice) and whether it matters at the oscillator's own currents
(header pfet_lvt Id ≈ 4.0e-8 A at \|Vsg\| 0.30 V, 27 °C, tt, W=0.42, Vds 0.9 V). No spec row or oscillator definition is changed by this verdict, so no decision
record is raised; the unresolved cold cells and the 5 MHz bench limit are for follow-up issues.
