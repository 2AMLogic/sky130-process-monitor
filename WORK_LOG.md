# Work Log

Chronological record of merged PRs and closed issues, maintained by the Guide
role. Newest first.

### 2026-11-06

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
