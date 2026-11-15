# erc — T1 item 11 digital (issue #168)

`klt erc` supply-spec run over the routed readout stream, `klayout-tools==0.9.1` (the CI pin),
no PDK antenna table. **Tool output on drawn layout only; a simulated-flow result, not silicon
evidence; nothing here is measured.** The report is the `--format json` **stdout** of (there is
no `-o` flag on `klt erc`):

```console
uvx --from "klayout-tools==0.9.1" klt erc layout/readout/out/readout.gds erc/readout.erc.json \
    --top readout --findings-only --omit-antenna-tables --format json > erc/readout.report.json
uvx --from "klayout-tools==0.9.1" klt erc --validate-spec erc/readout.erc.json          # spec only
uvx --from "klayout-tools==0.9.1" klt erc --check erc/readout.report.json               # freshness (cheap)
uvx --from "klayout-tools==0.9.1" klt erc --check erc/readout.report.json --rerun       # freshness (full replay)
```

| Cited as | Report | Spec | Input (committed GDS) | `erc_status` | exit | Input hash |
|---|---|---|---|---|---|---|
| `11.digital` (ERC part) | `erc/readout.report.json` | `erc/readout.erc.json` | `layout/readout/out/readout.gds` | **clean** (0 findings) | 4 | `sha256:d590c9ea2cceef8e27a53d59848ab9e8e2ca7b6aa7b0cdc95c46ba5f4306f95e` |

