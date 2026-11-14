# sim

Analog flow (ngspice on the sky130 models). Everything here is toolchain
bring-up: nothing is a design result.

## Pins

- `pdk.json` — sky130A open_pdks revision, model library / cell SPICE / Liberty paths inside the PDK. The PDK
  root defaults to `~/.volare/sky130A`; override with `PDK_ROOT_SKY130A`.
- `toolchain.json` — ngspice (a `>=` floor), Icarus, Yosys, Verilator, cocotb (exact) versions, and the xschem package version
  (checked via `dpkg-query` only; raw `xschem` is never run, use `klt netlist`).
- `check_env.sh` — exits non-zero on any mismatch, version below the ngspice floor, or missing path; it prints the measured ngspice version. The analog smoke (`sim/smoke/run.sh`) and the readout flow (`verification/readout/Makefile`) call it first.

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

    sim/smoke/run.sh --no-record    # same run, appends nothing (repeatable cold start)

Runs one `ngspice -b` (single corner, local) on `sim/smoke/inv_smoke.spice`: `sky130_fd_sc_hd__inv_1`,
`tt`, 1.8 V, 27 °C, 10 fF load. It appends one line to `measurements/inv_smoke_records.jsonl`
(append-only; each record is labelled SIMULATED and names the corner, testbench, open_pdks revision,
model file and ngspice version). It proves the models and cell views load; it makes no design claim.

## Negative controls

    sim/negative_controls.sh

Wrong model path, edited PDK pin, edited tool pin and absent PDK must each fail **with the expected diagnostic**
(the script greps for it), after a baseline `check_env.sh` pass, so a broken environment is not read as a control
passing. Exit 0 means all did; exit 2 means the environment itself is broken. A failed run appends no record.

That pass rule is not this script's alone: `expect_fail` and the baseline live in
`sim/neg_control_common.sh`, which every negative-control script here sources (`sim/osc_bank/` and
`sim/subthreshold/` too), so there is one rule rather than one per directory.

## Oscillator bank

    sim/osc_bank/run.sh [osc_name ...]      # default: all five
    sim/osc_bank/run.sh --no-record [osc_name ...]   # same runs, appends nothing
    sim/osc_bank/negative_controls.sh

One `ngspice -b` per oscillator (`bench_<osc>.spice`, netlists from `design/osc_bank/`), `tt` / 1.8 V / 27 °C,
single-unit and local by design. After skipping the start-up edges each bench measures `f_osc_hz` and the mean
supply current `i_avg_ua` over a whole number of cycles. If **every** ring oscillates, one record per oscillator is
appended to `measurements/osc_bank_records.jsonl` (append-only, labelled SIMULATED, with corner, testbench, netlist,
open_pdks, model file and ngspice version); if any ring does not, `run.sh` exits non-zero, names it, and appends
nothing. `--no-record` runs the benches and prints the same results without appending — it is the repeatable
cold-start invocation that `attest/item9_analog.json` declares, so re-attesting does not grow the record. The PDK/ngspice pins are read via `check_env.sh`, not repeated. The PVT surfaces and Monte Carlo are #8
and go through `klt sim`. `osc_subth`'s `i_avg_ua` includes ~1 µA of bias divider (see `design/osc_bank/README.md`).
The controls check that a tied-off enable fails and appends nothing, and that a drifted schematic is reported by
`klt netlist --check`.

## Cold-start invocations (T1 item 9)

`attest/item9_analog.json` is the committed inventory of every analog testbench deck, every `klt
sim` request that drives one, the `solve/` post-processing bench, and the three `sensitivity/`
Python modules that bench imports at run time, with the cold start declared per bench; `klt
signoff --attest 9` runs them and writes `evidence/item9_analog.json`, cited by the
manifest as `9.analog`. What each cold start does — and which ones do **not** re-simulate — is
tabulated in `manifests/README.md` § "Item 9 (testbenches shipped)", together with the committed
files the inventory deliberately leaves out. In short:

| Bench | Cold start | Re-simulates? |
|---|---|---|
| `smoke/`, `osc_bank/` | `run.sh --no-record [osc]` | yes, the real single-corner `ngspice -b` |
| `sensitivity/`, `power/`, `pex/`, `subthreshold/` | `klt sim <request> --dry-run` | no — validates the committed request and deck against the pinned PDK (staging, models, corner/MC expansion). The full fleet run is the `klt sim --batch-set` / `klt pex --submit-only` command in each section above |
| `solve/mc/requests/` (18), `solve/mc/requests-sized/` (140) | `klt sim <request> --dry-run` | no — same as the row above. 20 of the 140 sized requests (the `tt`/1.62 V/−40 °C chunks) are committed and drift-checked but were **never run**; the rest have reports under `solve/mc/reports*/`. See `solve/mc/RECORD-2026-11-06-item6*.md` |
| `sensitivity/analyze.py`, `gen_requests.py`, `test_analyze.py` | `python3 -I sensitivity/test_analyze.py` (the two modules are pinned by hash) | no simulation — `analyze.py` builds the frequency and MC tables `solve.py` grades and is imported by it at run time (`gen_requests.py` likewise by `gen_binding_mc.py`), so `analyze.py extract` / `extract-mc` is the first step of the `5.analog` / `6.analog` reproduce chain. The suite runs for real (10 tests) and covers `analyze.py`; `gen_requests.py` has no suite |
| `solve/` drivers (`solve.py`, `gen_binding_mc.py`, `yield_samples.py`, `make_envelope.py`) and their two unittest suites | `python3 -I solve/test_solve.py`, `python3 -I solve/test_gen_binding_mc.py` | no simulation at all — this is the post-processing path behind `5.analog` and `6.analog`. Both suites run for real (8 and 6 tests: synthetic negative controls, and the request-drift check against the committed `requests-sized/` bytes). Regrading the recorded rows is the explicit `solve.py grade` / `yield_samples.py build` command in each `RECORD-*.md`, which the attestation does not run |

From a clean checkout, the precondition is `sim/check_env.sh` (the inventory's top-level cold start):
it fails unless the PDK revision and every tool pin match. cocotb is not provisioned on workers, so
make a worktree venv first — see § Environment, and `manifests/README.md` for why the `klt` that
produces the envelope must not share that venv.

## Rows 1-4 grading and power (issue #29)

    python3 -I sim/solve/solve.py grade freq_table.json mc_table.json --json out.json
    python3 -I sim/solve/test_solve.py                         # synthetic negative controls
    python3 -I sim/power/gen_requests.py                       # power testbenches + klt sim requests
    python3 -I sim/power/analyze_power.py extract|grade ...
    python3 -I sim/power/test_analyze_power.py                 # active-cell gradability is the #8 rule

`sim/solve/` post-processes #8's surfaces (no re-simulation); records in `sim/solve/records/`. `sim/power/` holds
the active/idle supply-current benches (oscillator bank only; counter power is NOT covered); records in
`sim/power/records/`. Power coverage: idle 45/45, active 219/225 cells (`records/2026-11-05-power-complete.md`; the earlier `-partial` record is kept). Which active cells are gradable is the #8 rule, read from `sim/sensitivity/analyze.py` (9 rising crossings: `SKIP_EDGES` dropped, then `MIN_CYCLES + 1`) and never restated locally — `records/2026-11-14-grader-threshold-correction.md` records the off-by-one that held until 2026-11-14 and why no recorded verdict moves. Every row is recorded failing. `sim/solve/make_envelope.py` builds `evidence/item5_analog.json`, the `model-run` citation for `5.analog` (`klt signoff` grades it `check_failed`, not `no_evidence`).
