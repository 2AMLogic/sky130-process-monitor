#!/usr/bin/env python3
"""Post-process the osc_subth cold-corner iteration reports (issue #278) into the
comparison tables of `sim/sensitivity/records/2026-11-21-osc-subth-cold-iteration.md`.

    python3 -I sim/subthreshold/variants/compare.py            # print every table
    python3 -I sim/subthreshold/variants/compare.py --selftest # synthetic-data checks

Pure post-processing (stdlib only): no simulator runs, nothing submitted. Every input is
a committed `klt sim` report. It reuses `sim/sensitivity/analyze.py` unchanged (imported
as a sibling module) for the frequency extraction rule (skip 3 start-up edges, >= 5
cycles, VDD/2 rising crossings), the sensitivity rows and the ratio-space margins, so a
variant table and the committed baseline tables are computed by the same code.

SIMULATED figures only, schematic-level; nothing measured. Counts are expected counts,
f_Hz * 2^k / 10 MHz (spec section 5 gate convention); no estimate accuracy is quoted.
"""
import gzip
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SENS = os.path.join(HERE, "..", "..", "sensitivity")
sys.path.insert(0, SENS)
import analyze  # noqa: E402  (sim/sensitivity/analyze.py, stdlib only)

REPORTS = os.path.join(HERE, "reports")
# The committed bank tables, in the load-bearing order of
# records/2026-11-14-osc-subth-gate-sizing.md section 1 (osc_subth rows are replaced by
# the variant's; probe_wire_sf_relaxed keeps osc_wire sf/1.98 V/-40 C resolvable).
BANK = [
    "grid_osc_hd_5p.json.gz", "grid_osc_hd.json.gz", "grid_osc_nmos.json.gz",
    "grid_osc_pmos.json.gz", "grid_osc_wire.json.gz", "grid_osc_wire_sf_cold.json.gz",
    "probe_wire_sf_relaxed.json.gz",
]
BANK_MC = ["mc_osc_hd.json.gz", "mc_osc_nmos.json.gz", "mc_osc_pmos.json.gz",
           "mc_osc_wire.json.gz"]
BASELINE_SUBTH = ["grid_osc_subth.json.gz", "grid_osc_subth_sf_cold.json.gz"]
VARIANTS = ["vbp_2_3", "vbp_1_2", "hw3", "hl35", "st11"]
# The five cold cells of the issue (osc_subth at -40 C: ss 1.62/1.80 V, sf 1.62/1.80/1.98 V).
COLD = [("ss", 1.62), ("ss", 1.80), ("sf", 1.62), ("sf", 1.80), ("sf", 1.98)]
# Baseline frequencies at those cells from the committed reports (grid + the 10 ms
# sf/1.98 V fill) and -- the four cells main cannot resolve -- from the #277 single-cell
# fleet reports quoted in its record (PR #297, branch feature/issue-277; not on main).
BASELINE_COLD_QUOTED = {("ss", 1.62): 1251.87, ("ss", 1.80): 3043.81,
                        ("sf", 1.62): 436.93, ("sf", 1.80): 586.21,
                        ("sf", 1.98): 1057.37}
REF_HZ = 1e7
K_DEFAULT, K_LONG = 10, 14


def _p(*a):
    print(*a)