`--findings-only` runs the connectivity scope (everything item 11 grades) and skips the per-gate
antenna accumulation, which dominates runtime on this 5341-component block; it is mutually
exclusive with `--pdk`, so no antenna-ratio limit table is applied. The run's **exit status is 4**
and the envelope's top-level `status` reads `not_checked` by design — that is the antenna scope
saying it did not run. The connectivity scope's own rollup, `erc_status`, reads `clean`.
Item 11 grades the connectivity scope only; an antenna verdict or `erc.floating_gate` finding
"is not this item's subject and does not block it" (`manifests/design-evidence-tiers.md`, #1994).
`--omit-antenna-tables` drops the 3844-gate `gates[]` array (every entry ungraded here) so the
report stays reviewable.

## Verdict

`erc_status: clean`, `erc_finding_count: 0`. Every declared supply resolves to exactly one
electrical island, and both declared ties were checked (not skipped) with zero
`erc.missing_tie`:

| Declared net | `kind` | `matched_islands` / expected |
|---|---|---|
| `VDD` | supply (`same_net_as` `VPWR`) | 1 / 1 |
| `VSS` | supply (`same_net_as` `VGND`) | 1 / 1 |
| `VPWR` | supply | 1 / 1 |
| `VGND` | supply | 1 / 1 |

The two label-name families are bound by `nets[].same_net_as` rather than declared as four
independent nets because the stream labels them differently: the PDN top-level names are
`VDD`/`VSS` (met5 label layer `72/5`), the standard-cell rails are `VPWR`/`VGND`
(met1 label layer `68/5`, 5345 labels each). Declared naively, `klt erc` sees `VDD` and `VPWR`
as distinct nets and the item cannot grade. No `erc.expected_short_missing` fired, so each
declared alias pair is verified connected through the declared via stack (`mcon` → `via` →
`via2` → `via3` → `via4`, the full met1–met5 PDN path the P&R `connects[]` describes).

Ties (`ties[]`, both `tap_is_dedicated` — sky130's `tap` layer `65/44` draws only taps, drawn
by the 468 `sky130_fd_sc_hd__tapvpwrvgnd_1` instances and nothing else):

- `nwell_tap` — well `nwell` (`64/20`, 35 merged shapes), tap → `li1`, net `VPWR`: checked, clean.
- `psub_tap` — well = top-cell extent minus `nwell` (`well_layer: null` +
  `well_complement_of: ["64/20"]` — the substrate is not a drawn layer), tap → `li1`,
  net `VGND`: checked, clean. Its well side rests on the caller-named complement, so the
  citation discloses it under `checked_by_well_assertion` — real evaluated work, not a skipped
  or asserted-away check.

## `erc_coverage` (connectivity scope), quoted verbatim

- `skipped`: `[]` — no tie was reported degenerate, so the zero-`missing_tie` verdict is a
  checked pass, not `supply_spec_incomplete`.
- `inapplicable`:
  `[{"id": "erc.supply_short", "reason": "substrate_continuity_not_modelled"}]` — with two or
  more supplies declared, the two-supply short rule is not computable (the substrate is not a
  conductor in the model); the item's short condition is instead carried by the single-island
  counts above.
- `missing_tie_checked`: `true` — both `erc.missing_tie:["nwell_tap"]` and
  `erc.missing_tie:["psub_tap"]` really ran.
- `checked_by_assertion`: `[]` — no tie needed a caller-asserted tap region.
- `checked_by_well_assertion`: `["erc.missing_tie:[\"psub_tap\"]"]`.
- `checked`: 3850 identities — the 6 connectivity work items above plus 3844
  `erc.floating_gate:["gate<i>"]` checks, **all clean** (declaring `licon1` between `poly` and
  `li1` gives every gate a conductive path, so no gate floats).
- `layers_in_stream_without_declaration`: `["64/5", "64/16", "64/59", "65/20", "66/15", "67/16", "68/16", "70/5", "70/16", "72/16", "78/44", "81/4", "81/23", "83/44", "93/44", "94/20", "95/20", "122/16", "235/4", "236/0"]`
  — the disclosure the spec never mentions: signal labels (`70/5`), implants/markers
  (`93/44` `nsdm`, `94/20` `psdm`, `95/20`, …), and cell-fill/cell-boundary purposes (`81/*`,
  `83/44`, `236/0`). Declared label layers and their measured text counts
  (`provenance.label_layers`): `li1` `67/5` = 9712, `met1` `68/5` = 10690, `met5` `72/5` = 2.
  `met2` and `met4` carry no label layer in this stream and declare none.

## What is not claimed

- **`--findings-only` leaves every antenna verdict unchecked.** The `coverage` (antenna scope)
  block records `skipped: [{"id": "antenna:[]", "reason": "findings_only"}]` and
  `nothing_checked_reasons: ["findings_only", "gate_reference_level"]`. No antenna-ratio limit
  table was applied (`--pdk` is mutually exclusive with `--findings-only`), and no antenna
  verdict is claimed here. Antenna coverage on this stream is separate work, not part of
  item 11 (#1994).
- **`VPB`/`VNB` are not declared in `nets[]`, and the ties target the rails.** The body-tie
  label texts exist (`VPB` on `64/5`, `VNB` on `64/59`, 4877 each) but sit physically over the
  cell rails, and a `klt erc` spec has one `label_layer` per stackup entry — the four slots go
  to the label layers the four declared supply names resolve through (`67/5`, `68/5`, `72/5`
  for `VPWR`/`VGND`/`VDD`/`VSS`; `70/5`'s signal-only labels are not needed). The taps are
  therefore graded against the nets they physically land on (`tapvpwrvgnd` taps tie the well/
  substrate to the rails), and the body names are the same islands by that tie:
  `lvs/readout.report.json`'s `power_connectivity.power_pins` is
  `["VGND", "VPB", "VPWR"]` (declared by every instantiated master), consistent with this.
- **`erc` coverage is a connectivity model over the declared stackup/vias only.** The source/
  drain `active` layer (`65/20`) is not declared — the model has no diffusion conductor — so
  signal-net connectivity below `li1` is not what a full extraction would see. The supply
  verdict does not rest on it: the PDN path is `li1` → `met5`, and the taps wire to `li1`.
- `status: not_checked` / exit 4 is the designed `--findings-only` outcome (see above), not a
  failure; the freshness pair (`--check`, and `--check --rerun` for full mode) both report
  `match` on the committed report.

## Item 11 (digital) grading

`11.digital` cites this report plus the two artifacts the compound rule requires
(`klt signoff` item 11 is graded over a cited *set*):

- `layout/readout/report.json` — the P&R response: `power.pdn: true`,
  `power.tapcell_master: sky130_fd_sc_hd__tapvpwrvgnd_1` (468 placed), and every
  `power.straps[].layer` (`met1`, `met4`, `met5`) — a subset of this spec's stackup, which
  declares the full `met1`–`met5` routing stack (the straps' met2/met3 shapes are that via
  stack's intermediate landing pads; `power.placed.special_nets[].stripe_layers` agrees).
- `lvs/readout.report.json` — `power_connectivity.status: "match"` (`finding_count: 0`), the
  same report item 4 grades (`4.digital`).

The verdict of record is in `manifests/sky130-process-monitor.signoff.json`:
**11.digital `met`**, `t1_met_count` 13 → 14. **11.analog stays `unmet` / `no_evidence`** —
that is issue #33's analog half, waiting on #26's `4.analog`; this run cites nothing for it.
