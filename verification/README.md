# verification

Digital flow (cocotb + Icarus, Verilator lint) for the readout partition. There is no root Makefile; run from the
repo root with `make -C verification/readout <target>`. Tool pins and `PATH` requirements: see `sim/README.md`
§ Environment. Synthesis is driven through `klt synthesize` (`synth/readout/`, see `rtl/README.md`). The analog
and pin negative controls are in `sim/negative_controls.sh`.

## Entry point

    make -C verification/readout            # check-env, Verilator lint (-Wall), cocotb on Icarus
    make -C verification/readout negative-control

`verification/readout/test_readout.py` tests `rtl/readout/` (register map: `rtl/README.md`): count correctness over
several (f_osc, k) pairs within the ±2 CDC tolerance, saturation and overflow, select switching, busy/done
sequencing, `start` while busy, `CAL` read-back, reset values and reset mid-gate. Saturation preloads the counter
through a hierarchical deposit because reaching 2^24 organically costs minutes of simulation. The log reports the
five-oscillator read at 10 MHz, k = 10 as a simulated figure (RTL simulation, Icarus). `negative-control` runs with
`READOUT_BREAK=1` (every expected count offset) and must fail with an `AssertionError`. cocotb is not provisioned on
workers: use a venv inside the worktree (`sim/README.md`).

## Post-layout re-run with back-annotated SDF (T1 item 7, digital; issue #32)

SIMULATED (Icarus 13.0, cocotb 2.1.0, `klt 0.9.2.dev460+g1c0ae85debd3`); nothing here is measured.

- SDF: `layout/readout/request.sdf.json` is `layout/readout/request.json` plus `post_route_spef` and
  `post_route_sdf` (output dir `out_sdf`, scratch removed except the SDF). `klt place-and-route` wrote
  `layout/readout/out_sdf/readout_route.sdf` (sha256 `1a8475c9…`) from its post-route `read_spef` session
  (SPEF sha256 `6fb61806…`, not committed). Re-running P&R reproduced the committed `readout.def`
  (`32aef484…`) and `readout.v` (`db50b86b…`) byte for byte. Report: `layout/readout/report.sdf.json`.
  `klt place-and-route` already had this capability; no SDF was hand-written.
- Run: `request-sdf.json` re-runs `test_readout.py` unchanged on the routed `layout/readout/out/readout.v`
  with the PDK timing models (`primitives.v`, `sky130_fd_sc_hd.v`, no `FUNCTIONAL`), SDF corner `typ`.
  The three source/SDF paths are `~/.ciel` absolute PDK paths on this host; adjust for another install.
  `functional-verification-sdf.report.json`: 8/8 passed, `environment.sdf.annotated: true`.
  cocotb is not provisioned on workers, so the run used a throwaway
  `uvx --from "klayout-tools[functional-verification] @ git+https://github.com/2AMLogic/klayout-tools.git@1c0ae85d…" klt functional-verification request-sdf.json -o verification/readout/.fv-sdf --format json`.
- Cited as `7.digital`; `klt signoff --manifest` grades it **met**.

Disclosed limits (not relaxed):

1. **`saturation_overflow` is not run.** It deposits into `u_cnt.count` / reads `u_cnt.running`, hierarchy
   that the flat routed netlist does not have. Selected tests (`testbench.testcase`): the other 8 of 9.
2. **Partial annotation.** `environment.sdf.partial: true`: 323 `TIMINGCHECK` entries are dropped (Icarus does
   not implement them, so setup/hold run against the cell library's placeholder checks, not the SDF's
   limits) and 164 zero-delay `INTERCONNECT` entries are removed. SPEF net coverage is 1254 of 1255
   design nets (`annotation_complete: false` in the P&R report).
3. **One corner.** The SDF is the `tt_025C_1v80` post-route session and was annotated at `typ`; no min/max
   or other-corner SDF was run, so this says nothing about the corner box. It does not replace the
   multi-corner STA of item 5.
4. **Oscillator timing.** `test_readout.py` drives the `osc` inputs as ideal clocks (periods ≥ 4 ns); the
   routed netlist's input-to-flop delay is not exercised at the real oscillator frequencies.
