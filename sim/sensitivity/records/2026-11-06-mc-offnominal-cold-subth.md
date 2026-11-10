# 2026-11-06 — off-nominal mismatch Monte Carlo, osc_subth at 1.98 V / -40 C (issue #48)

**SIMULATED. Schematic-level netlist `osc/tb_osc_subth.spice`, no layout/parasitics. Nothing measured. No estimate accuracy is quoted** (the solve procedure has not been run). Append-only: no existing record is edited, including `2026-11-06-mc-offnominal-complete.md` (which is partial despite its name). No spec change. The osc_subth mismatch model is still UNVALIDATED.

## 1. What ran
Request `requests/mc_offnom_osc_subth_1.98V_-40C.json` (unchanged: 5 process corners x n=10 mismatch samples, 1.98 V, -40 C, `tran 10n 2m`), submitted once with
`klt sim <request> --backend batch --resume --wait-for-capacity 600 --max-units-per-job 5` (client klt 0.9.2.dev29, runner klt 0.9.0). Backend `batch`; no local ngspice. Ten shards of 5 units each; all ten finished `done` on spot instances, **no interruption or reclaim this time** (the two earlier 75-unit shards were reclaimed at ~421 s and ~950 s; the 5-unit shards ran 65-396 s). Whether the smaller shard size is what helped is not established by one run.

Fleet job ids (all `done`, exit 0): klt-sim-731a3be6d2a2, klt-sim-dd8a7fd29f96, klt-sim-eaebacd75643, klt-sim-80bea66e559d, klt-sim-ea8373959e86, klt-sim-af80227fff56, klt-sim-79e3aae41470, klt-sim-d67e11e8404b, klt-sim-6d987e0da355, klt-sim-158cda6e77f1.
Merged report: `records/reports/mc_offnom_osc_subth_1.98V_-40C.json.gz` (50/50 units pass in klt's verdict; 15 units carry a `nonconvergence` warning).

## 2. Collected samples and sigma(ln f) (simulated, 1.98 V / -40 C)
A sample counts as a frequency only if `analyze.freq_from_crossings` finds one (skip 3 edges, then at least 5 cycles). The 2 ms window is too short for slow samples; those are counted **missing, not filled**.

| corner | samples run | usable f | edges seen (usable samples) | sigma(ln f) |
|---|---|---|---|---|
| ff | 10 | 10 | 400 (cap) | 0.1673 |
| fs | 10 | 10 | 400 (cap) | 0.1719 |
| tt | 10 | 10 | 400 (cap) | 0.2156 |
| ss | 10 | **6** (f = 4.8-7.8 kHz) | 9-15; 4 samples had 4-8 edges, below the cycle minimum | 0.1848 (n=6, truncated) |
| sf | 10 | **0** | 1-3 edges each (< 2.5 kHz) | **none** |

n=10 gives about 22 % sampling error on a sigma; the ss value comes from 6 samples of a truncated population (the slowest draws are exactly the ones lost), so it is biased low and not comparable to the others. Pooled RMS over the four corners with a sigma: 0.186 (the hot cell's five-corner pooled figure is 0.220, nominal pooled 0.266). That pool omits sf and is not a five-corner figure.

## 3. Cold-cell margin: NOT computed
The issue allows a cold-cell margin only if the osc_subth sigma is collected. It is not, for two independent reasons, checked with `analyze.py` (`extract`, `extract-mc`, `report`):
1. **sf has no sigma**: all ten sf samples are missing (window too short). A margin with one process corner lacking its noise term is a different quantity.
2. **The nominal grid cell is itself missing**: `analyze.py report` lists `MISSING osc_subth sf 1.98 V -40 C` and `MISSING osc_wire sf 1.98 V -40 C` from the 2026-11-05 grid (existing evidence, not edited), so `margin` returns n/a for both the absolute and ratio-only forms at this cell regardless of the MC. The sf centroid cannot be formed even before noise is added.

So there is no per-(V,T) margin for 1.98 V/-40 C, and no change versus the nominal-sigma-everywhere figure to list. The hot-cell result in `2026-11-06-mc-offnominal-complete.md` was re-derived here with the same code and reproduces it (absolute 2.57 -> 3.12, ratio-only 1.62 -> 1.96, nominal pooled sigma vs per-cell sigma at 1.62 V/125 C).

## 4. What it would take (not done; out of scope here)
Closing the cold cell needs a longer osc_subth transient window for the sf corner (the window, not the mismatch, is what drops the samples), plus grid cells for osc_subth sf and osc_wire sf at 1.98 V/-40 C (the wire `timestep too small` failures at this cell are not investigated; see the previous record). Each is a new fleet request and a new record; the spec is untouched.

## 5. Status of issue #48
Collected: osc_hd, osc_pmos, osc_nmos, osc_wire off-nominal MC (earlier records); osc_subth 1.62 V/125 C and, here, osc_subth 1.98 V/-40 C for ff/fs/tt (n=10) and ss (6/10). Not collected: osc_subth sf at 1.98 V/-40 C; cold-cell margin. The issue stays open (`Part of #48`).
