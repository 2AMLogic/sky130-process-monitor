# erc — T1 item 11 supply-spec evidence

Two `klt erc` runs over the two partitions, both `klayout-tools==0.9.1` (the CI pin), both
`--findings-only` (connectivity scope only — the scope item 11 grades) with no PDK antenna
table. **Tool output on drawn layout only; a simulated-flow result, not silicon evidence;
nothing here is measured.**

## Digital — routed readout (issue #168)

The report is the `--format json` **stdout** of (there is no `-o` flag on `klt erc`):

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

### Verdict

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

### `erc_coverage` (connectivity scope), quoted verbatim

- `skipped`: `[]` — no tie was reported degenerate, so the zero-`missing_tie` verdict is a
  checked pass, not `supply_spec_incomplete`.
- `inapplicable`:
  `[{"id": "erc.supply_short", "reason": "substrate_continuity_not_modelled"}]` — substrate
  continuity is not modeled, so supply-to-supply shorts through the substrate cannot be checked
  here. Rail-to-rail shorts on the **modeled conductors** (`stackup`/`vias`) are still checked
  and reported directly as `erc.supply_short` findings (zero here); the single-island counts
  above establish per-supply continuity (no `erc.unconnected_net`), not rail isolation.
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

### What is not claimed

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

### Item 11 (digital) grading

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
**11.digital `met`**, `t1_met_count` 13 → 14. **11.analog stays `unmet` / `no_evidence`** — issue
#33's analog half, waiting on #26's `4.analog`; the five per-oscillator ERC reports are committed
below (#276), with manifest citation deferred under `klayout-tools==0.9.1`.

## Analog — oscillator bank (issue #276)

`klt erc` supply-spec run over the generated stream `layout/osc_bank.gds`, same pin, same
connectivity-only scope, plus `--deck sky130` (why below). **Tool output on generated,
planning-level geometry (`layout/README.md`); a simulated-flow result, not silicon evidence;
nothing here is measured.** The stream's sole top cell `osc_bank` holds five child instances and
no shapes of its own, and no inter-oscillator power distribution is drawn, so the bank top
resolves each supply to **five** islands (one per oscillator — verified below). The graded scope
is therefore **one run per oscillator with an explicit `--top`**, sharing one spec: a per-cell
single-island expectation is what tests continuity *within* each oscillator. Reports are the
`--format json` **stdout** of:

```console
uvx --from "klayout-tools==0.9.1" klt erc --validate-spec erc/osc_bank.erc.json
for cell in osc_hd osc_nmos osc_pmos osc_wire osc_subth; do
  uvx --from "klayout-tools==0.9.1" klt erc layout/osc_bank.gds erc/osc_bank.erc.json \
      --top "$cell" --deck sky130 --findings-only --omit-antenna-tables --format json \
      > "erc/$cell.report.json"
  # exit 4 = connectivity clean, antenna scope not checked (--findings-only, by design);
  # exit 3 = the connectivity scope reported findings
done
uvx --from "klayout-tools==0.9.1" klt erc --check erc/osc_hd.report.json   # cheap freshness, per report
```

| Report | `--top` | `erc_status` | findings | `vdd` / `vss` islands | exit |
|---|---|---|---|---|---|
| `erc/osc_hd.report.json` | `osc_hd` | **violations** | 1 × `erc.missing_tie` (`vss`) | 1/1 · 1/1 | 3 |
| `erc/osc_nmos.report.json` | `osc_nmos` | **clean** | 0 | 1/1 · 1/1 | 4 |
| `erc/osc_pmos.report.json` | `osc_pmos` | **clean** | 0 | 1/1 · 1/1 | 4 |
| `erc/osc_wire.report.json` | `osc_wire` | **clean** | 0 | 1/1 · 1/1 | 4 |
| `erc/osc_subth.report.json` | `osc_subth` | **clean** | 0 | 1/1 · 1/1 | 4 |

Shared: spec `erc/osc_bank.erc.json`; input `layout/osc_bank.gds`,
`provenance.input.content_hash` `sha256:625c8ff90f34c6fac7a88339d2c10ad5925da02e118eb6a15a6539c11e05bf29`
(the GDS input hash recorded in all five reports; manifest citation is deferred under
`klayout-tools==0.9.1`, see "What is not claimed" below). Measured label counts (`provenance.label_layers`):
`osc_hd` `li1` `67/5` = 95, `met1` `68/5` = 76 (the PDK cells' own labels ride along); the custom
cells carry only the generator's 4 (5 on `osc_subth`: `en`, `out`, `vdd`, `vss`, `vbp`) on `68/5`.

### Spec (`erc/osc_bank.erc.json`)

- **Stackup** `poly`/`li1`/`met1`/`met2` with `licon1`/`mcon`/`via` — the full routing stack the
  analog cells draw (`layout/gen/gen_osc_bank.py` routes li1/met1/met2 only; met3+ is absent from
  this stream). Label layers `li1` `67/5`, `met1` `68/5`. The four custom cells print a stderr
  warning that `li1`'s `67/5` carries no text in that top cell — expected: only the PDK cells
  inside `osc_hd` label on `67/5`, the generator labels on `68/5`; stdout is unaffected.
- **Nets** `vdd`, `vss`, both `"kind": "supply"` — the stream's own labels (lowercase, drawn on
  `68/5` + `68/16` by the generator). The `sky130_fd_sc_hd` cells inside `osc_hd` additionally
  carry their own `VPWR`/`VGND`/pin labels on `67/5` and `68/5`; those are *undeclared* names
  riding the same islands, so no `same_net_as` binding is needed here — unlike the readout spec
  above, which had to bind two **declared** label families.
- **Ties** — the readout spec's two declarations, retargeted to the lowercase supplies:
  `nwell_tap` (well `64/20`, tap `65/44` dedicated, → `li1`, net `vdd`) and `psub_tap`
  (`well_layer: null` + `well_complement_of: ["64/20"]`, tap `65/44`, → `li1`, net `vss`). The
  substrate is not a drawn layer, so the psub tie's region is the caller-named complement and the
  citation discloses it under `checked_by_well_assertion` — real evaluated work, as in the
  digital run. The generator draws exactly these taps: per stage `tap`+implant+`licon`+`li1`+
  `mcon` at both rails in the custom cells, and the five `tapvpwrvgnd_1` instances in `osc_hd`.
- **`--deck sky130` is load-bearing on `osc_subth`**: it auto-carves the two `res_high_po`
  bias-divider bodies out of the `poly` conductor role (`provenance.devices`: `res_high_po`,
  body on `poly`, 570.47 µm², `source: "deck"`) — the tier doc's #2183 "device bodies are not
  wires" case. Without it the divider would read as a poly wire spanning `vdd` → `vbp` → `vss`.

### Verdict

Four cells: `erc_status: clean`, `erc_finding_count: 0`, every declared supply exactly one
island, both ties checked (not skipped, not degenerate). `osc_hd`: the same island counts and
checked ties, plus one recorded finding (below). Exit 4 on the clean cells is the designed
`--findings-only` outcome (antenna scope `not_checked`), exactly as in the digital run; exit 3 on
`osc_hd` is the finding.

### The `osc_hd` finding and its disposition (#292)

`erc.missing_tie`, net `vss`, tie `psub_tap`, region `(-190, 2910)–(45270, 2960)` dbu — checked
against the stream's conductor, device and well geometry:

- the region is the **50 nm strip between the `sky130_fd_sc_hd` cells' n-well top edge
  (y = 2910, spanning the cell's full width) and the met1 `VPWR` rail top edge (y = 2960)**. No
  `tap`, `diff`, `licon` or `li1` geometry exists inside it; its only conductor is the met1 rail.
- the n-well spans the cell's full width, so in per-cell scope the `psub_tap` region
  (`well_complement_of`) splits into two polygons — the tapped substrate below, the un-tapped
  sliver above: the model's isolated pocket.
- at `--top osc_bank` the **same spec reports no `missing_tie`** (probe, not committed): the
  sliver merges with the inter-row substrate the custom cells tap. That bank-level run instead
  reports the expected five islands per supply (two `erc.unconnected_net` findings) because no
  inter-oscillator PDN is drawn — which is why the bank is not the graded scope.

Disposition: **not a layout defect of this repo** — the sliver is inherent to every
`sky130_fd_sc_hd` row and comes from the pinned PDK GDS (`layout/gen/pdk_cells.json`), not from
`gen_osc_bank.py`; a generator "fix" would draw taps outside the site row in PDK territory and
invalidate the DRC/LVS/item-2 baselines. The finding is recorded, not suppressed, and tracked in
#292. Per the tier rule (zero `erc.missing_tie` from a checked tie) it blocks the analog ERC half
from `met` while the finding stands; because pinned `klayout-tools==0.9.1` resolves only one ERC
report per manifest key (last-wins in a list), citing all five per-cell reports under `11.analog`
would let a clean trailing cell mask this finding once LVS is added, so the manifest citation is
deferred (see "What is not claimed" below).

### `erc_coverage` (connectivity scope), quoted per cell

- `skipped`: `[]` on all five — no degenerate tie declaration, so every zero-`missing_tie`
  verdict is a checked pass, not `supply_spec_incomplete`.
- `inapplicable`: `erc.supply_short` (`substrate_continuity_not_modelled`) — same as the digital
  run: substrate continuity is not modeled, so supply-to-supply shorts through the substrate are
  not checked here. Rail-to-rail shorts on the **modeled conductors** (`poly`–`met2` via stack)
  are still checked and reported directly as `erc.supply_short` findings (zero on all five cells);
  the single-island counts establish per-supply continuity (no `erc.unconnected_net`), not rail
  isolation.
- `missing_tie_checked`: `true`; `checked_by_well_assertion`:
  `erc.missing_tie:["psub_tap"]` (the complement-derived substrate region);
  `checked_by_assertion`: `[]`.
- `checked`: 36 identities on `osc_hd`/`osc_nmos`/`osc_pmos`/`osc_wire` and 23 on `osc_subth`
  (32 / 19 `erc.floating_gate` gate checks — all clean — plus the 4 supply/tie work items).
- `layers_in_stream_without_declaration`: `65/20`, `68/16` everywhere, plus `64/5`, `64/59`,
  `83/44` in `osc_hd` — source/drain diffusion (not a conductor in this model), the generator's
  duplicate `met1_pin` labels, the PDK cells' `VPB`/`VNB` body labels and cell-outline markers.

### Internal nodes: what ERC can and cannot observe

`vbp` is a labelled node (`68/5`), observed as an undeclared signal net — the starved-gate bias
bus, deliberately not a `nets[]` supply. The schematic's `vh1`..`vh14` (the header/inverter
shared diffusion junctions, #117) are **not labelled in the stream and not observable by name**:
diffusion (`65/20`) is not a declared conductor, so those junctions have no named ERC result to
cite. Nothing about them is claimed here; their extraction split is #117 /
2AMLogic/klayout-tools#5311's subject, unchanged by this run.

### What is not claimed

- **Antenna verdicts are unchecked** (`--findings-only`), as in the digital run; item 11 grades
  the connectivity scope only (#1994).
- **The per-cell scope cannot be replayed by `--check --rerun` on 0.9.1.** The cheap
  `--check` (hash-only) reports `match` on all five committed reports, but `--check --rerun`
  re-runs the stream's **bank top** instead of the recorded `--top` (observed on
  `erc/osc_hd.report.json`: fresh `gate_count` 147 vs committed 32, five supply islands, status
  `drifted`, exit 3) — `--top` is not recorded in the report. Tracked as
  2AMLogic/klayout-tools#7022; full replay today = re-run the per-cell command above and diff.
- **`11.analog` is not claimed, and its manifest citation is deferred under `klayout-tools==0.9.1`.**
  All five per-oscillator reports are committed under `erc/osc_*.report.json` as evidence, but
  `manifests/sky130-process-monitor.json` does not cite them yet: pinned `klt signoff` (`0.9.1`)
  resolves only one report per evidence kind (last-wins in a list), so citing all five per-cell
  reports would let a clean trailing cell (`osc_subth`) mask the `osc_hd` `erc.missing_tie`
  finding (#292) once an LVS report is added, and citing any single cell would cover only one of
  the five oscillators. `11.analog` therefore stays `unmet` / `no_evidence` and the committed
  signoff record is unchanged from `main` until #26/#33 supply partition-level LVS alongside
  bank-level or multi-report ERC grading and #292 is resolved.
