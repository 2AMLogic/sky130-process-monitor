# 2026-11-14 — sizing the osc_subth gate: counts and cold-cell margin versus gate exponent k (issue #170)

**SIMULATED. Schematic-level netlists, no layout, no parasitics. Nothing measured — there is no
silicon.** This record is pure post-processing of already-committed `klt sim` reports: no simulator
ran, no PDK was read, nothing was submitted to the batch fleet. **No estimate accuracy is quoted**
(the solve procedure has not been run against any of this); every margin below is a
corner-discrimination statistic from `analyze.margin`, not an estimate error. Append-only: no
existing record is edited, and **no spec value and no RTL default is changed by this record** —
spec §5's default gate is still 2^10.

§3 of `records/2026-11-06-mc-offnominal-cold-margin.md` found the discrimination margin at
1.98 V / −40 °C to be below 1 σ and set by counter quantisation rather than mismatch, and said
"a longer osc_subth gate is the lever; this record does not size it". This record sizes it.

Code as of `8bedae6` plus the gate parameter added for this record
(`analyze.sigma_quant`/`margin` take an optional `gate_s`; `analyze.py gate-sweep`). CPython 3.12.3.

## 1. Inputs — pinned, ordered, no glob

`analyze.table()` is a dict comprehension (`analyze.py:150`), so **later rows overwrite earlier
ones and the input order decides the frequency table**. The order below is load-bearing and is
written out in full rather than as a glob (the `#140` lesson: a report added to
`records/reports/` later would silently join any glob).

Frequency table, in this order:

```
records/reports/grid_osc_hd_5p.json.gz
records/reports/grid_osc_hd.json.gz
records/reports/grid_osc_nmos.json.gz
records/reports/grid_osc_pmos.json.gz
records/reports/grid_osc_subth.json.gz
records/reports/grid_osc_subth_sf_cold.json.gz
records/reports/grid_osc_wire.json.gz
records/reports/grid_osc_wire_sf_cold.json.gz
records/reports/probe_wire_sf_relaxed.json.gz
```

Two orderings matter, and both were checked by re-running with the order changed:

- **`grid_osc_hd_5p` must come before `grid_osc_hd`**, so the default-step `osc_hd` value wins at
  `osc_hd ff` (1.02031 GHz, not the 5 ps-step 1.0358 GHz of
  `records/2026-11-05-osc-hd-step-refined.md`). With `hd_5p` last, the ratio-only figure at the
  cold cell comes out 0.825 instead of 0.822 and no longer matches the record this one extends.
  Note this is **not** the `GRID_8` order in `sim/solve/test_records_reproduce.py`, which lists
  `hd` before `hd_5p` for a different record.
- **`probe_wire_sf_relaxed.json.gz` must be included, after both `grid_osc_wire*`.** `osc_wire sf`
  at 1.98 V / −40 °C is `MISSING` in both committed grid reports (the `timestep_too_small`
  failure), so without the probe report `analyze.margin` returns `(None, None)` at this cell and no
  margin exists to tabulate. It supplies the 84.986 MHz relaxed-options value of §1 of the
  cold-margin record, **and carries that record's bias caveat**: the relaxed options
  (`reltol=0.01 gmin=1e-10 method=gear`) shifted f by up to +0.2 % at three cells that did
  converge under default options, and three cells do not bound the bias at the sf cell itself.
  It was a single-corner debug probe run **locally** (ngspice 46), not a fleet job.

MC table (mismatch σ(ln f) at the nominal cell), in this order:

```
records/reports/mc_osc_hd.json.gz
records/reports/mc_osc_nmos.json.gz
records/reports/mc_osc_pmos.json.gz
records/reports/mc_osc_subth.json.gz
records/reports/mc_osc_wire.json.gz
```

Provenance of the inputs: all eight grid reports are batch-fleet `klt sim` jobs on **ngspice 46**;
`open_pdks c6d73a35f524070e85faff4a6a9eef49553ebc2b` for the six original grids and
`open_pdks f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` for the two `*_sf_cold` re-runs (the runner's
own stamp, as reported in `environment.remote.worker_environment.pdk`). Job ids are in each
report and in the `environment` block of the extracted table.

## 2. Reproduce

```
cd sim/sensitivity
python3 -I analyze.py extract <the nine frequency reports above, in that order> -o freq.json
python3 -I analyze.py extract-mc <the five MC reports above, in that order> -o mc.json
python3 -I analyze.py gate-sweep freq.json mc.json --vdd 1.98 --temp -40               # table 3
python3 -I analyze.py gate-sweep freq.json mc.json --vdd 1.98 --temp -40 --quant-only  # table 4
```

