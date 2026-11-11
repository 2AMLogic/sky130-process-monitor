#!/usr/bin/env python3
"""Sensitivity matrix, conditioning and discrimination margin for the oscillator bank (issue #8).

Pure standard library (no numpy on the fleet workers; a one-sided Jacobi SVD is accurate for the
5x4 matrices used here). Everything printed is SIMULATED, schematic-level, no silicon.

    analyze.py extract REPORT.json[.gz]... -o freq_table.json   # klt sim grid reports -> frequency table
    analyze.py extract-mc REPORT.json[.gz]... -o mc_table.json  # klt sim MC reports   -> per-cell samples
    analyze.py report freq_table.json [mc_table.json] [--without osc_a,osc_b]   # matrices, SVD, kappa, margin

Conventions (stated again in every report):
  * f_osc comes from the rising-edge crossing times of v(out) at VDD/2: the first SKIP_EDGES edges
    (start-up) are dropped, f = (n-1)/(t_last - t_first) over the rest, and at least MIN_CYCLES
    cycles are required, otherwise the cell is MISSING (never interpolated, never imputed).
  * Process coordinates (Pn, Pp) in {-1,0,+1}: tt=(0,0) ff=(+1,+1) ss=(-1,-1); and from the recorded
    sf/fs probe (record 2026-11-05): sf = NMOS fast / PMOS slow = (+1,-1), fs = (-1,+1).
  * Columns are scaled by the box half-range so singular values are comparable:
      V: d ln f/dV * 0.18 V    T: d ln f/dT * 82.5 C    Pn, Pp: d ln f/dP * 1 (corner extent)
    V and T derivatives are finite differences of the tt surface across the box (central at the
    middle point, one-sided at the edges); P derivatives are corner contrasts at that (V,T):
      dPn = (ff + sf - ss - fs)/4,  dPp = (ff + fs - ss - sf)/4   (of ln f).
"""
import gzip
import json
import math
import sys

OSCS = ["osc_hd", "osc_nmos", "osc_pmos", "osc_wire", "osc_subth"]
BASELINE = "osc_hd"
PROCESS = ["tt", "ff", "ss", "sf", "fs"]
VDD = [1.62, 1.80, 1.98]
TEMP = [-40, 27, 125]
PCOORD = {"tt": (0, 0), "ff": (1, 1), "ss": (-1, -1), "sf": (1, -1), "fs": (-1, 1)}
V_HALF = 0.18
T_HALF = 82.5
SKIP_EDGES = 3
MIN_CYCLES = 5
GATE_S = 1024 / 10e6          # spec default: 2^10 reference cycles at 10 MHz
COLS = ["V", "T", "Pn", "Pp"]


# ---------------------------------------------------------------- frequency extraction

def freq_from_crossings(times, skip=SKIP_EDGES, min_cycles=MIN_CYCLES):
    """Mean frequency from rising-edge times, or None if the ring did not run long enough."""
    t = list(times)[skip:]
    if len(t) < min_cycles + 1:
        return None
    return (len(t) - 1) / (t[-1] - t[0])


