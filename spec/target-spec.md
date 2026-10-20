# Target specification

**Status: ratified by [decision 0001](decisions/0001-ratify-target-spec.md).**

Every figure below is a **target, not a result**. Accuracy, discrimination,
power, time and area figures are **unverified targets**: no simulation has
been run against them, the sensitivity matrix does not exist yet, and per the
repo rules no estimate accuracy may be quoted until the solve procedure has
been run against it. Rows carried over unchanged from the README draft are
marked *(carried over)*; rows new to this spec are marked *(proposed)* and are
equally unchecked against the models. Nothing here is measured until silicon
exists.

Each row gives target / fallback / stretch, the corner-box cells it binds
(see [PVT corner box](#pvt-corner-box)), and the planned testbench. Testbench
paths are under `sim/` (or `verification/` for RTL) and **do not exist yet**;
each is written by the issue that produces the evidence.

## Parameters

### 1. Oscillator bank composition *(proposed)*

| | |
|---|---|
| Target | Five oscillators: NMOS-dominated, PMOS-dominated, wire-dominated, subthreshold/leakage-starved, and a plain `sky130_fd_sc_hd` inverter chain as the baseline. Odd stage counts, initial planning figure 31 stages for the first three and the baseline, 15 for the subthreshold oscillator. Standard-cell: the baseline chain only. Custom-drawn: the other four. |
| Fallback | Three oscillators: NMOS-dominated, PMOS-dominated, plain `hd` chain (enough to attempt slow/fast separation). |
| Stretch | Add a second oscillator built on a second standard-cell library to probe library-level variation (see decision Q3). |
| Binds | All 45 cells of the box (5 corners × 3 V × 3 T) for frequency surfaces. |
| Testbench | `sim/osc_bank/` frequency-versus-PVT sweep, one bench per oscillator. |

Stage counts are planning figures; the sensitivity-matrix work may change them,
through a new decision record.

### 2. Process discrimination *(target carried over; decision rule proposed)*

| | |
|---|---|
| Target | Identify each of the five global corners (tt/ff/ss/sf/fs) at known V and T. |
| Fallback | Separate the slow and fast global corners. |
| Stretch | Estimate NMOS and PMOS skew as continuous values. |
| Decision rule | Classify the oscillator frequency vector to the nearest corner centroid in the calibrated ratio space. A corner is "identified" only if the margin to the next-nearest centroid exceeds the noise floor set by counter quantization plus the mismatch Monte Carlo spread of each oscillator. The numeric margin is **to be derived from the sensitivity matrix, not asserted here.** |
| Binds | "Known V and T": V in {1.62, 1.80, 1.98}, T in {−40, 27, 125 °C}, all five corners. Plus mismatch Monte Carlo (below). |
| Testbench | `sim/sensitivity/` (sensitivity matrix and its conditioning), `sim/solve/` (classification against simulated data). |

The stretch does not drive the bank architecture until the target closes.

### 3. Supply estimate *(carried over)*

| | |
|---|---|
| Target | ±20 mV over 1.62–1.98 V (1.8 V core rail). |
| Fallback | ±50 mV. |
| Stretch | ±10 mV. |
| T known or joint? | Target and fallback: T known (supplied by the one-point calibration reading, below), V solved. Stretch: joint solve of P, V and T. |
| Binds | All 45 cells; fixed-corner Monte Carlo for the mismatch term. |
| Testbench | `sim/solve/` using frequency surfaces from `sim/osc_bank/`. |

### 4. Temperature estimate *(carried over; scheme proposed)*

| | |
|---|---|
| Target | ±5 °C over −40…125 °C with one-point calibration. |
| Fallback | ±10 °C. |
| Stretch | ±2 °C. |
| Calibration | Target: one-point, at one known temperature (27 °C planning figure) and nominal supply; stores one calibration count per used oscillator (24-bit each) in a register file loaded from outside. Two-point is the fallback for any row that one point cannot meet and needs a new decision record. No calibration is not planned. |
| Binds | All 45 cells; mismatch Monte Carlo. |
| Testbench | `sim/solve/`. |

**Not `sky130-temp-por`.** This temperature estimate is derived from oscillator
frequencies. The sibling block `sky130-temp-por` builds a PTAT/CTAT analog
temperature sensor paired with a POR. They are different blocks; neither is
redesigned here and this repo does not copy or depend on the sibling. If a
later need arises for what that sibling builds, it is taken by a pinned
reference (`reuse.lock.json`), not a second design.

### 5. Readout *(proposed)*

| | |
|---|---|
| Counter | 24-bit, saturating, one oscillator selected at a time. |
| Gate time | Programmable, 2^k reference-clock cycles; default 2^10 (102.4 µs at 10 MHz). |
| Reference clock | **An input to the block; no on-die reference clock.** Target 10 MHz, accuracy ±100 ppm over the operating range. The requirement is only that reference error is negligible against the estimate error budget (100 ppm ≈ 0.01 %); a looser reference needs a new decision record. Fallback ±1000 ppm. Stretch: none. |
| Binds | Reference-clock accuracy applies at all T and V cells; the block does not generate it. |
| Testbench | `verification/readout/` (cocotb + Icarus): gate/count correctness, saturation, select. |

Register interface (consumer-facing, no consumer declared yet):

| Register | Access | Content |
|---|---|---|
| `CTRL` | RW | start, oscillator select, gate exponent `k` |
| `STATUS` | RO | busy, done, overflow (counter saturated) |
| `COUNT[i]` | RO | 24-bit count for oscillator `i`, latched at gate end |
| `CAL[i]` | RW | calibration count for oscillator `i` (written from outside) |

The block outputs **raw counts plus a status flag**; the solve for P, V and T
runs off-block. The register map is a planning figure, finalized with the RTL.

### 6. Conversion time *(carried over)*

| | |
|---|---|
| Target | < 1 ms for a full read of all oscillators. |
| Fallback | < 10 ms. |
| Stretch | < 100 µs. |
| Binds | Reference clock at its target frequency; all oscillator frequencies from the surfaces (counts per gate depend on them). |
| Testbench | `verification/readout/` (cycle count) combined with `sim/osc_bank/` (counts per gate). |

Planning check, unverified: five oscillators sequentially at the default gate
is 5 × 102.4 µs ≈ 0.5 ms.

### 7. Active and idle power *(active carried over; idle proposed)*

| | Active | Idle |
|---|---|---|
| Target | < 100 µW | < 1 µW |
| Fallback | < 500 µW | < 10 µW |
| Stretch | < 20 µW | < 100 nW |

Active: one oscillator running plus counter, averaged over a conversion. Idle:
oscillators gated off, leakage only. Idle leakage is mostly set by
corner and temperature, so it binds the hot and fast cells (ff/125 °C/1.98 V)
hardest.
Testbench: `sim/power/`.

### 8. Area budget *(proposed)*

| | |
|---|---|
| Target | ≤ 0.02 mm² including oscillators, counter and register file. |
| Fallback | ≤ 0.05 mm². |
| Stretch | ≤ 0.01 mm². |
| Testbench | Layout report from klayout-tools / OpenROAD, once layout exists (`layout/`). |

### 9. Signoff *(carried over)*

| | |
|---|---|
| Target | DRC + LVS clean, and post-layout re-verification of every row above. |
| Fallback | DRC + LVS clean. |
| Stretch | — |
| Testbench | `klt` DRC and LVS; post-layout re-run of each testbench above. |

## PVT corner box

Every row binds against this box.

| Axis | Values |
|---|---|
| Global corner | `tt`, `ff`, `ss`, `sf`, `fs` |
| Supply | 1.62 V, 1.80 V, 1.98 V |
| Temperature | −40 °C, 27 °C, 125 °C |
| Mismatch | Monte Carlo, for any row whose accuracy depends on matching between oscillators (process discrimination, supply, temperature) |

PDK pin and model files (confirmed against the PDK on the worker, 2026-10-17):

- PDK: sky130A from open_pdks revision
  `c6d73a35f524070e85faff4a6a9eef49553ebc2b`. This is the pin that the
  toolchain bring-up (issue #3, `sim/pdk.json`, in review) uses. If #3 changes
  it, this document changes by a decision record.
- Model library: `<PDK_ROOT>/sky130A/libs.tech/ngspice/sky130.lib.spice`.
- Corner sections in that file: `tt`, `ff`, `ss`, `sf`, `fs`.
- Mismatch: that file defines `mc_mm_switch` (and `mc_pr_switch`) parameters,
  default 0 in each corner section; the Monte Carlo runs set them to enable
  device mismatch. *Not yet exercised*: how these switches behave in the
  subthreshold regime is itself part of decision Q2.
- *Not confirmed here*: which letter of `sf`/`fs` is NMOS and which is PMOS.
  It must be established by a simulation before the skew stretch is attempted.
- Temperature is applied as the ngspice simulation temperature.

Open-ended variants of the global corners in the same file (`ll`, `hh`, `hl`,
`lh`, and the combined `*_ll` etc. sections) are not in this box.

## Out of scope

- An on-die reference clock, a PTAT/bandgap temperature sensor, an ADC.
- Running the sensitivity matrix or any solve in this spec; those are the
  follow-up issues named in the decision record.
