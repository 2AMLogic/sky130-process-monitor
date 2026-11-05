# layout

Oscillator-bank layout (T1 item 2, analog partition; issue #23). **Planning-level geometry,
generated from source, not DRC-, LVS- or extraction-checked** (those are #25, #26, #32). Nothing
here is measured; every area below is a **simulated/derived** figure from the committed stream.

- `osc_bank.gds` — committed stream. Top cell `osc_bank`; cells `osc_hd`, `osc_nmos`, `osc_pmos`,
  `osc_wire`, `osc_subth` (ports labelled `en`, `out`, `vdd`, `vss`, plus `vbp` on `osc_subth`).
- `gen/gen_osc_bank.py` — the generator. `python3 layout/gen/gen_osc_bank.py` rewrites the stream
  byte-for-byte (verified: two runs give the same sha256). Needs `klayout` (`gen/requirements.txt`,
  tested 0.30.10) and the sky130A PDK of `sim/pdk.json`; `gen/pdk_cells.json` pins the sha256 of the
  `sky130_fd_sc_hd.gds` it reads and the generator refuses a different file.
- `gen/check_connectivity.py` — net-connectivity sanity check (not LVS): labelled nets distinct,
  and the number of S/D-driven gate nets equals the #17 stage count (31 / 31 / 31 / 31 / 15), i.e.
  every stage output reaches the next stage's gate and the last output feeds back to the NAND.
- `gen/attest_item2.py` — writes `evidence/item2.json` (artifact-anchored generic envelope, item 2;
  `klt signoff --attest` has no item-2 verb). The manifest pins the stream's hash under `2.analog`;
  editing the stream without re-running it turns the row stale.

Stage counts and device sizes follow the merged #17 schematics (`design/osc_bank/*.spice`) device
for device. `osc_hd` places PDK `nand2_1` + 30 × `inv_1` (+ 5 `tapvpwrvgnd_1`) from the pinned PDK
GDS; the other four are transistor-level (single finger, vertical poly, li1/met1, per-stage taps).

## Not drawn (gaps against the #17 schematics — LVS #26 must resolve these)

- `osc_wire`: the 31 × 100 fF shunt capacitors (`C` in the schematic) are ideal placeholders and
  are **not drawn**. The `res_generic_m1` (W 0.14 µm, L 1000 µm) *is* drawn: met1 serpentine, 8
  runs, centreline 1000 µm (feed stubs excluded).
- `osc_subth`: the `Rb0`/`Rb1` bias divider (ideal resistors) is **not drawn**; `vbp` is a labelled
  met1 net that an external source or a later divider must drive.
- LVT header pFETs use `lvtn` (125/44), which the sky130A tech file defines for LVT devices.

## Area (derived from the stream; `klt stats --top <cell>`)

Footprint = bounding box of the cell (includes port stubs and, for `osc_wire`, the serpentine band).

| Cell | Footprint (µm) | Footprint (µm²) |
|---|---|---|
| `osc_hd` | 45.5 × 3.2 | 145 |
| `osc_nmos` | 84.8 × 8.8 | 742 |
| `osc_pmos` | 84.8 × 11.3 | 961 |
| `osc_wire` | 202.3 × 114.8 | 23 212 |
| `osc_subth` | 53.1 × 6.6 | 350 |
| **Sum of footprints** | | **25 410 µm² = 0.0254 mm²** |

Against spec §8 (≤ 0.02 mm² for the **whole** block, fallback ≤ 0.05 mm²): the oscillators alone,
as laid out here, are 127 % of the target budget and 51 % of the fallback, before any readout
(#24). **This issue does not pass/fail §8**; it records the oscillator share. The driver is
`osc_wire`: 31 serpentines of 1000 µm × 0.14 µm at a 0.28 µm pitch cannot occupy less than
about 31 × 280 µm² ≈ 0.0087 mm² of met1 even if packed perfectly, and this generator's loose
packing (3 µm row pitch, one stage-aligned column) uses 0.0232 mm². Whether the 1000 µm wire
length is affordable is a spec question for a decision record, not something this issue changes.

The five-corner/PVT behaviour of this layout is untested: no parasitics are extracted (#32), so
the #17 frequencies do not apply to this layout.
