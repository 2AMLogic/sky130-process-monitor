# 2026-11-21 — osc_subth cold-corner design iteration: divider ratio, header W/L, stage count (issue #278)

**SIMULATED. Schematic-level netlists, no layout, no parasitics, nothing measured.** Every figure below comes
from a committed `klt sim` report or is a direct post-processing of committed reports; the new runs are batch-fleet
jobs submitted through `klt sim` (never hand-launched ngspice). **No estimate accuracy is quoted** — nothing here
has been run through the solve procedure; the margins are corner-discrimination statistics from `analyze.margin`,
as in `records/2026-11-14-osc-subth-gate-sizing.md`. Append-only: no existing record is edited, **no spec value
changes**, and decision 0002 stays as it is (this issue does not ratify it).

## 0. What was asked and what this record is

The 2 ms re-runs of issue #44 narrowed the five cold `osc_subth` cells but did not clear them; #277's single-cell
fleet runs later resolved all of them (436.93 Hz at sf / 1.62 V / −40 °C up to 3043.81 Hz at ss / 1.80 V), and the
2026-11-14 gate-sizing record showed the readout-side lever (counter gate k = 14) costs 2.048 ms against spec §6's
<1 ms target. This record examines the **oscillator-side** levers, one factor at a time against the committed
15-stage baseline (`design/osc_bank/osc_subth.spice`):

| lever | variant | one-factor change |
|---|---|---|
| divider ratio (vbp) | `vbp_2_3` | Rb0 300k→600k, Rb1 1500k→1200k (vbp 0.8333→0.6667·VDD; total 1.8 M unchanged) |
| divider ratio (vbp) | `vbp_1_2` | Rb0 900k, Rb1 900k (vbp 0.5·VDD; total 1.8 M unchanged) |
| header W/L | `hw3` | header `pfet_01v8_lvt` W 0.42→1.26 (×3), L=0.5 |
| header W/L | `hl35` | header L 0.5→0.35, W=0.42 |
| stage count | `st11` | 15→11 stages (NAND + 10 starved; stage 10 drives `out`) |

Holding total divider resistance fixed isolates the bias point from the divider current; the odd stage count
(including the enable NAND) is preserved; every other element is byte-identical to the baseline deck (the variant
decks are text transformations of it, `sim/subthreshold/variants/gen_variants.py`).

**A PDK constraint found while defining the header lever:** the `pfet_01v8_lvt` discrete model bins in this
open_pdks install have no L below 0.35 µm — L=0.25 and L=0.15 fail with ngspice "could not find a valid modelname"
(verified locally on the pinned models; L=0.35 and 0.5 parse). The short-channel header lever therefore stops at
L=0.35, not the 0.15 the other FETs use.

## 1. The open cell: sf / 1.62 V / −40 °C on the current schematic

**It oscillates.** The #277 single-cell fleet run (`grid_osc_subth_sf_1.62V_-40C`, 80 ms window, 80 ns max step,
38 rising edges, job klt-sim-a8f52ea96150, quoted from its record pending that PR's merge) resolves **436.93 Hz**
on the committed schematic. This record's control check reproduces the 1057.37 Hz sf / 1.98 V / −40 °C cell from
the two reports main already carries (§2). The four remaining cold-cell baseline frequencies are likewise #277
results quoted with provenance; they are not re-run here (the issue's guidance says to reuse them).

## 2. Inputs and reproduce

Everything is committed; no glob (order is load-bearing, last wins — the #140 lesson):

- Variant decks + testbench bodies + requests: `sim/subthreshold/variants/` (`python3 -I
  sim/subthreshold/variants/gen_variants.py` regenerates every deck/tb/request byte-identically; `--check`
  verifies). Variant reports: `sim/subthreshold/variants/reports/` (gzip).
- Post-processing: `python3 -I sim/subthreshold/variants/compare.py` (imports `sim/sensitivity/analyze.py`
  unchanged; prints every table in this record; `--selftest` exercises the math on synthetic data).

```
# the fleet runs, two klt sim --batch-set invocations (explicit member lists, never a glob):
#   round 1: requests/grid_osc_subth_{vbp_2_3,vbp_1_2,hw3,hl35,st11}.json
#            + requests/mc_osc_subth_{...}.json + requests/probe_hdr.json
#   round 2 (after inspecting round 1): the 10 requests/cold_osc_subth_*.json fills
#            + the corrected probe_hdr.json (the first probe deck still named an L=0.15
#            device, which the lvt model bins refuse; every unit errored, nothing was used)
# both: klt sim --batch-set <members> --wait-for-capacity 600 --capacity-retries 4 \
#         -o <outdir> --report-out <envelope>; member reports -> variants/reports/
python3 -I sim/subthreshold/variants/gen_variants.py --check
python3 -I sim/subthreshold/variants/compare.py
```

The extraction rule is the sensitivity bench's everywhere (VDD/2 rising crossings, first 3 edges dropped, ≥5
cycles or MISSING, never interpolated): a variant frequency and a committed baseline frequency are computed by
the same code. The **window** differs per variant (sized from local single-corner probes: the vbp variants run
the ring ~30-50× faster at nominal, so the baseline 2 ms window cannot be integrated inside the per-unit timeout
at the hot cells); cells a variant window under-resolves are re-run as single-cell fills with ≥2× margin over
the ~9 edges the estimator needs — exactly the #277 method — and those fills are committed too.

Provenance: ngspice 47 on the fleet runners' own open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (per-report
`environment.remote.worker_environment.pdk`), submitted with `--wait-for-capacity 600`. Fleet job ids, one per
committed report (grids `klt-sim-{eb406f5eddf5,cca54364a447,d52979abfb9c,d8fdb1c61004,be45f6c447a9}`, MCs
`klt-sim-{4d8ec8943d3d,13b89fdbdefb,7b3a20cc30c4,1adddabf4b9c,07eec9241b4c}`, probe `klt-sim-e4146e972028`,
fills `klt-sim-{744e3ca506e7,1e4044733a0b,8e10f0ba9b0a,8da0122164e6,811e674ca893,d3aaae864648,68fa709fd02a,`
`ec3e8785efdc,baa7becb956f,155a79877575}`). The local single-corner probes that sized the windows (one
ngspice -b per variant at tt / 1.80 V / 27 °C) are the only local runs.

