# 0001: Ratify the target specification

- Status: accepted
- Date: 2026-10-17
- Issue: #2

## Decision

[`spec/target-spec.md`](../target-spec.md) is ratified as the target every
downstream item verifies against. It sets target, fallback, stretch, binding
corner-box cells and a planned testbench for each of the nine parameter rows,
and the PVT corner box with its model file and PDK pin.

All accuracy, discrimination, power, time and area figures are ratified **as
unverified targets**. Ratifying does not claim any is achievable; the evidence
comes from the simulations named below. The README table is a mirror of the
target / fallback / stretch columns and is updated with the spec.

The spec may change only through a new numbered record in this directory.
Agents do not relax a row to make a result pass.

## Open questions

### Q1. Are frequency ratios alone enough for the five-corner target? — **Deferred**

Cannot be answered without simulated surfaces. Deciding experiment: build the
sensitivity matrix of every oscillator's frequency to P, V and T over the
corner box, and report its conditioning (singular values, condition number),
including the Monte Carlo mismatch spread. If the matrix is ill-conditioned for
the target, the options are a better bank or an absolute reference input; the
reference clock stays an input either way. Follow-up: issue #8 (`loom:triage`).

### Q2. Does the open model represent subthreshold leakage and its temperature dependence well enough? — **Deferred**

Deciding evidence: the subthreshold oscillator's frequency versus temperature
and corner, compared with the model's own leakage and subthreshold slope
across temperature at the same bias, to separate "model-limited" (the model
disagrees with itself or is non-physical, for example non-monotonic or
discontinuous across bins) from "design-limited" (the oscillator is simply
insensitive or too noisy). Follow-up: issue #10 (`loom:triage`).

### Q3. `sky130_fd_sc_hd` only, or a second library? — **Resolved**

`sky130_fd_sc_hd` only for the target and fallback: it is the library the
digital flow targets and it keeps the corner box one-library. A second library
chain is a stretch item in row 1, to be added only if the sensitivity matrix
shows library-level variation matters.

### Q4. What does a downstream block need? — **Resolved**

Raw counts plus a status flag, through a small register map (`CTRL`, `STATUS`,
`COUNT[i]`, `CAL[i]`). Solving for P, V and T runs off-block. Recorded even
though no consumer is declared; revisit when one is.

### Q5. Relationship to `sky130-temp-por` — **Resolved**

Different block. `sky130-temp-por` is a PTAT/CTAT analog temperature sensor
with a POR; this repo's temperature estimate comes from oscillator
frequencies. Neither is redesigned here; anything needed from the sibling is
taken by a pinned reference (`reuse.lock.json`), never a second design.

## Not decided here

- Final stage counts, the numeric discrimination margin, and the solve
  procedure: they follow the sensitivity matrix.
- Which of `sf`/`fs` is slow-NMOS: confirmed by simulation before the skew
  stretch.

## Follow-up issues

- Q1: #8.
- Q2: #10.

## Tool friction

No klayout-tools gap was hit while scoping (no `klt` flow was needed for a
documentation-only change).