`--osc` defaults to `osc_subth`, `--kmin` to 10, and `--kmax` to that oscillator's own 24-bit
counter limit (20 here), so the sweep runs from the spec default gate up to the largest gate the
counter can hold for `osc_subth`.

## 3. Counts and margin versus k at 1.98 V / −40 °C (quantisation + MC)

`absU`/`ratU` are the absolute and ratio-only margins with the **whole bank** at 2^k; `absO`/`ratO`
the same with **only `osc_subth`** at 2^k and the other four at the default 2^10. `t_read` is
spec §6's **full read of all five oscillators**, not the one gate.

```
  k       gate t_read_uni t_read_osc        tt        ff        ss        sf        fs     sig_q   absU   ratU   absO   ratO  sat (uni | osc)
 10   102.4 us     512 us     512 us     31.86    349.14      0.77      0.11    579.71    2.6661  0.759  0.822  0.759  0.822  - | -
 11   204.8 us   1.024 ms   614.4 us     63.72    698.28      1.54      0.22   1159.42    1.3331  1.476  1.599  1.476  1.599  - | -
 12   409.6 us   2.048 ms   819.2 us    127.44   1396.55      3.09      0.43   2318.84    0.6665  2.194  2.068  2.194  2.068  - | -
 13   819.2 us   4.096 ms   1.229 ms    254.88   2793.11      6.18      0.87   4637.68    0.3333  2.194  2.068  2.194  2.068  - | -
 14   1.638 ms   8.192 ms   2.048 ms    509.76   5586.22     12.36      1.73   9275.36    0.1666  2.194  2.068  2.194  2.068  - | -
 15   3.277 ms   16.38 ms   3.686 ms   1019.52  11172.44     24.72      3.46  18550.72    0.0833  2.194  2.068  2.194  2.068  - | -
 16   6.554 ms   32.77 ms   6.963 ms   2039.04  22344.88     49.43      6.93  37101.44    0.0417  2.194  2.068  2.194  2.068  - | -
 17   13.11 ms   65.54 ms   13.52 ms   4078.08  44689.76     98.86     13.86  74202.88    0.0208  2.194  2.068  2.194  2.068  - | -
 18   26.21 ms   131.1 ms   26.62 ms   8156.15  89379.51    197.72     27.72 148405.75    0.0104  2.194  2.068  2.194  2.068  osc_hd | -
 19   52.43 ms   262.1 ms   52.84 ms  16312.31 178759.02    395.44     55.44 296811.51    0.0052  2.194  2.068  2.194  2.068  osc_hd,osc_nmos | -
 20   104.9 ms   524.3 ms   105.3 ms  32624.62 357518.04    790.88    110.87 593623.02    0.0026  2.194  2.068  2.194  2.068  osc_hd,osc_nmos | -
```

Pooled nominal MC σ(ln f) used above: `osc_hd` 0.00336, `osc_nmos` 0.00308, `osc_pmos` 0.00671,
`osc_wire` 0.00146, `osc_subth` 0.26613.

**The k = 10 row reproduces §3 of `2026-11-06-mc-offnominal-cold-margin.md` exactly**: absolute
**0.759**, ratio-only **0.822**, and the `osc_subth` counts 31.86 / 349.14 / 0.77 / 0.11 (tt / ff /
ss / sf) against that record's 31.9 / 349 / 0.77 / 0.11. The quantisation-only pair is in table 4.

## 4. The same sweep with the MC term dropped (quantisation only)

```
  k       gate t_read_uni t_read_osc        tt        ff        ss        sf        fs     sig_q   absU   ratU   absO   ratO  sat (uni | osc)
 10   102.4 us     512 us     512 us     31.86    349.14      0.77      0.11    579.71    2.6661  0.766  0.830  0.766  0.830  - | -
 11   204.8 us   1.024 ms   614.4 us     63.72    698.28      1.54      0.22   1159.42    1.3331  1.532  1.661  1.532  1.661  - | -
 12   409.6 us   2.048 ms   819.2 us    127.44   1396.55      3.09      0.43   2318.84    0.6665  3.065  3.322  3.065  3.322  - | -
 13   819.2 us   4.096 ms   1.229 ms    254.88   2793.11      6.18      0.87   4637.68    0.3333  6.130  6.643  6.130  6.643  - | -
 14   1.638 ms   8.192 ms   2.048 ms    509.76   5586.22     12.36      1.73   9275.36    0.1666 12.259 13.286 12.259 13.286  - | -
 15   3.277 ms   16.38 ms   3.686 ms   1019.52  11172.44     24.72      3.46  18550.72    0.0833 24.518 26.572 24.518 26.572  - | -
 16   6.554 ms   32.77 ms   6.963 ms   2039.04  22344.88     49.43      6.93  37101.44    0.0417 49.037 53.145 49.037 53.145  - | -
 17   13.11 ms   65.54 ms   13.52 ms   4078.08  44689.76     98.86     13.86  74202.88    0.0208 98.074 106.289 98.074 106.289  - | -
```