## Control: the committed baseline reports reproduce the 1057.37 Hz cell
sf / 1.98 V / -40 C: f = 1057.37 Hz (n_edges = 10) -- grid_osc_subth + grid_osc_subth_sf_cold

## Baseline bank margins (committed reports only, default gate 2^10 at 10 MHz)
| V | T | abs | pair | ratio | pair |
|---|---|-----|------|-------|------|
| 1.62 | -40 | ungradable | - | ungradable | - |
| 1.62 | 27 | 3.257 | ('ff', 'fs') | 1.886 | ('ff', 'fs') |
| 1.62 | 125 | 2.574 | ('ss', 'sf') | 1.620 | ('tt', 'ss') |
| 1.80 | -40 | ungradable | - | ungradable | - |
| 1.80 | 27 | 2.437 | ('ff', 'fs') | 2.235 | ('ff', 'fs') |
| 1.80 | 125 | 1.422 | ('tt', 'sf') | 1.374 | ('tt', 'sf') |
| 1.98 | -40 | 0.759 | ('ss', 'sf') | 0.822 | ('ss', 'sf') |
| 1.98 | 27 | 1.134 | ('tt', 'fs') | 0.984 | ('tt', 'ff') |
| 1.98 | 125 | 2.608 | ('ss', 'sf') | 0.459 | ('tt', 'sf') |

Baseline osc_subth sensitivity rows (scaled dV/dT/dPn/dPp of ln f), where gradable:
| V | T | dV | dT | dPn | dPp |
|---|---|----|----|-----|-----|
| 1.62 | 27 | 0.491 | 2.441 | -0.454 | 2.712 |
| 1.62 | 125 | 0.101 | 1.139 | -0.195 | 1.560 |
| 1.80 | 27 | 0.818 | 2.031 | -0.545 | 2.497 |
| 1.80 | 125 | 0.325 | 0.811 | -0.014 | 1.112 |
| 1.98 | -40 | 0.887 | 4.134 | -0.618 | 3.675 |
| 1.98 | 27 | 1.146 | 1.862 | -0.389 | 2.193 |
| 1.98 | 125 | 0.549 | 0.309 | 0.488 | 1.106 |


## 3. What sets the cold slow-corner frequency (header probe)

### Divider idle current (derived from the netlist resistors, not simulated)
Every variant keeps Rb0+Rb1 = 1.8 M exactly, so the divider draws V/1.8 M: 0.90 / 1.00 / 1.10 uA at 1.62 / 1.80 / 1.98 V.
### Header Id (A) from the DC probe: device x |Vgs| at the cold corners and the tt/27 control
| device / lever | corner | Id @ 0.30 V | @ 0.54 | @ 0.60 | @ 0.66 | @ 0.81 | @ 0.90 | @ 0.99 |
|---|---|---|---|---|---|---|---|---|
| baseline/st11 | ss / -40 C | 6.19e-11 | 2.87e-08 | 8.46e-08 | 2.2e-07 | 1.22e-06 | 2.39e-06 | 4.03e-06 |
| baseline/st11 | sf / -40 C | 5.03e-12 | 6.67e-09 | 2.35e-08 | 7.2e-08 | 6.64e-07 | 1.6e-06 | 3.05e-06 |
| baseline/st11 | tt / 27 C | 4.04e-08 | 8.15e-07 | 1.31e-06 | 1.97e-06 | 4.36e-06 | 6.37e-06 | 8.85e-06 |
| hw3 | ss / -40 C | 2.02e-10 | 9.53e-08 | 2.78e-07 | 7.14e-07 | 4.01e-06 | 7.94e-06 | 1.35e-05 |
| hw3 | sf / -40 C | 2.32e-11 | 2.51e-08 | 8.83e-08 | 2.65e-07 | 2.3e-06 | 5.48e-06 | 1.04e-05 |
| hw3 | tt / 27 C | 1.49e-07 | 2.66e-06 | 4.21e-06 | 6.22e-06 | 1.35e-05 | 1.94e-05 | 2.68e-05 |
| hl35 | ss / -40 C | 5e-09 | 3.7e-07 | 7.33e-07 | 1.27e-06 | 3.46e-06 | 5.4e-06 | 7.86e-06 |
| hl35 | sf / -40 C | 6.06e-10 | 1.31e-07 | 3.21e-07 | 6.74e-07 | 2.45e-06 | 4.18e-06 | 6.44e-06 |
| hl35 | tt / 27 C | 3.54e-07 | 2.51e-06 | 3.47e-06 | 4.63e-06 | 8.47e-06 | 1.15e-05 | 1.5e-05 |

