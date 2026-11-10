# layout

Two partitions: the digital readout (P&R, `readout/`, below) and the analog oscillator bank
(generated stream, this section).

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
| `osc_wire` | 83.9 × 146.1 | 12 257 |
| `osc_subth` | 53.1 × 6.6 | 350 |
| **Sum of footprints** | | **14 457 µm² = 0.0145 mm²** |

Against spec §8 (≤ 0.02 mm² for the **whole** block, fallback ≤ 0.05 mm²): the oscillators alone,
as laid out here, are 72 % of the target budget and 29 % of the fallback, before any readout
(#24). **This issue does not pass/fail §8**; it records the oscillator share. `osc_wire` was
23 212 µm² before the repack (202.3 × 114.8 µm); it is now 12 257 µm², 47 % smaller. All figures
are derived from the committed stream (`klt stats --top <cell> layout/osc_bank.gds`, summed by
hand); none is measured, and none is DRC- or LVS-checked.

**What limits `osc_wire` now.** The met1 floor is 31 × 1000 µm × 0.28 µm pitch ≈ 8 680 µm²
(0.0087 mm²); the cell is 1.41× that, 3 580 µm² over. Rough split (derived by arithmetic from the
generator constants and the 83.9 µm width, not separately measured): the 0.70 µm clear gap between
serpentine rows costs ≈ 1 800 µm²; the stage column plus the 2 µm lead-in above the band costs
≈ 1 900 µm² (the band sits below the stage devices, so their height adds to the box instead of
overlapping it); the 0.30 µm run pitch, chosen to leave 0.16 µm of met1 space against the
0.14 µm rule, costs ≈ 600 µm² against a 0.28 µm pitch. Feed stubs are a narrow met1/met2 column at the
band's left edge and add little. Each serpentine's two ends go out on met2 to that column, so no
feed crosses a run. Closing the gap would mean pitch exactly at the rule, a tighter row gap, or
interleaving serpentines; each gives up margin that DRC (#25) should judge first. The 1000 µm
wire length is unchanged.

The five-corner/PVT behaviour of this layout is untested: no parasitics are extracted (#32), so
the #17 frequencies do not apply to this layout.

## Digital readout (`readout/`, T1 item 2 digital; issue #24)

Routed `readout` block from `klt place-and-route`, regenerated from the gate-level netlist
`synth/readout/readout.gl.v` (#22). **Simulated-flow output (OpenROAD, `tt_025C_1v80`, seed 1); not
DRC-, LVS- or extraction-checked (#25, #26, #32); nothing here is measured.**

- `readout/request.json` — the request: `sky130_fd_sc_hd`, `power.preset: sky130hd` (tapcells, PDN, fillers),
  40 % target utilization, `clk_ref` at 100 ns (10 MHz, spec §reference clock), `target_stage: route`.
- `readout/report.json` — the `--format json` report (committed so `--check` has a baseline). It records
  absolute paths from the machine that produced it; the hash fields drive `--check`.
- `readout/out/readout.def`, `readout.gds` — routed DEF and merged GDS. `readout/out/readout.v` — the
  **as-built** netlist (CTS buffers, antenna diodes). **LVS (#26) should use `readout.v`, not the pre-CTS
  `synth/readout/readout.gl.v`.** Intermediate ODB, Tcl and per-corner metrics from the run are not committed.

Regenerate (run from the repo root: the OpenROAD wrapper mounts only `$PWD`; ~5 min):

```console
klt place-and-route layout/readout/request.json --format json > layout/readout/report.json
klt place-and-route layout/readout/request.json --check layout/readout/report.json          # cheap: re-hash netlist + liberty
klt place-and-route layout/readout/request.json --check layout/readout/report.json --rerun  # re-run OpenROAD, diff verdicts
```

`--check` (cheap) and `--check --rerun` both reported `match` for the committed files. Then re-attest:
`klt signoff --attest 2 --input layout/readout/out/readout.gds --inventory attest/item2_digital.json -o evidence/item2_digital.json`
(cited as `2.digital`).

Reported by the flow, **simulated, not a pass/fail claim here**: die 39 970 µm² (0.040 mm²), core
36 435 µm², 42.9 % utilization, 5 341 components (468 tapcells, 3 620 fillers), PDN present
(`power.pdn: true`), 0 setup / hold / antenna / route-DRC violations as counted by the flow (nominal-corner worst setup
slack 82.06 ns against the 100 ns clock; the 16 swept corners are in the report). The die includes the floorplan margin and
the 40 % utilization headroom; spec §8 (≤ 0.02 mm², *proposed*) is not judged here. Synthesis cell area was
14 734 µm². The `readout` top has no timing sign-off claim: timing and PVT belong to #30.
