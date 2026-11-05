# sim

Analog flow (ngspice on the sky130 models). Everything here is toolchain
bring-up: nothing is a design result.

## Pins

- `pdk.json` — sky130A open_pdks revision, model library / cell SPICE / Liberty paths inside the PDK. The PDK
  root defaults to `~/.volare/sky130A`; override with `PDK_ROOT_SKY130A`.
- `toolchain.json` — ngspice (a `>=` floor), Icarus, Yosys, Verilator, cocotb (exact) versions, and the xschem package version
  (checked via `dpkg-query` only; raw `xschem` is never run, use `klt netlist`).
- `check_env.sh` — exits non-zero on any mismatch, version below the ngspice floor, or missing path; it prints the measured ngspice version. Both smoke flows call it first.

## Environment

ngspice is a **floor** (`>= 46`, not an exact pin: the fleet tracks the current upstream release, operator ruling 2026-10-29, 2AMLogic/2am#6391); the measured version is printed by `check_env.sh` and recorded in each result. The Icarus 13.0, Yosys 0.67 and Verilator 5.050 pins stay exact. These are the tools provisioned in `~/.local/bin` on fleet
workers (2AMLogic/2am `infra/aws/loom-worker/`); `~/.local/bin` must come **before** `/usr/bin` on `PATH` (distro
packages there are older: e.g. ngspice 42, below the floor). The cocotb 2.1.0 pin is **not** in that worker spec (it has no cocotb
entry) and workers can differ: it is the version a reviewing worker reported (`cocotb-config --version`). Where cocotb
is absent, use a venv inside the worktree (`python3 -m venv .venv && .venv/bin/pip install cocotb==2.1.0`, with
`.venv/bin` on `PATH`) rather than touching host-wide tools; the worker-spec gap is tracked as a spec change, not a host
change. On a shell without the pinned tools, `check_env.sh` fails and names the resolved binary. Nothing here installs
or modifies those tools. The flows were verified from a worktree, not a fresh clone.

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

## Oscillator bank

    sim/osc_bank/run.sh [osc_name ...]      # default: all five
    sim/osc_bank/negative_controls.sh

One `ngspice -b` per oscillator (`bench_<osc>.spice`, netlists from `design/osc_bank/`), `tt` / 1.8 V / 27 °C,
single-unit and local by design. After skipping the start-up edges each bench measures `f_osc_hz` and the mean
supply current `i_avg_ua` over a whole number of cycles. If **every** ring oscillates, one record per oscillator is
appended to `measurements/osc_bank_records.jsonl` (append-only, labelled SIMULATED, with corner, testbench, netlist,
open_pdks, model file and ngspice version); if any ring does not, `run.sh` exits non-zero, names it, and appends
nothing. The PDK/ngspice pins are read via `check_env.sh`, not repeated. The PVT surfaces and Monte Carlo are #8
and go through `klt sim`. `osc_subth`'s `i_avg_ua` includes ~1 µA of bias divider (see `design/osc_bank/README.md`).
The controls check that a tied-off enable fails and appends nothing, and that a drifted schematic is reported by
`klt netlist --check`.
