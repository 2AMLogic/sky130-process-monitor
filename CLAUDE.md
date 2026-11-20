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
- **Four ordinary-looking files are hashed T1 evidence.** `attest/item10.json`
  inventories `README.md`, `LICENSE`, `spec/target-spec.md` and
  `.github/workflows/signoff.yml`, hashing their bytes into
  `evidence/item10.json` — so editing any of them, even a documentation-only
  edit, turns T1 item 10 stale and reds the `klt signoff` gate. A PR that
  touches one of the four runs `attest/regen-item10.sh` and commits the
  regenerated `evidence/item10.json` **in the same commit** as the edit. The
  script reads the `klayout-tools` pin from `.github/workflows/signoff.yml`;
  never re-attest with the host's `klt`, which writes a non-reproducing
  envelope. Dropping a file from the inventory to quiet the gate is a
  `spec/` decision record, not a CI fix.
- **Item 9 hash-pins the sim/ and verification/readout/ testbench sources.**
  `attest/item9_analog.json` (every committed deck and `klt sim` request, the
  `sim/solve/` and `sim/sensitivity/` Python modules, the PEX grader
  `sim/pex/grade_pex.py` (issue #267, the item-8 measurement path), the shared
  sibling-module loader those benches import at run time (`sim/_siblings.py`),
  the owner data files those benches load — `sim/corner_box.json`,
  `sim/pdk.json` and `sim/toolchain.json` — and the four shell entrypoints,
  `sim/check_env.sh` plus the three `sim/**/run*.sh` runners) and
  `attest/item9_digital.json` (the
  `verification/readout/` bench files plus the `sim/` environment files its
  cold start reads) hash their bytes into
  `evidence/item9_*.json` — so editing any of them, even a refactor or a
  test-only edit, turns T1 item 9 stale and reds the `klt signoff` gate. A PR
  that touches an inventoried source file runs `attest/regen-item9.sh analog`
  (or `digital`, or `both`) and commits the regenerated envelope **in the
  same commit** as the edit. The script reads the `klayout-tools` pin from
  `.github/workflows/signoff.yml` and runs the partition's declared cold
  starts for real on a host with the pinned PDK and ngspice (analog) or
  cocotb/Icarus/Verilator (digital) — a bounded local single-unit attestation
  pass, not a batch grid; never re-attest with the host's `klt`, which writes
  a non-reproducing envelope. Dropping a file from an inventory to quiet the
  gate is a `spec/` decision record, not a CI fix.
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
This repository has [Repo Skills](https://github.com/rjwalters/repo) v0.26.1 installed —
general repository hygiene and environment commands invoked as `/repo:<command>`. Run
`/repo:help` for the command list, or see `.claude/skills/repo/SKILL.md` for the full
guide. Hygiene commands apply safe, reversible fixes by default and report each
change; run with `--ask` to review first, and `--prune` to allow irreversible
removals. Managed by `install.sh` — edit outside the markers only.
<!-- END REPO-SKILLS -->
