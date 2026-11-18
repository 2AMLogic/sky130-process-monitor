# Work Log

Chronological record of merged PRs and closed issues, maintained by the Guide
role. Newest first.

### 2026-11-18

- **PR #256**: ci: declare merge_group triggers on all workflows and guard them
- **Issue #254** (closed): Merge queue: add the merge_group trigger to the required-check workflow(s)
- **PR #251**: test: guard WORK_PLAN.md generated region against hand-written bullet suffixes
- **Issue #250** (closed): WORK_PLAN.md generated region keeps re-acquiring hand-written tokens the Guide generator cannot emit — no guard catches it

### 2026-11-17

- **PR #245**: fix: name sim/_siblings.py in the item-9 analog gate message
- **Issue #244** (closed): signoff.yml / regen-item9.sh / CLAUDE.md analog item-9 descriptions omit sim/_siblings.py (post-#221)
- **PR #243**: fix: name the sim/ env files in the item-9 digital gate message
- **PR #242**: fix: check xschem via the binary on PATH, pin fleet 3.4.7
- **PR #239**: chore(loom): resync installed Loom to v0.19.1306
- **Issue #241** (closed): xschem pin migration: migrate sky130-process-monitor to the fleet 3.4.7
- **Issue #230** (closed): signoff.yml CI error echo describes the item-9 digital inventory incompletely (post-#224)

### 2026-11-16

- **PR #149**: ci: enable the local buildGate on npm run check:ci
- **PR #234**: docs: scope ROADMAP blocked-work claim to the page, not the live query
- **PR #233**: fix: pin the shared sibling-module loader in the item-9 analog attestation inventory
- **PR #228**: ci: chain npm run lint into the check:ci and check:all aggregate gates
- **PR #225**: docs: document the osc_subth divider owner JSON in layout and lvs READMEs
- **PR #224**: fix: pin the sim environment files in the item-9 digital attestation inventory
- **PR #220**: fix: derive osc_subth res_high_po device variant from poly_w_nm
- **PR #205**: ci: run shellcheck as the npm run lint gate and in CI, clearing 6 pre-existing findings
- **Issue #135** (closed): loom-daemon preflight runs nothing: .loom/config.json has no buildGate block
- **Issue #226** (closed): npm run check:ci / check:all do not include the new shellcheck lint gate
- **Issue #223** (closed): ROADMAP 'Blocked and waiting' still asserts a static property of the live loom:issue set
- **Issue #221** (closed): sim/_siblings.py is neither inventoried in attest/item9_analog.json nor named in manifests/README.md's omission list
- **Issue #218** (closed): attest/item9_digital.json does not pin sim/check_env.sh, sim/pdk.json or sim/toolchain.json, which its own cold start depends on
- **Issue #208** (closed): osc_subth_divider.json owns poly_w_nm, but the res_high_po_0p35 device variant it must agree with is still a literal
- **Issue #204** (closed): layout/README.md enumerates layout/gen/ file by file and omits the new owner file osc_subth_divider.json
- **Issue #188** (closed): No shellcheck gate in CI: 15 tracked shell scripts, several driving simulations, are unlinted
- **PR #214**: docs: drop ROADMAP's completed Now list and cite the sized osc_subth gate
- **PR #202**: docs: add erc/ to the README tree; bring ROADMAP up to the 14-met record
- **Issue #203** (closed): ROADMAP.md '## Now' list is stale: all 4 of its items are closed, completed work
- **Issue #194** (closed): README Repo layout tree omits erc/, the one remaining tracked content directory
- **PR #227**: docs: name the four shell entrypoints and owner data files in the item-9 hazard clause
- **Issue #206** (closed): Item-9 hazard docs name "the four sim/**/run*.sh entrypoints", but sim/check_env.sh is the fourth and matches no named class

### 2026-11-15

