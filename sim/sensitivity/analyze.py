#!/usr/bin/env python3
"""Sensitivity matrix, conditioning and discrimination margin for the oscillator bank (issue #8).

Pure standard library (no numpy on the fleet workers; a one-sided Jacobi SVD is accurate for the
5x4 matrices used here). Everything printed is SIMULATED, schematic-level, no silicon.

    analyze.py extract REPORT.json[.gz]... -o freq_table.json   # klt sim grid reports -> frequency table
    analyze.py extract-mc REPORT.json[.gz]... -o mc_table.json  # klt sim MC reports   -> per-cell samples
    analyze.py report freq_table.json [mc_table.json] [--without osc_a,osc_b] [--gate-exp K]
    analyze.py gate-sweep freq_table.json mc_table.json --vdd V --temp T   # counts/margin vs gate 2^k
        [--osc OSC] [--kmin K] [--kmax K] [--quant-only]

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
REF_HZ = 10e6                 # spec section 5: reference clock is an INPUT, target 10 MHz
GATE_EXP = 10                 # spec section 5 default gate exponent k (gate = 2^k reference cycles)
GATE_S = 2 ** GATE_EXP / REF_HZ   # spec default: 2^10 reference cycles at 10 MHz
COUNTER_BITS = 24             # spec section 5: 24-bit saturating counter
COUNTER_MAX = 2 ** COUNTER_BITS - 1
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

def fmt_time(s):
    """A gate time as s / ms / us / ns, 4 significant figures (ASCII only, so 'us' not the micro sign)."""
    for unit, scale in (("s", 1.0), ("ms", 1e-3), ("us", 1e-6), ("ns", 1e-9)):
        if s >= scale:
            return "%.4g %s" % (s / scale, unit)
    return "%.4g s" % s


def gate_desc(gate_s=None):
    """A gate time in the spec's own parameterisation, e.g. '2^10 ref cycles @10 MHz'.

    A gate that is not a whole power of two in reference cycles is printed as the cycle count.
    """
    g = GATE_S if gate_s is None else gate_s
    cycles = g * REF_HZ
    k = math.log2(cycles)
    head = "2^%d" % round(k) if abs(k - round(k)) < 1e-9 else "%.6g" % cycles
    return "%s ref cycles @%g MHz" % (head, REF_HZ / 1e6)


def gate_phrase(gate_s=None):
    """'the default gate (2^10 @ 10 MHz)', or 'the 1.638 ms gate (2^14 @ 10 MHz)' for a longer one."""
    g = GATE_S if gate_s is None else gate_s
    short = gate_desc(g).replace(" ref cycles @", " @ ")
    if g == GATE_S:
        return "the default gate (%s)" % short
    return "the %s gate (%s)" % (fmt_time(g), short)


def _gate_of(gate_s, osc):
    """Resolve a gate spec for one oscillator: None -> module GATE_S, a float -> uniform, a dict -> per-osc.

    The dict form models a longer gate on some oscillators only (spec section 5 selects one oscillator
    at a time, so the gate need not be the same for all five); an osc absent from the dict keeps GATE_S.
    """
    if gate_s is None:
        return GATE_S
    if isinstance(gate_s, dict):
        return gate_s.get(osc, GATE_S)
    return gate_s


def sigma_quant(f_hz, gate_s=None):
    """sigma of ln f from counter quantization: uniform +-0.5 count over the gate (default GATE_S).

    Valid only while the count n = f * gate is at least about 1: below one count the counter reads 0 or
    1, which the +-0.5-count uniform-dither model does not describe. Callers sweeping the gate must
    check `counts()` rather than read this number blind (record 2026-11-14-osc-subth-gate-sizing.md).
    """
    n = f_hz * (GATE_S if gate_s is None else gate_s)
    return 1.0 / (n * math.sqrt(12.0))


def counts(f_hz, gate_s=None):
    """Counter reading (unrounded) for a cell at this gate: f * gate, in reference-clock-defined units."""
    return f_hz * (GATE_S if gate_s is None else gate_s)


def counter_limit(tab, osc):
    """Largest gate exponent k whose worst-case count for `osc` still fits the 24-bit counter.

    Over every cell of the box present in `tab` (the fastest cell binds). None if the oscillator has no
    usable cell. Saturation is a property of the counter width, not of the gate alone.
    """
    fs = [f for (o, _p, _v, _t), f in tab.items() if o == osc and f]
    if not fs:
        return None
    return int(math.floor(math.log2(COUNTER_MAX * REF_HZ / max(fs))))


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


def margin(tab, iv, it, sigma_mc, ratio=False, gate_s=None):
    """Minimum over corner pairs of |centroid difference| / noise sigma along their separation line.

    Feature vector: ln f_i (absolute) or ln f_i - ln f_baseline (ratio-only). Noise per oscillator:
    quantization (at that corner's f) and MC mismatch spread, independent, in quadrature. Returns
    (margin, (corner_a, corner_b)) or (None, None) if any needed cell, or any oscillator's MC sigma, is
    missing. sigma_mc=None means quantization only.

    gate_s sets the counter gate behind the quantization term: None keeps the spec default GATE_S, a
    float applies one gate to the whole bank, a dict {osc: gate_s} applies a longer gate to some
    oscillators only. It does NOT make the result an accuracy; this is a discrimination statistic.
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
        var_abs[p] = {o: sigma_quant(tab[(o, p, v, t)], _gate_of(gate_s, o)) ** 2
                         + (sigma_mc[o] if sigma_mc else 0.0) ** 2 for o in OSCS}
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


def report(freq, mc=None, out=sys.stdout, gate_s=None):
    """Full report at one counter gate. gate_s: None or a float (uniform); see `margin` for the dict form.

    At the spec default gate the output is byte-identical to the pre-gate-parameter version: the two
    header strings below render the gate in use, and `2026-11-05-mc-margin.md` quotes that default
    output verbatim, so the extra non-default caveats are printed only when the gate is not the default.
    """
    tab = table(freq["rows"])
    gate = GATE_S if gate_s is None else gate_s
    nondefault = gate != GATE_S
    P = lambda *a: print(*a, file=out)
    if nondefault:
        P("# GATE: %s = %s (spec default is %s); counts and quantization sigma below use it"
          % (gate_desc(gate), fmt_time(gate), gate_desc(GATE_S)))
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
        P("noise = counter quantization (%s) + pooled MC mismatch sigma, quadrature" % gate_desc(gate))
        worst = {}
        for form, ratio_flag in (("absolute", False), ("ratio-only", True)):
            for iv, v in enumerate(VDD):
                for it, t in enumerate(TEMP):
                    m, pair = margin(tab, iv, it, sig_pool, ratio_flag, gate_s=gate)
                    P("%-10s V=%.2f T=%4d  margin=%s  closest pair=%s" %
                      (form, v, t, "n/a" if m is None else "%.2f" % m, pair))
                    if m is not None and (form not in worst or m < worst[form][0]):
                        worst[form] = (m, v, t, pair)
        for form, (m, v, t, pair) in worst.items():
            P("MIN margin (%s) = %.2f at V=%.2f T=%d, pair %s" % (form, m, v, t, pair))
    low = [(r["osc"], r["process"], r["vdd"], r["temp_c"], counts(r["f_hz"], gate))
           for r in freq["rows"] if r["f_hz"] and counts(r["f_hz"], gate) < 100]
    if low:
        P("\n## cells with < 100 counts in %s: quantization dominates" % gate_phrase(gate))
        for x in low:
            P("  %s %s %.2f V %d C: %.2f counts" % x)
        if nondefault and any(x[4] < 1.0 for x in low):
            P("NOTE: the cells above under 1.00 count are outside sigma_quant's validity range (it models")
            P("      +-0.5 count of uniform dither); the counter reads 0 or 1 there, so a margin computed")
            P("      from them is a model artefact, not a result.")
    sat = [(r["osc"], r["process"], r["vdd"], r["temp_c"], counts(r["f_hz"], gate))
           for r in freq["rows"] if r["f_hz"] and counts(r["f_hz"], gate) > COUNTER_MAX]
    if sat:
        P("\n## cells SATURATING the %d-bit counter (> %d counts) in %s: the count is not a measurement"
          % (COUNTER_BITS, COUNTER_MAX, gate_phrase(gate)))
        for x in sat:
            P("  %s %s %.2f V %d C: %.4g counts" % x)
    return res


# ---------------------------------------------------------------- gate sweep

def gate_sweep(freq, mc, vdd, temp_c, osc="osc_subth", kmin=GATE_EXP, kmax=None,
               quant_only=False, out=sys.stdout):
    """Counts and discrimination margin at one (V,T) cell as the counter gate exponent k is swept.

    Two gate readings are tabulated side by side, because spec section 5 selects one oscillator at a
    time and so does not force one gate on the whole bank:
      * `uni` - the whole bank reads at 2^k;
      * `osc` - `osc` reads at 2^k, the other four stay at the spec default 2^10.
    Conversion time is the section 6 FULL read of all five oscillators, not the one gate.

    quant_only drops the MC mismatch term from the margin (`margin(..., sigma_mc=None)`), isolating
    what the gate alone does; the MC table is still read, for the sigma_quant-versus-sigma_MC line.

    Everything here is post-processing of committed SIMULATED reports: no simulator, no PDK. The
    margin is a corner-discrimination statistic from `margin`, never an estimate accuracy.
    """
    tab = table(freq["rows"])
    _per, pool = mc_sigmas(mc)
    iv, it = VDD.index(vdd), TEMP.index(temp_c)
    lim = {o: counter_limit(tab, o) for o in OSCS}
    uni_lim = min(v for v in lim.values() if v is not None)
    if kmax is None:
        kmax = lim[osc] if lim[osc] is not None else uni_lim
    P = lambda *a: print(*a, file=out)
    num = lambda x, w, p: ("%*s" % (w, "n/a")) if x is None else ("%*.*f" % (w, p, x))
    P("# Gate sweep (SIMULATED, schematic-level, post-processing of committed reports; nothing measured)")
    P("# cell V=%.2f T=%d C; counts column oscillator: %s; gate = 2^k ref cycles at %g MHz (spec 5)"
      % (vdd, temp_c, osc, REF_HZ / 1e6))
    P("# %d-bit counter limit per oscillator over every cell of the box (the fastest cell binds):"
      % COUNTER_BITS)
    P("#   " + "  ".join("%s k<=%s" % (o, lim[o]) for o in OSCS))
    P("#   the uniform reading is bound by the lowest of those, k<=%d; the %s-only reading by k<=%s"
      % (uni_lim, osc, lim[osc]))
    P("# pooled MC sigma(ln f) (nominal cell, from the MC table): "
      + "  ".join("%s %s" % (o, "%.5f" % pool[o] if o in pool else "n/a") for o in OSCS))
    P("# t_read = spec 6 FULL read of all five: uni = 5*2^k/f_ref, osc = (4*2^10 + 2^k)/f_ref")
    if quant_only:
        P("# QUANT-ONLY: the margins below drop the MC mismatch term (quantization noise alone)")
    P("# sig_q = sigma_quant of the lowest-count corner in this row; absU/ratU = absolute and")
    P("#   ratio-only margin with the whole bank at 2^k; absO/ratO = the same with only %s at 2^k" % osc)
    P("# sat = oscillators whose fastest cell saturates the counter at this k (uni | %s-only)" % osc)
    P("")
    P("%3s %10s %10s %10s%s %9s %6s %6s %6s %6s  %s"
      % ("k", "gate", "t_read_uni", "t_read_osc", "".join("%10s" % p for p in PROCESS),
         "sig_q", "absU", "ratU", "absO", "ratO", "sat (uni | osc)"))
    rows = []
    for k in range(kmin, kmax + 1):
        g = 2 ** k / REF_HZ
        fz = {p: tab.get((osc, p, vdd, temp_c)) for p in PROCESS}
        c = {p: None if not f else counts(f, g) for p, f in fz.items()}
        slow = min((f for f in fz.values() if f), default=None)
        sq = None if slow is None else sigma_quant(slow, g)
        sig = None if quant_only else pool
        mu = [margin(tab, iv, it, sig, r, gate_s=g)[0] for r in (False, True)]
        mo = [margin(tab, iv, it, sig, r, gate_s={osc: g})[0] for r in (False, True)]
        satu = [o for o in OSCS if lim[o] is not None and k > lim[o]]
        sato = [osc] if lim[osc] is not None and k > lim[osc] else []
        P("%3d %10s %10s %10s%s %9s %6s %6s %6s %6s  %s | %s"
          % (k, fmt_time(g), fmt_time(5 * g), fmt_time(4 * GATE_S + g),
             "".join(num(c[p], 10, 2) for p in PROCESS), num(sq, 9, 4),
             num(mu[0], 6, 3), num(mu[1], 6, 3), num(mo[0], 6, 3), num(mo[1], 6, 3),
             ",".join(satu) or "-", ",".join(sato) or "-"))
        rows.append({"k": k, "gate_s": g, "counts": c, "sigma_quant": sq,
                     "margin_uniform": mu, "margin_osc_only": mo, "saturating": satu})
    # Mechanical answers only: each line states its own criterion, and the record interprets them.
    full = [r for r in rows if all(v is not None for v in r["counts"].values())]
    ok_counts = [r["k"] for r in full if all(v >= 1.0 for v in r["counts"].values())]
    ok_sigma = [r["k"] for r in rows if r["sigma_quant"] is not None and osc in pool
                and r["sigma_quant"] < pool[osc]]
    best = max((r["margin_uniform"][0] for r in rows if r["margin_uniform"][0] is not None), default=None)
    plateau = [] if not best else [r["k"] for r in rows if r["margin_uniform"][0] is not None
                                   and r["margin_uniform"][0] >= 0.99 * best]
    P("")
    P("# smallest k with every %s corner at this cell reading >= 1.00 count: %s"
      % (osc, min(ok_counts) if ok_counts else "none in range"))
    P("# smallest k with sig_q < pooled MC sigma(%s) = %s: %s"
      % (osc, "%.5f" % pool[osc] if osc in pool else "n/a", min(ok_sigma) if ok_sigma else "none in range"))
    P("# smallest k within 1%% of the largest absolute margin in range%s (%s): %s"
      % (" (quantization only)" if quant_only else "",
         "n/a" if best is None else "%.3f" % best, min(plateau) if plateau else "none in range"))
    P("# A k that meets the plateau criterion but not the >= 1.00 count one is NOT sufficient:")
    P("#   sigma_quant models +-0.5 count of dither and is outside its validity range below one count,")
    P("#   so the margin there is a property of the model, not of the block.")
    return rows


def _gate_exp(args, flag="--gate-exp"):
    """Pull `--gate-exp K` out of args -> (args without it, gate seconds or None). Validates K."""
    if flag not in args:
        return args, None
    i = args.index(flag)
    if i + 1 >= len(args):
        sys.exit("%s needs an integer exponent k (gate = 2^k reference cycles)" % flag)
    try:
        k = int(args[i + 1])
    except ValueError:
        sys.exit("%s: %r is not an integer exponent" % (flag, args[i + 1]))
    if not 0 <= k <= 40:
        sys.exit("%s: k=%d is outside 0..40" % (flag, k))
    return args[:i] + args[i + 2:], 2 ** k / REF_HZ


def _opt(args, flag, cast, default=None):
    """Pull `flag VALUE` out of args -> (args without it, cast(VALUE) or default)."""
    if flag not in args:
        return args, default
    i = args.index(flag)
    if i + 1 >= len(args):
        sys.exit("%s needs a value" % flag)
    try:
        v = cast(args[i + 1])
    except ValueError:
        sys.exit("%s: %r is not valid" % (flag, args[i + 1]))
    return args[:i] + args[i + 2:], v


def main(argv):
    if len(argv) >= 3 and argv[1] in ("extract", "extract-mc"):
        args = argv[2:]
        if "-o" not in args:
            sys.exit("usage: analyze.py %s REPORT... -o OUT.json" % argv[1])
        if "--gate-exp" in args:   # meaningless here: extraction records frequencies, not counts
            sys.exit("analyze.py %s: --gate-exp is not accepted (the gate applies to `report`"
                     " and `gate-sweep`, which compute counts; extraction records f_osc)" % argv[1])
        i = args.index("-o")
        out, paths = args[i + 1], args[:i]
        data = (extract if argv[1] == "extract" else extract_mc)(paths)
        with open(out, "w") as f:
            json.dump(data, f, indent=1, sort_keys=True)
            f.write("\n")
        return 0
    if len(argv) >= 3 and argv[1] == "report":
        args, gate_s = _gate_exp(argv[2:])
        global OSCS
        if "--without" in args:   # subset analysis, e.g. --without osc_subth
            i = args.index("--without")
            drop = args[i + 1].split(",")
            args = args[:i] + args[i + 2:]
            OSCS = [o for o in OSCS if o not in drop]
            print("# SUBSET: oscillators dropped from the analysis: %s" % ", ".join(drop))
        freq = json.load(open(args[0]))
        mc = json.load(open(args[1])) if len(args) > 1 else None
        report(freq, mc, gate_s=gate_s)
        return 0
    if len(argv) >= 4 and argv[1] == "gate-sweep":
        args = argv[2:]
        args, vdd = _opt(args, "--vdd", float)
        args, temp = _opt(args, "--temp", int)
        args, osc = _opt(args, "--osc", str, "osc_subth")
        args, kmin = _opt(args, "--kmin", int, GATE_EXP)
        args, kmax = _opt(args, "--kmax", int)
        quant_only = "--quant-only" in args
        args = [a for a in args if a != "--quant-only"]
        if vdd is None or temp is None or len(args) != 2:
            sys.exit("usage: analyze.py gate-sweep FREQ.json MC.json --vdd V --temp T"
                     " [--osc OSC] [--kmin K] [--kmax K] [--quant-only]")
        if vdd not in VDD or temp not in TEMP:
            sys.exit("gate-sweep: cell V=%s T=%s is outside the box (V in %s, T in %s)"
                     % (vdd, temp, VDD, TEMP))
        if osc not in OSCS:
            sys.exit("gate-sweep: --osc %s is not one of %s" % (osc, OSCS))
        gate_sweep(json.load(open(args[0])), json.load(open(args[1])), vdd, temp,
                   osc=osc, kmin=kmin, kmax=kmax, quant_only=quant_only)
        return 0
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
