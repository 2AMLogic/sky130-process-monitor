# sim/pex — post-layout re-verification, analog (T1 item 7, issue #32)

**SIMULATED only (ngspice 46 on the batch fleet, sky130A `open_pdks f6eeac7d…`); nothing here is measured.**
Evidence for `7.analog`: `klt pex` reports (`klt 0.9.2.dev460+g1c0ae85debd3`) that re-run the #29 45-cell
PVT-box grid (5 process × 1.62/1.80/1.98 V × −40/27/125 °C) on the schematic and on the layout-extracted
netlist of each oscillator and report the per-corner schematic-vs-extracted delta.

**Result: `7.analog` is NOT met.** `klt signoff` grades it `unmet` (`check_failed`), and the evidence is
incomplete for two independent reasons (below). Nothing was relaxed; the failing and missing rows are the result.

## Files

| Path | What |
|---|---|
| `gen_requests.py` | writes `requests/*.json` (the #29 `grid_<osc>.json` with only the testbench body swapped) and `osc/osc_hd_dut.spice`. Deterministic |
| `osc/tb_<osc>.spice` | testbench bodies, one `.include` each as `klt pex` requires. `osc_hd_dut.spice` is generated (see "osc_hd pin order") |
| `requests/<osc>.json` | `klt pex` testbench requests (`batch.capacity_wait_s: 600`) |
| `extracted/<osc>.spice` | the extracted netlists (`klt extract --parasitics`, deck `sky130`, `--pdk sky130A`) |
| `records/2026-11-10-<osc>.pex.report.json` | the `klt pex` reports (append-only; a re-run is a new dated file) |
| `records/2026-11-10-osc_subth.pex-submit.json` | the submit manifest of the `osc_subth` run that did not complete |

Reproduce one oscillator (fleet; never hand-launched ngspice):

    klt pex layout/osc_bank.gds sim/pex/requests/osc_nmos.json --deck sky130 --pdk sky130A --top osc_nmos \
        --pins en,out,vdd,vss --backend batch --submit-only -o sim/pex/extracted/osc_nmos.spice --outdir <dir>
    klt pex --attach <dir>/pex-submit.json --envelope-out <report.json> --format json

`osc_hd` additionally takes `--rename-declared-pins`. Extraction fields disclosed in every report:
`extraction.model` (lumped RC: net-to-ground area/perimeter, vertical-overlap coupling, one lumped series
R per net as a star, quasi-static; no lateral coupling because no `--critical-net` was named) and
`body_bias.status = biased` (0 unbiased devices) for all five extractions.

## Result (per-cell delta of the measured quantity, extracted vs schematic)

The measurement is the #29 `t_rise` crossings measurement on `v(out)` at VDD/2 over a fixed `.tran` window
(`cap` 400). `klt pex` reports one scalar per cell; its values (e.g. 177 vs 139) are consistent with the
number of rising crossings inside the window, i.e. a quantised frequency proxy. That reading is inferred from
the data, not from `docs/cli/sim.md`. Negative delta = fewer crossings = slower extracted ring.

| Oscillator | pex status | cells with a delta | delta % min / median / max | min at / max at | devices/nets | extracted netlist sha256 |
|---|---|---|---|---|---|---|
| `osc_hd` | pass | 45/45 | −21.9 / −14.2 / −5.9 | fs/1.98 V/125 C / sf/1.62 V/−40 C | 64/35 | `06e20067…` |
| `osc_nmos` | error | 44/45 | −24.0 / −21.4 / −19.0 | fs/1.98 V/−40 C / sf/1.98 V/125 C | 64/35 | `68b62d0e…` |
| `osc_pmos` | pass | 45/45 | −27.2 / −24.0 / −21.6 | tt/1.80 V/−40 C / fs/1.80 V/125 C | 64/35 | `3ace67c3…` |
| `osc_wire` | error | 44/45 | −26.8 / −16.6 / +6.6 | tt/1.80 V/−40 C / ff/1.98 V/125 C | 64/35 | `76c8872a…` |
| `osc_subth` | **no result** | 0/45 | — | — | 46/34 | `73f06dc4…` |

"pass" means every extracted-side measurement ran inside its declared limits; the request declares no
delta threshold, so **no pass/fail verdict on the size of the delta is made or implied** here. The spec
rows' frequency-window limits (#29) have not been re-graded on the extracted values; that is not done in this PR.

## What is missing or not comparable (findings, not relaxed)

1. **`osc_subth` has no result.** Its schematic leg (job `klt-sim-6aff7841c09f`, extracted leg
   `klt-sim-c37d82e8c234`; 2 ms windows, 50-420 s per unit in #29) was still running after ~70 min of
   polling, past the fleet's 3600 s whole-job ceiling, so the run is recorded as incomplete. A re-run needs
   `request.remote.hosts >= 45` (one unit per shard) or a scoped corner set; either is a new dated record.
2. **Two schematic-side cells did not converge** (`osc_nmos` tt/1.80 V/−40 C and `osc_wire` sf/1.98 V/−40 C,
   `timestep_too_small`); the extracted leg did converge at both (159 and 156). They have no delta and make
   the report `error`. #29 already records the cold-cell convergence trouble for these oscillators.
3. **`osc_wire` and `osc_subth` extractions are not the item-1 netlist** (see `lvs/README.md`): the 31 × 100 fF
   shunt capacitors and the `Rb0`/`Rb1` bias divider are not drawn, and the met1 serpentine is plain metal to
   the extractor. The `osc_wire` delta therefore under-states the schematic's own wire load and is not a
   like-for-like layout effect. `osc_subth`'s `vbp` is an undriven net in the extraction.
4. **`osc_hd` pin order.** `klt pex --pins` does not reorder the extracted subcircuit: it comes out as
   `out en vss vdd` (label order) against the schematic `en out vdd vss`, which `klt pex` refuses
   (`pin_order_mismatch`). `osc/osc_hd_dut.spice` therefore wraps the unmodified schematic under the extracted
   pin order (only its subcircuit name changes, `osc_hd` → `osc_hd_sch`). `klt pex` reports a `model_mismatch`
   for `osc_hd` (hierarchical reference vs flat extraction: one extra `X` card); the devices are identical.
5. **Model-set scope.** One extraction (no `--critical-net`, no lateral coupling, quasi-static lumped RC)
   and one PDK build (`f6eeac7d…`; `sim/pdk.json` pins `c6d73a35…`). The fleet runner stamps its own PDK
   (`environment.remote.worker_environment.pdk`); the client-side stamp is not comparable.

## Re-run 2026-11-11: `osc_subth` full box, sharded (still no usable result)

SIMULATED only (ngspice on the batch fleet; `klt 0.9.2.dev596+g97e73934a9f4`). Record:
`records/2026-11-11-osc_subth.pex.report.json` (sha256 `896c1fa7…`; append-only, the 2026-11-10 files are untouched).
Command (one clean run, one `--hosts` value, `batch.capacity_wait_s: 600` from the request, no `--resume`):

    klt pex layout/osc_bank.gds sim/pex/requests/osc_subth.json --deck sky130 --pdk sky130A --top osc_subth \
        --pins en,out,vdd,vss --backend batch --hosts 45 -o <dir>/osc_subth.spice --outdir <dir> \
        --envelope-out <report.json> --format json

**Result: report `error`, 2/45 cells with a delta, 43/45 errored. `7.analog` is still NOT met.**

| Cause (per cell) | Cells |
|---|---|
| fleet `lost_shard`: launch refused, vCPU budget (`BATCH_MAX_VCPU=224`) exhausted | 31 |
| extracted leg: ngspice did not complete within the 3000 s unit limit | 8 |
| schematic leg: Spot job `interrupted` | 4 |
| both legs errored | 9 (incl. above) |

The two cells that did produce a delta (`ss/1.62 V/−40 C`: 2 vs 341999; `ss/1.62 V/27 C`: 173 vs 287334) are
**not valid comparisons** and must not be read as frequency deltas. See finding 6.

6. **`osc_subth` extraction is not like-for-like (device models).** `klt pex` reports `model_mismatch`: the schematic
   has 14 `sky130_fd_pr__pfet_01v8_lvt`, the extracted netlist has 0 (those devices extract as plain
   `pfet_01v8`, 16 → 30). The layout carries no LVT marker geometry, so the extractor cannot recognise them.
   Re-running the grid will not fix this: the layout needs the LVT marker (#23's domain) before any `osc_subth`
   delta means anything. This, not fleet capacity, is the blocker for `osc_subth`.

Not done in this increment (no fleet headroom for another full run, no local grid by host rule): a converged
schematic leg for `osc_nmos` tt/1.80 V/−40 C and `osc_wire` sf/1.98 V/−40 C; grading extracted values against the
#29 frequency-window limits; any change to `manifests/`. `klt signoff` still grades `T1 #7 [analog]` `unmet`
(`check_failed`); `T1 #7 [digital]` is MET.

## Increment 2026-11-11 (issue #32): grading, the two cold cells, signoff

SIMULATED only. Records are new dated files under `records/`; nothing earlier was edited. No spec threshold was
touched and no local ngspice grid was run (two single-corner `klt pex` probes ran locally, which the host rules allow).

### Grading the extracted values (`grade_pex.py`, `records/2026-11-11-grade-extracted-values.json`)

    python3 -I sim/pex/grade_pex.py <out.json> records/2026-11-10-osc_{hd,nmos,pmos,wire}.pex.report.json

- **#29 row 1 (oscillates), extracted side: met for `osc_hd`, `osc_nmos`, `osc_pmos`, `osc_wire` at all 45 cells.**
  The criterion needs at least 9 rising edges (3 dropped start-up edges + 5 cycles + 1); the smallest extracted
  count is 70 (`osc_nmos`). This is the extracted leg only. `osc_subth` has no valid extraction (finding 6).
- **The #29 frequency limits cannot be applied to the pex values, so rows 2-4 are NOT re-graded.** The pex scalar is a quantised
  rising-edge count in an 800 ns window and the report carries no crossing times, so #29's
  `f_osc = (n-1)/(t_last - t_first)` cannot be reproduced. #29 has no per-cell frequency window either: its limits are
  row 1 (oscillates), row 2 (five-corner identification in ln-ratio space), row 3 (V, ±20/50 mV) and row 4 (T, ±5/10 C).
  Rows 2-4 need all five oscillators' frequencies, and `osc_subth` has none. The record gives a count-based frequency
  proxy (counts/800 ns, 81-334 MHz across the four, start-up bias up to ~6 %) labelled as a proxy only.
- **What the layout does to the row-2 coordinate** (ln f_i − ln f_osc_hd, extracted vs schematic, from counts; percent
  change in f_i/f_osc_hd): `osc_nmos` median −7.8 % (−17.6 … +0.7), `osc_pmos` median −10.9 % (−19.8 … −0.2),
  `osc_wire` median −1.6 % (−21.5 … +32.2; not like-for-like, finding 3). These are shifts of the classifier inputs;
  a recalibration on extracted data is needed before any post-layout row-2 claim. No claim is made here.

### The two non-converged cold cells (`records/2026-11-11-osc_{nmos,wire}-coldcell-*.pex.report.json`)

Single-unit local `klt pex` runs (`klt 0.9.2.dev599`, ngspice 46), requests `requests/osc_{nmos,wire}_coldcell.json`.
1. Default solver, `tran 20p 800n 0 10p` (tmax capped): the schematic leg still hits `timestep_too_small` at
   `osc_nmos` tt/1.80 V/−40 C and `osc_wire` sf/1.98 V/−40 C (`*-coldcell-tmax10p`; their request file was later
   edited to the relaxed bench, so the committed request is the second variant).
2. Same bench plus `.options reltol=0.01 gmin=1e-10 method=gear` (`osc/tb_*_relaxed.spice`, the option set #69 used):
   both converge. `osc_nmos`: 204 vs 158, −22.5 %. `osc_wire`: 68 vs 50, −26.5 %.

Caveats: the relaxed solver changes the numerics for these two cells only, so the counts are not interchangeable with
the other 44 cells'; the `osc_nmos` extracted netlist is the committed one (sha256 `68b62d0e…`), but the local klt
re-extracted `osc_wire` to a different netlist (`09374950…`, committed as `extracted/osc_wire.dev599.spice`, same
structure, different numbers) because the installed `klt` is newer than the one that produced `76c8872a…`. The `osc_wire` cell
is therefore a different extraction build and, like the rest of `osc_wire`, not like-for-like (finding 3).
The 2026-11-10 reports are not amended: they still read `error` with 44/45 cells.

### Signoff

`klt signoff --manifest manifests/sky130-process-monitor.json`: `T1 #7 [analog]` stays **UNMET** (`check_failed`);
`T1 #7 [digital]` MET. The manifest already cites `7.analog`; no citation was added, because the cited reports are
`error`/incomplete (`osc_nmos`, `osc_wire`: one cell each, now covered by the supplementary cold-cell records above but
not merged into those reports; `osc_subth`: no valid extraction). Remaining to close `7.analog`: the `osc_subth` LVT
marker layout fix (#98), then one clean sharded `osc_subth` run.
