# verification

Digital flow (cocotb + Icarus, Verilator lint, Yosys). Today only a toolchain smoke exists, against the
placeholder `rtl/smoke/smoke.v` (a 4-bit counter, not part of the design).

## Entry point

    make -C verification/smoke all

Runs `sim/check_env.sh` (pins in `sim/pdk.json`, `sim/toolchain.json`), Verilator lint, the cocotb test
`verification/smoke/test_smoke.py` on Icarus, then Yosys synthesis to `sky130_fd_sc_hd` against the
typical Liberty (`tt_025C_1v80`). Scratch output goes to `sim/build/` (gitignored).

## Negative controls

    make -C verification/smoke negative-control

A broken cocotb expectation (`SMOKE_BREAK=1`) and a wrong Liberty path must each fail; the target exits 0
only if both do. The analog and pin controls are in `sim/negative_controls.sh`.