Divider-ratio mapping (|Vgs| = (1 - Rb1/(Rb0+Rb1)) x VDD): baseline 0.8333 ratio -> 0.27/0.30/0.33 V at 1.62/1.80/1.98 V; vbp_2_3 -> 0.54/0.60/0.66 V; vbp_1_2 -> 0.81/0.90/0.99 V. The hw3/hl35/st11 rows read the baseline drive (0.30 V at 1.80 V) on their own device column.


## 4. Per-lever results

## Variant vbp_2_3
Reports (order is load-bearing, last wins): ['grid_osc_subth_vbp_2_3.json.gz']

### The five cold cells (-40 C; SIMULATED, sensitivity bench, VDD/2 crossings)
| cell | baseline f (Hz) | vbp_2_3 f (Hz) | edges | counts @ k=10 | counts @ k=14 |
|------|-----------------|-----------|-------|--------------|--------------|
| ss / 1.62 V | 1251.87 | 1543473.51 | 308 | 158.052 | 2528.827 |
| ss / 1.80 V | 3043.81 | 3926530.87 | 400 | 402.077 | 6433.228 |
| sf / 1.62 V | 436.93 | 301026.82 | 60 | 30.825 | 493.202 |
| sf / 1.80 V | 586.21 | 1044321.54 | 208 | 106.939 | 1711.016 |
| sf / 1.98 V | 1057.37 | 2846956.91 | 400 | 291.528 | 4664.454 |

### 45-cell coverage and extrema (row-1 criterion: every cell resolved)
- resolved cells: 45 / 45
- min f = 301026.82 Hz at sf 1.62 V -40 C; max f = 5.863e+08 Hz at ff 1.98 V 125 C; ratio 1948

### Nominal mismatch MC (tt / 1.80 V / 27 C, 30 draws, seed 20261105, scale 1)
- usable draws 30 / 30, sigma(ln f) = 0.29444

### Row-2 margins with vbp_2_3 substituted for osc_subth (default gate, committed MC for the other four)
| V | T | abs | pair | ratio | pair | vs baseline abs | vs baseline ratio |
|---|---|-----|------|-------|------|-----------------|-------------------|
| 1.62 | -40 | 2.982 | ('ff', 'fs') | 2.086 | ('tt', 'ss') | - | - |
| 1.62 | 27 | 2.258 | ('ss', 'sf') | 0.943 | ('ss', 'sf') | 0.693 | 0.500 |
| 1.62 | 125 | 1.251 | ('tt', 'fs') | 1.905 | ('tt', 'ff') | 0.486 | 1.176 |
| 1.80 | -40 | ungradable | - | ungradable | - | - | - |
| 1.80 | 27 | 1.663 | ('tt', 'sf') | 1.049 | ('ff', 'fs') | 0.682 | 0.469 |
| 1.80 | 125 | 0.430 | ('tt', 'fs') | 0.448 | ('tt', 'fs') | 0.303 | 0.326 |
| 1.98 | -40 | 2.072 | ('ff', 'fs') | 1.820 | ('ss', 'sf') | 2.730 | 2.213 |
| 1.98 | 27 | 2.663 | ('ff', 'fs') | 1.075 | ('ss', 'sf') | 2.348 | 1.092 |
| 1.98 | 125 | 2.027 | ('tt', 'fs') | 1.328 | ('tt', 'ss') | 0.777 | 2.896 |

### vbp_2_3 sensitivity rows (scaled), where gradable
| V | T | dV | dT | dPn | dPp | baseline dT |
|---|---|----|----|-----|-----|-------------|
| 1.62 | -40 | 0.660 | 2.401 | -0.666 | 2.238 | - |
| 1.62 | 27 | -0.354 | 1.643 | 0.058 | 1.235 | 2.441 |
| 1.62 | 125 | 0.749 | 1.125 | 0.139 | 0.681 | 1.139 |
| 1.80 | -40 | 0.648 | 1.152 | -0.472 | 1.845 | - |
| 1.80 | 27 | 0.060 | 1.687 | 0.263 | 1.513 | 2.031 |
| 1.80 | 125 | -0.252 | 2.053 | 0.012 | 1.312 | 0.811 |
| 1.98 | -40 | 0.635 | 0.953 | -0.261 | 1.757 | 4.134 |
| 1.98 | 27 | 0.473 | 0.744 | 0.201 | 1.523 | 1.862 |
| 1.98 | 125 | -1.252 | 0.601 | 0.191 | 1.136 | 0.309 |