- **PR #219**: docs: correct ROADMAP item-8 reason token from no_evidence to check_failed
- **PR #210**: refactor: drop dead need_all_proc policy from yield_samples usable()
- **PR #200**: test(sim): byte-drift suites for the sensitivity and binding request sets; re-attest item-9 analog
- **Issue #212** (closed): ROADMAP:27 item-8 reason token is stale: no_evidence should be check_failed in both columns
- **Issue #193** (closed): Remove the dead need_all_proc parameter in sim/solve/yield_samples.py: its A.PROCESS branch is unreachable
- **Issue #183** (closed): Add byte-drift suites for sim/sensitivity/requests/ and sim/solve/mc/requests/ (pattern exists only for requests-sized/)
- **PR #217**: docs: add characterization/ to README repo-layout tree, re-pad to col 20
- **PR #216**: test: guard all three corner-box lists against literal re-statement in tracked *.py
- **PR #215**: fix: pin the sim owner data files in the item-9 analog attestation inventory
- **PR #211**: docs: drop hand-maintained npm test suite enumerations
- **Issue #209** (closed): README repo-layout tree is missing characterization/ (pre-existing on main)
- **Issue #201** (closed): Owner data files (sim/pdk.json, sim/corner_box.json) are load-bearing for attested generators but pinned by no attest/ inventory
- **Issue #198** (closed): Hard-coded test-suite enumerations in README.md and tests.yml go stale every time a suite is added
- **Issue #192** (closed): Collapse the five ambiguous sibling-module loads in sim/ into one shared by-path loader (sim/_siblings.py)
- **Issue #191** (closed): Corner-box single-source guard misses sim/subthreshold/analyze.py (not importable, so the new test cannot reach it)
- **Issue #189** (closed): ROADMAP.md is stale after 11.digital grades met (met count and the item-11 row)
- **Issue #179** (closed): Remove four dead declarations in layout/gen/gen_osc_bank.py: an unused import, a pdk parameter always passed None, a never-drawn layer, and a discarded return value
- **Issue #178** (closed): Remove two of the three hand-copied mismatch-MC request blocks: mc(), mc_offnom() and gen_binding_mc.request() each restate the monte_carlo settings
- **Issue #177** (closed): Remove the hand-copied osc_subth divider geometry: lvs/make_reduced_refs.py restates RB from layout/gen/gen_osc_bank.py, and klt lvs cannot catch a drift
- **Issue #174** (closed): Remove the duplicated PVT corner box: sensitivity's generator and analyzer each define PROCESS/VDD/TEMP, and V_HALF/T_HALF restate their spans
- **Issue #173** (closed): Remove the last hand-copied oscillation threshold: sim/power/analyze_power.py restates SKIP_EDGES/MIN_CYCLES and is off by one
- **Issue #171** (closed): manifests/README.md says only items 10 and 2.analog are cited; the manifest cites sixteen evidence keys
- **Issue #170** (closed): Size the osc_subth gate: counts and cold-cell margin versus gate exponent k
- **Issue #169** (closed): T1 item 8: characterization report for both partitions, cited through the generic evidence envelope
- **PR #207**: refactor: collapse six hand-rolled sibling-module loaders in sim/ into one shared by-path helper
- **PR #199**: refactor: read osc_subth divider geometry from one owner JSON both generators share
- **PR #197**: feat: item-9 re-attest guardrails - regen-item9.sh, shared pin lib, gate remedy
- **PR #196**: docs: list all 17 cited evidence keys in manifest Files section
- **PR #187**: refactor(layout): drop four dead declarations from gen_osc_bank.py
- **PR #185**: refactor: single-owner PVT corner box (sim/corner_box.json) with derived V_HALF/T_HALF
- **PR #184**: refactor: collapse the three hand-copied mismatch-MC request blocks into mc_request()
- **PR #182**: docs: aggregate both partitions' spec-row verdicts into T1 item-8 reports
- **PR #180**: fix(power): grade active cells on the #8 oscillation rule, not a local 8-edge literal
- **PR #176**: feat: parameterise the counter gate in analyze.py and record the osc_subth gate sizing
- **Issue #175** (closed): Collapse the duplicated sibling-module loaders in sim/ to one mechanism

### 2026-11-14

