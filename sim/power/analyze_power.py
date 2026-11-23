#!/usr/bin/env python3
"""Row 7 (active and idle power) grading from `klt sim` reports (issue #29). Pure stdlib. SIMULATED.

    analyze_power.py extract REPORT.json[.gz]... [-o power_table.json] [--carry-active PRIOR_TABLE.json]
    analyze_power.py grade power_table.json [--json OUT]
    analyze_power.py cand-idle CAND_IDLE_REPORT.json UNGATED_POWER_TABLE.json -o cand_idle.json   (issue #279 candidate)
    analyze_power.py cand-ab ACTIVE_REPORT.json GATED_REPORT.json -o cand_ab.json                 (issue #279 candidate)

Scope, stated with every verdict: the OSCILLATOR BANK ONLY. The counter has no SPICE-level netlist, so COUNTER
POWER IS NOT COVERED; the spec's "one oscillator plus counter" active figure is therefore not graded in full
and no counter number is folded into any pass/fail here.
  * Active: one oscillator enabled, P = VDD * |mean supply current| (second half of the tran window; the
    averaging window is not an integer number of cycles, error <= 1 cycle / cycles in the window). A cell
    whose ring did not run long enough for a frequency is MISSING, never graded; gradability is the #8 rule
    read from sensitivity/analyze.py (MIN_EDGES below), not a second threshold stated here.
    Binding = the largest P over all oscillators and cells (worst oscillator, worst cell).
  * Idle: enable tied to vss, op analysis. Bank idle = SUM over the five oscillators at a cell (all gated
    off). Graded only where all five are present; partial sums are reported as lower bounds and NOT graded.
    osc_subth's schematic carries an ideal ~1 uA bias divider that is not gated by `en`: it is included.
  * Spec row 7: active target < 100 uW, fallback < 500 uW, stretch < 20 uW; idle < 1 uW, < 10 uW, < 100 nW.
    Cells not gradable make the row INCOMPLETE; the row is never reported PASS with ungraded cells.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Report loading and the oscillator list are defined once, in sensitivity/analyze.py. `python3 -I` drops
# the script directory from sys.path, so the module is loaded by path via the shared sim/ helper.
sys.path.insert(0, os.path.join(HERE, ".."))
import _siblings  # noqa: E402

_SENS = _siblings.load("sensitivity", "analyze")
OSCS, _load, _remote = _SENS.OSCS, _SENS._load, _SENS._remote
BOUNDS_UW = {"active": (100.0, 500.0, 20.0), "idle": (1.0, 10.0, 0.1)}
# Gradability is the #8 rule, not a power-side threshold: freq_from_crossings drops SKIP_EDGES start-up
# edges and then needs MIN_CYCLES full cycles, i.e. MIN_CYCLES + 1 further crossings. A cell the #8 surface
# records as MISSING must not be graded for power here, so the count comes from _SENS, never a literal.
MIN_EDGES = _SENS.SKIP_EDGES + _SENS.MIN_CYCLES + 1


def classify_bench(path):
    """(kind, oscillator) for a graded bench path, else (None, None).

    Graded benches are exactly `active_<osc>`, `idle_<osc>` and `idle_<osc>_settle`; any other deck
    (cross-checks, the gated candidate) is not a row-7 grading input."""
    stem = os.path.splitext(os.path.basename(path))[0]
    for o in OSCS:
        if stem == "active_" + o:
            return "active", o
        if stem in ("idle_" + o, "idle_" + o + "_settle"):
            return "idle", o
    return None, None


def extract(paths, carry_active=None):
    rows, envs = [], []
    for p in paths:
        rep = _load(p)
        path = rep["netlist"]["path"]
        kind, osc = classify_bench(path)
        if osc is None:
            # A bench this grader does not grade: the issue #279 candidate and cross-check decks
            # (xcheck_*, gated_subth_*) whose reports may sit in the same -o tree. Recorded as
            # environment, never as a row, so it can never shadow a graded cell.
            envs.append({"report": p, "kind": None, "oscillator": None, "job_id": None, "job_ids": None,
                         "runner_pdk": None})
            continue
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
                if len(cr) >= MIN_EDGES and v_i is not None:
                    cur = abs(v_i)
            elif ok and kind == "idle":
                v_i = (m.get("i_vdd") or {}).get("value")
                cur = abs(v_i) if v_i is not None else None
            rows.append({"kind": kind, "osc": osc, "process": c["process"], "vdd": round(v, 2), "temp_c": c["temperature_c"],
                         "i_a": cur, "unit_status": c["status"]})
    if carry_active is not None:
        # Issue #279: the idle half alone is re-run (active benches unchanged), so the new table
        # carries the prior committed table's active rows verbatim -- never re-simulated, never
        # re-derived; the record names the carried file and its own record.
        with open(carry_active) as f:
            prior = json.load(f)
        rows.extend(r for r in prior["rows"] if r["kind"] == "active")
    return {"kind": "SIMULATED", "rows": rows, "environment": envs}


EN_MID_NS = 1.05  # the A/B benches' behavioural enable: 0 until 1 ns, 100 ps ramp -> half-rail at 1.05 ns
VBP_TIMES = ("2n", "5n", "10n", "20n", "50n", "100n", "1u")
VBP_TOL = 0.01    # bias counted settled when within 1% of the long-window mean


def _cell(c):
    return "%s|%.2f|%d" % (c["process"], c["supply_v"]["vdd"], c["temperature_c"])


def cand_idle(report_path, ungated_table):
    """Per-cell result of the gated candidate's 45-cell idle grid, beside the ungated osc_subth design's
    idle current at the same cell (from the committed power table) -- the comparison is derived here, from
    data, never typed into the record."""
    rep = _load(report_path)
    un = {"%s|%.2f|%d" % (r["process"], r["vdd"], r["temp_c"]): r["i_a"]
          for r in ungated_table["rows"] if r["kind"] == "idle" and r["osc"] == "osc_subth"}
    cells = {}
    for c in rep["corners"]:
        m = {x["name"]: x for x in c["measurements"]}
        v = (m.get("i_vdd") or {}).get("value")
        i = abs(v) if v is not None and c["status"] == "pass" else None
        k = _cell(c)
        u = un.get(k)
        cells[k] = {"gated_i_a": i, "ungated_i_a": u, "unit_status": c["status"],
                    "reduction_x": (u / i) if (i and u) else None,
                    "gated_uW": (i * c["supply_v"]["vdd"] * 1e6) if i is not None else None}
    return {"kind": "SIMULATED", "bench": rep["netlist"]["path"], "cells": cells,
            "cells_present": sum(x["gated_i_a"] is not None for x in cells.values()), "cells_expected": 45}


def cand_ab(active_path, gated_path):
    """A/B of the unchanged and gated osc_subth on the same cells, from output-edge timestamps: frequency
    by sensitivity/analyze.py freq_from_crossings (the nine-edge rule, so an unresolvable ring is reported
    MISSING, never compared), first output edge after the enable midpoint, and bias settling reported
    separately (first sampled time at which vbp is within VBP_TOL of the long-window mean)."""
    out = {}
    for tag, path in (("ungated", active_path), ("gated", gated_path)):
        for c in _load(path)["corners"]:
            m = {x["name"]: x for x in c["measurements"]}
            times = ((m.get("t_rise") or {}).get("crossings") or {}).get("times") or []
            ref = (m.get("vbp_avg") or {}).get("value")
            settle = None
            if ref:
                for t in VBP_TIMES:
                    v = (m.get("vbp_" + t) or {}).get("value")
                    if v is not None and abs(v - ref) <= VBP_TOL * abs(ref):
                        settle = t
                        break
            out.setdefault(_cell(c), {})[tag] = {
                "status": c["status"], "edges": len(times), "f_hz": _SENS.freq_from_crossings(times),
                "first_edge_after_en_ns": (times[0] * 1e9 - EN_MID_NS) if times else None,
                "vbp_avg_v": ref, "vbp_settled_by": settle,
                "vbp_samples_v": {t: (m.get("vbp_" + t) or {}).get("value") for t in VBP_TIMES}}
    for d in out.values():
        a, g = d.get("ungated", {}), d.get("gated", {})
        fa, fg = a.get("f_hz"), g.get("f_hz")
        d["f_ratio_gated_over_ungated"] = (fg / fa) if (fa and fg) else None
        d["pair"] = "resolved" if (fa and fg) else "MISSING (below the %d-edge rule in: %s)" % (
            MIN_EDGES, ", ".join(t for t, x in (("ungated", fa), ("gated", fg)) if not x))
    return {"kind": "SIMULATED", "cells": out}


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
        carry = a[a.index("--carry-active") + 1] if "--carry-active" in a else None
        paths = [x for x in a[2:i] if x != "--carry-active" and x != carry]
        json.dump(extract(paths, carry), open(a[i + 1], "w"), indent=1, sort_keys=True)
        return 0
    if len(a) >= 5 and a[1] == "cand-idle" and "-o" in a:
        with open(a[3]) as f:
            r = cand_idle(a[2], json.load(f))
        json.dump(r, open(a[a.index("-o") + 1], "w"), indent=1, sort_keys=True)
        return 0
    if len(a) >= 5 and a[1] == "cand-ab" and "-o" in a:
        json.dump(cand_ab(a[2], a[3]), open(a[a.index("-o") + 1], "w"), indent=1, sort_keys=True)
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
