# lvs — T1 item 4 (issue #26)

`klt lvs` reports, engine `klayout` (0.30.13 as resolved here; `klt 0.9.2.dev441`), deck `sky130`,
PDK `sky130A`. **Simulated-flow results; nothing here is measured.** Each `*.report.json` is the
`--format json -o` output of the same-named `*.request.json` (run from this directory's parent:
`klt lvs lvs/<cell>.request.json --format json -o lvs/<cell>.report.json`; `--check` re-hashes inputs).

| Cell | Layout side | Reference | status | Counts (nets/devices) |
|---|---|---|---|---|
| `readout` (4.digital) | `readout.gate.spice` (`klt extract --abstract-cells 'sky130_fd_sc_hd__*' --def-net-names`) | as-built `layout/readout/out/readout.v`, `gate-level-verilog` | **match**, `power_connectivity` **match** | 1290 / 0 (cells are black boxes) |
| `osc_nmos` | `layout/osc_bank.gds` | `design/osc_bank/osc_nmos.spice` (item 1) | **match** | 35/35, 64/64 |
| `osc_pmos` | same | `design/osc_bank/osc_pmos.spice` (item 1) | **match** | 35/35, 64/64 |
| `osc_hd` | same | item-1 `osc_hd.spice` + PDK cell bodies (`make_osc_hd_ref.py`), flattened | **match** (warning `topology.flattened`) | 35/35, 64/64 |
| `osc_wire` | same | **reduced** `osc_wire.ref.spice` (`make_reduced_refs.py`) | match, *not item-1* | 35/36, 64/64 |
| `osc_subth` | same | `osc_subth.ref.spice` (`make_reduced_refs.py`): item-1 netlist with `Rb0`/`Rb1` realised as PDK `res_high_po_0p35` | match, *not item-1* (ideal R replaced) | 34/34, 48/48 |

## What is and is not claimed

- `4.digital` is cited in the manifest and graded `met`.
- **`4.analog` is NOT cited and stays unmet.** `osc_wire` and `osc_subth` match only against references with
  schematic elements removed, so they are transistor-topology results, not LVS against the item-1 netlist:
  - `osc_wire`: the 31 ideal 100 fF shunt caps are dropped and each wire resistor is shorted (the met1 serpentine
    is plain metal to the extractor, so both ends are one net).
  - `osc_subth` (issue #109): the divider is now drawn. The reference keeps `Rb0`/`Rb1` but swaps each ideal R for a
    `sky130_fd_pr__res_high_po_0p35` at L = 270 / 1360 µm, W 0.35 µm (layout: 269.99 / 1359.92 µm by `klt extract`).
    The item-1 schematic still has ideal 300k / 1500k, so this is still not LVS against item 1; closing it needs the
    schematic to carry the PDK resistor (a `spec/` decision), not done here. **`klt lvs` does not compare resistor
    L/W** (`device.geometry_not_compared`; `R` is a placeholder 0 on the reference side), so the L agreement above is
    checked by hand from the extract, not by LVS. Topology (which net each resistor joins) is compared and matches.
  Against the unreduced item-1 netlists `osc_wire` cannot match (no capacitor or wire resistor is drawn).
  Closing it needs either those devices drawn or a ratified schematic/netlist change; neither is done here.
- The pin-count line for `osc_hd` (34 layout pins vs 4) is the flattened reference; see the report.

## Layout fixes this run required (`layout/gen/gen_osc_bank.py`, `layout/osc_bank.gds` regenerated)

LVS against the first-pass stream mismatched on device parameters (all values from `klt extract`):
1. One straight poly stripe crossed NFET and PFET, so every PFET extracted at the NFET gate length
   (0.5 µm instead of the schematic 0.15 µm in `osc_nmos`; the converse in `osc_pmos`). The stripe now steps
   between the two widths in the gap.
2. In `osc_subth` the series LVT header PFET shared the 0.84 µm inverter-PFET diffusion; the schematic header is
   0.42 µm. The diffusion now steps to 0.42 µm across the header.

`evidence/item2.json` was re-attested for the new stream. DRC was re-run (#25, `drc/README.md`); extraction (#32) has not been.

## Divider added (issue #109) — all re-run with `klayout-tools==0.9.1`

`layout/osc_bank.gds` now draws the `osc_subth` bias divider (two `res_high_po_0p35` serpentines). Re-run with the CI pin
(`uvx --from klayout-tools==0.9.1 klt extract … ; klt lvs …`): `osc_subth` `match` (34/34 nets, 48/48 devices); the other
four cells still `match` with unchanged counts. The deck reads the resistors as `res_high_po` with its own sheet
resistance, so the extracted `r=` (1.263 MΩ / 252 kΩ) differs from the 1.50 MΩ / 300 kΩ the *ngspice* model gives for the
same L; the layout lengths were set from the ngspice model, not the extractor's `r`. Note: the current host `klt`
(0.9.2.dev661) extracts the *unmodified* main stream with 14 `osc_subth` header-pFET mismatches, so these results are for
the pin only; that drift is not caused by this change.

## PDK provenance

The report records `open_pdks f6eeac7d…` found under `~/.ciel`; `sim/pdk.json` pins `c6d73a35…` (also present under
`~/.volare`). The sky130A decks and the cell SPICE used here come from the search roots as listed in each report.
