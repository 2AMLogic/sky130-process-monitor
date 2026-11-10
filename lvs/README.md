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
| `osc_subth` | same | **reduced** `osc_subth.ref.spice` (`make_reduced_refs.py`) | match, *not item-1* | 34/34, 46/46 |

## What is and is not claimed

- `4.digital` is cited in the manifest and graded `met`.
- **`4.analog` is NOT cited and stays unmet.** `osc_wire` and `osc_subth` match only against references with
  schematic elements removed, so they are transistor-topology results, not LVS against the item-1 netlist:
  - `osc_wire`: the 31 ideal 100 fF shunt caps are dropped and each wire resistor is shorted (the met1 serpentine
    is plain metal to the extractor, so both ends are one net).
  - `osc_subth`: the ideal `Rb0`/`Rb1` bias divider is dropped (`vbp` is a labelled net, not driven by a divider).
  Against the unreduced item-1 netlists these cells cannot match (no capacitor, wire resistor or divider is drawn).
  Closing it needs either those devices drawn or a ratified schematic/netlist change; neither is done here.
- The pin-count line for `osc_hd` (34 layout pins vs 4) is the flattened reference; see the report.

## Layout fixes this run required (`layout/gen/gen_osc_bank.py`, `layout/osc_bank.gds` regenerated)

LVS against the first-pass stream mismatched on device parameters (all values from `klt extract`):
1. One straight poly stripe crossed NFET and PFET, so every PFET extracted at the NFET gate length
   (0.5 µm instead of the schematic 0.15 µm in `osc_nmos`; the converse in `osc_pmos`). The stripe now steps
   between the two widths in the gap.
2. In `osc_subth` the series LVT header PFET shared the 0.84 µm inverter-PFET diffusion; the schematic header is
   0.42 µm. The diffusion now steps to 0.42 µm across the header.

`evidence/item2.json` was re-attested for the new stream. DRC (#25) and extraction (#32) have not been re-run on it.

## PDK provenance

The report records `open_pdks f6eeac7d…` found under `~/.ciel`; `sim/pdk.json` pins `c6d73a35…` (also present under
`~/.volare`). The sky130A decks and the cell SPICE used here come from the search roots as listed in each report.