Its k = 10 row gives the other two numbers of that record's §3: quantisation-only **0.766** /
**0.830**. With MC dropped the margin simply **doubles with every k** (no plateau), which is the
mechanical statement that the gate is the quantisation lever. Rows 18–20 are omitted here only
because the uniform reading has already saturated the counter by then (§6); they are in the tool's
own output.

## 5. "Quantisation no longer sets the margin" — the definition used, and the answer

Stated before answering, because the aggregate margin and the worst cell disagree and the
aggregate one is a trap:

> Quantisation no longer sets the margin at gate exponent k when, **at the cell being judged**,
> every `osc_subth` corner reads at least one count (so `sigma_quant` is inside its validity
> range at all) **and** `sigma_quant` at the lowest-count corner is below the mismatch σ the
> margin is otherwise limited by.

Both legs are needed. `sigma_quant` is `1/(n√12)`, the σ of a **±0.5-count uniform dither**; below
about one count the counter reads 0 or 1 and that model does not describe it at all. The aggregate
margin reaches its MC-limited plateau of **2.194 / 2.068 at k = 12**, but at k = 12 and k = 13 the
sf cell still reads **0.43** and **0.87** counts — the counter reads zero there. **The k = 12–13
plateau is therefore an artefact of applying `sigma_quant` outside its validity range, not a
result.** `analyze.py` now prints this caveat itself whenever a non-default gate leaves a cell
under one count.

Every criterion that stays inside the model lands on the same k:

| criterion | threshold | smallest k |
|---|---|---|
| every `osc_subth` corner at this cell reads ≥ 1.00 count | sf cell: f = 1057.37 Hz, T_osc = 945.75 µs | **14** |
| draft decision 0003's own gate rule, `2^k · T_ref ≥ T_osc` | k ≥ 13.207 | **14** |
| `sigma_quant`(sf) < pooled nominal MC σ(`osc_subth`) | < 0.26613 (k = 13 gives 0.3333) | **14** |
| `sigma_quant`(sf) < the cold per-cell σ of §2 of the cold-margin record | < 0.1858 (k = 14 gives 0.1666) | **14** |

**Answer: k = 14** — a 1.638 ms `osc_subth` gate. At that gate the sf cell reads 1.73 counts,
`sigma_quant`(sf) = 0.1666 against an MC σ of 0.26613, and the margin is at its MC-limited
plateau: absolute **2.194**, ratio-only **2.068**, up from 0.759 / 0.822 at the default gate. The
aggregate-margin answer (k = 12) and the worst-cell answer (k = 14) are both reported here because
they differ, and **k = 12 is not sufficient**.

## 6. Which gate reading, and the 24-bit counter bound

Spec §5 gives one 24-bit saturating counter with **one oscillator selected at a time** and `k`
programmable in `CTRL`, so a longer gate need not apply to the whole bank. Both readings are
tabulated above and they are **numerically indistinguishable**: the largest relative difference
between `absU` and `absO` anywhere in the sweep is 1.3 × 10⁻⁹. The reason is visible in the σ
figures — at this cell the other four oscillators' worst `sigma_quant` is 5.3 × 10⁻⁶ … 3.7 × 10⁻⁵
at k = 10, which is 2 to 3 orders of magnitude below their mismatch σ (0.00146 … 0.00671), so
lengthening their gate removes noise that was never in the quadrature sum to begin with. **Both
readings therefore give k = 14; the choice between them is a conversion-time and RTL question,
not a margin question.**

The 24-bit bound does differ between them. Largest k whose worst-case count over **every** cell of
the 45-cell box still fits `2^24 − 1` (the fastest cell binds; `analyze.counter_limit`):

