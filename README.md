# sky130-process-monitor

An on-die process / voltage / temperature (PVT) monitor on
[SkyWater sky130](https://github.com/google/skywater-pdk), the 130 nm open
PDK — a bank of ring oscillators plus a subthreshold-biased sensing path,
read out by a digital counter — designed by AI agents driving
[klayout-tools](https://github.com/2AMLogic/klayout-tools), xschem + ngspice
on the analog side and cocotb + Icarus, Yosys and OpenROAD on the digital
side.

**Status: just opened, specification phase.** Nothing is designed yet.

**Built agent-native.** Every specification, decision record, testbench, and
line of documentation here is produced by AI agents working from a ratified
spec and an append-only evidence trail — not human-authored work that agents
merely assisted with. Verification is the product: every claim traces to a
recorded result under PVT corners. Where the agents hit friction with the
open-source tooling — most often
[klayout-tools](https://github.com/2AMLogic/klayout-tools) — that friction is
filed as a public issue against the tool itself, so the fix benefits everyone
using sky130, not just this repo.

## Why this block, on this PDK

A process monitor answers a question every other block on a die eventually
asks: *which corner did this die land in, and what are its supply and
temperature right now?* Ring oscillators whose frequency is dominated by
different device types (NMOS-limited, PMOS-limited, wire-limited, and a
leakage-starved subthreshold oscillator) each respond differently to
process, voltage and temperature; reading several of them against a
reference clock and solving for P, V and T is the classic approach.

To our knowledge, no open-source process-monitor block on an open PDK is
available with a committed, reproducible evidence chain from schematic to
layout. That gap is the reason to open this repo.

It is also a useful canary because it is **small but mixed-signal at the
seam**: the oscillators are drawn from standard cells and custom cells, the
counter and readout are synthesized, and the result is only meaningful if
the simulated frequency-versus-PVT surfaces are trustworthy — which puts the
open sky130 models, especially in subthreshold, directly under test.

## Scope

- **In scope**: the oscillator bank (standard-cell and custom-cell
  variants), the enable/select logic, a counter-based frequency readout
  against an external reference clock, and a documented calibration and
  solve procedure that turns counts into P, V and T estimates.
- **Not in scope**: an on-die reference clock, a full temperature sensor of
  the PTAT/bandgap kind, or an ADC. The readout assumes a reference clock is
  supplied from outside the block.
- **A different block from `sky130-temp-por`.** That sibling's temperature
  sensor is a PTAT/CTAT analog sensor paired with a POR. This repo's
  temperature estimate comes from oscillator frequencies. The two are not
  duplicates; the spec says so by name.

## Target specification (ratified by [decision 0001](spec/decisions/0001-ratify-target-spec.md), issue #2)

All rows are *targets*, not results: every figure is an unverified target
until the simulations named in [`spec/target-spec.md`](spec/target-spec.md)
have been run. That file is the source of truth; this table mirrors it.

| Parameter | Fallback | Target | Stretch |
|---|---|---|---|
| Oscillator bank | 3 oscillators (NMOS, PMOS, plain `hd` chain) | 5 oscillators (NMOS, PMOS, wire, subthreshold, plain `hd` chain) | add a second-library chain |
| Process discrimination | separate the slow and fast global corners | identify each of the five global corners (tt/ff/ss/sf/fs) at known V and T | estimate NMOS and PMOS skew as continuous values |
| Supply estimate (1.8 V core, 1.62–1.98 V) | ±50 mV | ±20 mV | ±10 mV |
| Temperature estimate (−40…125 °C, one-point calibration) | ±10 °C | ±5 °C | ±2 °C |
| Readout (reference clock is an input) | 24-bit counter, ref ±1000 ppm | 24-bit counter, 10 MHz ref ±100 ppm | — |
| Conversion time | < 10 ms | < 1 ms | < 100 µs |
| Active power | < 500 µW | < 100 µW | < 20 µW |
| Idle power | < 10 µW | < 1 µW | < 100 nW |
| Area | ≤ 0.05 mm² | ≤ 0.02 mm² | ≤ 0.01 mm² |
| Signoff | DRC + LVS clean | DRC + LVS clean, post-layout re-verified | — |

Maturity ladder: spec ratified → oscillator cells simulated across PVT →
readout RTL verified → calibration and solve procedure validated on
simulated data → layout DRC/LVS-clean → post-layout re-verification →
shuttle seat → measured silicon. **Current position: pre-spec.**

## Tool flow

- **Analog / custom cells**: xschem + ngspice, sky130 corner models.
- **Digital readout**: cocotb + Icarus for verification, Yosys for
  synthesis, OpenROAD for place-and-route.
- **Layout, DRC, LVS**: klayout-tools (`klt`).

## Repo layout

```
spec/          ratified spec + decision records
design/        oscillator and sensing-path schematics (xschem)
rtl/           counter, select and readout sources
sim/           testbenches + PVT corner results (ngspice)
verification/  cocotb testbenches for the readout
layout/        GDS + DRC/LVS reports (klayout-tools driven)
measurements/  silicon characterization (empty until tape-out)
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
