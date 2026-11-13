# Block manifest and tier-verdict record

The machine-readable statement of this block's gap to the klayout-tools T1
checklist: the `klt signoff` input and its committed output.

## Files

- **`sky130-process-monitor.json`** — the block manifest. `kind` is
  `mixed-signal`; `partition_boundary` states the intended analog/digital
  split as the top-level README describes it today (the grader reports it and
  does not grade it; refine it once the spec issue #2 ratifies). `evidence`
  cites T1 item 10 (repo hygiene): `evidence/item10.json`, the
  `klt signoff --attest 10` envelope over `attest/item10.json`, pinned by that
  inventory's `content_hash`; and T1 item 2 analog (layout): `evidence/item2.json`,
  an artifact-anchored generic envelope over `layout/osc_bank.gds`, pinned by the
  stream's `content_hash` under `2.analog` (written by `layout/gen/attest_item2.py`;
  `klt signoff --attest` has no item-2 verb). No other design artifact is cited yet.
  The bare key `"10"` covers both the analog and digital partitions.
- **`design-evidence-tiers.md`** — the checklist the grader parses. Vendored
  **byte-identical** from
  [`2AMLogic/klayout-tools@31a3e3c`](https://github.com/2AMLogic/klayout-tools/blob/31a3e3c41c08bbd58719e0b99a3b6d19beb9be63/docs/design-evidence-tiers.md)
  `docs/design-evidence-tiers.md` (the commit the sibling `sky130-opamp` vendors). Upstream is MIT-licensed; this
  repo's `LICENSE` does not relicense the vendored copy. When upstream moves,
  re-vendor and regenerate the record in the same PR.
- **`sky130-process-monitor.signoff.json`** — the **verdict of record**,
  graded with `klayout-tools==0.9.1`. Today 13 of the 22 T1 rows read `met`
  (items 1, 2, 3, 9 and 10 on both partitions, plus 4.digital, 5.digital and 7.digital); 6.digital
  reads `not_applicable`; 5.analog, 6.analog and 7.analog read `unmet` / `check_failed` (their
  cited envelopes grade, and fail their targets); and 4.analog, 8 and 11 on both partitions read
  `unmet` / `no_evidence`. The T2-T4 tier rows read `unmet` / `tier_not_supported` (the grader does
  not grade those tiers). Never hand-edit it.

## Regenerate

```console
uvx --from "klayout-tools==0.9.1" klt signoff \
    --manifest manifests/sky130-process-monitor.json \
    --tiers-doc manifests/design-evidence-tiers.md \
    --format json > manifests/sky130-process-monitor.signoff.json
```

Exit `3` (some item `unmet`) and `0` (all met) are both valid runs. Any change
that affects the verdict — new evidence, a manifest edit, a vendored-doc bump,
a version-pin bump — regenerates and commits the record in the same PR.

## Item 10 attestation

`attest/item10.json` lists the hygiene files (README, LICENSE, spec, CI
workflow) and one check: that the committed record above still reproduces.
Regenerate the envelope with `klt signoff --attest 10 --inventory
attest/item10.json -o evidence/item10.json` (needs `klt` on `PATH`), and do so
whenever an inventoried file changes. The check is circular by construction
(the record cites the envelope that vouches for the record); bootstrap or
repair it by regenerating the envelope, then the record, then confirming both
`--check` commands report `match`.

## CI

`.github/workflows/signoff.yml` re-runs this on every push and PR with the
same pinned version and byte-compares against the committed record.
It also runs `klt signoff --attest 10 --check evidence/item10.json`.

## Item 1 attestations

`attest/item1_digital.json` (readout RTL, synthesis request, `synth/readout/readout.gl.v`, freshness via
`klt synthesize --check`) and `attest/item1_analog.json` (the five `design/osc_bank/osc_*.sch` and their
`klt netlist --check` netlists) produce `evidence/item1_{digital,analog}.json` with
`klt signoff --attest 1 --inventory <inv> -o <envelope>`, run with `PDK=sky130A` and `PDK_ROOT` set to the pinned
PDK and `klayout-tools==0.9.1` on `PATH`. The manifest cites them as `1.digital` / `1.analog` (hash = the
envelope's `provenance.input.content_hash`). Their freshness commands are `local_only` (need the PDK, xschem,
Yosys), so CI re-checks the input hashes and carries the committed outcome; regenerate the signoff record after
any change.

## Item 2 attestations

- `2.analog`: `evidence/item2.json`, over `layout/osc_bank.gds` (see above).
- `2.digital`: `evidence/item2_digital.json`, `klt signoff --attest 2 --input layout/readout/out/readout.gds
  --inventory attest/item2_digital.json -o evidence/item2_digital.json`. The inventory's one declared check,
  `klt place-and-route layout/readout/request.json --check layout/readout/report.json`, is `local_only`
  (needs OpenROAD and the pinned PDK); CI re-hashes the routed GDS and carries the committed outcome. The
  manifest pins the GDS's hash; re-running P&R without re-attesting turns the row stale.

## Item 3 (DRC)

- `3.analog`: `drc/osc_bank.report.json`; `3.digital`: `drc/readout.report.json` (hash = the report's `provenance.input.content_hash`,
  i.e. the GDS). Re-run `klt drc` (commands in `drc/README.md`) after any GDS change, then re-attest item 2 and regenerate the signoff record.
  The coverage disclosure and the native-deck disagreement on the analog stream are in `drc/README.md`.

## Item 9 (testbenches shipped)

Two inventories, one per partition (item 9 is graded per partition):

- `attest/item9_analog.json` -> `evidence/item9_analog.json`, cited as `9.analog`. It pins every
  committed analog SPICE deck **and** every committed `klt sim` request that drives one (91 files).
- `attest/item9_digital.json` -> `evidence/item9_digital.json`, cited as `9.digital`. It pins the
  readout cocotb bench and its two `klt functional-verification` requests.

Regenerate either with `klt signoff --attest 9 --inventory attest/item9_<p>.json -o
evidence/item9_<p>.json`, then regenerate the signoff record. The manifest pins each envelope by
its `provenance.input.content_hash` (the inventory's own sha256), so an inventory edit without a
re-attest turns the row stale.

**Run the producer from a different environment than the benches.** `klt signoff --attest` strips
its own venv's `bin` from every declared command's `PATH` (so a bare `python3` resolves to the
repo's interpreter). If `klt` and the pinned `cocotb`/`ngspice` share one venv, the cold starts
lose that venv. Install the toolchain pins in a worktree venv, put its `bin` on `PATH`, and invoke
the producer through a throwaway environment:

```console
python3 -m venv .venv && .venv/bin/pip install cocotb==2.1.0 klayout-tools==0.9.1
PATH="$PWD/.venv/bin:$PATH" uvx --from "klayout-tools==0.9.1" klt signoff --attest 9 \
    --inventory attest/item9_analog.json -o evidence/item9_analog.json
```

### What the cold starts do and do not cover (disclosure)

`klt signoff --attest 9` only records that each declared cold start exited `0`; it cannot check that
the command reproduces the measurement it is attached to (the tier doc says so for items 1, 2, 9 and
10 — "Citing them honestly is the claimant's responsibility"). Stated plainly, then:

| Bench family | Declared cold start | Does it reproduce the claimed numbers? |
|---|---|---|
| `sim/smoke/`, `sim/osc_bank/` | `run.sh --no-record [osc]` — the real single-corner `ngspice -b` | **Yes**, in full: these benches are single-unit and local by design. `--no-record` exists so repeating the cold start does not grow the append-only `measurements/*.jsonl`. |
| `sim/sensitivity/`, `sim/power/`, `sim/pex/`, `sim/subthreshold/` | `klt sim <request> --dry-run` | **No.** The dry run validates the committed request and deck against the pinned PDK — deck staging, model resolution, corner / Monte-Carlo expansion and seeds — without simulating. Those grids ran on the batch fleet over hours; re-running them is not an attestation-time operation. Each bench's README gives the full fleet invocation (`klt sim --batch-set …`, `klt pex … --submit-only` / `--attach`), and the committed `records/` carry the results. |
| `sim/pex/probe/osc_subth_vbp_probe.cir` | none (pinned by hash only) | **No.** One `ngspice -b`, but minutes on the extracted `osc_subth` netlist; it is a vh-split diagnosis probe (#117), not a spec-row measurement. |
| `verification/readout/` | `make -C verification/readout` | **Yes** for the pre-layout run cited as `5.digital`: check-env, Verilator lint `-Wall`, then the full cocotb suite on Icarus (9/9). |
| `verification/readout/request-sdf.json` | none (pinned by hash only) | **No.** The SDF-annotated re-run cited as `7.digital` names host-absolute PDK timing-model and SDF paths (`verification/README.md`); a third party adjusts them for their own install. |

Rows the spec names that no committed bench covers, so no inventory lists one: **counter power**
(spec §7's "one oscillator running plus counter" — the counter has no SPICE-level netlist, stated
with every verdict in `sim/power/analyze_power.py`) and **spec §8 area**, whose testbench is the
layout/P&R report, not a bench (`layout/README.md`). `verification/smoke/` is excluded on purpose:
it exercises the placeholder `rtl/smoke/smoke.v` and backs no claimed measurement.

### CI

`.github/workflows/signoff.yml` runs `klt signoff --attest 9 --check evidence/item9_<p>.json` for
both partitions. Every declared cold start is `local_only` (they need the pinned PDK, ngspice,
Icarus, Verilator and cocotb, which the runner lacks), so `--check` re-hashes the inventoried files
and carries the committed outcome of the commands, exactly as it does for items 1 and 2.

## Item 5 (digital)

`5.digital` cites two envelopes (list form): `sta/readout.sta.report.json` (`klt sta`, three liberty corners,
reference clock only) and `verification/readout/functional-verification.report.json` (`klt
functional-verification`, 9/9). Read `sta/README.md` for what the `constrained` verdict does not cover
(oscillator-clocked counter untimed; 125 C / 1.62 V / 1.98 V not in the liberty set). Regenerate both with
`uvx --from "klayout-tools==0.9.1" [--with cocotb==2.1.0] klt ...`, then the record.
