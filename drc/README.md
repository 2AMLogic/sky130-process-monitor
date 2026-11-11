# drc — T1 item 3 (issue #25)

`klt drc --deck sky130` (curated engine), `klayout-tools==0.9.1` (the CI pin), PDK `sky130A`, deck content hash
`sha256:029ef177c1f4e872c13cc81093f94a02a9bbfe1f51939a88194a83532d60bf7c`. **Tool output on drawn layout only; a
simulated-flow result, not silicon evidence; nothing here is measured.** Reports are the `--format json -o` output of:

```console
klt drc layout/osc_bank.gds --deck sky130 --top osc_bank --pdk sky130A --format json -o drc/osc_bank.report.json
klt drc layout/readout/out/readout.gds --deck sky130 --top readout --pdk sky130A --format json -o drc/readout.report.json
klt drc layout/osc_bank.gds --deck sky130 --top osc_bank --pdk sky130A --check drc/osc_bank.report.json   # freshness
```

| Cited as | Report | Input (committed GDS) | status | Input hash |
|---|---|---|---|---|
| `3.analog` | `drc/osc_bank.report.json` | `layout/osc_bank.gds` | **clean** (0 violations) | `sha256:625c8ff90f34c6fac7a88339d2c10ad5925da02e118eb6a15a6539c11e05bf29` |
| `3.digital` | `drc/readout.report.json` | `layout/readout/out/readout.gds` | **clean** (0 violations) | `sha256:d590c9ea2cceef8e27a53d59848ab9e8e2ca7b6aa7b0cdc95c46ba5f4306f95e` |

## Coverage fields, quoted verbatim from each report's `coverage` block

A `clean` status does **not** mean these are checked. `klt signoff` grades on `status` alone.

### 3.analog

- `coverage.layers_in_stream_without_rules`: `["64/5", "64/16", "64/59", "66/13", "67/5", "67/16", "68/5", "68/16", "81/4", "83/44", "94/44", "122/16", "236/0"]`
- `coverage.rules_skipped`: `["areaid_re.ongrid.1", "capm.enclosing.via3.1", "capm.separation.via3.1", "capm.space.1", "capm.width.1", "capm2.enclosing.via4.1", "capm2.separation.via4.1", "capm2.space.1", "capm2.width.1", "dnwell.angle.1", "dnwell.ongrid.1", "hvi.angle.1", "hvi.ongrid.1", "hvntm.angle.1", "hvntm.ongrid.1", "hvtr.angle.1", "hvtr.ongrid.1", "met2.enclosing.via2.1", "met2.enclosing_adjacent.via2.1", "met3.angle.1", "met3.area.1", "met3.enclosing.capm.1", "met3.enclosing.via2.1", "met3.enclosing.via3.1", "met3.enclosing_adjacent.via3.1", "met3.holes_area.1", "met3.ongrid.1", "met3.space.1", "met3.width.1", "met4.angle.1", "met4.area.1", "met4.enclosing.capm2.1", "met4.enclosing.via3.1", "met4.enclosing.via4.1", "met4.holes_area.1", "met4.ongrid.1", "met4.space.1", "met4.width.1", "met5.angle.1", "met5.area.1", "met5.enclosing.via4.1", "met5.holes_area.1", "met5.ongrid.1", "met5.space.1", "met5.width.1", "mf.angle.1", "mf.ongrid.1", "ncm.angle.1", "ncm.ongrid.1", "nsm.angle.1", "nsm.ongrid.1", "nwell.enclosed.hvi.1", "pad.angle.1", "pad.ongrid.1", "pwbm.angle.1", "pwbm.ongrid.1", "pwde.angle.1", "pwde.ongrid.1", "pwell_rs.angle.1", "pwell_rs.ongrid.1", "tunm.angle.1", "tunm.ongrid.1", "uhvi.angle.1", "uhvi.ongrid.1", "urpm.width.1", "vhvi.angle.1", "vhvi.ongrid.1", "via2.angle.1", "via2.ongrid.1", "via2.space.1", "via2.width.1", "via3.angle.1", "via3.ongrid.1", "via3.space.1", "via3.width.1", "via4.angle.1", "via4.ongrid.1", "via4.space.1", "via4.width.1", "vpp.angle.1", "vpp.ongrid.1"]`
- `coverage.deck_scope`: `["cap2m", "capm", "ct", "difftap", "li", "licon", "m1", "m2", "m3", "m4", "m5", "npc", "nsdm", "nwell", "poly", "psdm", "rpm", "urpm", "via", "via2", "via3", "via4", "x"]`

