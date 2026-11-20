# Work Plan

Prioritized roadmap from current GitHub label state, maintained by the Guide role.

<!-- guide:plan-body:start -->
_Generated: 2026-11-20T06:53:00Z (snapshot; compare against live labels)_
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

_None._

## Very Important

`loom:very-important` (one counts per workspace); every stage takes these first.

- **#26**: T1 item 4 (LVS clean): klt lvs for the oscillator bank (vs schematics) and the readout (vs gate-level netlist) *(held)*

## Important

`loom:important`; taken before unlabelled work.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md)
- **#31**: T1 item 6 (Monte Carlo): klt yield evidence for the matching-dependent rows 2-4, and a not-applicable statement for the digital partition
- **#32**: T1 item 7 (post-layout verification): klt pex re-run of the oscillator benches and SDF-annotated readout re-run *(held)*
- **#33**: T1 item 11 (power delivery): klt erc supply specs for both partitions plus readout PDN and power_connectivity evidence *(held)*
- **#117**: osc_subth: 14 series-header nets (vh1..vh14) are split in the extraction, ring stage PFET sources float *(held)*

## Ready

Human-approved issues ready for implementation (`loom:issue`).

_None._

## In Progress

Issues currently being built (`loom:building`).

_None._

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

_None._

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

_None._

## Proposed

Issues carrying `loom:curated`.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*
- **#26**: T1 item 4 (LVS clean): klt lvs for the oscillator bank (vs schematics) and the readout (vs gate-level netlist) *(curated)* *(held)*
- **#117**: osc_subth: 14 series-header nets (vh1..vh14) are split in the extraction, ring stage PFET sources float *(curated)* *(held)*
- **#190**: klt signoff gate: item 9 pins sim/ source modules, but has no CLAUDE.md warning and no regen script (the item-10 guardrails from #172 have no item-9 sibling) *(curated)* *(held)*

## Proposed (Architect / Hermit)

- **#146**: Remove .github/workflows/drift.yml: its only step already runs in tests.yml (npm test) *(hermit)* *(held)*
- **#165**: Remove the superseded osc-probe STA pair: a second, assumed-period slack table for a question readout.osc-corner.sta.report.json now answers with measured periods *(hermit)* *(held)*

## Epics

_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 0 |
| Very important | 1 |
| Important | 5 |
| Ready (`loom:issue`) | 0 |
| In Progress (`loom:building`) | 0 |
| PRs awaiting review | 0 |
| Approved PRs awaiting merge | 0 |
| Curated | 4 |
| Architect / Hermit proposals | 2 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
