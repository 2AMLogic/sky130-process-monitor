# sim

Analog flow (ngspice on the sky130 models). Everything here is toolchain
bring-up: nothing is a design result.

## Pins

- `pdk.json` — sky130A open_pdks revision, model library / cell SPICE / Liberty paths inside the PDK. The PDK
  root defaults to `~/.volare/sky130A`; override with `PDK_ROOT_SKY130A`.
- `toolchain.json` — ngspice, Icarus, Yosys, Verilator, cocotb versions, and the xschem package version
  (checked via `dpkg-query` only; raw `xschem` is never run, use `klt netlist`).
- `check_env.sh` — exits non-zero on any mismatch or missing path. Both smoke flows call it first.

## Environment

The pins describe the fleet worker spec (2AMLogic/2am `infra/aws/loom-worker/`): the pinned ngspice 46, Icarus 13.0,
Yosys 0.67, Verilator 5.050 and cocotb 2.0.1 live in `~/.local/bin`, which must come **before** `/usr/bin` on `PATH`
(distro packages there are older: e.g. ngspice 42). On a shell without it, `check_env.sh` fails and names the resolved
binary. Nothing here installs or modifies those tools. The flows were verified from this worktree, not a fresh clone.

## Entry point

    sim/smoke/run.sh

Runs one `ngspice -b` (single corner, local) on `sim/smoke/inv_smoke.spice`: `sky130_fd_sc_hd__inv_1`,
`tt`, 1.8 V, 27 °C, 10 fF load. It appends one line to `measurements/inv_smoke_records.jsonl`
(append-only; each record is labelled SIMULATED and names the corner, testbench, open_pdks revision,
model file and ngspice version). It proves the models and cell views load; it makes no design claim.

## Negative controls

    sim/negative_controls.sh

Wrong model path, edited PDK pin, edited tool pin and absent PDK must each fail **with the expected diagnostic**
(the script greps for it), after a baseline `check_env.sh` pass, so a broken environment is not read as a control
passing. Exit 0 means all did; exit 2 means the environment itself is broken. A failed run appends no record.
