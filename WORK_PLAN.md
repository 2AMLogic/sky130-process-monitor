# Work Plan

Prioritized roadmap from current GitHub label state, maintained by the Guide role.

<!-- guide:plan-body:start -->
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

- **#149**: ci: enable the local buildGate on npm run check:ci

## Very Important

`loom:very-important` (one counts per workspace); every stage takes these first.

- **#26**: T1 item 4 (LVS clean): klt lvs for the oscillator bank (vs schematics) and the readout (vs gate-level netlist)

## Important

`loom:important`; taken before unlabelled work.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md)
- **#31**: T1 item 6 (Monte Carlo): klt yield evidence for the matching-dependent rows 2-4, and a not-applicable statement for the digital partition
- **#32**: T1 item 7 (post-layout verification): klt pex re-run of the oscillator benches and SDF-annotated readout re-run
- **#33**: T1 item 11 (power delivery): klt erc supply specs for both partitions plus readout PDN and power_connectivity evidence
- **#117**: osc_subth: 14 series-header nets (vh1..vh14) are split in the extraction, ring stage PFET sources float

## Ready

Human-approved issues ready for implementation (`loom:issue`).

- **#204**: layout/README.md enumerates layout/gen/ file by file and omits the new owner file osc_subth_divider.json

## In Progress

Issues currently being built (`loom:building`).

- **#135**: loom-daemon preflight runs nothing: .loom/config.json has no buildGate block
- **#183**: Add byte-drift suites for sim/sensitivity/requests/ and sim/solve/mc/requests/ (pattern exists only for requests-sized/)
- **#188**: No shellcheck gate in CI: 15 tracked shell scripts, several driving simulations, are unlinted
- **#193**: Remove the dead need_all_proc parameter in sim/solve/yield_samples.py: its A.PROCESS branch is unreachable
- **#194**: README Repo layout tree omits erc/, the one remaining tracked content directory
- **#203**: ROADMAP.md '## Now' list is stale: all 4 of its items are closed, completed work
- **#208**: osc_subth_divider.json owns poly_w_nm, but the res_high_po_0p35 device variant it must agree with is still a literal
- **#212**: ROADMAP:27 item-8 reason token is stale: no_evidence should be check_failed in both columns

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

- **#205**: ci: run shellcheck as the npm run lint gate and in CI, clearing 6 pre-existing findings
- **#214**: docs: drop ROADMAP's completed Now list and cite the sized osc_subth gate
- **#220**: fix: derive osc_subth res_high_po device variant from poly_w_nm

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

- **#149**: ci: enable the local buildGate on npm run check:ci
- **#200**: test(sim): byte-drift suites for the sensitivity and binding request sets; re-attest item-9 analog
- **#210**: refactor: drop dead need_all_proc policy from yield_samples usable()
- **#219**: docs: correct ROADMAP item-8 reason token from no_evidence to check_failed

## Proposed

Issues carrying `loom:curated`.

- **#5**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*
- **#26**: T1 item 4 (LVS clean): klt lvs for the oscillator bank (vs schematics) and the readout (vs gate-level netlist) *(curated)*
- **#117**: osc_subth: 14 series-header nets (vh1..vh14) are split in the extraction, ring stage PFET sources float *(curated)*
- **#135**: loom-daemon preflight runs nothing: .loom/config.json has no buildGate block *(curated)*
- **#183**: Add byte-drift suites for sim/sensitivity/requests/ and sim/solve/mc/requests/ (pattern exists only for requests-sized/) *(curated)*
- **#188**: No shellcheck gate in CI: 15 tracked shell scripts, several driving simulations, are unlinted *(curated)*
- **#190**: klt signoff gate: item 9 pins sim/ source modules, but has no CLAUDE.md warning and no regen script (the item-10 guardrails from #172 have no item-9 sibling) *(curated)*
- **#193**: Remove the dead need_all_proc parameter in sim/solve/yield_samples.py: its A.PROCESS branch is unreachable *(curated)*
- **#194**: README Repo layout tree omits erc/, the one remaining tracked content directory *(curated)*
- **#203**: ROADMAP.md '## Now' list is stale: all 4 of its items are closed, completed work *(curated)*
- **#204**: layout/README.md enumerates layout/gen/ file by file and omits the new owner file osc_subth_divider.json *(curated)*
- **#208**: osc_subth_divider.json owns poly_w_nm, but the res_high_po_0p35 device variant it must agree with is still a literal *(curated)*
- **#212**: ROADMAP:27 item-8 reason token is stale: no_evidence should be check_failed in both columns *(curated)*
- **#218**: attest/item9_digital.json does not pin sim/check_env.sh, sim/pdk.json or sim/toolchain.json, which its own cold start depends on *(curated)*

## Proposed (Architect / Hermit)

- **#146**: Remove .github/workflows/drift.yml: its only step already runs in tests.yml (npm test) *(hermit)*
- **#165**: Remove the superseded osc-probe STA pair: a second, assumed-period slack table for a question readout.osc-corner.sta.report.json now answers with measured periods *(hermit)*

## Epics

_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 1 |
| Very important | 1 |
| Important | 5 |
| Ready (`loom:issue`) | 1 |
| In Progress (`loom:building`) | 8 |
| PRs awaiting review | 3 |
| Approved PRs awaiting merge | 4 |
| Curated | 14 |
| Architect / Hermit proposals | 2 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