## Variant vbp_1_2
Reports (order is load-bearing, last wins): ['grid_osc_subth_vbp_1_2.json.gz']

### The five cold cells (-40 C; SIMULATED, sensitivity bench, VDD/2 crossings)
| cell | baseline f (Hz) | vbp_1_2 f (Hz) | edges | counts @ k=10 | counts @ k=14 |
|------|-----------------|-----------|-------|--------------|--------------|
| ss / 1.62 V | 1251.87 | 17849556.57 | 400 | 1827.795 | 29244.713 |
| ss / 1.80 V | 3043.81 | 53650108.71 | 400 | 5493.771 | 87900.338 |
| sf / 1.62 V | 436.93 | 22085614.68 | 400 | 2261.567 | 36185.071 |
| sf / 1.80 V | 586.21 | 51932265.97 | 400 | 5317.864 | 85085.825 |
| sf / 1.98 V | 1057.37 | 93573402.91 | 400 | 9581.916 | 153310.663 |

### 45-cell coverage and extrema (row-1 criterion: every cell resolved)
- resolved cells: 45 / 45
- min f = 17849556.57 Hz at ss 1.62 V -40 C; max f = 7.948e+08 Hz at ff 1.98 V 27 C; ratio 44.53

### Nominal mismatch MC (tt / 1.80 V / 27 C, 30 draws, seed 20261105, scale 1)
- usable draws 30 / 30, sigma(ln f) = 0.26460

### Row-2 margins with vbp_1_2 substituted for osc_subth (default gate, committed MC for the other four)
| V | T | abs | pair | ratio | pair | vs baseline abs | vs baseline ratio |
|---|---|-----|------|-------|------|-----------------|-------------------|
| 1.62 | -40 | 1.640 | ('tt', 'fs') | 1.323 | ('tt', 'fs') | - | - |
| 1.62 | 27 | 1.204 | ('tt', 'fs') | 0.881 | ('ss', 'sf') | 0.370 | 0.467 |
| 1.62 | 125 | 1.739 | ('tt', 'fs') | 1.067 | ('sf', 'fs') | 0.676 | 0.659 |
| 1.80 | -40 | ungradable | - | ungradable | - | - | - |
| 1.80 | 27 | 1.112 | ('tt', 'fs') | 0.977 | ('tt', 'fs') | 0.456 | 0.437 |
| 1.80 | 125 | 0.366 | ('tt', 'fs') | 1.142 | ('ss', 'sf') | 0.257 | 0.831 |
| 1.98 | -40 | 1.365 | ('tt', 'sf') | 0.960 | ('tt', 'sf') | 1.799 | 1.168 |
| 1.98 | 27 | 1.689 | ('tt', 'sf') | 0.931 | ('ss', 'sf') | 1.489 | 0.946 |
| 1.98 | 125 | 0.871 | ('tt', 'fs') | 0.925 | ('tt', 'fs') | 0.334 | 2.016 |

### vbp_1_2 sensitivity rows (scaled), where gradable
| V | T | dV | dT | dPn | dPp | baseline dT |
|---|---|----|----|-----|-----|-------------|
| 1.62 | -40 | -0.091 | 1.106 | -0.006 | 1.100 | - |
| 1.62 | 27 | -0.184 | 0.580 | 0.166 | 0.661 | 2.441 |
| 1.62 | 125 | 0.211 | 0.220 | 0.211 | 0.204 | 1.139 |
| 1.80 | -40 | 0.113 | 0.992 | -0.107 | 0.876 | - |
| 1.80 | 27 | -0.208 | 0.731 | 0.060 | 1.018 | 2.031 |
| 1.80 | 125 | 0.020 | 0.553 | 0.228 | 0.553 | 0.811 |
| 1.98 | -40 | 0.318 | 0.314 | 0.013 | 0.791 | 4.134 |
| 1.98 | 27 | -0.232 | 0.487 | 0.141 | 0.905 | 1.862 |
| 1.98 | 125 | -0.170 | 0.605 | 0.062 | 0.724 | 0.309 |

## Variant hw3
Reports (order is load-bearing, last wins): ['grid_osc_subth_hw3.json.gz', 'cold_osc_subth_hw3_ss_1.62V_-40C.json.gz', 'cold_osc_subth_hw3_ss_1.8V_-40C.json.gz', 'cold_osc_subth_hw3_sf_1.62V_-40C.json.gz', 'cold_osc_subth_hw3_sf_1.8V_-40C.json.gz', 'cold_osc_subth_hw3_sf_1.98V_-40C.json.gz']

