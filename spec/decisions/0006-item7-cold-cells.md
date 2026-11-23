# 0006: Close T1 item 7 (`7.analog`) using the #102 cold-cell PEX supplements

- Status: accepted (operator ruling 2026-11-23, attended `/fleet:decide` session, round `20261121-r19`, `r19-q316`, slate `r19-s29`, option `a`; issue #264)
- Date: 2026-11-23
- Issue: #264 (closes the remaining `7.analog` signoff gap from #32; inputs from #29 and #102)
- Evidence:
  - [`sim/pex/records/2026-11-10-osc_nmos.pex.report.json`](../../sim/pex/records/2026-11-10-osc_nmos.pex.report.json) and [`sim/pex/records/2026-11-11-osc_nmos-coldcell-relaxed.pex.report.json`](../../sim/pex/records/2026-11-11-osc_nmos-coldcell-relaxed.pex.report.json)
  - [`sim/pex/records/2026-11-10-osc_wire.pex.report.json`](../../sim/pex/records/2026-11-10-osc_wire.pex.report.json) and [`sim/pex/records/2026-11-11-osc_wire-coldcell-relaxed.pex.report.json`](../../sim/pex/records/2026-11-11-osc_wire-coldcell-relaxed.pex.report.json)
  - Context and run history: [`sim/pex/README.md`](../../sim/pex/README.md). **All figures SIMULATED** (ngspice-46, sky130A `open_pdks f6eeac7d…`); nothing here is measured.

## Background

After the 2026-11-20 `osc_subth` full-box re-run on the net-split-fixed extractor
([`sim/pex/records/2026-11-20-osc_subth-dev2493.pex.report.json`](../../sim/pex/records/2026-11-20-osc_subth-dev2493.pex.report.json),
status `pass`, 45/45 corners compared), `klt signoff` (`klayout-tools==0.9.1`) continued to grade
`T1 #7 [analog]` `unmet` (`check_failed`) solely because the 2026-11-10 `osc_nmos` and `osc_wire`
reports carry aggregate `status: "error"`:

- In each of those two 45-cell runs, **44 corners passed** on both legs and produced a
  schematic-vs-extracted delta, while **1 schematic-leg cold cell** deterministically aborted with
  `timestep_too_small` (`osc_nmos` at `tt/1.800V/-40C`, `osc_wire` at `sf/1.980V/-40C`; the
  extracted leg converged at both with 159 and 156 rising edges).
- Issue #102 recorded converged single-corner supplementary `klt pex` runs for those two missing
  cold cells (`2026-11-11-osc_{nmos,wire}-coldcell-relaxed.pex.report.json`, status `pass`).
- `klt signoff` grades whole cited `klt pex` reports and requires every citation in an evidence
  list to pass. Appending the two #102 supplements alongside the two `status: "error"` 2026-11-10
  reports grades the two supplements `met` and the two originals `unmet`, leaving `7.analog`
  `unmet` (`check_failed`). Substituting the two supplements into `evidence["7.analog"]` grades all
  five citations `met`, but one-corner reports on their own cannot show full 45-cell PVT-box
  coverage without a paired evidence record.

## Decision

Per the 2026-11-23 operator ruling (`rjwalters`, round `20261121-r19`, `r19-q316`, slate `r19-s29`,
option `a`), T1 item 7 (`7.analog`) accepts the #102 converged cold-cell supplements paired with
the 44 passing default-bench cells of each 2026-11-10 report:

| Oscillator | Source for the 44 default-bench corners | #102 source for the 1 missing cold corner | Supplement corner (`corner_id`) | Simulated rising edges (sch → ext, `delta_pct`) |
|---|---|---|---|---|
| `osc_nmos` | [`sim/pex/records/2026-11-10-osc_nmos.pex.report.json`](../../sim/pex/records/2026-11-10-osc_nmos.pex.report.json) (`087abaf2…`, 44 passing `delta[]` rows; excludes `tt/1.800V/-40C`) | [`sim/pex/records/2026-11-11-osc_nmos-coldcell-relaxed.pex.report.json`](../../sim/pex/records/2026-11-11-osc_nmos-coldcell-relaxed.pex.report.json) (`fa8e958b…`, sole `delta[]` row) | tt / 1.80 V / −40 °C (`tt/1.800V/-40C`) | 204 → 158 (−22.549 %) |
| `osc_wire` | [`sim/pex/records/2026-11-10-osc_wire.pex.report.json`](../../sim/pex/records/2026-11-10-osc_wire.pex.report.json) (`e1efa71a…`, 44 passing `delta[]` rows; excludes `sf/1.980V/-40C`) | [`sim/pex/records/2026-11-11-osc_wire-coldcell-relaxed.pex.report.json`](../../sim/pex/records/2026-11-11-osc_wire-coldcell-relaxed.pex.report.json) (`dbd04bd9…`, sole `delta[]` row) | sf / 1.98 V / −40 °C (`sf/1.980V/-40C`) | 68 → 50 (−26.471 %) |

Each 2026-11-10 report contributes **44 corners** (every `delta[]` entry with `status == "pass"`
and non-null `delta_pct`) and each 2026-11-11 supplement contributes **only its single named
corner** above, covering all 45 distinct corners of [`sim/corner_box.json`](../../sim/corner_box.json)
for both oscillators.

In [`manifests/sky130-process-monitor.json`](../../manifests/sky130-process-monitor.json),
`evidence["7.analog"]` substitutes the two passing cold-cell reports in place of the two
`status: "error"` 2026-11-10 reports while retaining the existing 45-corner citations for
`osc_hd` (`2026-11-10-osc_hd.pex.report.json`), `osc_pmos` (`2026-11-10-osc_pmos.pex.report.json`)
and `osc_subth` (`2026-11-20-osc_subth-dev2493.pex.report.json`). This decision record provides the
full-box evidence trail behind those two manifest substitutions so `klt signoff` grades both item-7
partitions (`7.analog` and `7.digital`) `met`.

Rejected alternatives (from the operator decision block in #264):

- **Option B — new 45-cell `klt pex` runs with relaxed solver options on all 45 cells**: yields
  single-file `status: "pass"` reports, but alters how the 43 already-converging default-bench
  cells are solved and spends fleet batch capacity to re-simulate healthy corners.
- **Option C — leave `7.analog` `unmet`**: keeps the signoff gate red on a known schematic-side
  transient solver artefact that the committed #102 supplements already resolve.

## Disclosures and comparison limitations

1. **Relaxed transient and solver settings on the two supplemented corners only.** Both #102
   supplements run [`sim/pex/osc/tb_osc_nmos_relaxed.spice`](../../sim/pex/osc/tb_osc_nmos_relaxed.spice)
   and [`sim/pex/osc/tb_osc_wire_relaxed.spice`](../../sim/pex/osc/tb_osc_wire_relaxed.spice),
   which append `.options reltol=0.01 gmin=1e-10 method=gear` (the #69 solver option set) to the
   #29 bench body, driven by
   [`sim/pex/requests/osc_nmos_coldcell.json`](../../sim/pex/requests/osc_nmos_coldcell.json) and
   [`sim/pex/requests/osc_wire_coldcell.json`](../../sim/pex/requests/osc_wire_coldcell.json) with
   `.tran 20p 800n 0 10p` (`tmax` capped at 10 ps; local single-corner ngspice-46). By contrast,
   the 44 default-bench corners use un-relaxed ngspice tolerances with `.tran 20p 800n`
   (`sim/pex/requests/osc_nmos.json`) and `.tran 50p 2.5u` (`sim/pex/requests/osc_wire.json`).
   Because of the relaxed solver numerics — and, for `osc_wire`, the 800 ns window vs 2.5 µs on the
   44 default-bench corners (where the 2026-11-10 extracted leg counted 156 edges in 2.5 µs vs 50
   in 800 ns here; both legs of the supplement share the 800 ns window) — the two supplemented edge
   counts are not numerically interchangeable with the other 44 cells' raw counts.
2. **Different `osc_wire` extraction build (`09374950…` vs `76c8872a…`) and existing wire
   comparison caveat.** For `osc_nmos`, both paired reports simulate the identical extracted
   netlist (`extraction.netlist_sha256` `68b62d0e…`, committed at
   `sim/pex/extracted/osc_nmos.spice`, 64 devices / 35 nets). For `osc_wire`, the 2026-11-10 report
   (`klt 0.9.2.dev460+g1c0ae85debd3`, deck `029ef177…`) ran against extracted netlist `76c8872a…`
   (`sim/pex/extracted/osc_wire.spice`), whereas the 2026-11-11 cold-cell run
   (`klt 0.9.2.dev599+g651481155211`, deck `5313927e…`) re-extracted `osc_wire` to `09374950…`
   (committed at `sim/pex/extracted/osc_wire.dev599.spice`; same 64 devices / 35 nets, different
   parasitic values). In addition, both `osc_wire` extractions carry finding 3 of
   [`sim/pex/README.md`](../../sim/pex/README.md) (see also [`lvs/README.md`](../../lvs/README.md)):
   neither extraction is like-for-like against the item-1 schematic netlist
   `design/osc_bank/osc_wire.spice`, because the 31 × 100 fF shunt capacitors are not drawn in
   layout and the met1 serpentine extracts as plain metal wiring rather than `res_generic_m1`
   devices, so the `osc_wire` delta under-states the schematic's own wire RC load.
3. **Body bias and extraction model.** Every report in both pairs (and the three retained item-7
   analog reports) records `body_bias.status = "biased"` (`unbiased_device_count = 0`) under the
   same lumped-RC extraction model (net-to-ground plus vertical-overlap coupling, one star series R
   per net, quasi-static, no `--critical-net` lateral coupling).

## Scope boundaries and append-only preservation

- **All committed PEX records retain their exact bytes.** Neither
  `2026-11-10-osc_nmos.pex.report.json` nor `2026-11-10-osc_wire.pex.report.json` is edited or
  synthesized over; both keep `status: "error"` and their schematic-leg `timestep_too_small`
  entries as append-only historical evidence.
- **Item-7 evidence coverage only, not an oscillator or solve performance pass.** `7.analog = met`
  records that post-layout parasitic extraction and schematic-vs-extracted re-simulation cover all
  five oscillators across the 45-cell PVT box. No threshold in
  [`spec/target-spec.md`](../target-spec.md) is changed or relaxed, analog LVS (`4.analog`, #26) is
  unaffected, and the recorded performance failures stand unchanged: extracted `osc_subth` falls
  below row 1's ≥ 9-edge criterion in 5 cold `ss`/`sf` cells
  (`2026-11-20-osc_subth-dev2493.pex.report.json`), and on measured extracted frequencies
  (`sim/pex/records/2026-11-22-grade-extracted-frequencies.json`, #282) spec rows 1, 3 and 4 fail
  their target bounds (`5.analog` and `8.analog` remain `unmet` / `check_failed`).

## Reproducible coverage check

From the repository root, stdlib Python verifies that each pair's 44 passing default-bench cells
plus 1 passing relaxed cold-cell supplement match the sole original error and partition the 45-cell
Cartesian product in `sim/corner_box.json`:

```sh
python3 -I - <<'PY'
import json
from pathlib import Path

box = json.loads(Path("sim/corner_box.json").read_bytes())
expected = {
    f"{p}/{v:.3f}V/{t}C"
    for p in box["process"]
    for v in box["vdd"]
    for t in box["temp_c"]
}
assert len(expected) == 45

pairs = [
    (
        "osc_nmos",
        "sim/pex/records/2026-11-10-osc_nmos.pex.report.json",
        "sim/pex/records/2026-11-11-osc_nmos-coldcell-relaxed.pex.report.json",
        "tt/1.800V/-40C",
        (204, 158),
    ),
    (
        "osc_wire",
        "sim/pex/records/2026-11-10-osc_wire.pex.report.json",
        "sim/pex/records/2026-11-11-osc_wire-coldcell-relaxed.pex.report.json",
        "sf/1.980V/-40C",
        (68, 50),
    ),
]

for osc, orig_path, supp_path, expected_gap, expected_edges in pairs:
    orig = json.loads(Path(orig_path).read_bytes())
    supp = json.loads(Path(supp_path).read_bytes())
    orig_pass = [r for r in orig["delta"] if r.get("status") == "pass" and r.get("delta_pct") is not None]
    orig_err = [r for r in orig["delta"] if not (r.get("status") == "pass" and r.get("delta_pct") is not None)]
    supp_pass = [r for r in supp["delta"] if r.get("status") == "pass" and r.get("delta_pct") is not None]

    assert len(orig_pass) == 44 and len(orig_err) == 1
    assert len(supp["delta"]) == 1 and len(supp_pass) == 1
    assert orig_err[0]["error"]["code"] == "timestep_too_small"
    assert supp_pass[0]["corner_id"] == orig_err[0]["corner_id"] == expected_gap
    assert (supp_pass[0]["schematic_value"], supp_pass[0]["extracted_value"]) == expected_edges

    orig_keys = [r["corner_id"] for r in orig_pass]
    assert len(orig_keys) == len(set(orig_keys))
    assert expected - set(orig_keys) == {expected_gap}

    combined = orig_keys + [supp_pass[0]["corner_id"]]
    assert len(combined) == 45 == len(set(combined))
    assert set(combined) == expected
    print(f"{osc}: 44 default + 1 supplement ({expected_gap}, {expected_edges[0]}->{expected_edges[1]}) == 45/45 box")
PY
```
