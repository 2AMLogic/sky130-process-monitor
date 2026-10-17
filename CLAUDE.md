# sky130-process-monitor — agent instructions

Open-source canary block: a process / voltage / temperature monitor on the
SkyWater sky130 PDK — a ring-oscillator bank plus a subthreshold sensing
path with a counter readout — designed and verified by AI agents.
**Mixed-signal**, so both flows apply.

- **PDK**: SkyWater sky130 (open PDK, google/skywater-pdk). Analog: xschem +
  ngspice. Digital: cocotb + Icarus, Yosys, OpenROAD. Layout, DRC, and LVS
  through klayout-tools (`klt`) in both cases.
- **The models are the risk.** The block's output is only as good as the
  simulated frequency-versus-PVT surfaces it is calibrated against. The
  subthreshold path depends on leakage and subthreshold-slope behaviour that
  is the least-exercised part of any open model set, and separating P, V and
  T from a handful of frequencies is ill-conditioned if the oscillators'
  sensitivities are too similar. Show the sensitivity matrix and its
  conditioning before claiming any estimate; never quote an estimate
  accuracy that the solve procedure has not been run against.
- **Scope discipline.** No on-die reference clock, no PTAT/bandgap
  temperature sensor, no ADC. The reference clock is an input; specify its
  frequency and accuracy requirement and stop. `sky130-temp-por` builds a
  PTAT/CTAT temperature sensor on this PDK; this repo's oscillator-based
  temperature estimate is a different block, and the spec says so by name
  rather than redesigning either one. If a later need arises for anything
  that sibling builds, take it by a pinned reference (`reuse.lock.json`),
  not a second design.
- **Friction protocol (the canary's job)**: every time klayout-tools is
  awkward, missing a capability, or wrong for what you need, file an issue at
  `2AMLogic/klayout-tools` describing the tool gap generically — that tracker
  is scoped to the tool, so keep design-specific detail out of it and describe
  the gap, not the design.
- **Verification is the product**: no claim without a testbench. PVT corners
  on every recorded analog result; recorded results are append-only evidence.
  Every simulated figure is labelled as simulated, with its corner and
  testbench — nothing here is measured until silicon exists.
- Spec changes go through `spec/` with a decision record; agents do not relax
  the ratified spec to make results pass.
- **The five-corner target is the target.** Separating slow from fast is the
  fallback; continuous NMOS/PMOS skew estimation is a stretch. Do not let the
  stretch drive the oscillator-bank architecture before the target closes.

<!-- BEGIN LOOM ORCHESTRATION -->
This repository uses [Loom](https://github.com/rjwalters/loom) for AI-powered development orchestration — see the Loom repository for the full guide (roles, labels, worktrees, configuration). When installed, Loom also writes a locally-substituted copy of that guide to `.loom/CLAUDE.md`.

Work is coordinated through `loom:` labels on issues and pull requests, and the same roles run either under `loom-daemon` or by hand in an attended session — daemon mode is optional. Create the labels once with `.loom/scripts/sync-labels.sh` (an install ships `.github/labels.yml` but does not create the labels on the forge). A pull request ready for review carries `loom:review-requested`; Judge reviews it and applies `loom:pr` (approved) or `loom:changes-requested`; Doctor fixes a `loom:changes-requested` pull request and returns it to `loom:review-requested`. Only a `loom:pr` pull request gets merged, and always via this repo's merge script (`.loom/scripts/merge-pr.sh`) — never a raw forge merge command such as `gh pr merge`. Full state machine: `.loom/docs/label-state-machine.md`.
<!-- END LOOM ORCHESTRATION -->

<!-- BEGIN REPO-SKILLS -->
This repository has [Repo Skills](https://github.com/rjwalters/repo) v0.24.3 installed —
general repository hygiene and environment commands invoked as `/repo:<command>`. Run
`/repo:help` for the command list, or see `.claude/skills/repo/SKILL.md` for the full
guide. Hygiene commands apply safe, reversible fixes by default and report each
change; run with `--ask` to review first, and `--prune` to allow irreversible
removals. Managed by `install.sh` — edit outside the markers only.
<!-- END REPO-SKILLS -->
