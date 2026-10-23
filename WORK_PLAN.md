# Work Plan

Prioritized roadmap from current GitHub label state, maintained by the Guide role.

<!-- guide:plan-body:start -->
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

- **#18**: feat(rtl): add saturating gated readout counter and register file with cocotb tests

## Very Important

`loom:very-important` (one counts per workspace); every stage takes these first.

- **#8**: Sensitivity matrix and conditioning across the PVT corner box (spec Q1)

## Important

`loom:important`; taken before unlabelled work.

- **#10**: Subthreshold oscillator: model-limited vs design-limited across temperature (spec Q2)

## Ready

Human-approved issues ready for implementation (`loom:issue`).

_None._

## In Progress

Issues currently being built (`loom:building`).

- **#3**: Bring up both flows: pinned sky130 + ngspice smoke and a digital cocotb/Yosys skeleton (T1 item 9 groundwork)
- **#16**: Readout RTL: 24-bit saturating gated counter and register file, with cocotb tests in verification/readout/

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

- **#6**: feat: add pinned analog and digital toolchain smoke flows

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

- **#18**: feat(rtl): add saturating gated readout counter and register file with cocotb tests

## Proposed

Issues carrying `loom:curated`.

- **#3**: Bring up both flows: pinned sky130 + ngspice smoke and a digital cocotb/Yosys skeleton (T1 item 9 groundwork) *(curated)*
- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*
- **#16**: Readout RTL: 24-bit saturating gated counter and register file, with cocotb tests in verification/readout/ *(curated)*

## Proposed (Architect / Hermit)


_None._

## Epics


_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 1 |
| Very important | 1 |
| Important | 1 |
| Ready (`loom:issue`) | 0 |
| In Progress (`loom:building`) | 2 |
| PRs awaiting review | 1 |
| Approved PRs awaiting merge | 1 |
| Curated | 3 |
| Architect / Hermit proposals | 0 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
