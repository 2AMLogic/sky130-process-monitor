# verification

Digital flow (cocotb + Icarus, Verilator lint, Yosys). Today only a toolchain smoke exists, against the
placeholder `rtl/smoke/smoke.v` (a 4-bit counter, not part of the design).

## Entry point

There is no root Makefile; run from the repo root with `make -C verification/smoke <target>`. Tool pins and `PATH`
requirements: see `sim/README.md` § Environment.

    make -C verification/smoke all

Runs `sim/check_env.sh` (pins in `sim/pdk.json`, `sim/toolchain.json`), Verilator lint, the cocotb test
`verification/smoke/test_smoke.py` on Icarus, then Yosys synthesis to `sky130_fd_sc_hd` against the
typical Liberty (`tt_025C_1v80`). Scratch output goes to `sim/build/` (gitignored).

## Negative controls

    make -C verification/smoke negative-control

A broken cocotb expectation (`SMOKE_BREAK=1`, must show an `AssertionError`) and a wrong Liberty path (Yosys must report it not found) must each fail; the target exits 0
only if both do. The analog and pin controls are in `sim/negative_controls.sh`.