- **PR #186**: erc: cite the readout supply-spec run as T1 11.digital evidence
- **PR #181**: feat: add attest/regen-item10.sh for pinned item-10 re-attestation
- **PR #167**: docs: roadmap as of 2026-11-13
- **Issue #168** (closed): T1 item 11 (digital): klt erc supply spec and report for the routed readout
- **Issue #172** (closed): Guide docs PRs that touch README.md red the klt signoff gate: README is an inventoried item-10 hygiene input
- **PR #164**: refactor: read the open_pdks pin from sim/pdk.json in the subthreshold analyzer
- **Issue #163** (closed): Read the open_pdks pin from sim/pdk.json in sim/subthreshold/analyze.py instead of two hardcoded copies

### 2026-11-13

- **PR #154**: chore: drop five .gitignore rules for flow/ and sim-harness paths this repo never had
- **Issue #147** (closed): Remove stale .gitignore rules for flow/, sim harness and corners paths that never existed in this repo
- **PR #162**: refactor: attest the analog item-2 envelope with klt signoff --attest 2
- **Issue #157** (closed): Remove layout/gen/attest_item2.py: klt signoff --attest 2 now exists and the digital partition already uses it
- **PR #161**: refactor(sim): share one negative-control pass rule; subthreshold no longer passes with klt missing
- **Issue #159** (closed): Share one expect_fail helper across the negative-control scripts: the subthreshold one passes with klt missing
- **PR #160**: docs: disclose the two SDF-run logs cited by hash but not retained
- **Issue #156** (closed): SDF functional-verification report cites two log files by sha256 that are not in the repo
- **PR #155**: chore: untrack regenerated SDF scaffolding under verification/readout/.fv-sdf
- **Issue #152** (closed): Untrack two uncited generated files in verification/readout/.fv-sdf
- **PR #151**: docs: narrow three claims to the runs and records that back them
- **Issue #142** (closed): README post-layout osc_subth wording and solve.py MC docstring are broader than the records
- **PR #150**: docs(manifests): name the three uninventoried sim/ scripts in the item-9 scope list
- **Issue #138** (closed): manifests/README.md item-9 scope list omits sim/pex/gen_requests.py
- **PR #145**: ci: put every workflow on one CPython 3.12 floor and enforce it repo-wide
- **Issue #144** (closed): Put drift.yml, signoff.yml and the README on the CPython >= 3.12 floor that #140 sets for tests.yml
- **PR #143**: test(solve): pin each committed sim/solve output to an explicit input report list
- **Issue #140** (closed): The rows 1-4 record's Reproduce line does not name its input report set
- **PR #115**: chore: remove superseded digital smoke flow
- **Issue #114** (closed): Remove digital smoke flow (rtl/smoke, verification/smoke): superseded by readout flow
- **PR #141**: refactor: define each row 2-4 estimator once in solve.py and share it
- **Issue #136** (closed): Share the row 2-4 estimators between solve.py and yield_samples.py (duplicated solve logic)
- **PR #133**: docs: give each README result class a verified reproduce command
- **Issue #131** (closed): README Reproduce section still says no simulated result is recorded, and every result-class row reads 'no recorded results yet'
- **PR #139**: refactor(pex): derive the klt pex testbenches from the sensitivity benches
- **Issue #137** (closed): Generate the sim/pex/osc testbenches from the sensitivity benches instead of keeping hand copies
- **PR #128**: evidence: attest T1 item 9 testbench inventories for both partitions
- **Issue #27** (closed): T1 item 9 (testbenches shipped): testbench inventories and klt signoff --attest 9 for both partitions
- **PR #134**: test: run the stdlib unit tests from npm test and in CI
- **Issue #127** (closed): Wire package.json test/check:ci stubs to the real unit tests (they exit 0 having run nothing)
- **PR #132**: docs: state actual artifact and sign-off status in README header
- **Issue #129** (closed): README status line is stale: 'no design, testbench or recorded result exists yet' is false on all three counts
- **PR #124**: sim: cold subthreshold cells at 2 ms, gmin/abstol floor sweep, 5 MHz step audit
- **Issue #44** (closed): Follow-on from PR #43: subthreshold Q2 bench follow-ups (cold-cell re-run, pfet S(T) reference, leakage floor)

### 2026-11-12

- **PR #122**: Bump Repo Skills 0.25.10 -> 0.26.1

### 2026-11-11

