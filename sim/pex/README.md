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
