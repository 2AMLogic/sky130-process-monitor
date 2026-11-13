#!/usr/bin/env python3
"""Rows 1-4 grading for the oscillator bank (issue #29): post-processing of the #8 frequency surfaces.
Pure stdlib. SIMULATED, schematic-level, no silicon. Does NOT re-simulate anything.

    solve.py grade freq_table.json mc_table.json [--draws N] [--seed S] [--json OUT]

Inputs are the tables written by `sim/sensitivity/analyze.py extract / extract-mc` (from #8's fleet reports).

Conventions (every one is a grading choice made here, none relaxes the spec):
  * Noise per oscillator = counter quantization (analyze.sigma_quant) + pooled mismatch-MC sigma(ln f), in
    quadrature. MC exists only at the nominal cell (1.80 V/27 C) and the pooled value is applied to every cell
    (assumption inherited from #8). osc_subth's MC is UNVALIDATED.
  * Oscillator set at a cell = those with all needed cells present; missing cells are never interpolated.
    Every result names the set used.
  * Row 1: pass iff every oscillator oscillates at all 45 cells (fallback bank: osc_hd, osc_nmos, osc_pmos).
  * Row 2: ratio space (ln f_i - ln f_osc_hd), nearest centroid at known (V,T). A cell is "identified" iff
    NO misclassification occurs in DRAWS noise draws per corner (empirical, so it is only an upper-bounded
    rate: 0 errors in 2000 draws => rate < 0.15% at 95%). The numeric margin was left to be derived by the
    spec; this zero-error-in-N criterion is this script's derivation and is stated with every verdict.
    Fallback = slow/fast separation: classifier restricted to {ss, tt, ff}, same criterion.
  * Row 3: V solved with T known, corner unknown (joint over corner and V). Per-corner model = quadratic
    through the 3 V grid points at that T. For the interior truth cell (1.80 V) the true cell is held out: its
    own corner's model uses only the other two V points (linear interpolation, other corners use all three).
    The two edge cells (1.62/1.98 V) are in-sample (flagged): holding out an edge would grade a linear
    extrapolation, which no estimator would be asked to do. Error = p99 |V_est - V_true| over noise draws,
    max over cells.
  * Row 4: T solved with one-point calibration at (27 C, 1.80 V) of the same die, V KNOWN (graded variant).
    Model = tt tensor-product quadratic of ln f(V,T) - ln f(1.8,27), corner-agnostic. The tt die itself is
    in-sample (model built from its own data) so it is noise-only; it is flagged and still counted in the max.
    A joint V+T solve is NOT implemented; the output key reports it as "not run".
  * Draws are seeded; results are deterministic.
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sensitivity"))
import analyze as A  # noqa: E402

OSCS, BASE, PROC, VDD, TEMP = A.OSCS, A.BASELINE, A.PROCESS, A.VDD, A.TEMP
FALLBACK_BANK = ["osc_hd", "osc_nmos", "osc_pmos"]
BOUNDS = {"row3_V": (0.020, 0.050, 0.010), "row4_T": (5.0, 10.0, 2.0)}  # target, fallback, stretch
# Search grids for the row 3 / row 4 estimators. One definition each: yield_samples.py searches the same
# grids, so a refinement here moves the grade and the yield samples together (they describe one procedure).
VGRID = [1.55 + 0.002 * i for i in range(251)]   # row 3 V search: 1.55..2.05 V, 2 mV step
TGRID = [-45 + 0.5 * i for i in range(351)]      # row 4 T search: -45..130 C, 0.5 C step


def lagr(xs, ys, x):
    s = 0.0
    for i, xi in enumerate(xs):
        w = 1.0
        for j, xj in enumerate(xs):
            if j != i:
                w *= (x - xj) / (xi - xj)
        s += w * ys[i]
    return s


def sigmas(tab, mc_pooled, oscs, p, v, t):
    return {o: math.sqrt(A.sigma_quant(tab[(o, p, v, t)]) ** 2 + mc_pooled[o] ** 2) for o in oscs}


# ------------------------------------------------------------------ row 1
def row1(tab):
    def ok(bank):
        miss = [(o, p, v, t) for o in bank for p in PROC for v in VDD for t in TEMP if not tab.get((o, p, v, t))]
        return {"oscillates_everywhere": not miss, "missing_cells": miss, "cells_checked": len(bank) * 45}
    allb = ok(OSCS)
    fb = ok(FALLBACK_BANK)
    # binding cell when everything oscillates = the lowest frequency (hardest for a counter gate); recorded either way
    fl = {k: f for k, f in tab.items() if f}
    kmin = min(fl, key=fl.get)
    return {"target_bank_5": allb, "fallback_bank_3": fb,
            "lowest_f_cell": {"cell": list(kmin), "f_hz": fl[kmin]},
            "verdict_target": "PASS" if allb["oscillates_everywhere"] else "FAIL",
            "verdict_fallback": "PASS" if fb["oscillates_everywhere"] else "FAIL"}


# ------------------------------------------------------------------ row 2
def distances(centroids, x, w):
    """Whitened squared distance from feature vector x to each centroid; w = per-coordinate noise std."""
    return {p: sum(((a - b) / s) ** 2 for a, b, s in zip(x, c, w)) for p, c in centroids.items()}


def classify(centroids, x, w):
    """Nearest centroid in the whitened space; ties go to the first centroid in iteration order."""
    d = distances(centroids, x, w)
    return min(d, key=d.get)


def row2_cell(tab, mc, v, t, rng, draws, classes, ratio=True):
    oscs = [o for o in OSCS if all(tab.get((o, p, v, t)) for p in PROC)]
    if BASE not in oscs or len(oscs) < 2:
        return {"gradable": False, "oscillators": oscs}
    if any(o not in mc for o in oscs):
        return {"gradable": False, "oscillators": oscs, "why": "no MC sigma"}
    use = [o for o in oscs if (not ratio or o != BASE)]
    def feat(vals):
        return [vals[o] - (vals[BASE] if ratio else 0.0) for o in use]
    ln = {p: {o: math.log(tab[(o, p, v, t)]) for o in oscs} for p in classes}
    cen = {p: feat(ln[p]) for p in classes}
    errs, conf = 0, {}
    for p in classes:
        sg = sigmas(tab, mc, oscs, p, v, t)
        # feature noise std per use-coordinate (ratio coordinates share osc_hd noise: sample at osc level)
        for _ in range(draws):
            noisy = {o: ln[p][o] + rng.gauss(0, sg[o]) for o in oscs}
            # whitening: weight by the nominal per-coordinate noise (ratio var = var_o + var_base)
            w = [math.sqrt(sg[o] ** 2 + (sg[BASE] ** 2 if ratio else 0.0)) for o in use]
            got = classify(cen, feat(noisy), w)
            if got != p:
                errs += 1
                conf[p + "->" + got] = conf.get(p + "->" + got, 0) + 1
    return {"gradable": True, "oscillators": oscs, "draws_per_corner": draws, "errors": errs,
            "identified": errs == 0, "confusions": conf}


def row2(tab, mc, draws, seed, ratio=True):
    out = {}
    for fam, classes in (("target_5_corner", PROC), ("fallback_slow_fast", ["ss", "tt", "ff"])):
        cells = {}
        for v in VDD:
            for t in TEMP:
                rng = random.Random("%s|%s|%s|%s|%s" % (seed, fam, v, t, ratio))
                cells["%.2f|%d" % (v, t)] = row2_cell(tab, mc, v, t, rng, draws, classes, ratio)
        g = [c for c in cells.values() if c["gradable"]]
        out[fam] = {"cells": cells, "gradable_cells": len(g), "total_cells": 9,
                    "identified_cells": sum(1 for c in g if c["identified"]),
                    "verdict": "PASS" if len(g) == 9 and all(c["identified"] for c in g) else "FAIL"}
    return out


# ------------------------------------------------------------------ row 3
def vmodel(tab, o, p, t, skip_v, vgrid):
    pts = [(v, math.log(tab[(o, p, v, t)])) for v in VDD if v != skip_v]
    return [lagr([a for a, _ in pts], [b for _, b in pts], v) for v in vgrid]


def solve_v(meas, models, sg, oscs, vgrid):
    """Joint search over (corner, V): the row 3 estimator.

    models[(osc, corner)] = ln f over vgrid; sg[osc] = reading noise std. Returns (residual, V, corner)
    for the lowest weighted squared residual, ties going to the first (corner, grid point) visited.
    The caller chooses the models, which is where the row 3 hold-out rule lives.
    """
    best = None
    for p in PROC:
        for i, v in enumerate(vgrid):
            r = sum(((meas[o] - models[(o, p)][i]) / sg[o]) ** 2 for o in oscs)
            if best is None or r < best[0]:
                best = (r, v, p)
    return best


def row3(tab, mc, draws, seed):
    res, worst = {}, None
    for t in TEMP:
        oscs = [o for o in OSCS if all(tab.get((o, p, v, t)) for p in PROC for v in VDD) and o in mc]
        if len(oscs) < 2:
            res["%d" % t] = {"gradable": False, "oscillators": oscs}
            continue
        full = {(o, p): vmodel(tab, o, p, t, None, VGRID) for o in oscs for p in PROC}
        for p0 in PROC:
            for v0 in VDD:
                rng = random.Random("%s|r3|%s|%s|%s" % (seed, t, p0, v0))
                held = {o: vmodel(tab, o, p0, t, v0 if v0 == 1.8 else None, VGRID) for o in oscs}
                sg = sigmas(tab, mc, oscs, p0, v0, t)
                # hold-out rule: the TRUE corner's model drops the truth cell (interior cells only);
                # every other corner stays in-sample. yield_samples passes `full` for all corners.
                models = {(o, p): (held[o] if p == p0 else full[(o, p)]) for o in oscs for p in PROC}
                truth = {o: math.log(tab[(o, p0, v0, t)]) for o in oscs}
                sys_err = solve_v(truth, models, sg, oscs, VGRID)[1] - v0
                es = sorted(abs(solve_v({o: truth[o] + rng.gauss(0, sg[o]) for o in oscs},
                                        models, sg, oscs, VGRID)[1] - v0) for _ in range(draws))
                p99 = es[min(len(es) - 1, int(0.99 * len(es)))]
                res["%d|%s|%.2f" % (t, p0, v0)] = {"oscillators": oscs, "in_sample": v0 != 1.8, "systematic_err_v": sys_err, "p99_abs_err_v": p99}
                if worst is None or p99 > worst[0]:
                    worst = (p99, "%d C %s %.2f V" % (t, p0, v0))
    return {"cells": res, "worst_p99_abs_err_v": worst[0] if worst else None, "binding_cell": worst[1] if worst else None,
            "cells_graded": len(res), "cells_total": 45}


# ------------------------------------------------------------------ row 4
def tmodel_delta(tab, o, v, t):
    """tt ln f(v,t) - ln f(1.8,27) by tensor-product quadratic Lagrange."""
    def l(vv, tt_):
        rows = [lagr(TEMP, [math.log(tab[(o, "tt", vi, ti)]) for ti in TEMP], tt_) for vi in VDD]
        return lagr(VDD, rows, vv)
    return l(v, t) - l(1.8, 27)


def solve_t(d, mod, sd, oscs, tgrid):
    """Search over T: the row 4 estimator. d[osc] = calibrated ln f delta, mod[osc] = model over tgrid,
    sd[osc] = combined measurement+calibration noise std. Returns the index of the best tgrid point."""
    return min(range(len(tgrid)), key=lambda i: sum(((d[o] - mod[o][i]) / sd[o]) ** 2 for o in oscs))


def row4(tab, mc, draws, seed):
    oscs = [o for o in OSCS if all(tab.get((o, "tt", v, t)) for v in VDD for t in TEMP) and o in mc]
    other = [o for o in OSCS if o not in oscs]
    res, worst = {}, None
    if len(oscs) < 2:
        return {"gradable": False, "oscillators": oscs}
    for p0 in PROC:
        if not all(tab.get((o, p0, v, t)) for o in oscs for v in VDD for t in TEMP):
            res[p0] = {"gradable": False}
            continue
        for v0 in VDD:
            for t0 in TEMP:
                rng = random.Random("%s|r4|%s|%s|%s" % (seed, p0, v0, t0))
                sg = sigmas(tab, mc, oscs, p0, v0, t0)
                scal = sigmas(tab, mc, oscs, p0, 1.8, 27)
                sd = {o: math.sqrt(sg[o] ** 2 + scal[o] ** 2) for o in oscs}
                mod = {o: [tmodel_delta(tab, o, v0, tt_) for tt_ in TGRID] for o in oscs}
                truth = {o: math.log(tab[(o, p0, v0, t0)]) - math.log(tab[(o, p0, 1.8, 27)]) for o in oscs}
                se = TGRID[solve_t(truth, mod, sd, oscs, TGRID)] - t0
                es = sorted(abs(TGRID[solve_t({o: truth[o] + rng.gauss(0, sd[o]) for o in oscs},
                                              mod, sd, oscs, TGRID)] - t0) for _ in range(draws))
                p99 = es[min(len(es) - 1, int(0.99 * len(es)))]
                res["%s|%.2f|%d" % (p0, v0, t0)] = {"systematic_err_c": se, "p99_abs_err_c": p99, "in_sample": p0 == "tt"}
                if worst is None or p99 > worst[0]:
                    worst = (p99, "%s %.2f V %d C" % (p0, v0, t0))
    return {"gradable": True, "oscillators": oscs, "oscillators_excluded": other, "cells": res,
            "worst_p99_abs_err_c": worst[0] if worst else None, "binding_cell": worst[1] if worst else None,
            "cells_graded": len(res), "cells_total": 45, "joint_VT_variant": "not run"}


def grade_vs(err, key):
    t, f, s = BOUNDS[key]
    if err is None:
        return {"target": "NOT GRADED", "fallback": "NOT GRADED", "stretch": "NOT GRADED"}
    return {"target": "PASS" if err <= t else "FAIL", "fallback": "PASS" if err <= f else "FAIL",
            "stretch": "PASS" if err <= s else "FAIL"}


def main(argv):
    if len(argv) < 4 or argv[1] != "grade":
        sys.exit(__doc__)
    a = argv[2:]
    def opt(name, default):
        if name in a:
            i = a.index(name)
            v = a[i + 1]
            del a[i:i + 2]
            return v if default is None else type(default)(v)
        return default
    draws, seed, out = opt("--draws", 2000), opt("--seed", 20261105), opt("--json", None)
    tab = A.table(json.load(open(a[0]))["rows"])
    _, pooled = A.mc_sigmas(json.load(open(a[1])))
    mc = {o: s for o, s in pooled.items()}
    r = {"kind": "SIMULATED", "draws": draws, "seed": seed, "mc_pooled_sigma_lnf": mc,
         "row1": row1(tab), "row2_ratio": row2(tab, mc, draws, seed, True),
         "row3": row3(tab, mc, max(100, draws // 10), seed), "row4": row4(tab, mc, max(100, draws // 10), seed)}
    r["row3"]["grade"] = grade_vs(r["row3"]["worst_p99_abs_err_v"], "row3_V")
    r["row4"]["grade"] = grade_vs(r["row4"].get("worst_p99_abs_err_c"), "row4_T")
    if out:
        json.dump(r, open(out, "w"), indent=1, sort_keys=True, default=str)
    print("row1 target:", r["row1"]["verdict_target"], " fallback:", r["row1"]["verdict_fallback"],
          " missing:", len(r["row1"]["target_bank_5"]["missing_cells"]))
    for fam, d in r["row2_ratio"].items():
        print("row2", fam, d["verdict"], "identified %d/%d gradable %d" % (d["identified_cells"], 9, d["gradable_cells"]))
    print("row3 worst p99 |dV| =", r["row3"]["worst_p99_abs_err_v"], "at", r["row3"]["binding_cell"], r["row3"]["grade"])
    print("row4 worst p99 |dT| =", r["row4"].get("worst_p99_abs_err_c"), "at", r["row4"].get("binding_cell"), r["row4"]["grade"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