def _load(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt") as f:
        return json.load(f)


def _osc_of(report):
    path = report["netlist"]["path"]
    for o in OSCS:
        if o in path:
            return o
    raise ValueError("cannot tell oscillator from netlist %r" % path)


def _remote(report):
    """The report's `environment.remote` block ({} for a local run) and the runner PDK stamp inside it."""
    rem = (report.get("environment") or {}).get("remote") or {}
    return rem, ((rem.get("worker_environment") or {}).get("pdk") or {}).get("stamp_text")


def _env(report):
    e = report.get("environment", {})
    rem, runner_pdk = _remote(report)
    wk = rem.get("worker_environment") or {}
    return {"engine_version": e.get("engine_version"), "job_id": rem.get("job_id"),
            "runner_pdk": runner_pdk,
            "runner_ngspice": ((wk.get("simulator") or {}).get("version_banner") or "").split("\n")[1:2]}


def extract(paths):
    rows, envs = [], []
    for p in paths:
        rep = _load(p)
        osc = _osc_of(rep)
        envs.append(dict(_env(rep), oscillator=osc, report=p))
        for c in rep["corners"]:
            m = c["measurements"][0]
            times = (m.get("crossings") or {}).get("times") or []
            rows.append({"osc": osc, "process": c["process"], "vdd": c["supply_v"]["vdd"],
                         "temp_c": c["temperature_c"], "n_edges": len(times),
                         "f_hz": freq_from_crossings(times), "unit_status": c["status"]})
    return {"kind": "SIMULATED", "rows": rows, "environment": envs}


def extract_mc(paths):
    samples = {}
    envs = []
    for p in paths:
        rep = _load(p)
        osc = _osc_of(rep)
        envs.append(dict(_env(rep), oscillator=osc, report=p))
        for c in rep["corners"]:
            m = c["measurements"][0]
            f = freq_from_crossings((m.get("crossings") or {}).get("times") or [])
            key = "%s|%s|%.2f|%d" % (osc, c["process"], c["supply_v"]["vdd"], c["temperature_c"])
            samples.setdefault(key, []).append(f)
    return {"kind": "SIMULATED", "samples": samples, "environment": envs}


# ---------------------------------------------------------------- linear algebra (stdlib)

def svd_values(a, sweeps=60, eps=1e-15):
    """Singular values (descending) of a list-of-rows matrix, one-sided Jacobi (Hestenes)."""
    m, n = len(a), len(a[0])
    cols = [[a[i][j] for i in range(m)] for j in range(n)]
    for _ in range(sweeps):
        rotated = False
        for p in range(n - 1):
            for q in range(p + 1, n):
                alpha = sum(x * x for x in cols[p])
                beta = sum(x * x for x in cols[q])
                gamma = sum(x * y for x, y in zip(cols[p], cols[q]))
                if abs(gamma) <= eps * math.sqrt(alpha * beta) or gamma == 0.0:
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = math.copysign(1.0, zeta) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                cols[p], cols[q] = ([c * x - s * y for x, y in zip(cols[p], cols[q])],
                                    [s * x + c * y for x, y in zip(cols[p], cols[q])])
        if not rotated:
            break
    return sorted((math.sqrt(sum(x * x for x in col)) for col in cols), reverse=True)


def conditioning(a, rank_tol=1e-3):
    """(singular values, condition number, numerical rank at rank_tol * s_max)."""
    sv = svd_values(a)
    rank = sum(1 for s in sv if s > rank_tol * sv[0])
    kappa = sv[0] / sv[-1] if sv[-1] > 1e-12 * sv[0] else float("inf")   # rank-deficient -> inf
    return sv, kappa, rank


# ---------------------------------------------------------------- sensitivity matrix

def table(rows):
    """{(osc, process, vdd, temp): f_hz or None}"""
    return {(r["osc"], r["process"], round(r["vdd"], 2), r["temp_c"]): r["f_hz"] for r in rows}


def lnf(tab, osc, proc, v, t):
    f = tab.get((osc, proc, v, t))
    return math.log(f) if f else None


def _fd(vals, xs, i):
    """Derivative of vals(xs) at index i: central inside, one-sided at the ends."""
    if i == 0:
        a, b = 0, 1
    elif i == len(xs) - 1:
        a, b = i - 1, i
    else:
        a, b = i - 1, i + 1
    if vals[a] is None or vals[b] is None:
        return None
    return (vals[b] - vals[a]) / (xs[b] - xs[a])


def sensitivity_row(tab, osc, iv, it):
    """Scaled [dV, dT, dPn, dPp] of ln f_osc at box cell (VDD[iv], TEMP[it]); None if any input missing."""
    v, t = VDD[iv], TEMP[it]
    dv = _fd([lnf(tab, osc, "tt", vv, t) for vv in VDD], VDD, iv)
    dt = _fd([lnf(tab, osc, "tt", v, tt) for tt in TEMP], TEMP, it)
    g = {p: lnf(tab, osc, p, v, t) for p in PROCESS}
    if dv is None or dt is None or any(x is None for x in g.values()):
        return None
    dpn = (g["ff"] + g["sf"] - g["ss"] - g["fs"]) / 4.0
    dpp = (g["ff"] + g["fs"] - g["ss"] - g["sf"]) / 4.0
    return [dv * V_HALF, dt * T_HALF, dpn, dpp]


def matrices(tab, iv, it):
    """(absolute 5x4 | None, ratio-only 4x4 | None, list of missing oscillators)."""
    rows, miss = {}, []
    for o in OSCS:
        r = sensitivity_row(tab, o, iv, it)
        if r is None:
            miss.append(o)
        rows[o] = r
    absm = [rows[o] for o in OSCS] if not miss else None
    # ratio form: ln f_i - ln f_baseline; derivative of a difference is the difference of derivatives
    if rows[BASELINE] is None or any(rows[o] is None for o in OSCS if o != BASELINE):
        ratio = None
    else:
        ratio = [[x - y for x, y in zip(rows[o], rows[BASELINE])] for o in OSCS if o != BASELINE]
    return absm, ratio, miss


# ---------------------------------------------------------------- noise and margin

def sigma_quant(f_hz):
    """sigma of ln f from counter quantization: uniform +-0.5 count over a gate of GATE_S."""
    n = f_hz * GATE_S
    return 1.0 / (n * math.sqrt(12.0))


def mc_sigmas(mc):
    """Per-oscillator sigma(ln f): {osc: {(process, v, t): sigma}} and pooled-RMS {osc: sigma}."""
    per, pooled = {}, {}
    for key, vals in mc["samples"].items():
        osc, proc, v, t = key.split("|")
        xs = [math.log(x) for x in vals if x]
        if len(xs) < 3:
            continue
        mu = sum(xs) / len(xs)
        var = sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)
        per.setdefault(osc, {})[(proc, float(v), int(t))] = (math.sqrt(var), len(xs), len(vals))
    for osc, d in per.items():
        pooled[osc] = math.sqrt(sum(s * s for s, _, _ in d.values()) / len(d))
    return per, pooled


