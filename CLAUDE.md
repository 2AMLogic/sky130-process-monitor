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
