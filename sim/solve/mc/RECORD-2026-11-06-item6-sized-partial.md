# 2026-11-06 (sized campaign, partial) — T1 item 6: first n=50 chunk of the sized osc_subth binding-cell MC (issue #31)

**SIMULATED. Schematic-level netlists (sky130A open_pdks, ngspice-46 on the batch fleet), no layout or parasitics, nothing measured.** Append-only; `RECORD-2026-11-06-item6-full-bank.md` is not edited. No spec bound or limit is changed.

## What this adds
- `sim/solve/gen_binding_mc.py --sized` emits one request per (oscillator, binding cell, chunk) into `sim/solve/mc/requests-sized/` (140 requests: 5 oscillators x 7 cells x 4 chunks of n = 50, `mismatch_scale=1`, per-chunk seed `20261106 + 1000*chunk`, so chunks are independent and pool by concatenation). Only the requests are committed; they are not all run.
- One chunk was run through `klt sim --batch-set` (batch backend only, no local ngspice): `mc_sized_osc_subth_ff_1.62V_27C_c0` (row 4 binding cell), n = 50, 50/50 passed, 0 errored; fleet job `klt-sim-834df7092b79`, 610 s on one spot m7i.4xlarge. Report: `reports-sized/mc_sized_osc_subth_ff_1.62V_27C_c0.json.gz`.

## Not done (shortfall, stated, not imputed)
- A second chunk (osc_subth, ff @ 1.98 V / 27 C, c0, job `klt-sim-8c48c7a4123c`) was still `running` when the session's bounded wait ended; it is **not collected and not counted**.
- Sample-size verdict is **unchanged: `insufficient`** for rows 2, 3, 4 (needs n >= 183 / 6147 / 183). Largest completed n at the row-4 binding cell for osc_subth is 50 (+ the earlier 10 from a different seed scheme, not pooled here). `klt yield` was **not re-run**, the `6.analog` hash and signoff record are **not changed**, and the negative control is **not redone**.
- Cost basis: ~10 min per 50-draw osc_subth chunk. n >= 183 across the 6 row-2/4 cells for osc_subth alone is 24 such jobs; row 3 at n >= 6147 for all five oscillators is on the order of 120+ chunks per oscillator. That is an operator cost decision (per the issue's rev. 2026-11-06 step 5); pooling sigma across cells was rejected there and is not done.
