# Roadmap

sky130-process-monitor is an on-die process / voltage / temperature monitor on SkyWater sky130: a
five-oscillator bank plus a counter readout, built to carry a reproducible evidence chain from schematic
to layout.

**Status as of 2026-11-13, `main` @ `a75f76e`.** Every result named here is *simulated*; nothing is
measured. This file states direction and order. The per-row verdict of record is
[`manifests/sky130-process-monitor.signoff.json`](manifests/sky130-process-monitor.signoff.json); the
label-driven queue is [`WORK_PLAN.md`](WORK_PLAN.md); history is [`WORK_LOG.md`](WORK_LOG.md). Tracker
of the gap to T1: #5.

## Where it stands

`klt signoff` (`klayout-tools==0.9.1`) grades 14 of the 22 T1 rows `met`, one `not_applicable`, seven
`unmet`. Checklist: [`manifests/design-evidence-tiers.md`](manifests/design-evidence-tiers.md).

| T1 item | Analog (oscillator bank) | Digital (readout) |
|---|---|---|
| 1 Design sources | met | met |
| 2 Layout | met | met |
| 3 DRC clean | met (curated deck; see below) | met |
| 4 LVS clean | **unmet**, `no_evidence` (#26) | met |
| 5 Corner verification | **unmet**, `check_failed` | met |
| 6 Monte Carlo | **unmet**, `check_failed` (#31) | not applicable |
| 7 Post-layout | **unmet**, `check_failed` (#32, #117) | met |
| 8 Characterization report | **unmet**, `check_failed` | **unmet**, `check_failed` |
| 9 Testbenches shipped | met | met |
| 10 Repo hygiene | met | met |
| 11 Power delivery | **unmet**, `no_evidence` (#33) | met (`erc/readout.report.json` + `lvs/readout.report.json` + `layout/readout/report.json`) |

What sits behind the unmet rows, each from a committed record:

- **Spec rows fail at schematic level.** Rows 1, 3 and 4 and the row-2 five-corner target grade FAIL;
  only the row-2 slow/fast fallback passes
  ([`sim/solve/records/2026-11-05-rows1-4.md`](sim/solve/records/2026-11-05-rows1-4.md)). 7 of the 225
  grid cells show no or too-short oscillation, all at −40 °C.
- **The cold-cell margin is set by counter quantisation, not mismatch.** At 1.98 V / −40 °C `osc_subth`
  gets under one count in the default gate at the ss and sf corners
  ([`2026-11-06-mc-offnominal-cold-margin.md`](sim/sensitivity/records/2026-11-06-mc-offnominal-cold-margin.md)
  §3); a follow-up record sizes the lever: gate exponent k = 14 (a 1.638 ms `osc_subth` gate) puts the
  margin on its MC-limited plateau, absolute 2.194 against 0.759 at the default gate, inside the
  24-bit counter bound
  ([`2026-11-14-osc-subth-gate-sizing.md`](sim/sensitivity/records/2026-11-14-osc-subth-gate-sizing.md)).
- **The counter does not cover `osc_hd`.** Setup-limited counter fmax is about half the `osc_hd`
  frequency in all three timed corners ([decision
  0003](spec/decisions/0003-counter-max-input-frequency.md), draft).
- **LVS, analog.** `osc_hd`, `osc_nmos` and `osc_pmos` match their item-1 netlists; `osc_wire` and
  `osc_subth` match reduced references only ([`lvs/README.md`](lvs/README.md)).
- **Post-layout, analog.** Four oscillators re-run extracted and come out slower (median −14 % to −24 %
  on the `klt pex` edge-count proxy). The extracted `osc_subth` does not start: 14 `vh` header nets are
  split by the extractor (2AMLogic/klayout-tools#5311). Rows 2–4 are not re-graded on extracted values
  ([`sim/pex/README.md`](sim/pex/README.md)).
- **DRC is a curated-deck result.** The PDK-native deck reports 562 violations (`ct.4` ×220, `li.5`
  ×342) on the analog stream ([`drc/README.md`](drc/README.md); tool gap 2AMLogic/klayout-tools#5233).
- **Monte Carlo.** Row 2 ff and row 4 are `sufficient` at n ≈ 210; row 2 tt/fs/ss/sf and row 3 are short
  of the sample counts `klt yield` asks for
  ([`RECORD-2026-11-06-item6-sized-bank.md`](sim/solve/mc/RECORD-2026-11-06-item6-sized-bank.md)).

## Now

Startable today on `main`; each is one pull request, none needing a batch submission, a spec change
or a tool release. The dispatchable set is whatever `gh issue list --label loom:issue --state open`
returns when you read this. Every re-check during this page's last revision found zero to three
items, and the set turned over within hours — run the query rather than trusting any count quoted here.

In flight: #135 (local build gate; PR #149 approved and held), and the hermit proposals #165 and #146,
which await promotion.

## Next

- **Re-extract `osc_subth` and re-check ring start** (#117). Unblocked by a `klayout-tools` release
  carrying the fix for 2AMLogic/klayout-tools#5311. *Done when* `vh1`..`vh14` extract as one net each
  and a one-corner probe record (`sim/pex/probe/run_probe.sh`) is committed.
- **Finish the 45-cell extracted re-run and re-grade 7.analog** (#32). After #117. *Done when* a `klt
  pex` report exists for all five oscillators on a like-for-like extraction and the signoff record is
  regenerated.
- **Re-grade spec rows 2–4 on extracted frequencies.** After #32; needs a frequency, not the quantised
  edge count `klt pex` reports today. *Done when* a record under `sim/pex/records/` gives the row 2–4
  verdicts on extracted values. No issue yet.
- **Native-deck DRC on the analog stream.** After #117, because the layout must stay unchanged for that
  re-check. Rework the generator's li1 / licon geometry. *Done when* `klt drc --engine klayout` reports
  no `ct.4` / `li.5` on `osc_bank` and DRC, LVS and the item-2 attestation are re-run. No issue yet.
- **11.analog** (#33), after 4.analog is met (#26).
- **Readout change for `osc_hd`**, after decision 0003 is ratified: prescaler RTL, re-synthesis, P&R and
  re-verification if option 1 is taken.

## Later

- **Close the failing estimate rows (1, 3, 4, row-2 target).** First question: is the five-oscillator
  bank sufficient, or does it need a different bank or input ([decision
  0002](spec/decisions/0002-q1-verdict-proposal.md), proposed, held open)? That in turn needs a ratified
  margin threshold.
- **Trust in the subthreshold oscillator.** First question: is its mismatch σ(ln f) ≈ 0.27 a real spread
  or a model artefact? It is recorded as unvalidated and dominates every solve it enters.
- **Off-grid accuracy.** Rows 3 and 4 are graded on the 3×3 (V,T) grid points only. First question: what
  off-grid truth set is affordable to simulate?
- **Shuttle seat, measured silicon.** The last two rungs of the README ladder; not reached, and not
  scheduled here.

## Blocked and waiting

- **#26, 4.analog LVS** — decision needed: draw the `osc_wire` capacitors and wire resistors and close
  against the item-1 netlists, ratify a schematic change, or leave unmet. Blocks #33 (analog).
- **#31, 6.analog Monte Carlo** — decision needed on how many further draws to run for rows 2 and 3. A
  further gap: no released `klt` runs `klt yield` (2AMLogic/klayout-tools#5018).
- **#117 and #32** — wait on 2AMLogic/klayout-tools#5311 reaching a release.
- **Decisions 0002 and 0003** — proposed, not ratified.

The T1 issues listed above are the ones blocked or awaiting a decision; for what is dispatchable
right now, run the `gh issue list --label loom:issue --state open` query from `## Now` — this page
does not track the answer.

## Not planned

- An on-die reference clock, a PTAT/bandgap temperature sensor, or an ADC (README Scope; the PTAT/CTAT
  sensor is `sky130-temp-por`).
- Relaxing a ratified spec threshold to make a row pass. A failing result is recorded as the result.
