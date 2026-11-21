#!/usr/bin/env python3
"""Per-draw samples for `klt yield` (issue #31): rows 2, 3, 4 at their binding cells. Pure stdlib.
SIMULATED, schematic-level, no silicon. Post-processing only: the draws are the mismatch-MC samples
`klt sim` produced at the binding cells (sim/solve/gen_binding_mc.py); nothing is simulated here.

    yield_samples.py build freq.json mc_nominal.json mc_bind.json -o samples.json [--seed S] [--defect D] [--defect-osc OSC]

  freq.json        analyze.py extract of the #8 grid reports (the nominal surfaces / model data)
  mc_nominal.json  analyze.py extract-mc of the #8 nominal-cell MC reports (calibration read for row 4)
  mc_bind.json     analyze.py extract-mc of the binding-cell MC reports (sim/solve/mc/reports)

Conventions (grading choices made here; none relaxes the spec, no limit is edited):
  * Draw k pairs the k-th MC sample of every oscillator at the cell. Oscillators are separate simulations, so
    the pairing is arbitrary but each draw is an independent die-set. n = the smallest sample count over the
    oscillators used. A draw missing any needed oscillator reading is NOT imputed: it is reported as a null
    (counted `errored` by klt yield) so the shortfall is visible.
  * Reading noise = the MC sample itself (mismatch) plus counter quantization (analyze.sigma_quant), seeded.
    Estimator weights = per-oscillator sqrt(sigma_quant^2 + sigma_mc_cell^2), sigma_mc_cell the per-cell
    estimate analyze.mc_sigmas already computes from that cell's own samples (not the pooled value
    solve.py uses). A cell is weightable only when that estimate exists -- a zero mismatch sigma counts
    as existing -- so eligibility is the estimate's availability, never a raw slot count: a cell with
    too few usable draws is excluded up front instead of passing selection and failing the weighting
    with a None sigma (#288).
  * Row 3 (V solve, T known, corner unknown): `solve.solve_v` over `solve.VGRID` -- literally the estimator and
    grid solve.row3 grades -- with every model in-sample (the binding cell is the 1.62 V edge, which solve.py
    also treats as in-sample). Sample = V_est - V_true [V].
  * Row 4 (T solve, one-point calibration at 27 C / 1.80 V of the same die, V known): `solve.solve_t` over
    `solve.TGRID` on `solve.tmodel_delta`, the estimator, grid and model solve.row4 grades.
    The calibration read is drawn from the #8 nominal-cell MC of the same corner, independent of the measurement
    draw (a real die would correlate them; independence is conservative). Sample = T_est - T_true [C].
  * Row 2 (corner ID at known V,T, ratio space): `solve.distances`, the whitened distances solve.classify ranks;
    sample = d(nearest wrong centroid) - d(true centroid); > 0 means classified correctly.
    Limit: margin > 0 (strict). One measurement per true corner.
  * Negative control (per measurement): the same draws with a seeded defect, +DEFECT added to ln f of osc_hd.
    Expected to fail. It is a software-injected defect on the same data, not a second simulation; labelled so.
"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S  # noqa: E402

A = S.A
LIMITS = {"row3": {"min": -0.020, "max": 0.020, "target_yield": 0.99},
          "row4": {"min": -5.0, "max": 5.0, "target_yield": 0.99},
          "row2": {"min": 0.0, "exclusive_min": True, "target_yield": 0.99}}
CELLS = {"row2": (1.98, 27), "row3": ("tt", 1.62, -40), "row4": ("ff", 1.62, 27)}
DEFECT = 0.05
DEFECT_OSC = "osc_hd"   # oscillator carrying the seeded negative-control defect (--defect-osc)


def cell_samples(mc, osc, p, v, t):
    return mc["samples"].get("%s|%s|%.2f|%d" % (osc, p, v, t), [])


def _cell_sigma(per, osc, p, v, t):
    """The sensitivity analyzer's per-cell mismatch sigma (analyze.mc_sigmas `per` map); None if absent.

    analyze.mc_sigmas skips cells with fewer than three usable draws, so availability of the estimate
    -- not a raw slot count -- is what makes a cell weightable (#288). A zero sigma (no observed
    spread) is a real estimate and counts as available.
    """
    e = per.get(osc, {}).get((p, float(v), int(t)))
    return None if e is None else e[0]


def draws(tab, mc, oscs, p, v, t, rng, defect=0.0):
    """-> (list of {osc: ln f reading} or None per draw k, {osc: weight sigma}, n)."""
    sam = {o: cell_samples(mc, o, p, v, t) for o in oscs}
    n = min(len(s) for s in sam.values()) if sam else 0
    per, _ = A.mc_sigmas(mc)
    sg = {}
    for o in oscs:
        sm = _cell_sigma(per, o, p, v, t)
        sg[o] = None if sm is None else math.sqrt(A.sigma_quant(tab[(o, p, v, t)]) ** 2 + sm ** 2)
    out = []
    for k in range(n):
        if any(not sam[o][k] for o in oscs):
            out.append(None)
            continue
        rd = {}
        for o in oscs:
            f = sam[o][k]
            rd[o] = math.log(f) + rng.gauss(0, A.sigma_quant(f)) + (defect if o == DEFECT_OSC else 0.0)
        out.append(rd)
    return out, sg, n


def usable(mc, tab, p, v, t):
    per, _ = A.mc_sigmas(mc)
    return [o for o in A.OSCS if _cell_sigma(per, o, p, v, t) is not None
            and tab.get((o, p, v, t))]


def row3_samples(tab, mc, seed, defect=0.0):
    p0, v0, t0 = CELLS["row3"]
    oscs = [o for o in usable(mc, tab, p0, v0, t0)
            if all(tab.get((o, p, v, t0)) for p in A.PROCESS for v in A.VDD)]
    if len(oscs) < 2:
        return None, oscs
    full = {(o, p): S.vmodel(tab, o, p, t0, None, S.VGRID) for o in oscs for p in A.PROCESS}
    rng = random.Random("%s|y3|%s" % (seed, defect))
    ds, sg, n = draws(tab, mc, oscs, p0, v0, t0, rng, defect)
    out = []
    for rd in ds:
        if rd is None:
            out.append(None)
            continue
        out.append(round(S.solve_v(rd, full, sg, oscs, S.VGRID)[1] - v0, 6))
    return out, oscs


def row4_samples(tab, mc, mc_nom, seed, defect=0.0):
    p0, v0, t0 = CELLS["row4"]
    per_nom, _ = A.mc_sigmas(mc_nom)
    oscs = [o for o in usable(mc, tab, p0, v0, t0)
            if all(tab.get((o, "tt", v, t)) for v in A.VDD for t in A.TEMP)
            and _cell_sigma(per_nom, o, p0, 1.8, 27) is not None]
    if len(oscs) < 2:
        return None, oscs
    rng = random.Random("%s|y4|%s" % (seed, defect))
    ds, sg, n = draws(tab, mc, oscs, p0, v0, t0, rng, defect)
    cs, scal, ncal = draws(tab, mc_nom, oscs, p0, 1.8, 27, random.Random("%s|y4cal|%s" % (seed, defect)), defect)
    mod = {o: [S.tmodel_delta(tab, o, v0, tt) for tt in S.TGRID] for o in oscs}
    sd = {o: math.sqrt(sg[o] ** 2 + scal[o] ** 2) for o in oscs}
    out = []
    for k, rd in enumerate(ds):
        cal = cs[k % ncal] if ncal else None
        if rd is None or cal is None:
            out.append(None)
            continue
        d = {o: rd[o] - cal[o] for o in oscs}
        out.append(round(S.TGRID[S.solve_t(d, mod, sd, oscs, S.TGRID)] - t0, 4))
    return out, oscs


def row2_samples(tab, mc, seed, defect=0.0):
    v0, t0 = CELLS["row2"]
    per, _ = A.mc_sigmas(mc)
    oscs = [o for o in A.OSCS if all(_cell_sigma(per, o, p, v0, t0) is not None
                                    and tab.get((o, p, v0, t0))
                                    for p in A.PROCESS)]
    if A.BASELINE not in oscs or len(oscs) < 2:
        return None, oscs
    use = [o for o in oscs if o != A.BASELINE]
    cen = {p: [math.log(tab[(o, p, v0, t0)]) - math.log(tab[(A.BASELINE, p, v0, t0)]) for o in use]
           for p in A.PROCESS}
    out = {}
    for p in A.PROCESS:
        rng = random.Random("%s|y2|%s|%s" % (seed, p, defect))
        ds, sg, n = draws(tab, mc, oscs, p, v0, t0, rng, defect)
        w = [math.sqrt(sg[o] ** 2 + sg[A.BASELINE] ** 2) for o in use]
        col = []
        for rd in ds:
            if rd is None:
                col.append(None)
                continue
            x = [rd[o] - rd[A.BASELINE] for o in use]
            dist = S.distances(cen, x, w)
            wrong = min(d for q, d in dist.items() if q != p)
            col.append(round(wrong - dist[p], 6))
        out[p] = col
    return out, oscs


def build(tab, mc_nom, mc_bind, seed, defect=DEFECT):
    ms, meta = [], {}
    r2, o2 = row2_samples(tab, mc_bind, seed)
    r2b, _ = row2_samples(tab, mc_bind, seed, defect)
    meta["row2"] = {"cell": "all 5 corners @ 1.98 V / 27 C", "oscillators": o2}
    if r2:
        for p in A.PROCESS:
            ms.append({"name": "row2_margin_%s" % p, "spec_row": "2", "unit": "whitened d^2 margin",
                       "samples": r2[p], "limits": LIMITS["row2"],
                       "negative_control": {"samples": r2b[p], "description": "seeded defect: +%g on ln f of %s" % (defect, DEFECT_OSC)}})
    r3, o3 = row3_samples(tab, mc_bind, seed)
    r3b, _ = row3_samples(tab, mc_bind, seed, defect)
    meta["row3"] = {"cell": "tt @ 1.62 V / -40 C", "oscillators": o3}
    if r3:
        ms.append({"name": "row3_dV", "spec_row": "3", "unit": "V", "samples": r3, "limits": LIMITS["row3"],
                   "negative_control": {"samples": r3b, "description": "seeded defect: +%g on ln f of %s" % (defect, DEFECT_OSC)}})
    r4, o4 = row4_samples(tab, mc_bind, mc_nom, seed)
    r4b, _ = row4_samples(tab, mc_bind, mc_nom, seed, defect)
    meta["row4"] = {"cell": "ff @ 1.62 V / 27 C (cal at 1.80 V / 27 C)", "oscillators": o4}
    if r4:
        ms.append({"name": "row4_dT", "spec_row": "4", "unit": "C", "samples": r4, "limits": LIMITS["row4"],
                   "negative_control": {"samples": r4b, "description": "seeded defect: +%g on ln f of %s" % (defect, DEFECT_OSC)}})
    return {"kind": "SIMULATED", "measurements": ms,
            "provenance": {"seed": seed, "rng": "ngspice-46 mismatch MC via klt sim (fleet); python random for reading noise",
                           "corner_matrix": ["tt", "ff", "ss", "sf", "fs"]},
            "cells": meta}


def main(argv):
    a = argv[1:]
    if len(a) < 5 or a[0] != "build":
        sys.exit(__doc__)
    def opt(name, default):
        if name in a:
            i = a.index(name)
            v = a[i + 1]
            del a[i:i + 2]
            return type(default)(v) if default is not None else v
        return default
    global DEFECT_OSC
    out, seed, defect = opt("-o", None), opt("--seed", 20261105), opt("--defect", DEFECT)
    DEFECT_OSC = opt("--defect-osc", DEFECT_OSC)
    tab = A.table(json.load(open(a[1]))["rows"])
    doc = build(tab, json.load(open(a[2])), json.load(open(a[3])), seed, defect)
    if out:
        json.dump(doc, open(out, "w"), indent=1)
        open(out, "a").write("\n")
    for m in doc["measurements"]:
        print(m["name"], "n=%d" % len(m["samples"]), "nulls=%d" % sum(x is None for x in m["samples"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