| oscillator | largest k | count at that k |
|---|---|---|
| `osc_hd` | **17** | 1.337 × 10⁷ (ff, 1.98 V, −40 °C, 1.02031 GHz) |
| `osc_nmos` | 18 | 9.976 × 10⁶ |
| `osc_pmos` | 20 | 1.498 × 10⁷ |
| `osc_wire` | 20 | 1.162 × 10⁷ |
| `osc_subth` | **20** | 1.584 × 10⁷ (151.08 MHz) |

- **Uniform gate across the bank: k ≤ 17**, set by `osc_hd`. This bound is **contingent on
  unratified draft decision 0003** (`spec/decisions/0003-counter-max-input-frequency.md`), which
  finds the counter cannot clock `osc_hd` in **any** corner and whose leading option is a ÷N
  prescaler; that would raise `osc_hd`'s limit by log₂(N) and change the gate rule. This record
  cites 0003 as a contingency and neither ratifies nor pre-empts it.
- **`osc_subth`-only: k ≤ 20**, set by `osc_subth`'s own fastest cell. This bound does not depend
  on 0003.

Either way k = 14 is comfortably inside the counter, and `analyze.py report` now flags any cell
whose count exceeds `2^24 − 1` rather than presenting a saturated count as a measurement.

## 7. Against spec §6 (conversion time)

§6 budgets a **full read of all five oscillators** — the spec does that arithmetic itself ("five
oscillators sequentially at the default gate is 5 × 102.4 µs ≈ 0.5 ms") — so the comparison is the
full-read time, not the `osc_subth` gate alone:

| reading at k = 14 | full-read time | vs §6 target < 1 ms | vs §6 fallback < 10 ms |
|---|---|---|---|
| uniform, all five at 2^14 | 5 × 2^14 / 10 MHz = **8.192 ms** | misses | **inside** |
| `osc_subth` at 2^14, other four at 2^10 | (4 × 2^10 + 2^14) / 10 MHz = **2.048 ms** | misses | **inside** |

**A gate that removes the quantisation limit at the cold cell does exist inside §6's < 10 ms
fallback, and does not exist inside the < 1 ms target.** The `osc_subth`-only reading costs 2.048
ms and is 4× cheaper than the uniform one for an identical margin — the natural reading if a later
decision wants the shortest conversion time, at the price of a per-oscillator gate in the readout
(explicitly out of scope here, and a decision record's call). Even the stretch-adjacent k = 12,
which this record rejects on the counts criterion, costs 2.048 ms uniform and so does not reach
the < 1 ms target either.

## 8. What this record does NOT say

- **It does not say the margin problem is solved.** Removing the quantisation limit hands the
  cold-cell margin to the `osc_subth` **mismatch** model, and that model is **UNVALIDATED**
  (mismatch switches in subthreshold, the open question of #10) and **biased low at exactly these
  cells**: §2 of the cold-margin record notes the cold sf/ss `osc_subth` MC samples are truncated
  at n = 6/10, and the lost draws are the slowest ones. The 2.194 / 2.068 plateau is therefore an
  **optimistic** figure resting on an unvalidated, low-biased σ. A validated σ could put the
  plateau lower, and nothing here bounds by how much.
- **It does not quote an estimate accuracy.** 2.194 is a minimum-over-corner-pairs discrimination
  margin from `analyze.margin`, in units of the noise σ along the closest pair's separation line.
  The solve procedure has not been run against any of these numbers.
- **It does not choose k.** This record sizes the gate and states what each choice costs; picking
  the value and amending spec §5's default 2^10 is a decision record, not this record.
- **It does not relax or change the spec.** §5's default gate and §6's rows are untouched; the
  tool's default gate is still 2^10 and its default output is byte-identical to before (checked by
  diff, and by `sim/solve/test_records_reproduce.py`).
- **No new simulation was run**, including the truncated cold `osc_subth` MC samples and the
  `osc_wire` sf default-solver failure — both still open from the cold-margin record.

## 9. Not done

- The other eight (V,T) cells are not swept. 1.98 V / −40 °C is the cell §3 identified as
  quantisation-limited; the hot cell (1.62 V / 125 °C) already has margin 2.57 → 3.12 at the
  default gate (`2026-11-06-mc-offnominal-complete.md`) and is not quantisation-limited.
- No layout, no parasitics, no SPEF: both this record's frequencies and decision 0003's STA are
  schematic-level and optimistic.
- Fast-oscillator step bias (#54) is not checked here; it is why `grid_osc_hd_5p` exists and why
  the input order above is pinned.
