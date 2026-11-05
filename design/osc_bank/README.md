# design/osc_bank

The five oscillators of the bank (`spec/target-spec.md` §1), one xschem schematic each, with the
`klt netlist` output committed beside it. **Simulation intent only**: planning-level device sizes,
no layout, nothing measured. Stage counts are the ratified planning figures; changing one needs a
new decision record, not an edit here.

| Oscillator | Stages | What dominates the delay |
|---|---|---|
| `osc_hd` | 31 | plain `sky130_fd_sc_hd` baseline: NAND2 enable stage + 30 × `inv_1` (the only standard-cell chain) |
| `osc_nmos` | 31 | NMOS: long-L (0.5 µm) minimum-W pull-downs, wide fast pull-ups |
| `osc_pmos` | 31 | PMOS: long-L minimum-W pull-ups, wide fast pull-downs |
| `osc_wire` | 31 | wire: strong inverters driving a lumped `res_generic_m1` (W 0.14 µm, L 1000 µm) + 100 fF shunt C per stage |
| `osc_subth` | 15 | subthreshold: every inverter after the NAND has a LVT PMOS header whose gate is held ~0.3 V inside the rail |

Every ring starts with a NAND2 whose second input is `en`, so each has an odd inversion count and
`en` = 0 parks it in a defined state. Ports: `en`, `out`, `vdd`, `vss`.

## Caveats (read before using a number)

- **Placeholders, not designs.** The wire RC uses an ideal capacitor, and the `osc_subth` header bias
  (`vbp`, ~1.5 V) comes from an **ideal resistor divider** inside the schematic (1.8 V / 1.8 MΩ ≈ 1 µA,
  no tempco, no mismatch). This is not a bias-generator design; the supply current `osc_subth` reports
  **includes that ~1 µA**. The wire cap in particular hides any voltage/temperature dependence.
- **Why a header only.** A header *and* footer (diode-connected, or biased, standard-Vt or LVT) left
  every stage in a stable low-gain equilibrium in simulation: no oscillation. The single-sided header
  design oscillates (`measurements/osc_bank_records.jsonl`). Whether it is the right subthreshold
  oscillator is exactly the model question left to #10.
- **Subthreshold models.** Frequency of `osc_subth` rests on the least-exercised part of the open
  model set; one tt point says nothing about its slope or tempco.

## Files

- `gen_schematics.py` — how the `.sch` files were drawn (`python3 -I design/osc_bank/gen_schematics.py`).
  Connectivity is by `lab_pin` net names, so the files read cleanly in xschem.
- `xschemrc` — project-local symbol search path (stock xschem devices + the sky130A PDK `libs.tech/xschem`).
- `osc_*.sch` / `osc_*.spice` — schematic and its committed netlist.

## Regenerating / checking the netlists

    klt netlist design/osc_bank/osc_hd.sch -o design/osc_bank/osc_hd.spice --block \
        --rcfile design/osc_bank/xschemrc --pdk sky130A --pdk-root <pinned PDK root>
    klt netlist ... --check --ignore-comments      # must report: match

`--block` emits the top-level `.subckt` so a bench can `.include` it. `--ignore-comments` is needed
because xschem writes an absolute `** sch_path:` comment line into every netlist, which differs per
checkout. Run the benches with `sim/osc_bank/run.sh`.
