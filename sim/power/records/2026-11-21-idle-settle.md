# 2026-11-21 — row 7 idle power re-bench: the nine suspect op cells settled; gated-divider candidate; hot-leakage attribution (issue #279)

**SIMULATED. Oscillator bank only: COUNTER POWER IS NOT COVERED (no SPICE-level counter netlist).** Schematic-level, no layout.
ngspice-47, sky130A, via `klt sim --batch-set` on the batch fleet (runner open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`,
job ids in the table's `environment` block). Supersedes the idle half of `2026-11-05-power-complete.md` (kept; records are
append-only; its active half is carried forward verbatim, see below). Tables: `2026-11-21-power-table.json`,
`2026-11-21-power-grade.json`.

## Coverage and method
- Idle: 45/45 cells, all five oscillators present at every cell. `osc_hd`, `osc_pmos`, `osc_subth` re-run unchanged (op).
  `osc_nmos` and `osc_wire` move to **transient-settle benches** (`tb/idle_osc_<osc>_settle.spice`): `en` held at vss for a
  transient from t=0, `i(Vdd)` averaged over the
  final half-window (1 us window for osc_nmos, 5 us for osc_wire; adjacent-quarter agreement in every cell, and the two
  windows were cross-checked against 5x longer local runs at the slowest and hottest cells). rshunt=1e12 is kept (below).
  **The graded settle decks are plain `tran` from the DC operating point, not from an all-zero start** (no `uic`, no
  `.ic`; `gen_requests.py settle_request`): the DC solve initialises them, so they do not by themselves establish a zero
  start. The defined zero-start runs (`uic`, every ring node 0 V) are the `xcheck_settle_*_zero` rows in section 1.
- Active: **carried verbatim** from `2026-11-05-power-table-complete.json` (`analyze_power.py extract ... --carry-active`);
  the active benches are unchanged and were not re-simulated. 219/225 cells as before.

## 1. The nine suspect cells: all `op` artifacts (bench defect, not an enable-scheme defect)

Every flagged 2026-11-05 cell moves to nA-scale leakage under the settle bench, by 3-6 orders of magnitude. Exactly these
nine cells move >10x; **no other cell in either 45-cell grid moves >10x** (the hot fast cells agree with the old op to
four significant figures — they were real leakage all along).

| Oscillator | Cell | 2026-11-05 `op` | settle (graded) | zero start (`uic`, all nodes 0 V) | norshunt xcheck | `.ic` 1.8 V xcheck | op / settle ratio |
|---|---|---|---|---|---|---|---|
| osc_nmos | sf / 1.62 V / 27 C | 301.8 uA | 0.356 nA | 0.391 nA | 0.349 nA | 0.391 nA | 847 000x |
| osc_nmos | ff / 1.62 V / -40 C | 11.22 uA | 1.98 nA | 2.006 nA | 1.69 nA | 1.97 nA | 5 679x |
| osc_nmos | ff / 1.80 V / -40 C | 8.13 uA | 3.17 nA | 3.195 nA | 2.84 nA | 3.14 nA | 2 567x |
| osc_nmos | sf / 1.98 V / -40 C | 2.99 uA | 0.811 nA | 0.482 nA | 0.455 nA | 0.563 nA | 3 689x |
| osc_nmos | sf / 1.80 V / -40 C | 1.11 uA | 0.717 nA | 0.422 nA | 0.390 nA | 0.541 nA | 1 542x |
| osc_wire | ss / 1.98 V / -40 C | 69.66 uA | 0.879 nA | 0.537 nA | 0.490 nA | 0.874 nA | 79 227x |
| osc_wire | ss / 1.80 V / -40 C | 43.89 uA | 0.784 nA | 0.477 nA | FAIL (timestep) | 0.757 nA | 55 995x |
| osc_wire | ss / 1.62 V / -40 C | 18.79 uA | 0.701 nA | 0.432 nA | FAIL (timestep) | 0.602 nA | 26 790x |
| osc_wire | sf / 1.80 V / -40 C | 17.77 uA | 0.782 nA | 0.463 nA | 0.422 nA | 0.651 nA | 22 739x |

Cross-checks (`requests/xcheck_settle_*.json`, fleet-run; reports in `records/reports/`): the **norshunt** variants drop
`.options rshunt` — they agree with the settle bench at the nA scale everywhere they converge, and fail with
`timestep too small` on the two ss/-40 osc_wire cells. The **`.ic`** variants start every ring node at 1.8 V (a
deliberately wrong defined state). The **zero-start** runs (added in the PR #295 review follow-up,
`xcheck_settle_osc_{nmos,wire}_zero`: `tran ... uic`, every ring node `.ic` 0 V, so no DC solve is involved) pass in all
nine cells. Reading the columns: every start (op-derived settle, 1.8 V `.ic`, 0 V `uic`, no shunt) lands at nA-scale
leakage, 3-6 orders of magnitude below the op values, so the high-current op points are not the settled state from any
start tried. They do **not** agree to digits in the cold sf/ss cells: there the zero-start current is 0.42-0.54 nA against
0.72-0.88 nA for the graded settle bench (1.2-1.7x lower; ff and the 27 C cell agree within 4%). The graded settle values
are therefore the upper of the defined-start results in those cells, and the spread is of the order of the rshunt floor
(~0.3-0.4 nA at 1e12 ohm), not a different state. None of these cells binds any verdict (the binding cell is the 125 C
uA-scale fs/1.98 V cell).

**rshunt sensitivity at the two ss/-40 C osc_wire cells** (the cells whose no-shunt run failed to converge;
`xcheck_settle_osc_wire_shunt13` / `_shunt14` change only the shunt resistance, same settle bench):

| Cell | rshunt 1e12 (graded) | 1e13 | 1e14 | no shunt |
|---|---|---|---|---|
| ss / 1.62 V / -40 C | 0.701 nA | 0.417 nA | 0.388 nA | FAIL (timestep) |
| ss / 1.80 V / -40 C | 0.784 nA | 0.468 nA | FAIL (error) | FAIL (timestep) |

Both cells converge at 1e13 (0.42 and 0.47 nA); 1.62 V also at 1e14 (0.39 nA); 1.80 V at 1e14 errors. The current falls as
the shunt is raised and approaches the zero-start values (0.432 / 0.477 nA), so ~0.3 nA of the graded value in these
cold cells is the rshunt=1e12 term, i.e. the graded settle figure overstates the shunt-free leakage by up to ~1.7x there.
A converged no-shunt result was not obtained at either cell; the statement that rshunt is "negligible" holds only for the
uA-scale hot cells and is disclosed, not removed, at the nA-scale cold ones.

Mechanism: the op solve on the gated-off ring is suspect. ngspice `op` prints `Warning: Dynamic gmin stepping failed` on
the 2026-11-05 deck and recovers via true gmin stepping to a high-current point. Reproduced here as single-unit local runs
(`requests/probe_op_osc_nmos_sf162_{a,b}.json`, reports in `records/reports/`): at sf/1.62 V/27 C the op-form deck gives
**301.8 uA** with both the i(Vdd)-only measurement set (a) and an i(Vdd)+node-voltage set (b), with that warning and a
logic-consistent state (v(out)=v(n0)=1.62 V, v(n1)=8 nV). **The earlier statement that a different measurement set flips
this cell to 0.36 nA was not reproduced** with these two sets and is withdrawn; what is established is that the op value
is 3 orders above the value reached by every transient start, not why ngspice lands on it (non-uniqueness of the DC
solution is the working explanation, not shown here). The transient from the defined initial states tried (0 V `uic`,
all-1.8 V `.ic`, op-derived) reaches nA-scale leakage in every cell, so the high-current `op` points are **not shown to be
stable states of the gated-off ring** — no enable-scheme defect follows from them (the real hot-cell leakage below is a
different mechanism, in the 30 un-gated stages). The bench change that fixes it is the settle bench itself; the op-form
idle decks stay committed (pinned history) but no longer feed a graded table.

## 2. `en`-gated `osc_subth` bias divider — candidate only (issue #279)

`cand/osc_subth_gated.spice` is the design netlist with exactly one edit: the divider return `Rb1` goes to vss through
en-gated nfet `XMsw1` (W=1.0/L=0.15; on-resistance ~1-2 kOhm against the 1.8 MOhm string). `design/osc_bank/` is
untouched. Idle grid `requests/gated_subth_idle.json` (op + rshunt=1e12 — with the divider cut, vbp has no DC path),
**45/45 cells, committed per cell** in `2026-11-23-cand-idle.json` (the grid re-run in the PR #295 review follow-up;
raw report `records/reports/gated_subth_idle.json.gz`), with the ungated `osc_subth` current at each cell taken from
`2026-11-21-power-table.json` and the reduction derived per cell (`analyze_power.py cand-idle`). The op is
tran-cross-checked on **15 cells** (`requests/gated_subth_idle_tran_xcheck.json`: nominal, plus each of the five corners at
1.62 V/-40 C, 1.80 V/27 C and 1.98 V/125 C, with tt/1.80/27 counted once; report
`records/reports/gated_subth_idle_tran_xcheck.json.gz`): the transient settle agrees with the op to better than 1e-4
relative in every one of the 15 cells.

All numbers below are currents in the units shown (the ungated column is the `osc_subth` idle current, not power):

| | ungated (2026-11-21 table) | gated candidate | reduction |
|---|---|---|---|
| tt / 1.80 V / 27 C | 1.0044 uA | 0.478 nA | ~2 100x |
| ss / 1.62 V / -40 C (lowest gated) | 0.900 uA (900 nA) | 0.234 nA | ~3 850x |
| fs / 1.98 V / 125 C (hottest, highest gated) | 5.034 uA | 643 nA (0.643 uA) | ~7.8x |

Across the 45 cells the gated current spans 0.234 nA (ss/1.62/-40) to 643 nA (fs/1.98/125); the reduction spans 6x
(fs/1.62/125) to 3 846x (ss/1.62/-40) (the earlier versions of this table gave "~4x" and "~7800x" for the two extreme
rows; both were unit slips and are corrected here). The reduction is at least 39x in every cell; by group: fs at 125 C 6-8x, ff at 125 C 10-14x, fs at 27 C 39-51x,
tt at 125 C 51-62x, and 170x or more in the remaining 27 cells (ff at 27 C is 171-201x).

**Non-divider term.** With the divider cut, the gated current is everything else. Bound on the switch itself
(isolated-device probe `requests/probe_off_devices.json`, W=1.0/L=0.15 nfet at Vgs=0, Vds=1.98 V): **4.3 pA at fs/125 C,
295 pA at ff/125 C, 8.5 pA at ss/125 C, 2.0 pA at fs/-40 C** — orders of magnitude below the gated cell currents wherever
the gated current binds (643 nA at fs/125), so the switch is not the residual. The residual is the rest of the
`osc_subth` leakage at hot fast corners. The earlier explanation of its mechanism (vbp floating to vdd, vh_k collapsing,
the stage pfets shutting) was not measured and is **not asserted** here; the device bounds above show only that
the stage pfet (W=0.84/L=0.15, 1.46 uA isolated at fs/125 C, Vgs=0) and the lvt pfet (187 nA isolated) *could* carry that
current if they conducted in the gated circuit, which this record does not establish.

Side effects, A/B on the same 16 cells (`requests/active_osc_subth_cells.json` vs `requests/gated_subth_active_cells.json`,
behavioural enable ramping at 1 ns; both re-run in the review follow-up with an identical measurement set; derived in
`2026-11-23-cand-ab.json` by `analyze_power.py cand-ab`; reports `records/reports/{active_osc_subth_cells,gated_subth_active_cells}.json.gz`).
Frequency and start-up come from output-edge timestamps, not from edge counts (the request caps the crossing list at
400, so the counts at 400/400 say nothing about agreement):
- **vbp (settled, mean over 1-2 ms)**: the gated bench sits 0.07-0.11 mV above the ungated one in every cell
  (tt/1.80/27: 1.5000 V ungated, 1.5001 V gated; design tap 1.5000 V). The earlier "0.8-1.7 mV" was an order-of-magnitude slip.
- **frequency**, `freq_from_crossings` on each variant's timestamps (the nine-edge rule): **11 of the 16 cells resolve in
  both variants; 5 cells (sf at all three V, ss at 1.62 and 1.80 V, all at -40 C) are MISSING in both** (0-6 edges) and are
  not compared. Of the 11 resolved pairs the gated/ungated frequency ratio is within 1% in 6 (tt/1.80/27 0.9932, tt/1.80/-40
  0.9909, tt/1.62/-40 0.9946, ss/1.98/-40 0.9927, ff/1.80/-40 0.9912, ff/1.98/-40 0.9974) and **outside 1% in 5**:
  ff/1.62/-40 0.9882 (1.2% low), fs/1.62/-40 1.081, fs/1.80/-40 0.9455, fs/1.98/-40 1.069 and tt/1.98/-40 1.047 (the
  fs and tt/1.98 cells differ by 5-8%). The earlier "identical within 1% wherever both resolve" is therefore **not supported** and is
  withdrawn; the candidate's frequency equivalence is established only at the six cells above, and not at the fs and
  tt/1.98 cold cells, where the difference is not explained here (a 400-edge mean in a ring that starts up differently
  in each variant is the first suspect, not tested).
- **start-up after en rises**, measured as two separate things. *Bias settling*: the first sampled time at which vbp is
  within 1% of its settled mean is **2 ns for the ungated bench** (its vbp is held by the DC divider from t=0, so this
  is not a start-up measurement) and **10 ns for the gated one** in all 16 cells (samples at 2/5/10/20/50/100 ns/1 us).
  vbp overshoots rather than creeping in: the gated vbp is ~0.19 V above its final value at 2 ns (tt/1.80/27: 1.690 V
  against 1.5001 V), 30-40 mV above at 5 ns and 1-6 mV above at 10 ns. *First output edge after enable*: the first rising
  crossing of v(out)/2 comes 0.13 us to 130 us after the enable midpoint in the 11 resolved cells (tt/1.80/27: 494 ns
  ungated, 413 ns gated; fs/1.98/-40: 131 ns / 174 ns; tt/1.62/-40: 17.9 us / 16.1 us; ss/1.98/-40: 130 us) and 0.3-1.9
  ms in the four slow sf/ss cells that show 2-6 edges (sf/1.62/-40 shows none). Bias settling (<=10 ns) is therefore at
  least ~13x faster than the first output edge in every cell that has one (closest: fs/1.98/-40, 10 ns against 131 / 174 ns),
  so the first edge is set by the ring, not the divider; whether the first edge itself is
  identical between variants was not tested (the two differ by tens of percent in several cells).
- **Mean supply current when enabled** (`i_avg`, second half of the window): within 1% at 12 of 16 cells; the gated
  bench is lower by 17% at fs/1.62/-40 (1.45 -> 1.20 uA), 9% at fs/1.80/-40 (2.00 -> 1.82), 16% at sf/1.98/-40 (2.64 ->
  2.23, a cell that does not resolve in either variant) and 2.6% at tt/1.98/-40 — recorded, not interpreted; this issue does not adopt the variant.

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

(`osc_subth` here is the **ungated** divider design, as ratified; its 9.97 uW at fs/1.98/125 (5.034 uA) is ~2.2 uW of divider
plus ~7.8 uW of other leakage — section 2's candidate cuts the divider and measures 643 nA = 1.27 uW remaining there.)

Dominant devices. Isolated-device probes (`requests/probe_off_devices.json`, deck `tb/probe_off_devices.spice`, one
single-device instance per geometry at Vgs=0, |Vds|=1.98 V; fleet run, report `records/reports/probe_off_devices.json.gz`;
regenerated by `gen_requests.py`) give the OFF current per device:

| Device (geometry) | fs / 125 C | ff / 125 C | ss / 125 C | fs / -40 C |
|---|---|---|---|---|
| pfet, osc_wire stage (W=8.0/L=0.15) | 2.38 uA | 1.01 uA | 19.5 nA | 1.61 nA |
| pfet, osc_nmos stage (W=3.0/L=0.15) | 1.56 uA | 552 nA | 5.36 nA | 1.55 nA |
| pfet, osc_subth stage (W=0.84/L=0.15) | 1.46 uA | 631 nA | 2.62 nA | 5.46 nA |
| pfet lvt, osc_subth (W=0.42/L=0.5) | 187 nA | 79.5 nA | 1.0 nA | 0.459 nA |
| nfet, ring stage (W=4.0/L=0.15) | 117 pA | 2.07 nA | 192 pA | 2.0 pA |
| nfet, enable stack (W=0.84/L=0.5) | 7.7 pA | 29 pA | 9.8 pA | 2.0 pA |
| nfet (W=0.42/L=0.5) | 3.2 pA | 37 pA | 3.7 pA | 2.0 pA |
| nfet, candidate switch (W=1.0/L=0.15) | 4.3 pA | 295 pA | 8.5 pA | 2.0 pA |

In the settled gated-off state every ring sits in a forced logic state, so on alternate stages the OFF device is the
pull-up pfet. The probe closes against the measured cell currents: **osc_wire** 15 stage pfets x 2.38 uA = 35.7 uA against
the measured 35.67 uA (fs/1.98/125; 70.63 uW / 1.98 V), and ff 15 x 1.01 = 15.2 uA against 15.19 uA; **osc_nmos** 15 x 1.56 =
23.4 uA against 22.72 uA (fs), and 15 x 0.552 = 8.3 uA against 8.24 uA (ff). The nfet-side OFF devices are two to four orders
below (pA to low nA; the ff/125 W=4/L=0.15 nfet at 2 nA is the largest and still <0.03% of the osc_wire cell current).
(The 2.0 pA at -40 C in the last column is identical for every nfet and equals gmin 1e-12 S x 1.98 V, so it is
the solver's floor, not a device leakage figure; those cells are an upper bound only.) **Next design iteration** (input to the follow-up issue, not a change here): the
gated-off idle at hot corners is min-channel-length pfet subthreshold leakage in the 30 un-gated stages — lengthen the OFF
pull-up devices (L 0.15 -> >=0.5; the L=0.5 lvt pfet leaks 187 nA against 1.46 uA for the L=0.15 pfet of similar
width class) or stack/gate the pull-ups per stage; gating the divider (section 2) removes the divider share. No spec bound
is touched by this attribution.

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

Everything below is a `klt sim` request or a single-corner local run; nothing is hand-edited. Raw reports are committed
gzipped in `records/reports/`; derived JSON files are named by the command that wrote them.

    python3 -I sim/power/gen_requests.py     # writes every deck and request named in this record (idempotent)
    klt sim --batch-set sim/power/requests/{idle_osc_hd,idle_osc_pmos,idle_osc_subth,idle_osc_nmos_settle,idle_osc_wire_settle,gated_subth_idle,gated_subth_idle_tran_xcheck,gated_subth_active_cells,active_osc_subth_cells,xcheck_settle_osc_nmos_norshunt,xcheck_settle_osc_nmos_ic,xcheck_settle_osc_nmos_zero,xcheck_settle_osc_wire_norshunt,xcheck_settle_osc_wire_ic,xcheck_settle_osc_wire_zero,xcheck_settle_osc_wire_shunt13,xcheck_settle_osc_wire_shunt14,probe_off_devices}.json --wait-for-capacity 600 -o <dir>
    python3 -I sim/power/analyze_power.py extract <dir>/idle_osc_hd/report.json <dir>/idle_osc_pmos/report.json <dir>/idle_osc_subth/report.json <dir>/idle_osc_nmos_settle/report.json <dir>/idle_osc_wire_settle/report.json --carry-active sim/power/records/2026-11-05-power-table-complete.json -o sim/power/records/2026-11-21-power-table.json
    python3 -I sim/power/analyze_power.py grade sim/power/records/2026-11-21-power-table.json --json sim/power/records/2026-11-21-power-grade.json
    python3 -I sim/power/analyze_power.py cand-idle <dir>/gated_subth_idle/report.json sim/power/records/2026-11-21-power-table.json -o sim/power/records/2026-11-23-cand-idle.json
    python3 -I sim/power/analyze_power.py cand-ab <dir>/active_osc_subth_cells/report.json <dir>/gated_subth_active_cells/report.json -o sim/power/records/2026-11-23-cand-ab.json
    # op-solve probe (single unit, stays local; two measurement sets on the identical op-form deck):
    klt sim sim/power/requests/probe_op_osc_nmos_sf162_a.json --backend local -o <dir>/probe_a
    klt sim sim/power/requests/probe_op_osc_nmos_sf162_b.json --backend local -o <dir>/probe_b

Note on the `extract` line: it is given only the five graded reports. A cross-check or candidate report passed to it is
recorded as environment and yields no row (`analyze_power.classify_bench`; regression-tested in
`test_analyze_power.py`), so it can never displace a graded cell.

The 2026-11-21 idle-half reports (`idle_osc_*`, the first nine cross-check cells) and the 2026-11-23 reports were fleet
runs of the requests above; the 2026-11-21 table was graded from the first set and is unchanged by the 2026-11-23 re-runs
(which add the zero-start, shunt, probe and candidate data and re-run the candidate grid and A/B). `xcheck_settle_osc_wire_norshunt`
reports `error` by design on its two ss/-40 C units (`timestep too small`); `xcheck_settle_osc_wire_shunt14` errors on
ss/1.80 V/-40 C. Every figure on this page is SIMULATED, schematic-level, with its corner and bench named.