def _load(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt") as f:
        return json.load(f)


def _report_path(name):
    return os.path.join(SENS, "records", "reports", name)


def _var_reports(stem):
    """Committed variant report paths in this order: grid first, then fills last-wins."""
    paths = [os.path.join(REPORTS, "grid_osc_subth_%s.json.gz" % stem)]
    for kind in ("cold", "fast"):
        for proc, v in COLD if kind == "cold" else []:
            p = os.path.join(REPORTS, "%s_osc_subth_%s_%s_%gV_-40C.json.gz"
                             % (kind, stem, proc, v))
            if os.path.exists(p):
                paths.append(p)
    # any cold fill for a non-COLD cell or hot fast fill discovered by glob-free listing
    for fn in sorted(os.listdir(REPORTS)):
        if fn.startswith(("cold_osc_subth_%s_" % stem, "fast_osc_subth_%s_" % stem)) \
                and os.path.join(REPORTS, fn) not in paths:
            paths.append(os.path.join(REPORTS, fn))
    return paths


def counts(f_hz, k):
    return None if f_hz is None else f_hz * (2 ** k) / REF_HZ


def extract(paths):
    return analyze.extract(paths)


def freq_rows(rep_paths):
    rows = extract(rep_paths)["rows"]
    return {(r["process"], round(r["vdd"], 2), r["temp_c"]): (r["f_hz"], r["n_edges"])
            for r in rows if r["osc"] == "osc_subth"}


def mc_sigma(rep_paths):
    mc = analyze.extract_mc(rep_paths)
    per, pooled = analyze.mc_sigmas(mc)
    return per.get("osc_subth", {}), pooled.get("osc_subth")


def margins(freq_paths, mc_paths):
    """(absolute, ratio-only) min margins per (V,T) cell; None where ungradable."""
    freq = extract(freq_paths)
    tab = analyze.table(freq["rows"])
    mc = analyze.extract_mc(mc_paths)
    _per, pooled = analyze.mc_sigmas(mc)
    out = {}
    for iv in range(len(analyze.VDD)):
        for it in range(len(analyze.TEMP)):
            a, pa = analyze.margin(tab, iv, it, pooled, ratio=False)
            r, pr = analyze.margin(tab, iv, it, pooled, ratio=True)
            out[(analyze.VDD[iv], analyze.TEMP[it])] = (a, pa, r, pr)
    return out, tab, pooled


def sensitivity_rows(tab):
    out = {}
    for iv in range(len(analyze.VDD)):
        for it in range(len(analyze.TEMP)):
            out[(analyze.VDD[iv], analyze.TEMP[it])] = analyze.sensitivity_row(
                tab, "osc_subth", iv, it)
    return out






def probe_table():
    """Header DC probe (reports/probe_hdr.json.gz): Id of the baseline/variant header
    devices at the |Vgs| drives the levers actually reach, per corner. The probe is the
    gen_probe.py convention: Vdd fixed 1.8 V, |Vds| = 0.90 V -- a device characterization,
    not the ring's operating point."""
    path = os.path.join(REPORTS, "probe_hdr.json.gz")
    if not os.path.exists(path):
        _p("(probe report not present)")
        return
    rep = _load(path)
    data = {}
    for c in rep["corners"]:
        corner = (c["process"], c["temperature_c"])
        vals = {}
        for m in c["measurements"]:
            if m["status"] == "pass" and m["value"] is not None:
                vals[m["name"]] = abs(m["value"])
        data[corner] = vals
    devs = {"baseline/st11": "l050_w042", "hw3": "l050_w126", "hl35": "l035_w042"}
    # |Vgs| the divider ratios reach at the three VDDs (vbp = Rb1/(Rb0+Rb1)):
    drives = {"baseline/st11/hw3/hl35": [0.30], "vbp_2_3": [0.54, 0.60, 0.66],
              "vbp_1_2": [0.81, 0.90, 0.99]}
    _p("### Header Id (A) from the DC probe: device x |Vgs| at the cold corners and the tt/27 control")
    _p("| device / lever | corner | Id @ 0.30 V | @ 0.54 | @ 0.60 | @ 0.66 | @ 0.81 | @ 0.90 | @ 0.99 |")
    _p("|---|---|---|---|---|---|---|---|---|")
    for label, dev in devs.items():
        for corner in [("ss", -40), ("sf", -40), ("tt", 27)]:
            vals = data.get(corner, {})
            cells = []
            for vg in (0.30, 0.54, 0.60, 0.66, 0.81, 0.90, 0.99):
                v = vals.get("i%03d_%s" % (round(vg * 100), dev))
                cells.append("%.3g" % v if v is not None else "-")
            _p("| %s | %s / %d C | %s |" % (label, corner[0], corner[1], " | ".join(cells)))
    _p()
    _p("Divider-ratio mapping (|Vgs| = (1 - Rb1/(Rb0+Rb1)) x VDD): baseline 0.8333 ratio "
       "-> 0.27/0.30/0.33 V at 1.62/1.80/1.98 V; vbp_2_3 -> 0.54/0.60/0.66 V; "
       "vbp_1_2 -> 0.81/0.90/0.99 V. The hw3/hl35/st11 rows read the baseline drive "
       "(0.30 V at 1.80 V) on their own device column.")
    _p()


def main():
    _p("## Control: the committed baseline reports reproduce the 1057.37 Hz cell")
    base_rows = freq_rows([_report_path(n) for n in BASELINE_SUBTH])
    ctrl = base_rows.get(("sf", 1.98, -40), (None, None))
    _p("sf / 1.98 V / -40 C: f = %s Hz (n_edges = %s) -- grid_osc_subth + grid_osc_subth_sf_cold"
       % (("%.2f" % ctrl[0]) if ctrl[0] else "MISSING", ctrl[1]))
    _p()

    _p("## Baseline bank margins (committed reports only, default gate 2^10 at 10 MHz)")
    base_bank = [_report_path(n) for n in BANK + BASELINE_SUBTH]
    bm, base_tab, base_pooled = margins(base_bank, [_report_path(n) for n in
                                                    BANK_MC + ["mc_osc_subth.json.gz"]])
    base_sens = sensitivity_rows(base_tab)
    _p("| V | T | abs | pair | ratio | pair |")
    _p("|---|---|-----|------|-------|------|")
    for (v, t), (a, pa, r, pr) in sorted(bm.items()):
        _p("| %.2f | %d | %s | %s | %s | %s |" % (
            v, t, "%.3f" % a if a else "ungradable", pa or "-",
            "%.3f" % r if r else "ungradable", pr or "-"))
    _p()
    _p("Baseline osc_subth sensitivity rows (scaled dV/dT/dPn/dPp of ln f), where gradable:")
    _p("| V | T | dV | dT | dPn | dPp |")
    _p("|---|---|----|----|-----|-----|")
    for (v, t), row in sorted(base_sens.items()):
        if row:
            _p("| %.2f | %d | %.3f | %.3f | %.3f | %.3f |" % (v, t, *row))
    _p()

    for stem in VARIANTS:
        vpaths = _var_reports(stem)
        rows = freq_rows(vpaths)
        _p("## Variant %s" % stem)
        _p("Reports (order is load-bearing, last wins): %s"
           % [os.path.basename(p) for p in vpaths])
        _p()
        _p("### The five cold cells (-40 C; SIMULATED, sensitivity bench, VDD/2 crossings)")
        _p("| cell | baseline f (Hz) | %s f (Hz) | edges | counts @ k=10 | counts @ k=14 |" % stem)
        _p("|------|-----------------|-----------|-------|--------------|--------------|")
        for p, v in COLD:
            f, e = rows.get((p, v, -40), (None, None))
            b = base_rows.get((p, v, -40), (None, None))[0] or BASELINE_COLD_QUOTED[(p, v)]
            c10, c14 = counts(f, K_DEFAULT), counts(f, K_LONG)
            _p("| %s / %.2f V | %.2f | %s | %s | %s | %s |" % (
                p, v, b, ("%.2f" % f) if f else "MISSING", e,
                ("%.3f%s" % (c10, " **<1**" if c10 is not None and c10 < 1 else "")) if c10 else "-",
                ("%.3f%s" % (c14, " **<1**" if c14 is not None and c14 < 1 else "")) if c14 else "-"))
        _p()
        cov = sum(1 for k in rows if rows[k][0])
        fs = [(f, k) for k, (f, _e) in rows.items() if f]
        _p("### 45-cell coverage and extrema (row-1 criterion: every cell resolved)")
        _p("- resolved cells: %d / 45" % cov)
        if fs:
            _p("- min f = %.2f Hz at %s %.2f V %d C; max f = %.4g Hz at %s %.2f V %d C; ratio %.4g"
               % (min(fs)[0], min(fs)[1][0], min(fs)[1][1], min(fs)[1][2],
                  max(fs)[0], max(fs)[1][0], max(fs)[1][1], max(fs)[1][2],
                  max(fs)[0] / min(fs)[0]))
        _p()
        per, pooled = mc_sigma([os.path.join(REPORTS, "mc_osc_subth_%s.json.gz" % stem)])
        cell = per.get(("tt", 1.8, 27))
        _p("### Nominal mismatch MC (tt / 1.80 V / 27 C, 30 draws, seed 20261105, scale 1)")
        if cell:
            _p("- usable draws %d / 30, sigma(ln f) = %.5f" % (cell[1], cell[0]))
        else:
            _p("- no usable MC samples")
        _p()
        vbank = [_report_path(n) for n in BANK] + vpaths
        vmc = [_report_path(n) for n in BANK_MC] + [os.path.join(
            REPORTS, "mc_osc_subth_%s.json.gz" % stem)]
        mm, tab, _pool = margins(vbank, vmc)
        _p("### Row-2 margins with %s substituted for osc_subth (default gate, committed MC for the other four)"
           % stem)
        _p("| V | T | abs | pair | ratio | pair | vs baseline abs | vs baseline ratio |")
        _p("|---|---|-----|------|-------|------|-----------------|-------------------|")
        for (v, t), (a, pa, r, pr) in sorted(mm.items()):
            ba, _bpa, br, _bpr = bm[(v, t)]
            _p("| %.2f | %d | %s | %s | %s | %s | %s | %s |" % (
                v, t, "%.3f" % a if a else "ungradable", pa or "-",
                "%.3f" % r if r else "ungradable", pr or "-",
                "%.3f" % ((a / ba) if (a and ba) else float("nan")) if (a and ba) else "-",
                "%.3f" % ((r / br) if (r and br) else float("nan")) if (r and br) else "-"))
        _p()
        srows = sensitivity_rows(tab)
        _p("### %s sensitivity rows (scaled), where gradable" % stem)
        _p("| V | T | dV | dT | dPn | dPp | baseline dT |")
        _p("|---|---|----|----|-----|-----|-------------|")
        for (v, t), row in sorted(srows.items()):
            if row:
                brow = base_sens[(v, t)]
                _p("| %.2f | %d | %.3f | %.3f | %.3f | %.3f | %s |" % (
                    v, t, row[0], row[1], row[2], row[3],
                    ("%.3f" % brow[1]) if brow else "-"))
        _p()
    _p("## Divider idle current (derived from the netlist resistors, not simulated)")
    _p("Every variant keeps Rb0+Rb1 = 1.8 M exactly, so the divider draws "
       "V/1.8 M: %.2f / %.2f / %.2f uA at 1.62 / 1.80 / 1.98 V."
       % (1.62 / 1.8, 1.8 / 1.8, 1.98 / 1.8))
    _p()
    probe_table()


def selftest():
    # counts math, extraction rule reuse, and margin smoke on synthetic tables.
    assert abs(counts(9765.625, 10) - 1.0) < 1e-9
    assert abs(counts(1057.366320595822, 14) - 1.73239) < 1e-4
    rows = analyze.extract.__doc__ is not None
    tab = {}
    for oi, o in enumerate(analyze.OSCS):
        for p in analyze.PROCESS:
            for v in analyze.VDD:
                for t in analyze.TEMP:
                    tab[(o, p, v, t)] = 1e6 * (1 + (0.1 + 0.05 * oi) * analyze.PROCESS.index(p)
                                               + (0.2 + 0.03 * oi) * analyze.VDD.index(v)
                                               + (0.05 + 0.01 * oi) * analyze.TEMP.index(t))
    sigma = {o: 0.01 for o in analyze.OSCS}
    a, pa = analyze.margin(tab, 1, 1, sigma, ratio=False)
    r, pr = analyze.margin(tab, 1, 1, sigma, ratio=True)
    assert a and a > 0 and r and r > 0 and pa and pr
    row = analyze.sensitivity_row(tab, "osc_subth", 1, 1)
    assert row and all(x is not None for x in row)
    _p("selftest OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        main()
