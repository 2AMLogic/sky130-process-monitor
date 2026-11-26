# Work Plan

Prioritized roadmap from current GitHub label state, maintained by the Guide role.

_Generated: 2026-11-26T05:18:22Z (snapshot; compare against live labels)_

<!-- guide:plan-body:start -->
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

_None._

## Very Important

`loom:very-important` (one counts per workspace); every stage takes these first.

- **#26**: T1 item 4 (LVS clean): klt lvs for the oscillator bank (vs schematics) and the readout (vs gate-level netlist)

## Important

`loom:important`; taken before unlabelled work.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md)
- **#31**: T1 item 6 (Monte Carlo): klt yield evidence for the matching-dependent rows 2-4, and a not-applicable statement for the digital partition
- **#33**: T1 item 11 (power delivery): klt erc supply specs for both partitions plus readout PDN and power_connectivity evidence
- **#278**: osc_subth design iteration: at the slow corners and -40 C it runs at about 1-3 kHz or does not resolve, below one count in the default gate
- **#282**: Re-grade spec rows 2–4 on extracted frequencies for all five oscillators using klt pex --measure-command

## Ready

Human-approved issues ready for implementation (`loom:issue`).

_None._

## In Progress

Issues currently being built (`loom:building`).

- **#278**: osc_subth design iteration: at the slow corners and -40 C it runs at about 1-3 kHz or does not resolve, below one count in the default gate
- **#279**: Spec row 7 idle power: settle the nine suspect gated-off operating points (osc_nmos, osc_wire) and study an en-gated osc_subth bias divider
- **#303**: Replace the duplicated hand-rolled opt() CLI parsers in sim/solve/solve.py and sim/solve/yield_samples.py with argparse

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

_None._

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

_None._

## Proposed

Issues carrying `loom:curated`.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*
- **#26**: T1 item 4 (LVS clean): klt lvs for the oscillator bank (vs schematics) and the readout (vs gate-level netlist) *(curated)*
- **#190**: klt signoff gate: item 9 pins sim/ source modules, but has no CLAUDE.md warning and no regen script (the item-10 guardrails from #172 have no item-9 sibling) *(curated)*
- **#277**: Re-grade spec rows 1-4 on the fullest frequency table main supports: the 2026-11-05 solve record predates two cold-cell fills, and five cells still need a longer-window or relaxed-solver re-run *(curated)*
- **#278**: osc_subth design iteration: at the slow corners and -40 C it runs at about 1-3 kHz or does not resolve, below one count in the default gate *(curated)*
- **#279**: Spec row 7 idle power: settle the nine suspect gated-off operating points (osc_nmos, osc_wire) and study an en-gated osc_subth bias divider *(curated)*
- **#282**: Re-grade spec rows 2–4 on extracted frequencies for all five oscillators using klt pex --measure-command *(curated)*
- **#316**: Committed SDF functional-verification report names a producer-absolute path again at the klayout-tools 0.9.1 pin (upstream klayout-tools#5784 regression) *(curated)*
- **#321**: Pin sim/pex/measure_frequency.py in the item-9 analog inventory (run-time import of the pinned grader) *(curated)*

## Proposed (Architect / Hermit)

- **#146**: Remove .github/workflows/drift.yml: its only step already runs in tests.yml (npm test) *(hermit)*

## Epics

_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 0 |
| Very important | 1 |
| Important | 5 |
| Ready (`loom:issue`) | 0 |
| In Progress (`loom:building`) | 3 |
| PRs awaiting review | 0 |
| Approved PRs awaiting merge | 0 |
| Curated | 9 |
| Architect / Hermit proposals | 1 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
