# Work Plan

Prioritized roadmap from current GitHub label state, maintained by the Guide role.

<!-- guide:plan-body:start -->
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

- **#18**: feat(rtl): add saturating gated readout counter and register file with cocotb tests

## Very Important

`loom:very-important` (one counts per workspace); every stage takes these first.

_None._

## Important

`loom:important`; taken before unlabelled work.

- **#16**: Readout RTL: 24-bit saturating gated counter and register file, with cocotb tests in verification/readout/
- **#22**: T1 item 1 (design sources): synthesized readout netlist plus item-1 attestation covering both partitions

## Ready

Human-approved issues ready for implementation (`loom:issue`).

_None._

## In Progress

Issues currently being built (`loom:building`).

- **#16**: Readout RTL: 24-bit saturating gated counter and register file, with cocotb tests in verification/readout/
- **#31**: T1 item 6 (Monte Carlo): klt yield evidence for the matching-dependent rows 2-4, and a not-applicable statement for the digital partition

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

_None._

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

- **#18**: feat(rtl): add saturating gated readout counter and register file with cocotb tests

## Proposed

Issues carrying `loom:curated`.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*
- **#16**: Readout RTL: 24-bit saturating gated counter and register file, with cocotb tests in verification/readout/ *(curated)*
- **#27**: T1 item 9 (testbenches shipped): testbench inventories and klt signoff --attest 9 for both partitions *(curated)*
- **#31**: T1 item 6 (Monte Carlo): klt yield evidence for the matching-dependent rows 2-4, and a not-applicable statement for the digital partition *(curated)*
- **#44**: Follow-on from PR #43: subthreshold Q2 bench follow-ups (cold-cell re-run, pfet S(T) reference, leakage floor) *(curated)*

## Proposed (Architect / Hermit)


_None._

## Epics


_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 1 |
| Very important | 0 |
| Important | 2 |
| Ready (`loom:issue`) | 0 |
| In Progress (`loom:building`) | 2 |
| PRs awaiting review | 0 |
| Approved PRs awaiting merge | 1 |
| Curated | 5 |
| Architect / Hermit proposals | 0 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
