# Work Plan

Prioritized roadmap from current GitHub label state, maintained by the Guide role.

<!-- guide:plan-body:start -->
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

_None._

## Very Important

`loom:very-important` (one counts per workspace); every stage takes these first.

_None._

## Important

`loom:important`; taken before unlabelled work.

_None._

## Ready

Human-approved issues ready for implementation (`loom:issue`).

_None._

## In Progress

Issues currently being built (`loom:building`).

- **#25**: T1 item 3 (DRC clean): klt drc reports for the oscillator bank and readout layouts with coverage disclosed
- **#30**: T1 item 5 (corner verification, digital): multi-corner klt sta plus klt functional-verification for the readout

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

- **#87**: feat(drc): commit klt drc reports and fix analog generator DRC violations

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

_None._

## Proposed

Issues carrying `loom:curated`.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*
- **#25**: T1 item 3 (DRC clean): klt drc reports for the oscillator bank and readout layouts with coverage disclosed *(curated)*
- **#26**: T1 item 4 (LVS clean): klt lvs for the oscillator bank (vs schematics) and the readout (vs gate-level netlist) *(curated)*
- **#27**: T1 item 9 (testbenches shipped): testbench inventories and klt signoff --attest 9 for both partitions *(curated)*
- **#30**: T1 item 5 (corner verification, digital): multi-corner klt sta plus klt functional-verification for the readout *(curated)*
- **#44**: Follow-on from PR #43: subthreshold Q2 bench follow-ups (cold-cell re-run, pfet S(T) reference, leakage floor) *(curated)*

## Proposed (Architect / Hermit)


- **#71**: Stop committing 139 unrun, regenerable sized-MC request files (sim/solve/mc/requests-sized) *(hermit)*

## Epics

_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 0 |
| Very important | 0 |
| Important | 0 |
| Ready (`loom:issue`) | 0 |
| In Progress (`loom:building`) | 2 |
| PRs awaiting review | 1 |
| Approved PRs awaiting merge | 0 |
| Curated | 6 |
| Architect / Hermit proposals | 1 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