- **PR #119**: docs(pex): classify osc_subth vh net split as an extraction defect
- **PR #118**: docs(pex): diagnose osc_subth non-start as split vh header nets, not vbp or parasitics
- **Issue #116** (closed): osc_subth: diagnose why the extracted oscillator does not start (single-corner discriminating probe)
- **PR #113**: docs(pex): record osc_subth 45-cell pex run on divider-bearing GDS
- **PR #111**: feat(layout): draw osc_subth vbp bias divider as PDK poly resistors
- **Issue #109** (closed): osc_subth layout: draw the vbp bias divider (Rb0/Rb1) so the extracted oscillator can run
- **PR #108**: docs(pex): record osc_subth 45-cell pex run on a klt dev build, extracted side does not oscillate
- **PR #106**: docs(pex): record osc_subth LVT over-classification traced to the extractor
- **PR #104**: docs(pex): record osc_subth re-extraction on klt dev632 and aborted sharded submit
- **PR #102**: docs(pex): grade extracted oscillator values and record the two cold-cell probes
- **PR #100**: docs(pex): correct finding 6, LVT marker is drawn; klt extraction gap
- **Issue #98** (closed): Follow-on from PR #96: osc_subth layout lacks LVT marker (klt pex model_mismatch)
- **PR #99**: refactor(sim): single-source report loading and oscillator list
- **PR #96**: docs(pex): record osc_subth sharded re-run and LVT extraction mismatch
- **Issue #97** (closed): Consolidate duplicated sim report-loading helpers and OSCS lists

### 2026-11-10

- **PR #94**: test(solve): add CI drift check for committed sized MC request set
- **Issue #71** (closed): Stop committing 139 unrun, regenerable sized-MC request files (sim/solve/mc/requests-sized)
- **PR #93**: feat(verification): post-layout klt pex reports and SDF-annotated readout re-run
- **PR #91**: feat(sta): corner-matched oscillator STA for the readout counter and draft max-input-frequency decision
- **PR #88**: feat(sta): add multi-corner STA and functional-verification evidence for T1 item 5 digital
- **PR #87**: feat(drc): commit klt drc reports and fix analog generator DRC violations
- **Issue #89** (closed): Readout counter: time the oscillator clock domain per corner (STA completeness)
- **Issue #30** (closed): T1 item 5 (corner verification, digital): multi-corner klt sta plus klt functional-verification for the readout
- **Issue #25** (closed): T1 item 3 (DRC clean): klt drc reports for the oscillator bank and readout layouts with coverage disclosed
- **PR #86**: feat(lvs): LVS readout and oscillators, fix poly and diffusion widths
- **PR #85**: feat(layout): route readout with klt place-and-route and attest T1 item 2 digital
- **PR #84**: feat(signoff): synthesized readout netlist and T1 item 1 attestation
- **PR #83**: test(readout): phase-sweep short gate windows and document minimum k
- **PR #18**: feat(rtl): add saturating gated readout counter and register file with cocotb tests
- **Issue #24** (closed): T1 item 2 (layout, digital): placed-and-routed readout GDS from a committed klt place-and-route flow
- **Issue #22** (closed): T1 item 1 (design sources): synthesized readout netlist plus item-1 attestation covering both partitions
- **Issue #19** (closed): readout: read hangs busy if window is shorter than one oscillator period
- **Issue #82** (closed): readout: read can stay busy if no osc edge lands inside a very short gate window
- **Issue #16** (closed): Readout RTL: 24-bit saturating gated counter and register file, with cocotb tests in verification/readout/

### 2026-11-07

- **PR #79**: Bump Repo Skills 0.25.1 -> 0.25.10

### 2026-11-06