def margin(tab, iv, it, sigma_mc, ratio=False):
    """Minimum over corner pairs of |centroid difference| / noise sigma along their separation line.

    Feature vector: ln f_i (absolute) or ln f_i - ln f_baseline (ratio-only). Noise per oscillator:
    quantization (at that corner's f) and MC mismatch spread, independent, in quadrature. Returns
    (margin, (corner_a, corner_b)) or (None, None) if any needed cell, or any oscillator's MC sigma, is
    missing. sigma_mc=None means quantization only.
    """
    v, t = VDD[iv], TEMP[it]
    if sigma_mc is not None and any(o not in sigma_mc for o in OSCS):
        return None, None   # an oscillator without MC data is NOT assumed noiseless
    oscs = [o for o in OSCS if (not ratio or o != BASELINE)]
    feat, var_abs = {}, {}
    for p in PROCESS:
        l = {o: lnf(tab, o, p, v, t) for o in OSCS}
        if any(x is None for x in l.values()):
            return None, None
        feat[p] = [l[o] - (l[BASELINE] if ratio else 0.0) for o in oscs]
        var_abs[p] = {o: sigma_quant(tab[(o, p, v, t)]) ** 2 + (sigma_mc[o] if sigma_mc else 0.0) ** 2 for o in OSCS}
    best, pair = None, None
    for i, a in enumerate(PROCESS):
        for b in PROCESS[i + 1:]:
            d = [x - y for x, y in zip(feat[a], feat[b])]
            norm = math.sqrt(sum(x * x for x in d))
            if norm == 0:
                return 0.0, (a, b)
            u = [x / norm for x in d]
            # noise variance of u . feature: feature_k = ln f_k (- ln f_base); independent per osc
            vr = 0.0
            for p in (a, b):
                coef = {o: 0.0 for o in OSCS}
                for k, o in enumerate(oscs):
                    coef[o] += u[k]
                    if ratio:
                        coef[BASELINE] -= u[k]
                vr += sum(coef[o] ** 2 * var_abs[p][o] for o in OSCS)
            m = norm / math.sqrt(vr)
            if best is None or m < best:
                best, pair = m, (a, b)
    return best, pair


# ---------------------------------------------------------------- report

def fmt_matrix(m, rowlabels):
    out = ["%-10s" % "" + "".join("%12s" % c for c in COLS)]
    for lab, r in zip(rowlabels, m):
        out.append("%-10s" % lab + "".join("%12.5f" % x for x in r))
    return "\n".join(out)


