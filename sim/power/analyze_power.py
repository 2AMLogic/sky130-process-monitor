#!/usr/bin/env python3
"""Row 7 (active and idle power) grading from `klt sim` reports (issue #29). Pure stdlib. SIMULATED.

    analyze_power.py extract REPORT.json[.gz]... -o power_table.json
    analyze_power.py grade power_table.json [--json OUT]

Scope, stated with every verdict: the OSCILLATOR BANK ONLY. The counter has no SPICE-level netlist, so COUNTER
POWER IS NOT COVERED; the spec's "one oscillator plus counter" active figure is therefore not graded in full
and no counter number is folded into any pass/fail here.
  * Active: one oscillator enabled, P = VDD * |mean supply current| (second half of the tran window; the
    averaging window is not an integer number of cycles, error <= 1 cycle / cycles in the window). A cell
    whose ring did not oscillate (fewer than 5 rising crossings in the window) is MISSING, never graded.
    Binding = the largest P over all oscillators and cells (worst oscillator, worst cell).
  * Idle: enable tied to vss, op analysis. Bank idle = SUM over the five oscillators at a cell (all gated
    off). Graded only where all five are present; partial sums are reported as lower bounds and NOT graded.
    osc_subth's schematic carries an ideal ~1 uA bias divider that is not gated by `en`: it is included.
  * Spec row 7: active target < 100 uW, fallback < 500 uW, stretch < 20 uW; idle < 1 uW, < 10 uW, < 100 nW.
    Cells not gradable make the row INCOMPLETE; the row is never reported PASS with ungraded cells.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_sensitivity():
    """Report loading and the oscillator list are defined once, in sensitivity/analyze.py. `python3 -I` drops
    the script directory from sys.path, so load it by path."""
    spec = importlib.util.spec_from_file_location(
        "sens_analyze", os.path.join(HERE, "..", "sensitivity", "analyze.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_SENS = _load_sensitivity()
OSCS, _load, _remote = _SENS.OSCS, _SENS._load, _SENS._remote
BOUNDS_UW = {"active": (100.0, 500.0, 20.0), "idle": (1.0, 10.0, 0.1)}


def extract(paths):
    rows, envs = [], []
    for p in paths:
        rep = _load(p)
        path = rep["netlist"]["path"]
        kind = "idle" if "idle_" in path else "active"
        osc = next(o for o in OSCS if o in path)
        rem, runner_pdk = _remote(rep)
        envs.append({"report": p, "kind": kind, "oscillator": osc, "job_id": rem.get("job_id"),
                     "job_ids": rem.get("job_ids"), "runner_pdk": runner_pdk})
        for c in rep["corners"]:
            m = {x["name"]: x for x in c["measurements"]}
            v = c["supply_v"]["vdd"]
            cur, ok = None, c["status"] == "pass"
            if ok and kind == "active":
                cr = ((m.get("t_rise") or {}).get("crossings") or {}).get("times") or []
                v_i = (m.get("i_avg") or {}).get("value")
                if len(cr) >= 5 + 3 and v_i is not None:   # >= 5 edges inside the run (3 start-up edges skipped as in #8)
                    cur = abs(v_i)
            elif ok and kind == "idle":
                v_i = (m.get("i_vdd") or {}).get("value")
                cur = abs(v_i) if v_i is not None else None
            rows.append({"kind": kind, "osc": osc, "process": c["process"], "vdd": round(v, 2), "temp_c": c["temperature_c"],
                         "i_a": cur, "unit_status": c["status"]})
    return {"kind": "SIMULATED", "rows": rows, "environment": envs}


def grade(tab):
    out = {"scope": "oscillator bank only; counter power NOT covered", "kind": "SIMULATED"}
    cells = {(p, v, t) for r in tab["rows"] for p, v, t in [(r["process"], r["vdd"], r["temp_c"])]}
    get = {(r["kind"], r["osc"], r["process"], r["vdd"], r["temp_c"]): r["i_a"] for r in tab["rows"]}
    act, idle = {}, {}
    for (p, v, t) in sorted(cells):
        for o in OSCS:
            i = get.get(("active", o, p, v, t))
            if i is not None:
                act["%s|%s|%.2f|%d" % (o, p, v, t)] = v * i * 1e6
        parts = [get.get(("idle", o, p, v, t)) for o in OSCS]
        s = sum(x for x in parts if x is not None) * v * 1e6
        idle["%s|%.2f|%d" % (p, v, t)] = {"uW": s, "oscillators_present": sum(x is not None for x in parts),
                                         "complete": all(x is not None for x in parts)}
    a_exp, i_exp = 5 * 45, 45
    out["active"] = {"cells_graded": len(act), "cells_expected": a_exp, "uW": act}
    out["idle"] = {"cells_graded": sum(c["complete"] for c in idle.values()), "cells_expected": i_exp, "cells": idle}
    for k, d in (("active", act), ("idle", {a: c["uW"] for a, c in idle.items() if c["complete"]})):
        if d:
            b = max(d, key=d.get)
            out[k]["binding_cell"], out[k]["worst_uW"] = b, d[b]
            t_, f_, s_ = BOUNDS_UW[k]
            full = out[k]["cells_graded"] == out[k]["cells_expected"]
            def v(bound):
                if not full:
                    return "FAIL (worst graded cell exceeds)" if d[b] >= bound else "INCOMPLETE (ungraded cells remain)"
                return "PASS" if d[b] < bound else "FAIL"
            out[k]["target"], out[k]["fallback"], out[k]["stretch"] = v(t_), v(f_), v(s_)
        else:
            out[k]["target"] = out[k]["fallback"] = out[k]["stretch"] = "NOT GRADED"
    return out


def main(a):
    if len(a) >= 3 and a[1] == "extract" and "-o" in a:
        i = a.index("-o")
        json.dump(extract(a[2:i]), open(a[i + 1], "w"), indent=1, sort_keys=True)
        return 0
    if len(a) >= 3 and a[1] == "grade":
        r = grade(json.load(open(a[2])))
        if "--json" in a:
            json.dump(r, open(a[a.index("--json") + 1], "w"), indent=1, sort_keys=True)
        for k in ("active", "idle"):
            d = r[k]
            print(k, "cells %d/%d" % (d["cells_graded"], d["cells_expected"]), "worst uW", d.get("worst_uW"), "at", d.get("binding_cell"),
                  "| target", d["target"], "| fallback", d["fallback"], "| stretch", d["stretch"])
        return 0
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
