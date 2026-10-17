# sim

Analog flow (ngspice on the sky130 models). Everything here is toolchain
bring-up: nothing is a design result.

## Pins

- `pdk.json` — sky130A open_pdks revision, model library / cell SPICE / Liberty paths inside the PDK. The PDK
  root defaults to `~/.volare/sky130A`; override with `PDK_ROOT_SKY130A`.
- `toolchain.json` — ngspice, Icarus, Yosys, Verilator, cocotb versions, and the xschem package version
  (checked via `dpkg-query` only; raw `xschem` is never run, use `klt netlist`).
- `check_env.sh` — exits non-zero on any mismatch or missing path. Both smoke flows call it first.

## Entry point

    sim/smoke/run.sh

Runs one `ngspice -b` (single corner, local) on `sim/smoke/inv_smoke.spice`: `sky130_fd_sc_hd__inv_1`,
`tt`, 1.8 V, 27 °C, 10 fF load. It appends one line to `measurements/inv_smoke_records.jsonl`
(append-only; each record is labelled SIMULATED and names the corner, testbench, open_pdks revision,
model file and ngspice version). It proves the models and cell views load; it makes no design claim.

## Negative controls

    sim/negative_controls.sh

Wrong model path, edited PDK pin, edited tool pin and absent PDK must each fail (exit 0 means all did).
A failed run appends no record.