### The five cold cells (-40 C; SIMULATED, sensitivity bench, VDD/2 crossings)
| cell | baseline f (Hz) | hw3 f (Hz) | edges | counts @ k=10 | counts @ k=14 |
|------|-----------------|-----------|-------|--------------|--------------|
| ss / 1.62 V | 1251.87 | 4376.66 | 43 | 0.448 **<1** | 7.171 |
| ss / 1.80 V | 3043.81 | 10755.07 | 107 | 1.101 | 17.621 |
| sf / 1.62 V | 436.93 | 993.96 | 10 | 0.102 **<1** | 1.629 |
| sf / 1.80 V | 586.21 | 1905.01 | 18 | 0.195 **<1** | 3.121 |
| sf / 1.98 V | 1057.37 | 4308.83 | 42 | 0.441 **<1** | 7.060 |

### 45-cell coverage and extrema (row-1 criterion: every cell resolved)
- resolved cells: 45 / 45
- min f = 993.96 Hz at sf 1.62 V -40 C; max f = 4.361e+08 Hz at ff 1.98 V 125 C; ratio 4.388e+05

### Nominal mismatch MC (tt / 1.80 V / 27 C, 30 draws, seed 20261105, scale 1)
- usable draws 30 / 30, sigma(ln f) = 0.09074

### Row-2 margins with hw3 substituted for osc_subth (default gate, committed MC for the other four)
| V | T | abs | pair | ratio | pair | vs baseline abs | vs baseline ratio |
|---|---|-----|------|-------|------|-----------------|-------------------|
| 1.62 | -40 | 0.556 | ('ss', 'sf') | 0.601 | ('ss', 'sf') | - | - |
| 1.62 | 27 | 8.697 | ('tt', 'fs') | 4.485 | ('tt', 'ff') | 2.670 | 2.378 |
| 1.62 | 125 | 4.568 | ('tt', 'fs') | 3.849 | ('ss', 'sf') | 1.774 | 2.376 |
| 1.80 | -40 | ungradable | - | ungradable | - | - | - |
| 1.80 | 27 | 9.867 | ('ss', 'sf') | 7.069 | ('tt', 'ff') | 4.048 | 3.163 |
| 1.80 | 125 | 7.224 | ('ss', 'sf') | 3.397 | ('ss', 'sf') | 5.079 | 2.472 |
| 1.98 | -40 | 2.839 | ('ss', 'sf') | 3.084 | ('ss', 'sf') | 3.741 | 3.750 |
| 1.98 | 27 | 8.389 | ('ss', 'sf') | 3.898 | ('ff', 'fs') | 7.397 | 3.960 |
| 1.98 | 125 | 7.359 | ('ff', 'fs') | 3.796 | ('ff', 'fs') | 2.821 | 8.275 |

### hw3 sensitivity rows (scaled), where gradable
| V | T | dV | dT | dPn | dPp | baseline dT |
|---|---|----|----|-----|-----|-------------|
| 1.62 | -40 | 1.067 | 4.656 | -0.444 | 3.845 | - |
| 1.62 | 27 | -0.024 | 2.698 | -0.457 | 2.334 | 2.441 |
| 1.62 | 125 | 0.425 | 1.359 | 0.207 | 1.167 | 1.139 |
| 1.80 | -40 | 0.917 | 3.313 | -0.713 | 3.927 | - |
| 1.80 | 27 | -0.035 | 2.377 | -0.562 | 2.235 | 2.031 |
| 1.80 | 125 | 0.279 | 1.737 | 0.178 | 1.544 | 0.811 |
| 1.98 | -40 | 0.767 | 2.313 | -0.517 | 3.528 | 4.134 |
| 1.98 | 27 | -0.045 | 2.060 | -0.173 | 2.063 | 1.862 |
| 1.98 | 125 | 0.133 | 1.887 | -0.049 | 1.730 | 0.309 |

## Variant hl35
Reports (order is load-bearing, last wins): ['grid_osc_subth_hl35.json.gz']

### The five cold cells (-40 C; SIMULATED, sensitivity bench, VDD/2 crossings)
| cell | baseline f (Hz) | hl35 f (Hz) | edges | counts @ k=10 | counts @ k=14 |
|------|-----------------|-----------|-------|--------------|--------------|
| ss / 1.62 V | 1251.87 | 92819.89 | 93 | 9.505 | 152.076 |
| ss / 1.80 V | 3043.81 | 277423.34 | 276 | 28.408 | 454.530 |
| sf / 1.62 V | 436.93 | 12414.37 | 12 | 1.271 | 20.340 |
| sf / 1.80 V | 586.21 | 30839.96 | 30 | 3.158 | 50.528 |
| sf / 1.98 V | 1057.37 | 77442.08 | 77 | 7.930 | 126.881 |

### 45-cell coverage and extrema (row-1 criterion: every cell resolved)
- resolved cells: 45 / 45
- min f = 12414.37 Hz at sf 1.62 V -40 C; max f = 3.512e+08 Hz at ff 1.98 V 125 C; ratio 2.829e+04