- **PR #77**: feat(layout): repack osc_wire serpentines under the stage column
- **Issue #75** (closed): Pack the osc_wire serpentines toward the met1 area floor and record what limits them
- **PR #76**: docs(sim): correct sensitivity MC coverage claim, collapse osc_subth override
- **Issue #53** (closed): Fix sensitivity README MC coverage claim and collapse duplicated osc_subth override in gen_requests.py
- **PR #73**: feat(sim): pool four-oscillator sized MC at row-2/4 cells and rerun klt yield at n=210
- **PR #72**: feat(sim): pool sized osc_subth binding-cell MC and rerun klt yield with a registering negative control
- **PR #69**: docs(sim): fill osc_wire sf cold cell with relaxed solver options and record the 1.98 V/-40 C margin
- **PR #68**: feat(sim): chunked sized-MC request generator and first osc_subth n=50 chunk
- **Issue #48** (closed): sim: run mismatch MC at the off-nominal (V,T) cells and explain osc_hd ff zero spread
- **PR #66**: feat(sim): complete nmos/wire binding-cell MC and rerun klt yield on the full bank
- **PR #65**: docs(sim): cold-cell sf osc_subth grid and MC on the fleet; osc_wire sf still missing
- **PR #64**: refactor(sim): derive power-bench box and windows from the sensitivity generator
- **Issue #59** (closed): Dedupe sim/power/gen_requests.py: PVT box and windows hand-copied from the sensitivity generator
- **PR #63**: docs(sim): cold-cell osc_subth off-nominal MC record (Part of #48)
- **PR #62**: docs(sim): record off-nominal MC for osc_nmos and osc_wire and hot-cell margin
- **PR #61**: feat: yield samples and klt yield evidence for rows 2-4 binding cells; digital not-applicable statement
- **PR #58**: feat(sim): complete row 7 power coverage and cite 5.analog as a failing model-run
- **Issue #29** (closed): T1 item 5 (corner verification, analog): sim/solve estimation benches graded over the 45-cell PVT box as klt sim envelopes for rows 1-4 and 7

### 2026-11-05

- **PR #56**: feat(sim): step-refined (5 ps) osc_hd grid and MC with coarse-vs-refined record
- **Issue #54** (closed): Follow-on from PR #52: step-refined osc_hd grid/MC (20 ps max-step bias)
- **PR #52**: docs(sim): partial off-nominal MC record and osc_hd ff zero-sigma timestep explanation
- **PR #51**: feat(sim): grade spec rows 1-4 and add oscillator-bank power benches (partial)
- **PR #47**: docs(sim): add fleet mismatch MC, discrimination margin and Q1 verdict proposal
- **PR #46**: feat(sim): five-oscillator grid sensitivity matrix and sf/fs mapping, MC pending
- **Issue #8** (closed): Sensitivity matrix and conditioning across the PVT corner box (spec Q1)
- **PR #43**: feat(sim): subthreshold oscillator grid, device probe and mismatch MC for spec Q2
- **PR #41**: feat(layout): generate five-oscillator bank GDS with item-2 evidence
- **PR #40**: feat(sim): add five-oscillator bank schematics, netlists and tt benches
- **PR #6**: feat: add pinned analog and digital toolchain smoke flows
- **Issue #10** (closed): Subthreshold oscillator: model-limited vs design-limited across temperature (spec Q2)
- **Issue #23** (closed): T1 item 2 (layout, analog): drawn GDS for the four custom oscillators and the hd baseline chain
- **Issue #17** (closed): Oscillator bank: schematics for the five spec oscillators and a tt frequency bench in sim/osc_bank/
- **Issue #3** (closed): Bring up both flows: pinned sky130 + ngspice smoke and a digital cocotb/Yosys skeleton (T1 item 9 groundwork)

### 2026-11-01

- **PR #38**: Bump Repo Skills 0.24.7 -> 0.25.1

### 2026-10-27

- **PR #34**: feat(hygiene): attest T1 item 10 and add README reproduce section
- **Issue #28** (closed): T1 item 10 (repo hygiene): hygiene inventory and klt signoff --attest 10 envelope

### 2026-10-21

- **PR #13**: Bump Repo Skills 0.24.3 -> 0.24.7

### 2026-10-20

- **PR #7**: ci: add T1 block manifest, klt signoff record and CI check
- **Issue #4** (closed): Commit a T1 block manifest and a klt signoff CI job (T1 item 10)

### 2026-10-17

- **PR #9**: docs(spec): ratify target spec, corner box and decision record
- **PR #1**: chore(loom): Install Loom 0.19.1181
- **Issue #2** (closed): Draft and ratify the target spec
