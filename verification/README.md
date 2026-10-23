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

## Readout

    make -C verification/readout            # check-env, Verilator lint (-Wall), cocotb on Icarus
    make -C verification/readout negative-control

`verification/readout/test_readout.py` tests `rtl/readout/` (register map: `rtl/README.md`): count correctness over
several (f_osc, k) pairs within the ±2 CDC tolerance, saturation and overflow, select switching, busy/done
sequencing, `start` while busy, `CAL` read-back, reset values and reset mid-gate. Saturation preloads the counter
through a hierarchical deposit because reaching 2^24 organically costs minutes of simulation. The log reports the
five-oscillator read at 10 MHz, k = 10 as a simulated figure (RTL simulation, Icarus). `negative-control` runs with
`READOUT_BREAK=1` (every expected count offset) and must fail with an `AssertionError`. cocotb is not provisioned on
workers: use a venv inside the worktree (`sim/README.md`).