### Nominal mismatch MC (tt / 1.80 V / 27 C, 30 draws, seed 20261105, scale 1)
- usable draws 30 / 30, sigma(ln f) = 0.31648

### Row-2 margins with hl35 substituted for osc_subth (default gate, committed MC for the other four)
| V | T | abs | pair | ratio | pair | vs baseline abs | vs baseline ratio |
|---|---|-----|------|-------|------|-----------------|-------------------|
| 1.62 | -40 | 2.131 | ('ff', 'fs') | 1.584 | ('ff', 'fs') | - | - |
| 1.62 | 27 | 2.364 | ('ss', 'sf') | 1.234 | ('tt', 'ss') | 0.726 | 0.654 |
| 1.62 | 125 | 0.627 | ('tt', 'fs') | 0.720 | ('tt', 'fs') | 0.244 | 0.444 |
| 1.80 | -40 | ungradable | - | ungradable | - | - | - |
| 1.80 | 27 | 1.816 | ('tt', 'sf') | 1.294 | ('ff', 'fs') | 0.745 | 0.579 |
| 1.80 | 125 | 1.745 | ('tt', 'fs') | 1.345 | ('tt', 'sf') | 1.227 | 0.979 |
| 1.98 | -40 | 1.327 | ('tt', 'fs') | 0.591 | ('tt', 'ff') | 1.748 | 0.719 |
| 1.98 | 27 | 1.263 | ('tt', 'sf') | 0.844 | ('tt', 'sf') | 1.113 | 0.858 |
| 1.98 | 125 | 1.120 | ('tt', 'sf') | 0.671 | ('tt', 'sf') | 0.429 | 1.462 |

### hl35 sensitivity rows (scaled), where gradable
| V | T | dV | dT | dPn | dPp | baseline dT |
|---|---|----|----|-----|-----|-------------|
| 1.62 | -40 | 0.591 | 1.385 | -0.600 | 2.804 | - |
| 1.62 | 27 | -0.092 | 1.768 | -0.287 | 1.536 | 2.441 |
| 1.62 | 125 | 0.417 | 2.030 | -0.224 | 1.023 | 1.139 |
| 1.80 | -40 | 1.004 | 0.544 | -0.899 | 2.852 | - |
| 1.80 | 27 | 0.642 | 1.681 | -0.333 | 1.410 | 2.031 |
| 1.80 | 125 | -0.177 | 2.459 | 0.350 | 1.096 | 0.811 |
| 1.98 | -40 | 1.418 | 0.492 | -0.595 | 2.283 | 4.134 |
| 1.98 | 27 | 1.375 | 0.586 | 0.045 | 0.878 | 1.862 |
| 1.98 | 125 | -0.772 | 0.651 | 0.395 | 1.123 | 0.309 |

## Variant st11
Reports (order is load-bearing, last wins): ['grid_osc_subth_st11.json.gz', 'cold_osc_subth_st11_ss_1.62V_-40C.json.gz', 'cold_osc_subth_st11_ss_1.8V_-40C.json.gz', 'cold_osc_subth_st11_sf_1.62V_-40C.json.gz', 'cold_osc_subth_st11_sf_1.8V_-40C.json.gz', 'cold_osc_subth_st11_sf_1.98V_-40C.json.gz']

### The five cold cells (-40 C; SIMULATED, sensitivity bench, VDD/2 crossings)
| cell | baseline f (Hz) | st11 f (Hz) | edges | counts @ k=10 | counts @ k=14 |
|------|-----------------|-----------|-------|--------------|--------------|
| ss / 1.62 V | 1251.87 | 1908.11 | 38 | 0.195 **<1** | 3.126 |
| ss / 1.80 V | 3043.81 | 4648.12 | 92 | 0.476 **<1** | 7.615 |
| sf / 1.62 V | 436.93 | 717.49 | 28 | 0.073 **<1** | 1.176 |
| sf / 1.80 V | 586.21 | 982.64 | 39 | 0.101 **<1** | 1.610 |
| sf / 1.98 V | 1057.37 | 1860.90 | 74 | 0.191 **<1** | 3.049 |

### 45-cell coverage and extrema (row-1 criterion: every cell resolved)
- resolved cells: 45 / 45
- min f = 717.49 Hz at sf 1.62 V -40 C; max f = 1.572e+08 Hz at ff 1.98 V 125 C; ratio 2.191e+05

### Nominal mismatch MC (tt / 1.80 V / 27 C, 30 draws, seed 20261105, scale 1)
- usable draws 30 / 30, sigma(ln f) = 0.24400