def report(freq, mc=None, out=sys.stdout):
    tab = table(freq["rows"])
    P = lambda *a: print(*a, file=out)
    P("# Sensitivity report (SIMULATED, schematic-level, tt/ff/ss/sf/fs x 3 V x 3 T; nothing measured)")
    P("# columns scaled by box half-range: V*0.18, T*82.5, Pn/Pp = corner extent (+-1)")
    missing = [(r["osc"], r["process"], r["vdd"], r["temp_c"]) for r in freq["rows"] if not r["f_hz"]]
    P("# cells: %d, missing (no/short oscillation): %d" % (len(freq["rows"]), len(missing)))
    for m in missing:
        P("#   MISSING", m)
    sig_per, sig_pool = ({}, {}) if mc is None else mc_sigmas(mc)
    if mc is not None:
        P("\n## MC mismatch sigma(ln f) (pooled RMS over corner x (V,T) cells; per-cell n shown in the table)")
        for o in OSCS:
            P("%-10s pooled sigma(ln f) = %s" % (o, "%.5f" % sig_pool[o] if o in sig_pool else "n/a"))
            for k, (s, n, nn) in sorted(sig_per.get(o, {}).items()):
                P("    %-3s %.2f V %4d C  sigma=%.5f  n=%d/%d" % (k[0], k[1], k[2], s, n, nn))
        if "osc_subth" in sig_pool:
            P("NOTE: osc_subth MC is UNVALIDATED (mismatch switches in subthreshold: question for #10).")
    res = {}
    for iv, v in enumerate(VDD):
        for it, t in enumerate(TEMP):
            absm, ratio, miss = matrices(tab, iv, it)
            P("\n## cell V=%.2f T=%d" % (v, t))
            if miss:
                P("missing oscillators here: %s -> absolute matrix not formed" % miss)
            if absm:
                sv, k, rk = conditioning(absm)
                P("absolute ln f (5x4):\n" + fmt_matrix(absm, OSCS))
                P("  singular values: %s\n  kappa=%.3g  rank=%d/4" % (" ".join("%.4g" % s for s in sv), k, rk))
                res[(v, t, "abs")] = (sv, k, rk)
            if ratio:
                sv, k, rk = conditioning(ratio)
                P("ratio-only ln f_i - ln f_hd (4x4):\n" + fmt_matrix(ratio, [o for o in OSCS if o != BASELINE]))
                P("  singular values: %s\n  kappa=%.3g  rank=%d/4" % (" ".join("%.4g" % s for s in sv), k, rk))
                res[(v, t, "ratio")] = (sv, k, rk)
    nvt = len(VDD) * len(TEMP)
    P("\n## formed (V,T) cells: absolute %d of %d, ratio-only %d of %d" % (
        sum(1 for k in res if k[2] == "abs"), nvt, sum(1 for k in res if k[2] == "ratio"), nvt))
    if mc is not None:
        P("\n## Discrimination margin (min over corner pairs, in sigma of the noise along the pair line)")
        P("noise = counter quantization (2^10 ref cycles @10 MHz) + pooled MC mismatch sigma, quadrature")
        worst = {}
        for form, ratio_flag in (("absolute", False), ("ratio-only", True)):
            for iv, v in enumerate(VDD):
                for it, t in enumerate(TEMP):
                    m, pair = margin(tab, iv, it, sig_pool, ratio_flag)
                    P("%-10s V=%.2f T=%4d  margin=%s  closest pair=%s" %
                      (form, v, t, "n/a" if m is None else "%.2f" % m, pair))
                    if m is not None and (form not in worst or m < worst[form][0]):
                        worst[form] = (m, v, t, pair)
        for form, (m, v, t, pair) in worst.items():
            P("MIN margin (%s) = %.2f at V=%.2f T=%d, pair %s" % (form, m, v, t, pair))
    low = [(r["osc"], r["process"], r["vdd"], r["temp_c"], r["f_hz"] * GATE_S)
           for r in freq["rows"] if r["f_hz"] and r["f_hz"] * GATE_S < 100]
    if low:
        P("\n## cells with < 100 counts in the default gate (2^10 @ 10 MHz): quantization dominates")
        for x in low:
            P("  %s %s %.2f V %d C: %.2f counts" % x)
    return res


def main(argv):
    if len(argv) >= 3 and argv[1] in ("extract", "extract-mc"):
        args = argv[2:]
        if "-o" not in args:
            sys.exit("usage: analyze.py %s REPORT... -o OUT.json" % argv[1])
        i = args.index("-o")
        out, paths = args[i + 1], args[:i]
        data = (extract if argv[1] == "extract" else extract_mc)(paths)
        with open(out, "w") as f:
            json.dump(data, f, indent=1, sort_keys=True)
            f.write("\n")
        return 0
    if len(argv) >= 3 and argv[1] == "report":
        args = argv[2:]
        global OSCS
        if "--without" in args:   # subset analysis, e.g. --without osc_subth
            i = args.index("--without")
            drop = args[i + 1].split(",")
            args = args[:i] + args[i + 2:]
            OSCS = [o for o in OSCS if o not in drop]
            print("# SUBSET: oscillators dropped from the analysis: %s" % ", ".join(drop))
        freq = json.load(open(args[0]))
        mc = json.load(open(args[1])) if len(args) > 1 else None
        report(freq, mc)
        return 0
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
