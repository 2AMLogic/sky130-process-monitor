# Work Plan

Prioritized roadmap from current GitHub label state, maintained by the Guide role.

_Generated: 2026-11-22T01:40:26Z (snapshot; compare against live labels)_

<!-- guide:plan-body:start -->
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

_None._

## Very Important

`loom:very-important` (one counts per workspace); every stage takes these first.

- **#26**: T1 item 4 (LVS clean): klt lvs for the oscillator bank (vs schematics) and the readout (vs gate-level netlist)
- **#280**: Spec row 7 active power: record what sets each oscillator's power and iterate the over-target ones (osc_wire worst at 1740 uW against a 100 uW target)

## Important

`loom:important`; taken before unlabelled work.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md)
- **#31**: T1 item 6 (Monte Carlo): klt yield evidence for the matching-dependent rows 2-4, and a not-applicable statement for the digital partition
- **#32**: T1 item 7 (post-layout verification): klt pex re-run of the oscillator benches and SDF-annotated readout re-run
- **#33**: T1 item 11 (power delivery): klt erc supply specs for both partitions plus readout PDN and power_connectivity evidence
- **#264**: 7.analog still unmet: 2026-11-10 osc_nmos/osc_wire pex reports are status=error (cold-cell timestep_too_small)
- **#278**: osc_subth design iteration: at the slow corners and -40 C it runs at about 1-3 kHz or does not resolve, below one count in the default gate
- **#282**: Re-grade spec rows 2–4 on extracted frequencies for all five oscillators using klt pex --measure-command

## Ready

Human-approved issues ready for implementation (`loom:issue`).

- **#282**: Re-grade spec rows 2–4 on extracted frequencies for all five oscillators using klt pex --measure-command

## In Progress

Issues currently being built (`loom:building`).

- **#275**: osc_subth: verify the original LVS report and one-corner ring start on klayout-tools 0.9.2
- **#276**: T1 item 11 (analog): klt erc supply spec and report for the oscillator bank
- **#277**: Re-grade spec rows 1-4 on the fullest frequency table main supports: the 2026-11-05 solve record predates two cold-cell fills, and five cells still need a longer-window or relaxed-solver re-run
- **#278**: osc_subth design iteration: at the slow corners and -40 C it runs at about 1-3 kHz or does not resolve, below one count in the default gate
- **#279**: Spec row 7 idle power: settle the nine suspect gated-off operating points (osc_nmos, osc_wire) and study an en-gated osc_subth bias divider
- **#280**: Spec row 7 active power: record what sets each oscillator's power and iterate the over-target ones (osc_wire worst at 1740 uW against a 100 uW target)
- **#281**: Record and grade spec section 6 conversion time at surface-derived oscillator periods (8.digital 'not recorded' row)
- **#283**: Share the six repeated checks in the binding and sized Monte Carlo request drift tests
- **#287**: Add a .gitignore rule for a worktree-local PDK install (.pdk/)
- **#288**: Use one per-cell sigma check for Monte Carlo yield eligibility

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

- **#290**: refactor: share the six drift checks in test_gen_binding_mc.py via a mixin
- **#291**: docs(pex): verify the osc_subth vh-split fix on released klayout-tools 0.9.2
- **#294**: erc: per-oscillator klt erc supply-spec evidence for the analog bank
- **#295**: fix: settle row 7 idle power with transient-settle benches; add en-gated osc_subth divider candidate
- **#296**: fix(sim): gate yield cell eligibility on the analyzer's per-cell sigma
- **#297**: feat(solve): re-grade spec rows 1-4 on the full 225-cell frequency table
- **#298**: test(readout): record spec §6 conversion time at surface-derived oscillator periods
- **#299**: feat(sim): sweep osc_subth cold-corner levers; propose the L=0.35 header
- **#300**: chore: ignore worktree-local PDK install (/.pdk/)
- **#301**: feat(power): row-7 active-power iteration — decomposition, lever sweeps, decision 0004 (proposed), six gap cells graded

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

_None._

## Proposed

Issues carrying `loom:curated`.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*
- **#26**: T1 item 4 (LVS clean): klt lvs for the oscillator bank (vs schematics) and the readout (vs gate-level netlist) *(curated)*
- **#190**: klt signoff gate: item 9 pins sim/ source modules, but has no CLAUDE.md warning and no regen script (the item-10 guardrails from #172 have no item-9 sibling) *(curated)*
- **#275**: osc_subth: verify the original LVS report and one-corner ring start on klayout-tools 0.9.2 *(curated)*
- **#276**: T1 item 11 (analog): klt erc supply spec and report for the oscillator bank *(curated)*
- **#277**: Re-grade spec rows 1-4 on the fullest frequency table main supports: the 2026-11-05 solve record predates two cold-cell fills, and five cells still need a longer-window or relaxed-solver re-run *(curated)*
- **#278**: osc_subth design iteration: at the slow corners and -40 C it runs at about 1-3 kHz or does not resolve, below one count in the default gate *(curated)*
- **#279**: Spec row 7 idle power: settle the nine suspect gated-off operating points (osc_nmos, osc_wire) and study an en-gated osc_subth bias divider *(curated)*
- **#280**: Spec row 7 active power: record what sets each oscillator's power and iterate the over-target ones (osc_wire worst at 1740 uW against a 100 uW target) *(curated)*
- **#281**: Record and grade spec section 6 conversion time at surface-derived oscillator periods (8.digital 'not recorded' row) *(curated)*
- **#282**: Re-grade spec rows 2–4 on extracted frequencies for all five oscillators using klt pex --measure-command *(curated)*
- **#287**: Add a .gitignore rule for a worktree-local PDK install (.pdk/) *(curated)*

## Proposed (Architect / Hermit)

- **#146**: Remove .github/workflows/drift.yml: its only step already runs in tests.yml (npm test) *(hermit)*
- **#165**: Remove the superseded osc-probe STA pair: a second, assumed-period slack table for a question readout.osc-corner.sta.report.json now answers with measured periods *(hermit)*

## Epics

_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 0 |
| Very important | 2 |
| Important | 7 |
| Ready (`loom:issue`) | 1 |
| In Progress (`loom:building`) | 10 |
| PRs awaiting review | 10 |
| Approved PRs awaiting merge | 0 |
| Curated | 12 |
| Architect / Hermit proposals | 2 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
