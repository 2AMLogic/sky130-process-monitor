# Block manifest and tier-verdict record

The machine-readable statement of this block's gap to the klayout-tools T1
checklist: the `klt signoff` input and its committed output.

## Files

- **`sky130-process-monitor.json`** — the block manifest. `kind` is
  `mixed-signal`; `partition_boundary` states the intended analog/digital
  split as the top-level README describes it today (the grader reports it and
  does not grade it; refine it once the spec issue #2 ratifies). `evidence`
  cites only T1 item 10 (repo hygiene): `evidence/item10.json`, the
  `klt signoff --attest 10` envelope over `attest/item10.json`, pinned by that
  inventory's `content_hash`. No design artifact exists yet, so nothing else
  is cited. The bare key `"10"` covers both the analog and digital partitions.
- **`design-evidence-tiers.md`** — the checklist the grader parses. Vendored
  **byte-identical** from
  [`2AMLogic/klayout-tools@31a3e3c`](https://github.com/2AMLogic/klayout-tools/blob/31a3e3c41c08bbd58719e0b99a3b6d19beb9be63/docs/design-evidence-tiers.md)
  `docs/design-evidence-tiers.md` (the commit the sibling `sky130-opamp` vendors). Upstream is MIT-licensed; this
  repo's `LICENSE` does not relicense the vendored copy. When upstream moves,
  re-vendor and regenerate the record in the same PR.
- **`sky130-process-monitor.signoff.json`** — the **verdict of record**,
  graded with `klayout-tools==0.8.0`. Today 10.analog and 10.digital read
  `met` and the other 20 T1 rows read `unmet` / `no_evidence`; the T2-T4 tier rows read `unmet` / `tier_not_supported` (the grader does not grade those tiers). Never hand-edit it.

## Regenerate

```console
uvx --from "klayout-tools==0.8.0" klt signoff \
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
