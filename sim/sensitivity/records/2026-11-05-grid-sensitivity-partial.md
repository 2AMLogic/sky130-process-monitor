# 2026-11-05 — five-oscillator frequency grid and sensitivity matrix (PARTIAL: no Monte Carlo)

**SIMULATED. Schematic-level netlists, no layout/parasitics. Nothing measured. No estimate accuracy is quoted.**
Append-only: a re-run is a new dated file.

## Provenance
- Testbenches: `sim/sensitivity/osc/tb_osc_*.spice` (reusing `design/osc_bank/*.spice`); requests `sim/sensitivity/requests/grid_*.json`.
- Backend: `klt sim --batch-set` on the batch fleet (job ids in `environment.remote.job_id` of each report in `records/reports/`). Runner ngspice-46 (`/usr/local/bin/ngspice`), sky130A, open_pdks `c6d73a35` (`sim/pdk.json`), klt runner 0.9.0.
- Frequency table = `analyze.py extract records/reports/grid_*.json.gz`; report = `analyze.py report freq.json` (reproduces everything below).

## sf/fs mapping (local single-corner probe, `probe_skew.sh`, DC op point, 1/0.15 um fets, |Vgs|=|Vds|=0.9 V, 27 C)
| corner | Id nfet (uA) | Id pfet (uA) |
|---|---|---|
| tt | 33.77 | 11.96 |
| sf | 74.34 | 3.00 |
| fs | 11.52 | 31.87 |

**sf = NMOS-fast / PMOS-slow; fs = NMOS-slow / PMOS-fast.** (Resolves the "not confirmed" item in the spec.)

## Results
- 225 grid cells (5 osc x 5 corners x 3 V x 3 T); 7 cells missing (no/short oscillation, reported missing, never interpolated):
  osc_nmos tt/1.8 V/-40 C; osc_subth ss/1.62, ss/1.8, sf/1.62, sf/1.8, sf/1.98 at -40 C; osc_wire sf/1.98 V/-40 C.
- Per (V,T) cell the report below gives the sensitivity matrices, singular values, kappa and rank, absolute and ratio-only,
  with column scaling V x 0.18, T x 82.5, Pn/Pp = corner extent +-1.
- Full 5x4 matrices form in 5 of 9 (V,T) cells (count printed by `analyze.py report`, see the "formed (V,T) cells" line below): absolute kappa 27.8 to 67.9; ratio-only kappa 19.8 to 67.9 (rank 4/4 in all).
  The three -40 C cells and V=1.8/27 C cannot be formed because of the missing cells above.
- The subthreshold oscillator has under 100 counts in the default gate (2^10 @ 10 MHz) in 10 cells: quantization dominates there.

## NOT done in this record
- Mismatch Monte Carlo (acceptance step 5) and so the discrimination margin (step 6): the fleet repeatedly interrupted spot
  instances (77 interruptions, about 7 of 20 shards done after ~75 min). No local fallback was run.
- The Q1 verdict is therefore **not** proposed here.