### 3.digital

- `coverage.layers_in_stream_without_rules`: `["64/5", "64/16", "64/59", "66/15", "67/5", "67/16", "68/5", "68/16", "70/5", "70/16", "72/5", "72/16", "81/4", "81/23", "83/44", "122/16", "235/4", "236/0"]`
- `coverage.rules_skipped`: `["areaid_re.ongrid.1", "capm.enclosing.via3.1", "capm.separation.via3.1", "capm.space.1", "capm.width.1", "capm2.enclosing.via4.1", "capm2.separation.via4.1", "capm2.space.1", "capm2.width.1", "dnwell.angle.1", "dnwell.ongrid.1", "hvi.angle.1", "hvi.ongrid.1", "hvntm.angle.1", "hvntm.ongrid.1", "hvtr.angle.1", "hvtr.ongrid.1", "lvtn.angle.1", "lvtn.ongrid.1", "met3.enclosing.capm.1", "met4.enclosing.capm2.1", "mf.angle.1", "mf.ongrid.1", "ncm.angle.1", "ncm.ongrid.1", "nsm.angle.1", "nsm.ongrid.1", "nwell.enclosed.hvi.1", "pad.angle.1", "pad.ongrid.1", "pwbm.angle.1", "pwbm.ongrid.1", "pwde.angle.1", "pwde.ongrid.1", "pwell_rs.angle.1", "pwell_rs.ongrid.1", "rpm.angle.1", "rpm.ongrid.1", "rpm.width.1", "tunm.angle.1", "tunm.ongrid.1", "uhvi.angle.1", "uhvi.ongrid.1", "urpm.width.1", "vhvi.angle.1", "vhvi.ongrid.1", "vpp.angle.1", "vpp.ongrid.1"]`
- `coverage.deck_scope`: `["cap2m", "capm", "ct", "difftap", "li", "licon", "m1", "m2", "m3", "m4", "m5", "npc", "nsdm", "nwell", "poly", "psdm", "rpm", "urpm", "via", "via2", "via3", "via4", "x"]`

## What is not claimed

- DRC covers **drawn geometry only**. `layout/README.md` lists what `osc_wire` does not draw (the shunt caps); that is
  not checked. The `osc_subth` bias divider is now drawn (issue #109): the curated deck reports the regenerated stream
  clean, `rpm.width.1` / `rpm.angle.1` / `rpm.ongrid.1` now have geometry and pass; the poly-resistor marker 66/13 is
  listed under `layers_in_stream_without_rules`, so it is not rule-checked.
- **The PDK-native deck disagrees on the analog stream.** Cross-check, not cited:
  `klt drc layout/osc_bank.gds --engine klayout --pdk sky130A --top osc_bank` reports **562 violations: `ct.4` x220,
  `li.5` x342**, in the hand-drawn cells. The curated deck neither checks nor lists those rules as unmodeled (tool gap
  filed: 2AMLogic/klayout-tools#5233). `3.analog` `clean` is therefore a curated-deck result; a foundry-deck clean
  needs the generator's li1/licon geometry reworked (follow-up, not done here). The same native run on the readout stream
  ends `coverage_unknown` (exit 4), which is not a clean verdict either.
- Standard-cell instances (`sky130_fd_sc_hd__*`) are DRC-clean standalone under the curated deck; no waivers are used.

## Layout fixes this run required (`layout/gen/gen_osc_bank.py`, `layout/osc_bank.gds` regenerated)

First pass on the #23 stream: 862 violations. All were in generator geometry:
1. `met1.ongrid.1` x744: serpentine run length was not on the 5 nm grid; rounded up (centreline is now 1 000.020 um,
   +0.002 %, not exactly 1000 um).
2. `nwell.space.1` x104: per-stage wells left 0.10 um gaps; one continuous well per cell (all on vdd).
3. `osc_hd` routing pads that notched the std cells' li1 (`li1.space.1`), an isolated 260 nm met1 pad
   (`met1.area.1`) and 70 nm met1 spurs at L-joints (`met1.width.1`).

LVS (#26) was re-run on the regenerated stream with the same pin: all six `lvs/*.report.json` still `match`
(`osc_wire`/`osc_subth` still against reduced references, so `4.analog` stays unmet). `evidence/item2.json` re-attested.
