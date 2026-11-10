# Work Log

Chronological record of merged PRs and closed issues, maintained by the Guide
role. Newest first.

### 2026-11-10

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