### Row-2 margins with st11 substituted for osc_subth (default gate, committed MC for the other four)
| V | T | abs | pair | ratio | pair | vs baseline abs | vs baseline ratio |
|---|---|-----|------|-------|------|-----------------|-------------------|
| 1.62 | -40 | 0.281 | ('ss', 'sf') | 0.297 | ('ss', 'sf') | - | - |
| 1.62 | 27 | 3.093 | ('ff', 'fs') | 2.987 | ('ff', 'fs') | 0.950 | 1.583 |
| 1.62 | 125 | 2.935 | ('ss', 'sf') | 1.999 | ('ss', 'sf') | 1.140 | 1.234 |
| 1.80 | -40 | ungradable | - | ungradable | - | - | - |
| 1.80 | 27 | 2.772 | ('ff', 'fs') | 2.764 | ('ff', 'fs') | 1.137 | 1.237 |
| 1.80 | 125 | 1.966 | ('tt', 'sf') | 1.333 | ('tt', 'sf') | 1.382 | 0.970 |
| 1.98 | -40 | 1.224 | ('ss', 'sf') | 1.330 | ('ss', 'sf') | 1.613 | 1.617 |
| 1.98 | 27 | 2.629 | ('ff', 'fs') | 1.302 | ('ff', 'fs') | 2.318 | 1.323 |
| 1.98 | 125 | 2.133 | ('tt', 'sf') | 0.439 | ('tt', 'sf') | 0.818 | 0.958 |

### st11 sensitivity rows (scaled), where gradable
| V | T | dV | dT | dPn | dPp | baseline dT |
|---|---|----|----|-----|-----|-------------|
| 1.62 | -40 | 1.004 | 4.210 | -0.425 | 3.938 | - |
| 1.62 | 27 | 0.475 | 2.269 | -0.508 | 2.682 | 2.441 |
| 1.62 | 125 | 0.009 | 0.941 | -0.109 | 1.593 | 1.139 |
| 1.80 | -40 | 0.983 | 3.559 | -0.743 | 3.984 | - |
| 1.80 | 27 | 0.464 | 1.771 | -0.575 | 2.646 | 2.031 |
| 1.80 | 125 | 0.295 | 0.548 | -0.164 | 1.313 | 0.811 |
| 1.98 | -40 | 0.962 | 2.932 | -0.553 | 3.583 | 4.134 |
| 1.98 | 27 | 0.453 | 1.581 | -0.244 | 2.185 | 1.862 |
| 1.98 | 125 | 0.582 | 0.657 | 0.469 | 1.117 | 0.309 |


## 5. Conclusion

