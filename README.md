# sky130-process-monitor

An on-die process / voltage / temperature (PVT) monitor on
[SkyWater sky130](https://github.com/google/skywater-pdk), the 130 nm open
PDK — a bank of ring oscillators plus a subthreshold-biased sensing path,
read out by a digital counter — designed by AI agents driving
[klayout-tools](https://github.com/2AMLogic/klayout-tools), xschem + ngspice
on the analog side and cocotb + Icarus, Yosys and OpenROAD on the digital
side.

**Status: specification ratified; design, verification and layout under way.**
The repo holds oscillator and sensing-path schematics, readout RTL, layout,
ngspice and cocotb testbenches, and recorded results. Every recorded result is
*simulated*, labelled with its corner and testbench — nothing here is measured,
and nothing will be until silicon exists. T1 evidence sign-off is in progress
and not every T1 row is met; the per-row verdict of record is
[`manifests/sky130-process-monitor.signoff.json`](manifests/sky130-process-monitor.signoff.json),
re-checkable with the commands under [Reproduce](#reproduce).

**Built agent-native.** Every specification, decision record, testbench, and
line of documentation here is produced by AI agents working from a ratified
spec and an append-only evidence trail — not human-authored work that agents
merely assisted with. Verification is the product: every claim traces to a
recorded result under PVT corners. Where the agents hit friction with the
open-source tooling — most often
[klayout-tools](https://github.com/2AMLogic/klayout-tools) — that friction is
filed as a public issue against the tool itself, so the fix benefits everyone
using sky130, not just this repo.

## Why this block, on this PDK

A process monitor answers a question every other block on a die eventually
asks: *which corner did this die land in, and what are its supply and
temperature right now?* Ring oscillators whose frequency is dominated by
different device types (NMOS-limited, PMOS-limited, wire-limited, and a
leakage-starved subthreshold oscillator) each respond differently to
process, voltage and temperature; reading several of them against a
reference clock and solving for P, V and T is the classic approach.

To our knowledge, no open-source process-monitor block on an open PDK is
available with a committed, reproducible evidence chain from schematic to
layout. That gap is the reason to open this repo.

It is also a useful canary because it is **small but mixed-signal at the
seam**: the oscillators are drawn from standard cells and custom cells, the
counter and readout are synthesized, and the result is only meaningful if
the simulated frequency-versus-PVT surfaces are trustworthy — which puts the
open sky130 models, especially in subthreshold, directly under test.

## Scope

- **In scope**: the oscillator bank (standard-cell and custom-cell
  variants), the enable/select logic, a counter-based frequency readout
  against an external reference clock, and a documented calibration and
  solve procedure that turns counts into P, V and T estimates.
- **Not in scope**: an on-die reference clock, a full temperature sensor of
  the PTAT/bandgap kind, or an ADC. The readout assumes a reference clock is
  supplied from outside the block.
- **A different block from `sky130-temp-por`.** That sibling's temperature
  sensor is a PTAT/CTAT analog sensor paired with a POR. This repo's
  temperature estimate comes from oscillator frequencies. The two are not
  duplicates; the spec says so by name.

## Target specification (ratified by [decision 0001](spec/decisions/0001-ratify-target-spec.md), issue #2)

All rows are *targets*, not results: every figure is an unverified target
until the simulations named in [`spec/target-spec.md`](spec/target-spec.md)
have been run. That file is the source of truth; this table mirrors it.

| Parameter | Fallback | Target | Stretch |
|---|---|---|---|
| Oscillator bank | 3 oscillators (NMOS, PMOS, plain `hd` chain) | 5 oscillators (NMOS, PMOS, wire, subthreshold, plain `hd` chain) | add a second-library chain |
| Process discrimination | separate the slow and fast global corners | identify each of the five global corners (tt/ff/ss/sf/fs) at known V and T | estimate NMOS and PMOS skew as continuous values |
| Supply estimate (1.8 V core, 1.62–1.98 V) | ±50 mV | ±20 mV | ±10 mV |
| Temperature estimate (−40…125 °C, one-point calibration) | ±10 °C | ±5 °C | ±2 °C |
| Readout (reference clock is an input) | 24-bit counter, ref ±1000 ppm | 24-bit counter, 10 MHz ref ±100 ppm | — |
| Conversion time | < 10 ms | < 1 ms | < 100 µs |
| Active power | < 500 µW | < 100 µW | < 20 µW |
| Idle power | < 10 µW | < 1 µW | < 100 nW |
| Area | ≤ 0.05 mm² | ≤ 0.02 mm² | ≤ 0.01 mm² |
| Signoff | DRC + LVS clean | DRC + LVS clean, post-layout re-verified | — |

Maturity ladder: spec ratified → oscillator cells simulated across PVT →
readout RTL verified → calibration and solve procedure validated on
simulated data → layout DRC/LVS-clean → post-layout re-verification →
shuttle seat → measured silicon.

**Current position: through "readout RTL verified"; the solve-procedure rung is
attempted and failing.** Progress up the ladder is not strictly sequential, and
a rung is not cleared by the existence of files, so each rung carries its own
verdict — every one of them *simulated*:

- *spec ratified* — cleared ([decision 0001](spec/decisions/0001-ratify-target-spec.md)).
- *oscillator cells simulated across PVT* — cleared with a recorded gap: the
  5-oscillator × 45-cell grid ran on the batch fleet, and **7 of its 225 cells
  show no or too-short oscillation** (`sim/sensitivity/`).
- *readout RTL verified* — cleared: 9 of 9 cocotb tests pass on `rtl/readout/`,
  and 8 of those 9 also pass re-run against the routed netlist with
  back-annotated SDF, under the limits `verification/README.md` discloses.
- *calibration and solve procedure validated on simulated data* — **attempted
  and failing.** Spec rows 1, 3 and 4 and the row-2 five-corner target all grade
  FAIL; only the row-2 slow/fast *fallback* passes
  ([`sim/solve/records/2026-11-05-rows1-4.md`](sim/solve/records/2026-11-05-rows1-4.md)).
- *layout DRC/LVS-clean* — **partial.** Both streams are DRC-clean under the
  curated `sky130` deck, but the PDK-native deck reports 562 violations on the
  analog stream ([`drc/README.md`](drc/README.md)), and LVS closes on the
  digital partition only — `4.analog` stays unmet because `osc_wire` and
  `osc_subth` match reduced references, not the item-1 netlists
  ([`lvs/README.md`](lvs/README.md)).
- *post-layout re-verification* — **digital cleared, analog attempted and
  unmet.** The SDF re-run above covers the digital partition. On the analog
  partition parasitic extraction and a 45-cell `klt pex` re-run exist for all
  five oscillators, and `klt signoff` still grades `7.analog` `unmet`
  ([`sim/pex/README.md`](sim/pex/README.md)): the four oscillators that
  produced a delta come out slower once extracted (per-oscillator median
  −14 % to −24 % on the edge-count proxy `klt pex` reports), the extracted
  `osc_subth` does not oscillate in either of the two re-runs those counts
  come from — 0 or 1 crossings in all 45 of 45 extracted cells on the
  `dev661` run and all 35 of 35 on the `gds109` run, none reaching the
  ≥ 9 rising edges row 1 needs. The earlier 2026-11-11 run is excluded: its
  14 LVT PFETs extracted as plain `pfet_01v8`, which `klt pex` flags as a
  `model_mismatch` and `sim/pex/README.md` records as not a valid comparison,
  so its three large extracted counts are not read as deltas. A local
  single-corner probe on the `gds109` extraction (tt / 1.80 V / 27 C) traced
  the non-start to 14 split `vh` nets and left layout-defect versus
  extraction-defect open; a separate structural diagnosis attributes the split
  to the extractor (2AMLogic/klayout-tools#5311). And spec rows 2–4 have not
  been re-graded on extracted values. The
  oscillator frequencies above are schematic-level and do not carry to the
  layout unchanged.
- *shuttle seat*, *measured silicon* — not reached. Nothing here is measured.

## Reproduce

Nothing here is measured, and nothing will be until silicon exists — but
simulated results *are* recorded, and they are reproducible.
`measurements/*.jsonl` holds 127 records, every one labelled `SIMULATED` with
its corner and testbench, and the batch-fleet reports behind the PVT surfaces
are committed under `sim/sensitivity/records/reports/` and `sim/solve/mc/`.
Each result class below names the cheapest command that reproduces its
committed record from a clean checkout. The standing rule for this table is
unchanged: a result class gets its command here in the same change that records
it, and the command is run — with its exit status and environment stated in
that change — before it is written down.

Recorded verdicts reproduce **as recorded, failures included**: the solve
procedure grades spec rows 1, 3 and 4 and the row-2 five-corner target FAIL,
and 7 of the 225 oscillator grid cells do not oscillate. Nothing in this
section quotes an estimate accuracy, because none has been established.

| Result class | Reproduce |
|---|---|
| Oscillator frequency-versus-PVT surfaces (`sim/sensitivity/`) | **command 1** — rebuilds the 225-cell frequency table from the committed grid reports. The PVT surface lives in `sim/sensitivity/`, *not* `sim/osc_bank/` |
| Single-corner oscillator bench (`sim/osc_bank/`) | **command 2** — re-simulates all five oscillators locally, at tt / 1.8 V / 27 °C only. Not a PVT surface, and its records say so |
| Sensitivity matrix and conditioning (`sim/sensitivity/`) | **command 3** — matrix, SVD, κ, rank and discrimination margin per (V,T) cell |
| Solve procedure on simulated data (`sim/solve/`) | **command 4** — grades spec rows 1–4; reproduces the recorded FAIL verdicts |
| Readout RTL verification (`verification/readout/`) | **command 5** — Verilator lint plus 9 cocotb tests on Icarus |
| Layout DRC / LVS (`drc/`, `lvs/`) | **command 6** — freshness-checks all eight committed DRC and LVS reports |
| T1 tier verdict of record | **command 7** |
| Post-layout re-verification, analog (`sim/pex/`) | **command 8** — re-grades the committed `klt pex` reports; reproduces the recorded extracted-side row-1 verdict and ratio-space layout shift |

Commands 1, 3, 4 and 8 need only `python3` (the scripts are standard-library
only); 2 needs `ngspice` and the pinned PDK; 5 needs Icarus, Verilator and a
`cocotb` virtualenv; 6 and 7 need `uv`. Tool pins are in
[`sim/toolchain.json`](sim/toolchain.json) and
[`sim/pdk.json`](sim/pdk.json); `sim/check_env.sh` reports what is missing.

**1 — oscillator frequency-versus-PVT surface.** Post-processing of the
committed fleet reports; writes the frequency table the next two commands read:

```console
python3 -I sim/sensitivity/analyze.py extract \
    sim/sensitivity/records/reports/grid_osc_{hd,nmos,pmos,wire,subth}.json.gz \
    -o /tmp/freq.json
```

This does **not** re-simulate the grid. Re-running the ngspice grid itself is a
225-unit batch-fleet submission,
`klt sim --batch-set sim/sensitivity/requests/grid_*.json` (see
[`sim/sensitivity/README.md`](sim/sensitivity/README.md) § Running) — named
here for completeness, not re-run.

**2 — single-corner oscillator bench.** One local `ngspice -b` per oscillator:

```console
sim/osc_bank/run.sh
```

Single corner by design (tt, 1.8 V, 27 °C), so it establishes **no** PVT
behaviour; each record it writes carries the note *"single-corner
start-up-skipped measurement; no PVT claim"*. Note that a successful run
**appends** five records to the tracked, append-only
`measurements/osc_bank_records.jsonl`; discard them (`git checkout --`) unless
you mean to record a new result.

**3 — sensitivity matrix and conditioning.** Needs `/tmp/freq.json` from
command 1:

```console
python3 -I sim/sensitivity/analyze.py extract-mc \
    sim/sensitivity/records/reports/mc_osc_{hd,nmos,pmos,wire,subth}.json.gz \
    -o /tmp/mc.json
python3 -I sim/sensitivity/analyze.py report /tmp/freq.json /tmp/mc.json
```

Reproduces the recorded matrices, singular values, κ and margin, and reports
the 7 missing cells by name. It forms an absolute matrix at 5 of the 9 (V,T)
cells — the four it cannot form are the ones with missing oscillators, never
interpolated. The `mc_osc_*` reports this command reads are mismatch Monte
Carlo at the nominal 1.80 V / 27 °C cell only, and command 4's `solve.py`
applies that pooled nominal σ to every cell. Off-nominal mismatch Monte Carlo
(1.62 V / 125 °C and 1.98 V / −40 °C) is recorded separately, under
`sim/sensitivity/records/reports/mc_offnom_*` and
`sim/sensitivity/records/2026-11-05-mc-offnom-partial.md` /
`2026-11-06-mc-offnominal-*.md`. All five oscillators have it at **both** of
those cells; what is **not** covered, per the latest of those records
([`2026-11-06-mc-offnominal-cold-margin.md`](sim/sensitivity/records/2026-11-06-mc-offnominal-cold-margin.md)
§4), is the other seven (V,T) cells, which have no off-nominal MC at all. Two
caveats carry on what *is* collected: the cold `osc_subth` ss and sf samples
are **truncated** (6 of 10 usable each — the slowest draws are exactly the ones
lost, so both σ are biased low), and `osc_wire` sf at 1.98 V / −40 °C has no
nominal grid cell, so no per-(V,T) margin is formed there.
`osc_subth`'s σ(ln f) is recorded as **unvalidated**; the margin it prints is a
discrimination statistic, not an accuracy.

**4 — solve procedure on simulated data.** Post-processing only — `solve.py`
re-simulates nothing:

```console
python3 -I sim/solve/solve.py grade /tmp/freq.json /tmp/mc.json --json /tmp/rows1-4.json
```

Reproduces [`sim/solve/records/2026-11-05-rows1-4.md`](sim/solve/records/2026-11-05-rows1-4.md):
row 1 FAIL (7 cells missing), row 2 five-corner **target** FAIL at 8 of 9 (V,T)
cells with the slow/fast **fallback** PASS at 9 of 9, row 3 FAIL (worst
p99 |ΔV| = 62 mV), row 4 FAIL (worst p99 |ΔT| = 19.0 °C). The grading
conventions are choices made in the script's docstring, not spec changes, and
the record lists the caveats behind each number. The printed verdicts and every
row 2/3/4 number reproduce on every CPython tried (3.10, 3.11, 3.12, 3.13), but
`/tmp/rows1-4.json` is byte-identical to the committed
[`sim/solve/records/2026-11-05-rows1-4.json`](sim/solve/records/2026-11-05-rows1-4.json)
only on **CPython >= 3.12**, which is this repo's declared floor and what CI
runs — on 3.10/3.11 two of the five `mc_pooled_sigma_lnf` values move by 1 ULP;
the measurement is in the dated interpreter note at the foot of
[`2026-11-05-rows1-4.md`](sim/solve/records/2026-11-05-rows1-4.md).

**5 — readout RTL verification.** `cocotb` is not part of the worker tool spec,
so install it in a worktree-local virtualenv rather than host-wide:

```console
python3 -m venv .venv && .venv/bin/pip install cocotb==2.1.0
PATH="$PWD/.venv/bin:$PATH" make -C verification/readout
```

Runs `check_env.sh`, `verilator --lint-only -Wall`, then the nine cocotb tests
of [`verification/readout/test_readout.py`](verification/readout/test_readout.py)
on Icarus. It does **not** re-run synthesis, place-and-route, or the
SDF-annotated post-layout re-verification; for that, and for the limits
disclosed on it, see [`verification/README.md`](verification/README.md).

**6 — layout DRC / LVS.** Freshness checks: each re-hashes its report's inputs
and reports `match` without re-running the engine.

```console
uvx --from "klayout-tools==0.9.1" klt drc layout/osc_bank.gds --deck sky130 \
    --top osc_bank --pdk sky130A --check drc/osc_bank.report.json
uvx --from "klayout-tools==0.9.1" klt drc layout/readout/out/readout.gds --deck sky130 \
    --top readout --pdk sky130A --check drc/readout.report.json
for c in osc_hd osc_nmos osc_pmos osc_wire osc_subth readout; do
    uvx --from "klayout-tools==0.9.1" klt lvs --check "lvs/$c.report.json"
done
```

Add `--rerun` to re-run the engine instead of re-hashing. A `match` means the
committed report still describes the committed input; it is **not** a clean
verdict. What the verdicts do and do not cover — the curated deck versus the
PDK-native deck's 562 analog violations, and why `4.analog` stays unmet — is in
[`drc/README.md`](drc/README.md) and [`lvs/README.md`](lvs/README.md).

**7 — tier verdict and repo-hygiene attestation** (needs only `uv`; the pin is
the one in [`manifests/README.md`](manifests/README.md)):

```console
uvx --from "klayout-tools==0.9.1" klt signoff \
    --manifest manifests/sky130-process-monitor.json \
    --tiers-doc manifests/design-evidence-tiers.md \
    --check manifests/sky130-process-monitor.signoff.json
uvx --from "klayout-tools==0.9.1" klt signoff --attest 10 \
    --inventory attest/item10.json --check evidence/item10.json
```

The first re-grades the block manifest and reports whether the committed
record still reproduces; the second re-runs the item-10 (repo hygiene)
attestation and diffs it against `evidence/item10.json`. The attestation's
`klt` check calls `klt` from `PATH`, so run the second from an environment
where `klt` 0.9.1 is installed (CI installs it with `pip`). CI runs both on
every push and pull request ([`signoff.yml`](.github/workflows/signoff.yml)).

**8 — post-layout re-verification, analog.** Post-processing of the committed
`klt pex` reports; re-runs no extraction and no simulation:

```console
python3 -I sim/pex/grade_pex.py /tmp/pexgrade.json \
    sim/pex/records/2026-11-10-osc_{hd,nmos,pmos,wire}.pex.report.json
```

Reproduces [`sim/pex/records/2026-11-11-grade-extracted-values.json`](sim/pex/records/2026-11-11-grade-extracted-values.json):
all four oscillators pass the row-1 "oscillates" criterion on the extracted
side, and the row-2 ratio-space coordinate shifts by a median −7.8 %
(`osc_nmos`), −10.9 % (`osc_pmos`) and −1.6 % (`osc_wire`). `osc_subth` is
**not** in this record — its extracted side does not oscillate in the
`dev661` or the `gds109` re-run (see the rung above) — and rows
2–4 are **not** re-graded, because the `klt pex` scalar is a quantised
edge count rather than a frequency. Re-running the extraction and the 45-cell
grid themselves is a batch-fleet submission, named in
[`sim/pex/README.md`](sim/pex/README.md) § "Reproduce one oscillator" — named
there for completeness, not re-run here. The caveats that keep `7.analog`
unmet, including the `osc_wire` extraction not being like-for-like, are in
that file.

## Tool flow

- **Analog / custom cells**: xschem + ngspice, sky130 corner models.
- **Digital readout**: cocotb + Icarus for verification, Yosys for
  synthesis, OpenROAD for place-and-route.
- **Layout, DRC, LVS**: klayout-tools (`klt`).

## Repo layout

```
spec/          ratified spec + decision records
design/        oscillator and sensing-path schematics (xschem)
rtl/           counter, select and readout sources
sim/           testbenches + PVT corner results (ngspice)
verification/  cocotb testbenches for the readout
layout/        GDS + DRC/LVS reports (klayout-tools driven)
measurements/  recorded results (simulated; silicon characterization after tape-out)
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
