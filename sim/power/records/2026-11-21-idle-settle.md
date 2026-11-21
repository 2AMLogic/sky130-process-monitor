# 2026-11-21 — row 7 idle power re-bench: the nine suspect op cells settled; gated-divider candidate; hot-leakage attribution (issue #279)

**SIMULATED. Oscillator bank only: COUNTER POWER IS NOT COVERED (no SPICE-level counter netlist).** Schematic-level, no layout.
ngspice-47, sky130A, via `klt sim --batch-set` on the batch fleet (runner open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`,
job ids in the table's `environment` block). Supersedes the idle half of `2026-11-05-power-complete.md` (kept; records are
append-only; its active half is carried forward verbatim, see below). Tables: `2026-11-21-power-table.json`,
`2026-11-21-power-grade.json`.

## Coverage and method
- Idle: 45/45 cells, all five oscillators present at every cell. `osc_hd`, `osc_pmos`, `osc_subth` re-run unchanged (op).
  `osc_nmos` and `osc_wire` move to **transient-settle benches** (`tb/idle_osc_<osc>_settle.spice`): `en` held at vss for a
  transient from t=0 (caps at 0 — the ring is powered up gated off, a fully defined initial state), `i(Vdd)` averaged over the
  final half-window (1 us window for osc_nmos, 5 us for osc_wire; adjacent-quarter agreement in every cell, and the two
  windows were cross-checked against 5x longer local runs at the slowest and hottest cells). rshunt=1e12 is kept (below).
- Active: **carried verbatim** from `2026-11-05-power-table-complete.json` (`analyze_power.py extract ... --carry-active`);
  the active benches are unchanged and were not re-simulated. 219/225 cells as before.

## 1. The nine suspect cells: all `op` artifacts (bench defect, not an enable-scheme defect)

Every flagged 2026-11-05 cell moves to nA-scale leakage under the settle bench, by 3-6 orders of magnitude. Exactly these
nine cells move >10x; **no other cell in either 45-cell grid moves >10x** (the hot fast cells agree with the old op to
four significant figures — they were real leakage all along).

| Oscillator | Cell | 2026-11-05 `op` | settle | norshunt xcheck | `.ic` xcheck | artifact ratio |
|---|---|---|---|---|---|---|
| osc_nmos | sf / 1.62 V / 27 C | 301.8 uA | 0.356 nA | 0.349 nA | 0.391 nA | 847 000x |
| osc_nmos | ff / 1.62 V / -40 C | 11.22 uA | 1.98 nA | 1.69 nA | 1.97 nA | 5 679x |
| osc_nmos | ff / 1.80 V / -40 C | 8.13 uA | 3.17 nA | 2.84 nA | 3.14 nA | 2 567x |
| osc_nmos | sf / 1.98 V / -40 C | 2.99 uA | 0.811 nA | 0.455 nA | 0.563 nA | 3 689x |
| osc_nmos | sf / 1.80 V / -40 C | 1.11 uA | 0.717 nA | 0.390 nA | 0.541 nA | 1 542x |
| osc_wire | ss / 1.98 V / -40 C | 69.66 uA | 0.879 nA | 0.490 nA | 0.874 nA | 79 227x |
| osc_wire | ss / 1.80 V / -40 C | 43.89 uA | 0.784 nA | FAIL (timestep) | 0.757 nA | 55 995x |
| osc_wire | ss / 1.62 V / -40 C | 18.79 uA | 0.701 nA | FAIL (timestep) | 0.602 nA | 26 790x |
| osc_wire | sf / 1.80 V / -40 C | 17.77 uA | 0.782 nA | 0.422 nA | 0.651 nA | 22 739x |

Cross-checks (`requests/xcheck_settle_*.json`, fleet-run): the **norshunt** variants drop `.options rshunt` — they agree
with the settle bench at the nA scale everywhere they converge, and fail with `timestep too small` on the two ss/-40
osc_wire cells (the failure rshunt was added to cure in 2026-11-05; that is robustness, not physics). The **`.ic`**
variants start every ring node at 1.8 V — a deliberately wrong defined state — and settle to the same currents. The
**rshunt floor**: at the nA scale of the -40 C cells rshunt=1e12 contributes ~0.3-0.4 nA (visible in the norshunt
column); it is six orders below the uA-scale hot cells that bind the verdict and is disclosed rather than removed.

Mechanism (local single-unit probes, decks reproduced verbatim in this record's reproduce section): the gated-off ring's
DC problem is **non-unique**. ngspice `op` prints `Warning: Dynamic gmin stepping failed` on these decks and then accepts
a solution on a solver-path-dependent branch: re-running the identical deck with a different measurement set flips the
same cell (sf/1.62/27 osc_nmos) between 301.8 uA and 0.36 nA, and the accepted "solution" can show a consistent logic
state with a current that violates KCL at its own node voltages. The transient from any defined initial state (zero-IC,
all-1.8 V `.ic`) reaches the same unique nA leakage state in every cell, so the high-current `op` points are **not real
stable states of the gated-off ring** — no enable-scheme defect follows from them (the real hot-cell leakage below is a
different mechanism, in the 30 un-gated stages). The bench change that fixes it is the settle bench itself; the op-form
idle decks stay committed (pinned history) but no longer feed a graded table.

## 2. `en`-gated `osc_subth` bias divider — candidate only (issue #279)

`cand/osc_subth_gated.spice` is the design netlist with exactly one edit: the divider return `Rb1` goes to vss through
en-gated nfet `XMsw1` (W=1.0/L=0.15; on-resistance ~1-2 kOhm against the 1.8 MOhm string). `design/osc_bank/` is
untouched. Idle grid `requests/gated_subth_idle.json` (op + rshunt=1e12 — with the divider cut, vbp has no DC path),
45/45 cells; the op is tran-cross-checked (`requests/gated_subth_idle_tran_xcheck.json`, 16 cells: nominal, and each
corner at 1.62 V/-40 C, 1.80 V/27 C, 1.98 V/125 C) and **agrees with the transient settle to four digits in every
sampled cell** — no artifact cell found in this bench.

| | ungated (2026-11-21 op re-run) | gated candidate | divider cut |
|---|---|---|---|
| tt / 1.80 V / 27 C | 1.0044 uA | 0.478 nA | ~2100x |
| ss / 1.62 V / -40 C (coldest) | 0.900 nA | 0.234 nA | ~4x (already divider-dominated) |
| fs / 1.98 V / 125 C (hottest) | 5.034 uA | 0.643 nA | ~7800x |

Residual (non-divider) term: per-cell values are the gated grid itself (min 0.234 nA, ss/1.62/-40; max 643 nA,
fs/1.98/125; nominal 0.478 nA). The ungated-vs-gated hot-cell gap is not just the ~1.1 uA divider: ungated, vbp = 5/6 x
vdd holds the lvt pfets and the stage pfet sources (vh_k) high, so the stage pfets (W=0.84/L=0.15) leak; gated, vbp
floats to vdd, the lvt pfets turn off, vh_k collapse and that path shuts too (isolated-device probes: stage pfet
W=0.84/L=0.15 at Vgs=0, Vsd=1.98, 125 C: 1.46 uA fs / n.a. ff; lvt pfet W=0.42/L=0.5: 187 nA fs, 79 nA ff — with vh_k
collapsed these do not conduct).

Side effects, A/B on the same 16 cells (`requests/active_osc_subth_cells.json` vs `requests/gated_subth_active_cells.json`,
behavioural enable ramping at 1 ns):
- **vbp**: 1.5001 V at tt/1.80/27 (design tap: 1.5000 V; the switch adds ~0.8-1.7 mV, corner-dependent, i.e. vbp sits
  `vdd*(Rb1+Ron)/(Rb0+Rb1+Ron)`-side of the tap by design). Same +~1 mV shift at every cold cell (1.3501/1.5001/1.6501 V).
- **frequency**: rising-crossing counts identical within 1% wherever both rings resolve (tt/1.80/27: 400 vs 400 over the
  2 ms window; tt/1.62/-40: 102 vs 103). The sf and ss -40 C cells remain below the #8 gradability rule in both variants
  (2-15 crossings) — the same cells the sensitivity surface could not resolve, unchanged by the edit.
- **start-up after en rises**: vbp is within mV of its final value 10 ns after the ramp (vbp@10n column; small ~1-2 mV
  overshoot gone by 100 ns), and the ring oscillates in every cell that resolves at all. The divider charges through
  ~250 kOhm Thevenin against the fF-scale vbp capacitance: sub-10 ns by construction, confirmed by measurement.
- Mean supply current when enabled: within ~3% at every resolvable cell except fs/1.62/-40 (1.45 -> 1.20 uA, ~-17%, same
  400-crossing count; recorded, not interpreted — this issue does not adopt the variant).

Downstream re-runs adoption would invalidate (listed, not run): the `osc_subth` rows 1-4 surface rows and their
`sim/solve/` regrade, the `osc_subth` mismatch Monte Carlo (`sim/solve/mc/`), `osc_subth` layout, the analog LVS decision
(#26, operator-held), and the extracted-`osc_subth` pex path (#117, #32, blocked upstream).

## 3. Hot-cell idle breakdown and the next design iteration

Per-oscillator idle power (uW) at 125 C from the settle/grid table:

| Cell | osc_wire | osc_nmos | osc_subth | osc_hd | osc_pmos | bank sum |
|---|---|---|---|---|---|---|
| fs / 1.62 V | 28.58 | 19.02 | 5.37 | 0.149 | 0.004 | 53.13 |
| fs / 1.80 V | 45.09 | 29.42 | 7.39 | 0.205 | 0.005 | 82.10 |
| fs / 1.98 V | **70.63** | **44.99** | 9.97 | 0.278 | 0.006 | **125.87** |
| ff / 1.62 V | 13.15 | 7.37 | 3.54 | 0.049 | 0.023 | 24.14 |
| ff / 1.80 V | 19.97 | 11.01 | 4.84 | 0.067 | 0.029 | 35.93 |
| ff / 1.98 V | 30.08 | 16.31 | 6.53 | 0.091 | 0.037 | 53.04 |

(`osc_subth` here is the **ungated** divider design, as ratified; its 9.97 uA at fs/1.98/125 is ~2.2 uW of divider plus
~7.8 uW of stage leakage — section 2's candidate would cut both.)

Dominant devices (isolated-device probes at Vgs=0, |Vds|=1.98 V, 125 C, same geometry as the ring): in the settled
gated-off state every ring sits in a forced logic state, so on alternate stages the OFF device is the pull-up pfet and it
carries essentially the whole cell current. **osc_wire**: 15 stages' pfets at W=8.0/L=0.15 leak 2.38 uA each (fs) /
1.01 uA (ff) -> 15 x 2.38 = 35.7 uA against the measured 35.67 uA (fs/1.98/125); ff closes the same way (15 x 1.01 =
15.2 vs 15.19 uA). **osc_nmos**: the W=3.0/L=0.15 stage pfets leak 1.56 uA (fs) / 0.55 uA (ff) each -> 15 x 1.56 =
23.3 uA against 22.72 uA measured (the remainder is the stage-0 enable stack's W=0.84/L=0.5 nfet at ~20 pA and junction
terms); ff: 15 x 0.55 = 8.3 vs 8.24 uA. The nfet-side OFF devices (W=4/L=0.15: 162 pA; W=0.42/L=0.5: 11 pA) and the
-40 C regime (pfet 3.9 pA) are orders below. **Next design iteration** (input to the follow-up issue, not a change
here): the gated-off idle at hot corners is min-channel-length pfet subthreshold leakage in the 30 un-gated stages —
lengthen the OFF pull-up devices (L 0.15 -> >=0.5, roughly the osc_nmos nfet's 11 pA/class) or stack/gate the pull-ups
per stage; gating the divider (section 2) removes the osc_subth share. No spec bound is touched by this attribution.

## 4. Verdicts (no bound edited; rows and cells all present)

| | Target | Fallback | Stretch | Binding cell |
|---|---|---|---|---|
| Active (oscillator only; carried) | < 100 uW FAIL | < 500 uW FAIL | < 20 uW FAIL | osc_wire ff / 1.98 V / -40 C = 1740 uW (219/225 cells) |
| Idle (bank sum) | < 1 uW FAIL | < 10 uW FAIL | < 100 nW FAIL | fs / 1.98 V / 125 C = **125.87 uW** (45/45 cells, no suspect point) |

The graded idle figure is no longer a suspect `op` artifact: it is the physical leakage of the gated-off bank, set by the
min-L pfet OFF current of the un-gated `osc_wire` and `osc_nmos` stages at 125 C (section 3), monotonically rising in V
and T. The remaining gap to the fallback bound is that leakage plus `osc_subth`'s ungated divider; both attributions are
recorded above with their candidate fixes (un-adopted).

## Reproduce

    python3 -I sim/power/gen_requests.py     # writes the settle/xcheck/gated decks and requests
    klt sim --batch-set sim/power/requests/{idle_osc_hd,idle_osc_pmos,idle_osc_subth,idle_osc_nmos_settle,idle_osc_wire_settle,gated_subth_idle,gated_subth_idle_tran_xcheck,gated_subth_active_cells,active_osc_subth_cells,xcheck_settle_osc_nmos_norshunt,xcheck_settle_osc_nmos_ic,xcheck_settle_osc_wire_norshunt,xcheck_settle_osc_wire_ic}.json --wait-for-capacity 600 -o <dir>
    python3 -I sim/power/analyze_power.py extract <dir>/idle_osc_hd/report.json <dir>/idle_osc_pmos/report.json <dir>/idle_osc_subth/report.json <dir>/idle_osc_nmos_settle/report.json <dir>/idle_osc_wire_settle/report.json --carry-active sim/power/records/2026-11-05-power-table-complete.json -o sim/power/records/2026-11-21-power-table.json
    python3 -I sim/power/analyze_power.py grade sim/power/records/2026-11-21-power-table.json --json sim/power/records/2026-11-21-power-grade.json

`xcheck_settle_osc_wire_norshunt` reports `error` by design on its two ss/-40 C units (`timestep too small`, the failure
rshunt exists to cure); its passing units are the cross-check evidence. The op-path-dependence probe (same deck, two
measurement sets, 301.8 uA vs 0.36 nA) is the local single-unit run of `requests/idle_osc_nmos.json`-shaped op probes
recorded above; the isolated-device probes are single-device decks at Vgs=0/|Vds|=vdd with the ring geometries, run
locally as single corners. Every figure on this page is SIMULATED, schematic-level, with its corner and bench named.
