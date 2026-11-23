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
five-oscillator read at 10 MHz, k = 10 as a simulated figure (RTL simulation, Icarus). `conversion_time_surfaces`
(spec §6, issue #281) drives the five oscillators at periods taken from the committed frequency surfaces
(`sim/sensitivity/records/reports/`) at the nominal cell and the slowest-`osc_subth` cell (sf, 1.98 V, −40 °C),
reads the bank at three gate settings (spec default 2^10; 2^14 on the whole bank; 2^14 on `osc_subth` only — the
two k = 14 readings of `sim/sensitivity/records/2026-11-14-osc-subth-gate-sizing.md`), and writes
`verification/readout/conversion-time.json` itself: per-oscillator and full-read conversion time in clk_ref cycles
and seconds at 10 MHz, every oscillator period traced to a named surface report and grid cell, reads that do not
complete recorded as such with gate and period, and each completed full read graded against the spec §6
target / fallback / stretch bounds exactly as it comes out (the SDF-annotated run of the same test writes
`conversion-time-sdf.json`, nominal cell only — see the post-layout section). `negative-control` runs with
`READOUT_BREAK=1` (every expected count offset) and must fail with an `AssertionError`. cocotb is not provisioned on
workers: use a venv inside the worktree (`sim/README.md`).

## Cold-start invocation (T1 item 9)

    make -C verification/readout

is the documented cold start for the digital partition, declared by `attest/item9_digital.json` and
run by `klt signoff --attest 9` to produce `evidence/item9_digital.json` (cited as `9.digital`). It
reproduces the pre-layout run cited as `5.digital` in full: `check_env.sh`, Verilator lint `-Wall`,
then the whole cocotb suite on Icarus. cocotb is not provisioned on workers — make a worktree venv
first (`sim/README.md` § Environment).

The attestation runs the RTL bench. To reproduce the separate SDF run, point the two absolute
PDK model paths in a local copy of `request-sdf.json` at your pinned sky130A installation.
That exclusion is stated in `manifests/README.md` § "Item 9 (testbenches shipped)".

## Post-layout re-run with back-annotated SDF (T1 item 7, digital; issue #32)

SIMULATED with Icarus 13.0, cocotb 2.1.0 and klayout-tools 0.9.1.

- SDF: `layout/readout/request.sdf.json` is `layout/readout/request.json` plus `post_route_spef` and
  `post_route_sdf` (output dir `out_sdf`, scratch removed except the SDF). `klt place-and-route` wrote
  `layout/readout/out_sdf/readout_route.sdf` (sha256 `1a8475c9…`) from its post-route `read_spef` session
  (SPEF sha256 `6fb61806…`, not committed). Re-running P&R reproduced the committed `readout.def`
  (`32aef484…`) and `readout.v` (`db50b86b…`) byte for byte. Report: `layout/readout/report.sdf.json`.
  `klt place-and-route` already had this capability; no SDF was hand-written.
- Run: `request-sdf.json` re-runs `test_readout.py` unchanged on the routed `layout/readout/out/readout.v`
  with the PDK timing models (`primitives.v`, `sky130_fd_sc_hd.v`, no `FUNCTIONAL`), SDF corner `typ`.
  The netlist and SDF paths resolve relative to the request. The report records the resolved absolute SDF path.
  `functional-verification-sdf.report.json` records 9/9 passed and `environment.sdf.annotated: true`.
  `conversion_time_surfaces` writes `conversion-time-sdf.json` for the nominal cell using the
  `tt_025C_1v80` SDF. To reproduce from the repo root, set `PDK_ROOT_SKY130A` to the revision in
  `sim/pdk.json` and keep the local request beside the original so its relative paths resolve.

  ```sh
  bench=verification/readout
  jq --arg lib "${PDK_ROOT_SKY130A:?}/libs.ref/sky130_fd_sc_hd/verilog" \
    '.sources[1:] |= map($lib + "/" + (split("/") | last))' \
    "$bench/request-sdf.json" > "$bench/.request-sdf-local.json"
  uvx --from 'klayout-tools[functional-verification]==0.9.1' --with 'cocotb==2.1.0' \
    klt functional-verification "$bench/.request-sdf-local.json" -o "$bench/.fv-sdf" --format json
  ```

- Cited as `7.digital`; `klt signoff --manifest` grades it **met**.

Disclosed limits (not relaxed):

1. **`saturation_overflow` is not run.** It deposits into `u_cnt.count` / reads `u_cnt.running`, hierarchy
   that the flat routed netlist does not have. Selected tests (`testbench.testcase`): the other 9 of 10.
2. **Partial annotation.** `environment.sdf.partial: true`: 323 `TIMINGCHECK` entries are dropped (Icarus does
   not implement them, so setup/hold run against the cell library's placeholder checks, not the SDF's
   limits) and 164 zero-delay `INTERCONNECT` entries are removed. SPEF net coverage is 1254 of 1255
   design nets (`annotation_complete: false` in the P&R report).
3. **One corner.** The SDF is the `tt_025C_1v80` post-route session and was annotated at `typ`; no min/max
   or other-corner SDF was run, so this says nothing about the corner box. It does not replace the
   multi-corner STA of item 5.
4. **Oscillator timing.** The conversion bench drives ideal clocks at nominal surface periods down to
   1.560 ns for `osc_hd` (641 MHz). At the default gate, 72,116 input rising edges produced one
   observed rise on the selected counter clock (`osc_sel_clk`). The completion toggle (`tog_o`) and
   `done` both recorded zero rising edges through the final STATUS poll.
   The independent setup slack at this corner is −1.227 ns (`sta/readout.osc-corner.sta.report.json`).
5. **Run artifacts.** The report's `environment` block records the SHA-256 digests of
   `.fv-sdf/test_icarus.log`, `.fv-sdf/build_icarus.log` and `.fv-sdf/results_icarus.xml`.
   The run generates the two logs locally. The committed XML carries the per-test results.
   From the repo root, verify its digest against the report with
   `jq -r '.environment.results_xml | (.sha256 | sub("^sha256:"; "")) + "  " + .path' verification/readout/functional-verification-sdf.report.json | sha256sum -c -`.