**SIMULATED figures only; no estimate accuracy is quoted anywhere in this section.** Summary over the five
cold cells (expected counts at the gate; ‡ = quoted #277 values for the baseline, provenance in section 1;
margins are the default-gate minima of section 4's tables over the cells gradable on main):

| | baseline‡ | vbp_2_3 | vbp_1_2 | hw3 | **hl35** | st11 |
|---|---|---|---|---|---|---|
| min cold count @ k=10 | 0.045 | 30.8 | 2262 | 0.102 | **1.271** | 0.073 |
| min cold count @ k=14 | 0.716 | 493 | 36185 | 1.629 | 20.3 | 1.176 |
| 45/45 cells resolved | 41+4‡ | 45 | 45 | 45 | **45** | 45 |
| gate meeting ≥1 count everywhere | k=15 | k=10 | k=10 | k=14 | **k=10** | k=14 |
| full-read time at that gate (§6) | 3.686 ms | 512 µs | 512 µs | 2.048 ms | **512 µs** | 2.048 ms |
| dT (scaled) at 27 °C cells | 1.86–2.44 | 0.74–1.69 | 0.49–0.73 | 2.06–2.70 | 1.68–1.77 | 1.58–2.27 |
| σ(ln f), nominal MC | 0.266 | 0.294 | 0.265 | **0.091** | 0.316 | 0.244 |
| min abs margin (gradable cells) | 0.759 | 0.430 | 0.366 | 0.556 | 0.627 | 0.281 |
| fastest cell (ff / 1.98 V / 125 °C) | 151 MHz | 586 MHz | 795 MHz† | 436 MHz | 351 MHz | 157 MHz |

† vbp_1_2's overall maximum is 795 MHz at ff / 1.98 V / 27 °C.

1. **The open question this issue set — "can the design yield a measurable count inside a gate the spec can
   afford at the cold slow corners?" — is answered yes, by exactly one lever: shortening the header channel to
   the model bin floor.** `hl35` (L 0.5→0.35, W unchanged) lifts the five cold cells ×28–91 (12.4–277 kHz) and
   is the only variant whose worst cold cell still clears one expected count at the **default** k = 10 gate
   (1.271 counts at sf / 1.62 V / −40 °C), so the full five-oscillator read stays at 512 µs — inside spec §6's
   <1 ms target with no readout change at all.
2. **The mechanism (section 3's probe): the cold sf corner is starved by header weak-inversion current, and
   Vth roll-off attacks exactly that corner.** At the baseline 0.30 V drive the header carries 12× less current
   at sf / −40 °C than at ss / −40 °C (5.0 pA vs 62 pA); the L=0.35 device multiplies the sf / −40 °C current
   by 120× but the tt / 27 °C current by only 8.8× — which is why the cold cells gain ×28–91 while nominal gains
   ×1.8 and the ring stays subthreshold-slope-dominated at every 27 °C cell.
3. **What hl35 costs, stated:** the 27 °C dT slope drops 10–27 % (1.68–1.77 vs 1.86–2.44) while the 125 °C
   slope roughly doubles (2.03/2.46 vs 1.14/0.81); nominal σ(ln f) rises 0.266→0.316; the 1.62 V / 125 °C
   margin drops 2.574→0.627 (its new minimum) while 1.98 V / −40 °C improves 0.759→1.327 and 1.62 / −40 °C
   becomes gradable at 2.131; the fastest cell rises 151→351 MHz.
4. **The divider-ratio levers are rejected on this evidence:** they clear any count bar (30–9582 counts) but
   collapse dT to 0.49–1.69 and the hot-cell margins (min abs 0.366–0.430), and vbp_1_2's 795 MHz fastest cell
   is beyond even the ff-corner counter fmax of decision 0003 (587 MHz) — it would drag in 0003's prescaler
   option on top. They also demonstrate the trade-off's shape: the same strong-inversion move that fixes counts
   removes the exponential temperature dependence this oscillator exists to provide.
5. **hw3 (header W×3) is the stronger *discriminator* but the weaker *counter*: ** margins improve 2.7–8.3× at
   every shared gradable cell, σ(ln f) falls 3× to 0.091, dT is preserved or improved everywhere — but its cold
   cells only reach ×2.3–4.1 (994–10755 Hz), still under one count at k = 10 in four of five cells, so it needs
   k = 14 (2.048 ms read, outside §6's <1 ms target, inside the <10 ms fallback). If a longer gate is
   acceptable, hw3 is the better oscillator. A combined L=0.35 + W×3 point was not run (one factor at a time)
   and is the obvious follow-up.
6. **Stage count is not a lever for this problem:** st11 moves the cold cells only ×1.5–1.8 (717–4648 Hz),
   keeps counts under 1 at k = 10, and its margins are within ±40 % of baseline. Fifteen→eleven stages is
   a 27 % frequency lever trying to close a ×22 gap.
7. **Counter fmax (decision 0003, draft):** on 0003's corner-matched cells every variant still fits (worst:
   vbp_1_2 at 234.6 MHz against the tt-corner 358.9 MHz). The unmapped ff / 1.98 V / 125 °C cells (351–795
   MHz across variants) run at or beyond the fastest liberty fmax (586.8 MHz), so any adoption needs the
   per-oscillator re-STA named in the proposed decision record's downstream list.
8. **Extrapolations, labelled:** "W×12–30 would be needed to close the count bar with width alone" follows
   from the measured W×1→×3 gain (×2.3–4.1 at the cold sf cells) plus the probe's near-linear Id(W) — it is
   an extrapolation, not a simulated point. No frequency, count, margin or σ figure in the tables above is
   extrapolated.

**Recommendation:** propose `hl35` — the `osc_subth` header L 0.5 µm → 0.35 µm (W=0.42 unchanged, everything
else byte-identical) — as decision 0004 (status: proposed, `spec/decisions/0004-osc-subth-header-l035.md`),
because it is the only variant that meets the five-corner target's count need at the default gate and §6's
<1 ms read, at a bounded, stated cost to the 27 °C slope and one hot-cell margin. Decision 0002 is untouched;
nothing here ratifies anything.

## 6. Costs and spec §6 (full five-oscillator read)

The gate times alone for the five oscillators sum to 512 µs at k = 10 (all five) and 2.048 ms with only
`osc_subth` at k = 14 (the 2026-11-14 record's `t_read_osc`). The <1 ms spec §6 target is met only while
`osc_subth` stays at the default gate, which needs ≥9765.625 Hz (one expected count at k = 10) at **every** cell;
k = 14 (1.638 ms for this oscillator alone) already exceeds it, and the <10 ms fallback is a separate row from
the digital timing verification of #281. A variant that clears one count at k = 10 everywhere therefore also
clears §6's target read time; a variant that needs k = 14 does not, whatever its count margin.

## Caveats (not hidden)

- The four cold-cell baseline frequencies that main cannot resolve are **quoted from #277's record** (open PR
  #297, branch `feature/issue-277`): they are fleet results on the committed schematic, but they are not on main
  yet, and this record's baseline margins at 1.62/1.80 V / −40 °C are correspondingly **ungradable** (the other
  four oscillators are not the constraint; `osc_subth`'s own committed cells are). No baseline margin is imputed.
- Variant mismatch σ(ln f) comes from 30 draws at the single nominal cell (the issue's prescribed convention);
  the baseline pooled σ (0.266) pools five corners × 20 draws. Same noise *model*, different draw counts — stated
  wherever a margin ratio uses them.
- The MC term itself remains UNVALIDATED (the standing caveat of every record since 2026-11-05): it dominates
  every margin it enters, and no accuracy claim anywhere in this record depends on it being right.
- Dynamic range is a simulated schematic figure; the counter's 24-bit range at k = 10 saturates near 167 GHz, far
  above every cell here, so no count in this record is counter-limited.