## Full report output
```
# Sensitivity report (SIMULATED, schematic-level, tt/ff/ss/sf/fs x 3 V x 3 T; nothing measured)
# columns scaled by box half-range: V*0.18, T*82.5, Pn/Pp = corner extent (+-1)
# cells: 225, missing (no/short oscillation): 7
#   MISSING ('osc_nmos', 'tt', 1.8, -40)
#   MISSING ('osc_subth', 'ss', 1.62, -40)
#   MISSING ('osc_subth', 'ss', 1.8, -40)
#   MISSING ('osc_subth', 'sf', 1.62, -40)
#   MISSING ('osc_subth', 'sf', 1.8, -40)
#   MISSING ('osc_subth', 'sf', 1.98, -40)
#   MISSING ('osc_wire', 'sf', 1.98, -40)

## cell V=1.62 T=-40
missing oscillators here: ['osc_nmos', 'osc_subth'] -> absolute matrix not formed

## cell V=1.62 T=27
absolute ln f (5x4):
                     V           T          Pn          Pp
osc_hd         0.21283     0.03765     0.14680     0.26566
osc_nmos       0.19133    -0.12890     0.15157     0.18481
osc_pmos       0.32564     0.13491     0.11248     0.25355
osc_wire       0.15035    -0.06307     0.05532     0.13712
osc_subth      0.49060     2.44094    -0.45383     2.71197
  singular values: 3.73 0.5671 0.1357 0.05495
  kappa=67.9  rank=4/4
ratio-only ln f_i - ln f_hd (4x4):
                     V           T          Pn          Pp
osc_nmos      -0.02150    -0.16654     0.00477    -0.08085
osc_pmos       0.11281     0.09726    -0.03432    -0.01211
osc_wire      -0.06248    -0.10072    -0.09148    -0.12854
osc_subth      0.27776     2.40329    -0.60063     2.44631
  singular values: 3.501 0.144 0.1269 0.05158
  kappa=67.9  rank=4/4

## cell V=1.62 T=125
absolute ln f (5x4):
                     V           T          Pn          Pp
osc_hd         0.17823     0.02659     0.16577     0.23783
osc_nmos       0.16629    -0.10855     0.15700     0.19374
osc_pmos       0.28012     0.12851     0.10090     0.26030
osc_wire       0.10592    -0.06174     0.05075     0.09767
osc_subth      0.10109     1.13939    -0.19506     1.55969
  singular values: 1.98 0.5065 0.1364 0.05841
  kappa=33.9  rank=4/4
ratio-only ln f_i - ln f_hd (4x4):
                     V           T          Pn          Pp
osc_nmos      -0.01194    -0.13514    -0.00878    -0.04409
osc_pmos       0.10189     0.10192    -0.06487     0.02246
osc_wire      -0.07231    -0.08832    -0.11502    -0.14017
osc_subth     -0.07714     1.11280    -0.36084     1.32185
  singular values: 1.778 0.1696 0.1382 0.06527
  kappa=27.2  rank=4/4

## cell V=1.80 T=-40
missing oscillators here: ['osc_nmos', 'osc_subth'] -> absolute matrix not formed

## cell V=1.80 T=27
missing oscillators here: ['osc_nmos'] -> absolute matrix not formed

## cell V=1.80 T=125
absolute ln f (5x4):
                     V           T          Pn          Pp
osc_hd         0.15618    -0.00254     0.15281     0.21188
osc_nmos       0.15017    -0.12963     0.13518     0.19114
osc_pmos       0.23302     0.09019     0.11749     0.22661
osc_wire       0.08907    -0.09914     0.04391     0.08216
osc_subth      0.32518     0.81149    -0.01422     1.11177
  singular values: 1.464 0.4294 0.1086 0.05267
  kappa=27.8  rank=4/4
ratio-only ln f_i - ln f_hd (4x4):
                     V           T          Pn          Pp
osc_nmos      -0.00601    -0.12709    -0.01763    -0.02074
osc_pmos       0.07684     0.09273    -0.03532     0.01474
osc_wire      -0.06712    -0.09660    -0.10890    -0.12972
osc_subth      0.16899     0.81403    -0.16704     0.89989
  singular values: 1.253 0.1395 0.1061 0.06324
  kappa=19.8  rank=4/4

## cell V=1.98 T=-40
missing oscillators here: ['osc_nmos', 'osc_wire', 'osc_subth'] -> absolute matrix not formed

## cell V=1.98 T=27
absolute ln f (5x4):
                     V           T          Pn          Pp
osc_hd         0.16487    -0.02757     0.12917     0.20021
osc_nmos       0.15093    -0.16157     0.10551     0.17580
osc_pmos       0.28142     0.00596     0.12057     0.16732
osc_wire       0.10938    -0.13322     0.04415     0.10398
osc_subth      1.14595     1.86244    -0.38873     2.19349
  singular values: 3.134 0.491 0.1243 0.06244
  kappa=50.2  rank=4/4
ratio-only ln f_i - ln f_hd (4x4):
                     V           T          Pn          Pp
osc_nmos      -0.01394    -0.13399    -0.02366    -0.02441
osc_pmos       0.11655     0.03354    -0.00860    -0.03288
osc_wire      -0.05549    -0.10564    -0.08501    -0.09623
osc_subth      0.98109     1.89002    -0.51789     1.99329
  singular values: 2.968 0.1297 0.1171 0.06984
  kappa=42.5  rank=4/4

## cell V=1.98 T=125
absolute ln f (5x4):
                     V           T          Pn          Pp
osc_hd         0.13414    -0.02841     0.14205     0.19134
osc_nmos       0.13405    -0.14384     0.11628     0.18911
osc_pmos       0.18591     0.00979     0.11294     0.20122
osc_wire       0.07221    -0.13043     0.03789     0.06925
osc_subth      0.54926     0.30917     0.48787     1.10564
  singular values: 1.434 0.2727 0.06312 0.03847
  kappa=37.3  rank=4/4
ratio-only ln f_i - ln f_hd (4x4):
                     V           T          Pn          Pp
osc_nmos      -0.00009    -0.11543    -0.02577    -0.00223
osc_pmos       0.05178     0.03821    -0.02911     0.00988
osc_wire      -0.06192    -0.10202    -0.10416    -0.12209
osc_subth      0.41513     0.33758     0.34582     0.91430
  singular values: 1.131 0.126 0.06749 0.02667
  kappa=42.4  rank=4/4

## formed (V,T) cells: absolute 5 of 9, ratio-only 5 of 9

## cells with < 100 counts in the default gate (2^10 @ 10 MHz): quantization dominates
  osc_subth tt 1.62 V -40 C: 5.23 counts
  osc_subth tt 1.80 V -40 C: 13.12 counts
  osc_subth tt 1.98 V -40 C: 31.86 counts
  osc_subth ss 1.62 V 27 C: 8.80 counts
  osc_subth ss 1.80 V 27 C: 20.27 counts
  osc_subth ss 1.98 V -40 C: 0.77 counts
  osc_subth ss 1.98 V 27 C: 43.12 counts
  osc_subth sf 1.62 V 27 C: 1.92 counts
  osc_subth sf 1.80 V 27 C: 3.79 counts
  osc_subth sf 1.98 V 27 C: 7.93 counts
```
