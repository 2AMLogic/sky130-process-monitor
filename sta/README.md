# Readout static timing (T1 item 5, digital)

SIMULATED / static timing only; nothing here is measured silicon.

- `readout.sta.json`: the `klt sta` request. Geometry: `layout/readout/out/readout.def`
  (routed, #24), no SPEF. Constraint: `clk_ref` at 100 ns (10 MHz, spec section 5), ideal clock.
  Corners: `ss_100C_1v60`, `tt_025C_1v80`, `ff_n40C_1v95`.
- `readout.sta.report.json`: its envelope (`klayout-tools==0.9.1`). Every corner is `constrained`;
  setup slack 95.39 / 97.89 / 98.71 ns, hold slack 0.678 / 0.331 / 0.204 ns (ss / tt / ff).
- `readout.sdc`: reference copy of the constraint; klt sta does not read it (see file header).
- `../verification/readout/functional-verification.json` + `.report.json`: 9/9 cocotb tests pass
  (Icarus 13.0, cocotb 2.1.0).

## What this does NOT cover (disclosed, not relaxed)

1. **Corner box.** The pinned hd liberty set has no 125 C file and no 1.62/1.98 V point. The three
   corners above are the nearest installed files; the spec box extremes (125 C, 1.62 V, 1.98 V)
   are not timed. Box coverage is not claimed.
2. **The oscillator-clocked counter is not timed in `readout.sta.json`** (it is timed in the corner-matched
   runs below, issue #89). Following the issue
   (SDC defines only the reference clock), the 29 `u_cnt` registers clocked by `osc[4:0]` are
   reported unclocked, and 57 endpoints (outputs, no I/O delays) unconstrained:
   `constraint_completeness.status` is `incomplete` in every corner. The `constrained` verdict
   applies to the reference-clock domain only.
3. **Exploratory result, not cited for 5.digital:** `readout.osc-probe.sta.json` declares `osc[0..4]`
   at 1.0 ns, asynchronous to `clk_ref`. The 1.0 ns figure is an assumption bounded by one local
   SIMULATED ngspice probe (`bench_osc_hd.spice`, ff model, 1.98 V, -40 C: 1.036 GHz, outside the
   liberty set; not appended to `measurements/`). Result: setup slack -4.85 / -1.79 / -0.70 ns
   (ss / tt / ff), hold >= 0.20 ns. The counter does not close at 1 GHz; the real per-corner
   oscillator frequencies (#29) decide whether that is a defect. Slack is bounding, not
   corner-matched (fastest cell frequency applied to every corner). Follow-up filed separately.

## Corner-matched oscillator STA (issue #89)

SIMULATED / static timing only. `run_osc_sta.py` writes `osc/<corner>.<oscillator>.sta.json` (15 requests) and
runs them with `klayout-tools==0.9.1`; the combined, append-only result is `readout.osc-corner.sta.report.json`.

- **Periods**: from the #29 `klt sim` frequency surfaces (`sim/sensitivity/records/reports/grid_*.json.gz`), per
  oscillator, at the grid cell nearest each liberty corner: ss_100C_1v60 -> ss/1.62 V/125 C, tt_025C_1v80 ->
  tt/1.80 V/27 C, ff_n40C_1v95 -> ff/1.98 V/-40 C. No assumed periods. None of the 7 non-oscillating cells of the
  #29 row 1 record is one of these three cells, so every period here is a measured one; a stopped oscillator
  has no clock edges to violate setup or hold, and those 7 cells are not timed.
- **One oscillator per request, shared by all five ports**: the `osc[i]` to oscillator assignment is not recorded in
  `rtl/` or `spec/`, and the counter is clocked by a mux of all five, so each request puts oscillator j's period on
  every `osc[i]` (async clock groups). Per-corner periods need separate requests (see gaps).
- **Completeness**: `complete` in all 15 runs, with scalar `input_delay_ns` / `output_delay_ns` = 10 ns (an
  assumption, 10 % of the `clk_ref` period) and the five oscillator clocks declared. The clk_ref-only reference
  record above is unchanged.

| corner | oscillator | period (ns) | setup slack (ns) | hold slack (ns) | counter fmax (MHz) |
|---|---|---|---|---|---|
| ss_100C_1v60 | osc_hd | 2.925 | **-2.921** | 0.678 | 171.1 |
| | osc_nmos | 9.075 | 3.229 | 0.678 | 171.1 |
| | osc_pmos | 22.550 | 16.704 | 0.678 | 171.1 |
| | osc_wire | 19.486 | 13.640 | 0.678 | 171.1 |
| | osc_subth | 342.467 | 77.223 | 0.678 | 171.1 |
| tt_025C_1v80 | osc_hd | 1.560 | **-1.227** | 0.331 | 358.9 |
| | osc_nmos | 4.505 | 1.718 | 0.331 | 358.9 |
| | osc_pmos | 12.600 | 9.813 | 0.331 | 358.9 |
| | osc_wire | 13.215 | 10.429 | 0.331 | 358.9 |
| | osc_subth | 351.994 | 78.580 | 0.331 | 358.9 |
| ff_n40C_1v95 | osc_hd | 0.980 | **-0.724** | 0.204 | 586.8 |
| | osc_nmos | 2.628 | 0.923 | 0.204 | 586.8 |
| | osc_pmos | 7.408 | 5.704 | 0.204 | 586.8 |
| | osc_wire | 9.027 | 7.323 | 0.204 | 586.8 |
| | osc_subth | 293.293 | 79.115 | 0.204 | 586.8 |

**Verdict: the counter does not cover `osc_hd` in any corner** (1.74x short at ff, 2.0x at ss). The other four
oscillators close everywhere. Draft decision record: `../spec/decisions/0003-counter-max-input-frequency.md`.
RTL and spec are unchanged.

Tool gaps filed at 2AMLogic/klayout-tools: #5240 (per-corner clock periods), #5241 (min-pulse-width not reported).

Not covered: clocks are ideal (no propagation through the select mux); no SPEF; oscillator frequencies are
schematic-level; liberty corners differ from the grid cells by up to 25 C / 0.03 V; spec-box extremes (125 C,
1.62/1.98 V) are not timed; `klt sta` reports no minimum-pulse-width check, so that edge case is unassessed.
