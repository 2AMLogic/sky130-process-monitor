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
| `gen_requests.py` | writes **everything in `osc/` and `requests/<osc>.json`**: the #29 `grid_<osc>.json` with only the testbench body swapped, and the bench bodies themselves derived from `sim/sensitivity/osc/`. Deterministic; a re-run must leave `git status --porcelain sim/pex` empty |
| `osc/tb_<osc>.spice`, `osc/tb_<osc>_relaxed.spice`, `osc/osc_hd_dut.spice` | GENERATED, do not edit. Derived from `sim/sensitivity/osc/tb_<osc>.spice` so the pex leg runs the #29 circuit and no second copy exists (issue #137): the line-2 provenance comment is swapped (except `osc_hd`, whose committed bench keeps the sensitivity wording and is reproduced as committed), `osc_hd` gets the one `.include` `klt pex` requires plus the extracted pin order (see "osc_hd pin order"), and `_relaxed` appends the #69 solver options. `sim/pex/test_gen_requests.py` (in `npm test`) fails if a committed file stops matching |
| `requests/<osc>.json` | `klt pex` testbench requests (`batch.capacity_wait_s: 600`). GENERATED |
| `requests/osc_{nmos,wire}_coldcell.json` | hand-written single-cell follow-up requests, not emitted by the generator (see "The two non-converged cold cells") |
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

   **Correction (2026-11-11, #98): the "no LVT marker geometry" premise above is wrong.** The layout already
   draws the marker: `layout/gen/gen_osc_bank.py` defines `lvtn` as GDS layer (125, 44) and emits one `lvtn`
   rectangle per LVT header gate (14 shapes; see lines 180-181). The extraction deck used by klt does not model
   the sky130 1.8 V LVT flavours, so those devices still extract as plain `pfet_01v8` even with the marker
   present. This is a tool gap, filed as 2AMLogic/klayout-tools#5283. No layout change is needed or wanted:
   do not redraw the LVT marker. The `osc_subth` extracted-versus-schematic deltas stay **not comparable**, and
   the #32 `osc_subth` re-run is deferred, until that klt fix lands. The `osc_subth` LVS `match`
   (`lvs/osc_subth.report.json`) does not cover the LVT flavour: it is a `match` only because its `device_map`
   collapses `pfet_01v8_lvt` to `pfet`, so it says nothing about whether the LVT marker is electrically correct.
   The recorded `records/*.pex.report.json` is append-only evidence and is unchanged.

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
  count is 65 (`osc_pmos`, ss/1.620V/-40C; `osc_nmos` is next at 70). This is the extracted leg only. `osc_subth` has no valid extraction (finding 6).
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

## Attempt 2026-11-11 (issue #32): `osc_subth` after klayout-tools#5283, extraction check and aborted grid

SIMULATED/extraction only; `klt 0.9.2.dev632+gdd128366053f`. No `osc_subth` delta was produced and
`7.analog` is still NOT met. Records are append-only; nothing earlier was edited.

1. **The LVT flavour now extracts, but not like-for-like.** `klt pex layout/osc_bank.gds --deck sky130 --pdk sky130A
   --top osc_subth --pins en,out,vdd,vss --extract-only` gives `extracted/osc_subth.dev632.spice` (sha256
   `0e0c8114…`). Device models by count:

   | | `nfet_01v8` | `pfet_01v8` | `pfet_01v8_lvt` |
   |---|---|---|---|
   | schematic `design/osc_bank/osc_subth.spice` | 16 | 16 | 14 |
   | extraction before (`extracted/osc_subth.spice`, `73f06dc4…`) | 16 | 30 | 0 |
   | extraction now (dev632) | 16 | 2 | **28** |

   The extractor now recognises LVT, but classifies 28 of the 30 PFETs as LVT where the schematic has 14.
   A grid would therefore still report `model_mismatch`. Not traced: whether the extra 14 come from the extraction deck
   (marker overlap or a classification rule) or from the drawn `lvtn` geometry. That needs a look at the marker
   shapes against the other 16 PFET gates before any layout change or tool issue is filed.
2. **Grid not completed.** `klt pex ... --backend batch --hosts 45 --wait-for-capacity 600 --submit-only` ran into the
   580 s wall clock after 34 of its schematic-side shard submissions and wrote no `pex-submit.json`
   (the sharded `--submit-only` gap, 2AMLogic/klayout-tools#5280). The 34 submitted jobs are orphaned
   (no manifest to attach to). Given finding 1 the grid was not retried: it would burn fleet capacity on a result
   that is not comparable. No local ngspice grid was run (host rule).

Remaining for `7.analog`: resolve the 28-vs-14 LVT classification, then one clean sharded `osc_subth` run.

## Attempt 2026-11-11 (issue #32, second): 28-vs-14 LVT traced to the extractor; no grid submitted

SIMULATED/extraction only; `klt 0.9.2.dev647+g1408ffee3fa6`. `7.analog` is still NOT met (`klt signoff`: `T1 #7 [analog]`
`unmet`, `check_failed`; `[digital]` met). No `osc_subth` delta was produced. Nothing earlier was edited.

1. **Re-extraction is unchanged from dev632.** `klt pex layout/osc_bank.gds --deck sky130 --pdk sky130A --top osc_subth
   --pins en,out,vdd,vss --extract-only` gives a netlist with the same sha256 as `extracted/osc_subth.dev632.spice`
   (`0e0c8114…`): 16 `nfet_01v8`, 2 `pfet_01v8`, 28 `pfet_01v8_lvt` (schematic: 16 / 16 / 14).
2. **The drawn layout is right; the 28 is not a layout fault.** Gate-level check on `layout/osc_bank.gds`, cell `osc_subth`
   (poly ∩ diff ∩ psdm, fraction of each gate covered by `lvtn` 125/44): 30 PFET gates, 14 at 100 % covered, 16 at 0 %, none
   partial. That is the schematic's 14 LVT / 16 regular split. The `lvtn` rectangle for each series header ends at the
   centre of the diffusion column it shares with the neighbouring inverter PFET (`layout/gen/gen_osc_bank.py:180-181`), so
   it overlaps that shared source/drain region. The extractor appears to classify by marker overlap with the device's
   diffusion terminal rather than its channel (hypothesis; the deck was not read). The marker was not redrawn.
3. **Upstream:** filed as 2AMLogic/klayout-tools#5301 (generic description). Until it ships, `klt pex` reports
   `model_mismatch` for `osc_subth` and any grid result is non-comparable, so no grid was submitted (no fleet capacity
   spent, no local ngspice grid, host rule).

Remaining for `7.analog`: a klt build that fixes #5301 (or a documented marker-enclosure rule that the layout then
meets), then one clean sharded `osc_subth` run (`--backend batch --hosts 45 --wait-for-capacity 600`, foreground).

## Re-run 2026-11-11 (issue #32, third): `osc_subth` full box on klt dev661, extracted side does not oscillate

SIMULATED only (ngspice on the batch fleet; `klt 0.9.2.dev661+g1de5c0432aad`). `7.analog` is still NOT met (`klt signoff`:
`T1 #7 [analog]` `unmet`, `check_failed`; `[digital]` met). Nothing earlier was edited or relaxed; both new files are dated records.

1. **The model mismatch is gone.** `klt pex --extract-only` on `layout/osc_bank.gds` (`--top osc_subth`) now extracts
   16 `nfet_01v8`, 16 `pfet_01v8`, 14 `pfet_01v8_lvt` against the schematic's 16 / 16 / 14 (klayout-tools#5301 fix,
   #5304). The report's `model_mismatch` is `null`. Extracted netlist `extracted/osc_subth.dev661.spice` sha256 `94256045…`.
2. **Run.** One clean sharded run, `--backend batch --hosts 45 --wait-for-capacity 600`, foreground, no `--resume`:

       klt pex layout/osc_bank.gds sim/pex/requests/osc_subth.json --deck sky130 --pdk sky130A --top osc_subth \
           --pins en,out,vdd,vss --backend batch --hosts 45 --wait-for-capacity 600 -o <dir>/osc_subth.spice \
           --outdir <dir> --envelope-out <report.json> --format json

   Record: `records/2026-11-11-osc_subth-dev661.pex.report.json` (sha256 `4d949f07…`). Report status `error`:
   45/45 cells have an extracted value, 34/45 have a delta, 11/45 have no delta because the **schematic** leg was lost
   (10 `lost_shard` at collect, 1 interrupted Spot job); the extracted leg completed everywhere. The 11 cells are
   ff/1.62 V/125 C, ss/1.98 V/27 C and 125 C, tt/1.98 V/−40 C, ff/1.98 V/125 C, sf/1.62 V/{−40,27,125} C,
   sf/1.98 V/{−40,125} C and fs/1.62 V/−40 C. No corner was dropped by choice; they are missing results.
3. **Result: the extracted `osc_subth` does not oscillate.** The extracted-side crossings count is 0 or 1 in all 45 cells
   (the schematic side is 102–27600 in the cells that completed). Delta is −99.98 % to −100 % in all 34 compared cells.
   Graded as in `grade_pex.py` (row 1 needs ≥ 9 rising edges): **45/45 cells fail row 1 on the extracted side.**
   Grading record: `records/2026-11-11-grade-extracted-values-osc_subth-dev661.json` (inputs: the `osc_hd`
   2026-11-10 report and this report; the ratio-space shift is computable for 8 cells only because a zero count has no
   log-ratio). Rows 2–4 are not re-graded (edge counts only, as before). No threshold was changed.
4. **Likely cause, not proven here.** Caveat 3 above: the extraction has `vbp` as an undriven net and the `Rb0`/`Rb1`
   bias divider is not drawn, so the subthreshold bias that sets the oscillator's current is absent. That is a layout
   gap (#23's domain), out of scope for this issue and not edited. Not verified by a probe run.
5. **`grade_pex.py`** now tolerates a zero count (division guard, and zero-count cells are skipped in the ratio-space
   shift). Re-deriving the 2026-11-11 grading from its inputs is byte-identical.

Remaining for `7.analog`: the `osc_subth` layout must carry the bias network (or the spec row must be re-decided through
`spec/` with a decision record, not here); the 11 lost schematic cells are only worth re-running after that.

## Re-run 2026-11-11 (issue #32, fourth): `osc_subth` on the #109 GDS (bias divider drawn); still does not oscillate

SIMULATED only (ngspice on the batch fleet; `klt 0.9.2.dev661+g1de5c0432aad`, layout `layout/osc_bank.gds` as of #111).
`7.analog` is still NOT met (`klt signoff`: `T1 #7 [analog]` `unmet`, `check_failed`; `[digital]` met). Nothing earlier was
edited; no threshold was changed; no local grid was run. Records (new, dated):
`records/2026-11-11-osc_subth-gds109.pex.report.json` (sha256 `96676c0b…`),
`records/2026-11-11-grade-extracted-values-osc_subth-gds109.json`; extraction `extracted/osc_subth.gds109.spice` (sha256 `9a728593…`).

Command (one clean run, `--hosts 45`, foreground, `--wait-for-capacity 600`, no `--resume`; ~70 min incl. Spot interruptions):

    klt pex layout/osc_bank.gds sim/pex/requests/osc_subth.json --deck sky130 --pdk sky130A --top osc_subth \
        --pins en,out,vdd,vss --backend batch --hosts 45 --wait-for-capacity 600 -o <dir>/osc_subth.spice \
        --outdir <dir> --envelope-out <report.json> --format json

1. **The bias divider is now extracted.** The extraction has 16 `nfet_01v8`, 16 `pfet_01v8`, 14 `pfet_01v8_lvt` (the
   schematic's 16/16/14) plus 2 `res_high_po` (`vss`-`vbp` l=1359.92 w=0.35; `vbp`-`vdd` l=269.99 w=0.35). `vbp` is no
   longer undriven. The report's `model_mismatch` is now `kind: model_set`, `extracted_only: [res_high_po]`: the
   schematic models `Rb0`/`Rb1` as ideal resistors (300 k / 1500 k), so this is expected, not a like-for-like device
   comparison for those two parts. `body_bias.status = biased`.
2. **Coverage.** Report status `error`; 25/45 cells have a delta (`pass`), 20/45 do not: the **schematic** leg is missing in
   11 cells (ff/1.62 V/-40 C, ff/1.80 V/125 C, ff/1.98 V/125 C, fs/1.62 V/125 C, fs/1.98 V/-40 C, fs/1.98 V/125 C,
   sf/1.62 V/-40 C, sf/1.80 V/125 C, sf/1.98 V/27 C, ss/1.62 V/125 C, ss/1.80 V/27 C) and the **extracted** leg in 10 (tt/1.98 V/-40 C and 125 C, ff/1.62 V/27 C,
   ff/1.80 V/27 C and 125 C, ff/1.98 V/-40 C and 27 C, ss/1.62 V/-40 C and 27 C, fs/1.62 V/-40 C); these are fleet
   losses (`unfinished` lists them, resumable), not corners dropped by choice. ff/1.80 V/125 C has neither leg.
3. **Result: the extracted `osc_subth` still does not oscillate.** In the 35 cells with an extracted value the count is 0 or
   1 (row 1 needs >= 9 rising edges): **0/35 pass row 1** on the extracted side; the schematic side is 2-151593. The 25
   deltas are -99.99 % to -100 %. Rows 2-4 are not re-graded (edge counts only, as before).
4. **Cause not established.** The divider is present but its extracted resistance was not verified against the schematic:
   at the PDK `res_high_po` sheet resistance both extracted legs look ~5x the schematic's 300 k / 1500 k (ratio kept),
   which is a hypothesis only, not checked by a probe run. Whether `vbp` then settles where the schematic expects is
   unverified. Diagnosing this is a layout/extraction question (#23's domain) and was not attempted here.

Remaining for `7.analog`: find why the extracted `osc_subth` does not start (probe one corner, e.g. tt/1.80 V/27 C,
locally is allowed by host rules), fix that in the layout under its own issue, then re-run; the 20 missing cells need a
`--resume` or a new run after that.

## Diagnosis 2026-11-11 (issue #116): why the extracted `osc_subth` does not start

SIMULATED only: ngspice-46, one local `ngspice -b` per case (5 total, no grid), tt / 1.80 V / 27 C, 100 us transient,
`sim/pex/probe/osc_subth_vbp_probe.cir` + `run_probe.sh`. Input: `extracted/osc_subth.gds109.spice` (sha256 `9a728593…`) and
`design/osc_bank/osc_subth.spice` (sha256 `b2676720…`). klt was not run. Record (new, append-only):
`records/2026-11-11-osc_subth-diagnosis.json`. Nothing earlier was edited; no threshold was changed.

| case (tt/1.80 V/27 C) | settled `vbp` | rising edges in 100 us |
| --- | --- | --- |
| schematic | 1.5000 V | 169 |
| extracted, free | 1.5002 V | 0 (`out` stuck 1.09-1.20 V) |
| extracted, `vbp` forced to 1.5 V | 1.5000 V | 0 |
| extracted, parasitic R -> 1 mohm and all C removed | 1.5011 V | 0 |
| extracted + 14 tie resistors across the split `vh` nets | 1.4999 V | 126 |

1. **`vbp` is not the cause.** The extracted divider settles at 1.5002 V against the schematic's 1.5000 V (the ~5x legs keep
   the 5:1 ratio), and forcing `vbp` to the schematic value changes nothing. The README's earlier hypothesis is refuted.
2. **Extractor parasitics are not the cause.** A devices-only version of the extracted netlist still does not start.
3. **Cause: the 14 series-header nets `vh1`..`vh14` are split in the extraction.** The 14 stage PFET sources
   (`$21 $24 $26 $27 $29 $31 $33 $35 $37 $39 $41 $44 $46 $47`) and the 14 header LVT PFET drains
   (`$22 $23 $25 $28 $30 $32 $34 $36 $38 $40 $42 $43 $45 $48`) are 28 distinct nets with nothing joining them, so every
   stage PFET source floats. Joining each pair with a 1 mohm resistor (pairing by stage order, see the record) restores
   oscillation with the extracted parasitics kept: 126 edges against 169 on the schematic.
4. **Not established:** whether this is a layout defect (no contact/metal between header drain and stage source) or an
   extraction/deck defect. The GDS was not inspected and not edited (out of scope). The spec row and the ideal `Rb0`/`Rb1`
   modelling are not implicated; no `spec/` change is needed.

Remaining for `7.analog`: resolve the split `vh` nets under their own issue, then #32 re-runs the 45 cells.

## Diagnosis 2026-11-11 (issue #117): the `vh` split in `osc_subth` is an extraction defect, not a layout one

SIMULATED/extraction only (`klt 0.9.2.dev661`); record `records/2026-11-11-vh-split-diagnosis-osc_subth.json`, script `diag/vh_split.py`.
The drawn diffusion at each of the 14 header/stage junctions is one merged polygon, but the extracted header drain and
stage-PFET source are different nets in 14/14 stages; with `lvtn` deleted from a scratch copy they are one net in 14/14. Moving the
marker edge to the gate edge or removing the diffusion step does not change it. Upstream: 2AMLogic/klayout-tools#5311 (generic repro added).
No layout, netlist or threshold change; the one-corner ring-start check waits for the tool fix.
