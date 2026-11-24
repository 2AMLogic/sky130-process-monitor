#!/usr/bin/env python3
"""Post-processing for the row-7 active-power iteration (issue #280). Pure stdlib, no simulator.

    analyze_iteration.py binding  POWER_TABLE.json[.gz]
    analyze_iteration.py decompose PROBE.json[.gz] ... --idle POWER_TABLE.json[.gz] -o OUT.json
    analyze_iteration.py screens  CAND.json[.gz] ... -o OUT.json
    analyze_iteration.py gaps     GAP.json[.gz] ... -o OUT.json
    analyze_iteration.py candgrid CANDGRID.json[.gz] BASELINE_GRID_REPORTS... -o OUT.json

Everything printed is SIMULATED, schematic-level, oscillator bank only (no counter netlist).

  binding    re-derives the worst graded active cell per oscillator from the committed power table
             and asserts it matches gen_candidates.BINDING (the cells the probes/screens ran at).
  decompose  splits each probe's supply power into the explicit-capacitor switching term
             (N * C * VDD * dV * f, dV the measured post-RC swing -- exact for a capacitor charged
             from a fixed rail, independent of waveform shape), the gated-off DC draw (the committed
             idle table at the same cell), and a residual that holds intrinsic-device-capacitance
             switching and crowbar (overlap) current. The residual is NOT attributed to crowbar
             alone: intrinsic charging is bounded below from the driver geometry in the record.
  screens    one row per single-corner candidate screen: supply power, frequency, and for the wire
             family the RC-delay fraction of stage delay (post-RC minus driver-output crossings
             against the period/2N stage delay).
  gaps       the six previously-ungraded active cells: n_edges, frequency, power; gradable iff the
             #8 rule yields a frequency (analyze_power.MIN_EDGES).
  candgrid   the 45-cell box of a carried candidate: per-cell power and frequency, worst cell,
             frequency range vs the counter's decision-0003 rates at the three nearest STA cells,
             and the candidate's scaled sensitivity row (V, T, Pn, Pp) against the committed
             baseline surface at those cells.

The baseline frequency surface is re-extracted from the committed #8 grid reports (deterministic
post-processing; see sim/solve/records/2026-11-05-rows1-4.md for the pinned report list).
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import _siblings  # noqa: E402

_SENS = _siblings.load("sensitivity", "analyze")
_POWER = _siblings.load("power", "analyze_power")
_GEN = _siblings.load("power", "gen_candidates")
freq_from_crossings, OSCS = _SENS.freq_from_crossings, _SENS.OSCS
_load, _osc_of, SKIP_EDGES = _SENS._load, _SENS._osc_of, _SENS.SKIP_EDGES
MIN_EDGES = _POWER.MIN_EDGES
# decision 0003: setup-limited counter fmax at the liberty corner nearest each grid cell
STA_LIMITS_MHZ = {(("ss", 1.62, 125)): 171.1, (("tt", 1.80, 27)): 358.9, (("ff", 1.98, -40)): 586.8}
# committed wire geometry (design/osc_bank/osc_wire.spice), for the explicit-switching term
WIRE_N, WIRE_C_F = 31, 100.0e-15


def _meas(corner):
    return {m["name"]: m for m in corner["measurements"]}


def _f(m):
    cr = ((m.get("t_rise") or {}).get("crossings") or {}).get("times") or []
    return freq_from_crossings(cr), len(cr)


def _corner(rep):
    cs = [c for c in rep["corners"] if c["status"] == "pass"]
    if len(cs) != 1:
        raise SystemExit("expected exactly one passing corner in %s" % rep.get("netlist", {}).get("path"))
    return cs[0]


def _cand_of(rep):
    """Candidate name (<family>_<tag>) from the netlist metadata active_cand_<name>.spice."""
    stem = os.path.basename(rep["netlist"]["path"])
    if not (stem.startswith("active_cand_") and stem.endswith(".spice")):
        raise ValueError("cannot tell candidate from netlist %r" % rep["netlist"]["path"])
    return stem[len("active_cand_"):-len(".spice")]


def _single_corner_row(rep, osc, nstages=WIRE_N):
    """Measurements shared by probe and candidate-screen rows of one passing corner."""
    c = _corner(rep)
    m = _meas(c)
    f, n = _f(m)
    en = (m["e_vdd"].get("energy") or {})
    win = en.get("to") - en.get("from")
    v = round(c["supply_v"]["vdd"], 2)
    row = {"cell": [c["process"], v, c["temperature_c"]], "n_edges": n, "f_hz": f,
           "P_supply_uW": en["net"] / win * 1e6,
           "P_iavg_uW": v * abs(m["i_avg"]["value"]) * 1e6,
           "swing_n1_V": m["vhi_n1"]["value"] - m["vlo_n1"]["value"]}
    if osc == "osc_wire":
        s = (((m.get("t_s1") or {}).get("crossings") or {}).get("times") or [])[SKIP_EDGES:]
        nn = (((m.get("t_n1") or {}).get("crossings") or {}).get("times") or [])[SKIP_EDGES:]
        k = min(len(s), len(nn))
        if k >= 4 and f:
            d = [nn[i] - s[i] for i in range(k)]
            rc = sum(d) / len(d)
            row["rc_delay_s"] = rc
            row["stage_delay_s"] = 1.0 / (2 * nstages * f)
            row["rc_fraction"] = rc * 2 * nstages * f
        row["swing_s1_V"] = m["vhi_s1"]["value"] - m["vlo_s1"]["value"]
    return row, m, v


def binding(table_path):
    tab = _load(table_path)
    act = {}
    for r in tab["rows"]:
        if r["kind"] == "active" and r["i_a"] is not None:
            act[(r["osc"], r["process"], r["vdd"], r["temp_c"])] = r["vdd"] * r["i_a"] * 1e6
    out = {}
    for o in OSCS:
        cells = [(uW, (p, v, t)) for (osc, p, v, t), uW in act.items() if osc == o]
        if not cells:
            raise SystemExit("no graded active cells for %s in %s" % (o, table_path))
        uW, (p, v, t) = max(cells)
        out[o] = {"cell": [p, v, t], "uW": uW, "cells_graded": len(cells),
                  "min_uW": min(u for u, _ in cells)}
        want = tuple(_GEN.BINDING[o])
        if (p, round(v, 2), t) != want:
            raise SystemExit("binding cell drift: table says %s %s, gen_candidates.BINDING says %s"
                             % (o, (p, v, t), want))
    return {"kind": "SIMULATED", "source": os.path.basename(table_path), "binding": out}


def decompose(probe_paths, idle_table):
    idle = {(r["osc"], r["process"], round(r["vdd"], 2), r["temp_c"]): r["i_a"]
            for r in _load(idle_table)["rows"] if r["kind"] == "idle" and r["i_a"] is not None}
    out = []
    for p in probe_paths:
        rep = _load(p)
        osc = _osc_of(rep)
        base, m, v = _single_corner_row(rep, osc)
        proc, t = base["cell"][0], base["cell"][2]
        i_dc = idle.get((osc, proc, v, t))
        p_dc = v * i_dc * 1e6 if i_dc is not None else None
        row = dict(base, osc=osc, P_dc_idle_uW=p_dc)
        if osc == "osc_wire":
            f = row["f_hz"]
            row["P_explicit_uW"] = WIRE_N * WIRE_C_F * v * row["swing_n1_V"] * f * 1e6 if f else None
        else:
            row["P_explicit_uW"] = 0.0
        terms = [x for x in (row["P_supply_uW"], row["P_explicit_uW"], row["P_dc_idle_uW"]) if x is not None]
        row["P_residual_uW"] = terms[0] - sum(terms[1:]) if len(terms) == 3 else None
        out.append(row)
    return {"kind": "SIMULATED", "probes": out}


def screens(paths):
    out = []
    for p in paths:
        rep = _load(p)
        name = _cand_of(rep)
        fam, tag = name.split("_", 1)
        lever = _GEN.CANDIDATES[fam]["levers"][tag]
        osc = _GEN.CANDIDATES[fam]["osc"]
        base, _, _ = _single_corner_row(rep, osc, nstages=lever.get("n", 31))
        out.append(dict(base, candidate=name, lever=lever))
    return {"kind": "SIMULATED", "screens": out}


def gaps(paths):
    out = []
    for p in paths:
        rep = _load(p)
        osc = _osc_of(rep)
        for c in rep["corners"]:
            m = _meas(c)
            f, n = _f(m)
            i = (m.get("i_avg") or {}).get("value")
            v = round(c["supply_v"]["vdd"], 2)
            out.append({"osc": osc, "cell": [c["process"], v, c["temperature_c"]],
                        "unit_status": c["status"], "n_edges": n, "f_hz": f,
                        "P_uW": v * abs(i) * 1e6 if i is not None else None,
                        "gradable": bool(f) and i is not None,
                        "rule": ">= %d rising crossings (the #8 rule via analyze_power.MIN_EDGES)" % MIN_EDGES})
    return {"kind": "SIMULATED", "gaps": out}


def _sens_rows(tab, osc):
    rows = {}
    for (p, v, t) in STA_LIMITS_MHZ:
        iv, it = _SENS.VDD.index(v), _SENS.TEMP.index(t)
        rows["%s|%.2f|%d" % (p, v, t)] = _SENS.sensitivity_row(tab, osc, iv, it)
    return rows


def candgrid(grid_report, baseline_reports):
    rep = _load(grid_report)
    name = _cand_of(rep)
    fam, tag = name.split("_", 1)
    osc = _GEN.CANDIDATES[fam]["osc"]
    cells, fs, ps = [], [], {}
    for c in rep["corners"]:
        m = _meas(c)
        f, n = _f(m)
        i = (m.get("i_avg") or {}).get("value")
        v = round(c["supply_v"]["vdd"], 2)
        p = None
        if i is not None and c["status"] == "pass":
            p = v * abs(i) * 1e6
            if f:
                ps["%s|%s|%.2f|%d" % (name, c["process"], v, c["temperature_c"])] = p
        cells.append({"cell": [c["process"], v, c["temperature_c"]], "unit_status": c["status"],
                      "n_edges": n, "f_hz": f, "P_uW": p})
        if f:
            fs.append(f)
    worst = max(ps, key=ps.get) if ps else None
    # baseline surface from the committed #8 grid reports, candidate row substituted for the osc
    base_tab = _SENS.table(_SENS.extract(baseline_reports)["rows"])
    cand_tab = dict(base_tab)
    for c in cells:
        if c["f_hz"]:
            cand_tab[(osc, c["cell"][0], round(c["cell"][1], 2), c["cell"][2])] = c["f_hz"]
    counter = {}
    for (p, v, t), lim in sorted(STA_LIMITS_MHZ.items()):
        key = (osc, p, v, t)
        row = {"counter_fmax_mhz": lim}
        if base_tab.get(key):
            row["baseline_f_mhz"] = base_tab[key] / 1e6
        if cand_tab.get(key):
            row["candidate_f_mhz"] = cand_tab[key] / 1e6
            row["covered"] = cand_tab[key] / 1e6 <= lim
        counter["%s|%.2f|%d" % (p, v, t)] = row
    return {"kind": "SIMULATED", "candidate": name, "osc": osc,
            "lever": _GEN.CANDIDATES[fam]["levers"][tag],
            "cells": cells, "cells_graded": len(ps),
            "worst_cell": worst, "worst_uW": ps.get(worst),
            "f_min_hz": min(fs) if fs else None, "f_max_hz": max(fs) if fs else None,
            "counter_limits": counter,
            "sensitivity_rows_baseline": _sens_rows(base_tab, osc),
            "sensitivity_rows_candidate": _sens_rows(cand_tab, osc)}


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("binding"); b.add_argument("table")
    d = sub.add_parser("decompose"); d.add_argument("probes", nargs="+"); d.add_argument("--idle", required=True)
    d.add_argument("-o", required=True)
    s = sub.add_parser("screens"); s.add_argument("screens", nargs="+"); s.add_argument("-o", required=True)
    g = sub.add_parser("gaps"); g.add_argument("gaps", nargs="+"); g.add_argument("-o", required=True)
    c = sub.add_parser("candgrid"); c.add_argument("report"); c.add_argument("baseline", nargs="+")
    c.add_argument("-o", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "binding":
        r = binding(a.table)
        print(json.dumps(r, indent=1, sort_keys=True))
        return 0
    if a.cmd == "decompose":
        r = decompose(a.probes, a.idle)
    elif a.cmd == "screens":
        r = screens(a.screens)
    elif a.cmd == "gaps":
        r = gaps(a.gaps)
    else:
        r = candgrid(a.report, a.baseline)
    with open(a.o, "w") as f:
        json.dump(r, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote %s" % a.o)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
