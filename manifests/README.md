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
  graded with `klayout-tools==0.9.1`. Today 2.analog, 10.analog and 10.digital read
  `met` and T1 5.analog reads `unmet` / `check_failed` (the cited `model-run` envelope grades, and fails its targets), and the other 18 T1 rows read `unmet` / `no_evidence`; the T2-T4 tier rows read `unmet` / `tier_not_supported` (the grader does not grade those tiers). Never hand-edit it.

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
