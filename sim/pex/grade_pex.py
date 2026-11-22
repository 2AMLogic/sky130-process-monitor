#!/usr/bin/env python3
"""Grade the committed `klt pex` reports against the #29 row-1 criterion and summarise the layout shift (issue #32).

    grade_pex.py OUT.json REPORT.pex.report.json [...]          # historical count reports (below)
    grade_pex.py freq MC.json OUT.json [--draws N] FREQ_REPORT.pex.report.json ...
                                                               # measured-frequency pass (issue #282)

SIMULATED, post-processing only (no simulation). Pure stdlib. Both paths read each report's per-cell
`delta` rows.

Count path (the historical 2026-11-10/2026-11-20 reports, kept unchanged): the pex scalar is the
`t_rise` crossings measurement (rising edges of v(out) at VDD/2 in the request's transient window);
it is a quantised edge COUNT, not a frequency, and the report carries no crossing times, so #29's
f_osc = (n-1)/(t_last - t_first) (analyze.freq_from_crossings) cannot be reproduced from it.
What this script can state exactly is:
  * row 1 (oscillates): analyze.py drops SKIP_EDGES start-up edges and needs MIN_CYCLES cycles, i.e. at least
    SKIP_EDGES + MIN_CYCLES + 1 rising edges (9 at the committed values). Both constants are read from
    sim/sensitivity/analyze.py below, not restated here. A cell passes iff its extracted-side count is >= that.
  * a frequency proxy f ~ count / window, including start-up and count quantisation. The window and proxy
    are null if the transient window cannot be read from the request identified by the report's SHA-256.
  * ratio-space shift: #29 row 2 classifies on ln f_i - ln f_osc_hd. The extracted-vs-schematic change of that
    coordinate is ln(ext_i/ext_hd) - ln(sch_i/sch_hd), computed from the counts where both legs exist.
No threshold is applied or changed by the count path: rows 2-4 are NOT re-graded from counts (see
sim/pex/README.md). The proxy is labelled as such wherever it appears.

Frequency path (`freq`, issue #282): the input reports are `klt pex --measure-command` runs whose
delta rows carry the measured f_hz per cell on both legs (sim/pex/measure_frequency.py reduced each
leg's crossings times with the same analyze.freq_from_crossings the schematic #29 frequencies use).
For each such report the grader
  * rebuilds each leg's f_hz from the committed nested `klt sim` report beside it
    (<report-stem>-{schematic,extracted}.sim.report.json.gz, the crossing times of record) and
    cross-checks them against the report's delta values,
  * writes one solve input per leg (<OUT stem>-leg-<leg>.json, the analyze.extract row shape) and
    replays `sim/solve/solve.py grade <leg table> MC.json` on it -- the same solver, seed and draws
    as the schematic record, so the row 1-4 verdicts on both legs are produced by the existing
    grader, not a reimplementation -- writing <OUT stem>-rows234-<leg>.json,
  * records the paired comparison: per-cell coverage and unresolved causes on both legs, the row-2
    classifier-coordinate shifts ln(f_i/f_osc_hd) extracted-vs-schematic, and the folded row 1-4
    verdicts, binding cells, coverage and oscillator subsets of both solve replays.
The MC table is a schematic-side input by construction (the pooled mismatch model of the #29 MC
reports); it is applied unchanged to both legs and the record says so.
"""
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The oscillation rule lives once, in sensitivity/analyze.py (as sim/pex/gen_requests.py already does for
# the oscillator list). `python3 -I` drops the script directory from sys.path, so the module is loaded
# by path via the shared sim/ helper (the bare name `analyze` is ambiguous in the tree).
sys.path.insert(0, os.path.join(HERE, ".."))
import _siblings  # noqa: E402

_SENS = _siblings.load("sensitivity", "analyze")
SIM_DIR = os.path.dirname(HERE)
SKIP_EDGES, MIN_CYCLES = _SENS.SKIP_EDGES, _SENS.MIN_CYCLES
MIN_EDGES = SKIP_EDGES + MIN_CYCLES + 1
REPO_ROOT = Path(HERE).parents[1]


def time_seconds(arg):
    """Read a numeric transient argument in seconds, with an optional SPICE scale suffix."""
    arg = arg.lower().removesuffix("s")
    divisors = {"f": 1e15, "p": 1e12, "n": 1e9, "u": 1e6, "m": 1e3}
    if arg[-1:] in divisors:
        return float(arg[:-1]) / divisors[arg[-1]]
    return float(arg)


def verified_window_s(bench):
    request = bench.get("request") or {}
    if request.get("scope") != "repo" or not request.get("path"):
        return None
    path = Path(request["path"])
    if path.is_absolute() or ".." in path.parts:
        return None
    try:
        raw = (REPO_ROOT / path).read_bytes()
        if "sha256:" + hashlib.sha256(raw).hexdigest() != bench.get("request_sha256"):
            return None
        analysis = json.loads(raw)["analysis"]
        if analysis["kind"] != "tran" or not isinstance(analysis["args"], str):
            return None
        args = analysis["args"].lower().split()
        if args[-1:] == ["uic"]:
            args.pop()
        if not 2 <= len(args) <= 4:  # tstep tstop [tstart [tmax]]
            return None
        times = [time_seconds(arg) for arg in args]
    except (OSError, KeyError, TypeError, ValueError):
        return None
    step, stop = times[:2]
    start = times[2] if len(times) >= 3 else 0
    if not all(map(math.isfinite, times)) or (len(times) == 4 and times[3] <= 0):
        return None
    if step <= 0 or not 0 <= start < stop:
        return None
    return stop - start


def load(path):
    with open(path) as f:
        d = json.load(f)
    bench = d["testbenches"][0]
    request_path = (bench.get("request") or {}).get("path")
    osc = Path(request_path).stem if request_path else Path(bench["netlist"]["path"]).stem.removeprefix("tb_")
    return osc, {r["corner_id"]: r for r in d["delta"]}, verified_window_s(bench)


# ------------------------------------------------------------------ frequency path (issue #282)

def _sha256_file(path):
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _load_maybe_gz(path):
    with (gzip.open if str(path).endswith(".gz") else open)(path, "rt") as f:
        return json.load(f)


def load_freq_report(path):
    """(osc, {corner_id: delta row}, report json) of one --measure-command pex report."""
    d = _load_maybe_gz(path)
    meas = d.get("measurement") or {}
    if meas.get("mode") != "command":
        raise SystemExit("%s: measurement.mode is %r, not 'command' (not a frequency-pass report)" % (path, meas.get("mode")))
    cmd = meas.get("command") or []
    osc = cmd[cmd.index("--osc") + 1] if "--osc" in cmd else None
    if osc is None:
        ref = (d.get("reference_netlist") or {}).get("path") or ""
        osc = next((o for o in _SENS.OSCS if o in ref), None)
    if osc not in _SENS.OSCS:
        raise SystemExit("%s: cannot tell oscillator from command %r" % (path, cmd))
    rows = {}
    for r in d["delta"]:
        if r["corner_id"] in rows:
            raise SystemExit("%s: duplicate corner %s in delta[]" % (path, r["corner_id"]))
        if r.get("spec_row") != "f_hz":
            raise SystemExit("%s: delta spec_row %r is not f_hz" % (path, r.get("spec_row")))
        rows[r["corner_id"]] = r
    return osc, rows, d


def nested_report_for(path, leg):
    """The committed nested `klt sim` report of one leg, or None when not beside the pex report."""
    stem = Path(path).name
    if stem.endswith(".json.gz"):
        stem = stem[:-8]
    elif stem.endswith(".json"):
        stem = stem[:-5]
    for suffix in ("-%s.sim.report.json.gz" % leg, "-%s.sim.report.json" % leg):
        p = Path(path).parent / (stem + suffix)
        if p.exists():
            return p
    return None


def leg_frequencies(osc, rows, leg, path):
    """({corner_id: f_hz or None}, {corner_id: cause}, nested env or None) for one leg.

    Frequencies are rebuilt from the nested sim report when one is committed beside the pex
    report (the crossing times of record, reduced by the same shared estimator the callback
    used) and cross-checked against the pex delta values; without it the delta values stand.
    """
    key, status_key = ("schematic_value", "schematic_status") if leg == "schematic" else ("extracted_value", "extracted_status")
    nested = nested_report_for(path, leg)
    recomputed, causes, env = None, {}, None
    if nested is not None:
        _MF = _siblings.load("pex", "measure_frequency")
        with open(os.path.join(HERE, "requests", "%s.json" % osc)) as f:
            req = json.load(f)
        rep = _load_maybe_gz(nested)
        env = dict(_SENS._env(rep), oscillator=osc, report=str(nested))
        doc = _MF.measurement_document(rep, list(_MF.expected_corners(req)))
        recomputed = {c["corner_id"]: (c["measurements"][0]["value"], c["measurements"][0].get("message"))
                      for c in doc["corners"]}
    freqs = {}
    for cid, r in rows.items():
        v = r.get(key)
        if recomputed is not None and cid in recomputed:
            rv, _ = recomputed[cid]
            if (v is None) != (rv is None) or (v is not None and rv != v):
                raise SystemExit("%s: %s %s: pex delta %r != frequency rebuilt from %s" % (path, cid, leg, v, nested))
        if v is not None:
            freqs[cid] = v
            continue
        msg = recomputed[cid][1] if recomputed is not None and cid in recomputed else None
        if not isinstance(msg, str) or not msg:
            err = r.get("error")
            msg = err.get("message") if isinstance(err, dict) and isinstance(err.get("message"), str) else None
        causes[cid] = msg or ("unresolved (%s leg status %s)" % (leg, r.get(status_key)))
    return freqs, causes, env


def solve_replay(table_path, mc_path, out_path, draws):
    """Replay sim/solve/solve.py grade on one leg table; returns its parsed output json."""
    cmd = [sys.executable, "-I", os.path.join(SIM_DIR, "solve", "solve.py"),
           "grade", str(table_path), str(mc_path), "--json", str(out_path), "--draws", str(draws)]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
    if p.returncode != 0:
        raise SystemExit("solve replay failed:\n%s%s" % (p.stdout, p.stderr))
    return json.loads(Path(out_path).read_bytes())


def _fold_solve(out):
    """The row verdicts, binding cells, coverage and oscillator subsets of one solve.py output."""
    fam = {}
    for name, d in out["row2_ratio"].items():
        failing = {k: c["confusions"] for k, c in d["cells"].items() if c.get("gradable") and not c["identified"]}
        ungradable = {k: c.get("oscillators") for k, c in d["cells"].items() if not c.get("gradable")}
        fam[name] = {"verdict": d["verdict"], "gradable_cells": d["gradable_cells"],
                     "identified_cells": d["identified_cells"], "failing_cells": failing,
                     "ungradable_cells": ungradable}
    r3, r4 = out["row3"], out["row4"]
    return {"row1": {"verdict_target": out["row1"]["verdict_target"], "verdict_fallback": out["row1"]["verdict_fallback"],
                     "missing_cells": out["row1"]["target_bank_5"]["missing_cells"],
                     "lowest_f_cell": out["row1"]["lowest_f_cell"]},
            "row2": fam,
            "row3": {"worst_p99_abs_err_v": r3["worst_p99_abs_err_v"], "binding_cell": r3["binding_cell"],
                     "grade": r3["grade"], "cells_graded": r3["cells_graded"], "cells_total": r3["cells_total"],
                     "temperature_rows_not_gradable": {k: v.get("oscillators") for k, v in r3["cells"].items()
                                                       if not v.get("gradable", True)}},
            "row4": {"gradable": r4.get("gradable"), "worst_p99_abs_err_c": r4.get("worst_p99_abs_err_c"),
                     "binding_cell": r4.get("binding_cell"), "grade": r4.get("grade"),
                     "cells_graded": r4.get("cells_graded"), "cells_total": r4.get("cells_total"),
                     "oscillators": r4.get("oscillators"), "oscillators_excluded": r4.get("oscillators_excluded"),
                     "corners_not_graded": {k: v for k, v in (r4.get("cells") or {}).items() if not v.get("gradable", True)}},
            "draws": out["draws"], "seed": out["seed"], "mc_pooled_sigma_lnf": out["mc_pooled_sigma_lnf"]}


def main_freq(mc_path, out_path, reports, draws):
    if not reports:
        raise SystemExit("freq: no reports given")
    out_p = Path(out_path)
    stem = out_p.name.removesuffix(".json")
    per, tables = {}, {"schematic": [], "extracted": []}
    for path in reports:
        osc, rows, d = load_freq_report(path)
        if osc in per:
            raise SystemExit("oscillator %s given twice (%s)" % (osc, path))
        legs, prov = {}, {"report": str(path), "klt_version": (d.get("provenance") or {}).get("klt_version"),
                          "layout": (d.get("provenance") or {}).get("input", {}).get("content_hash"),
                          "extraction_pdk": (d.get("provenance") or {}).get("pdk"),
                          "extracted_netlist": d.get("netlist"), "reference_netlist": d.get("reference_netlist"),
                          "measurement": {k: (d.get("measurement") or {}).get(k) for k in ("command", "timeout_s")}}
        req_path = Path(HERE) / "requests" / ("%s.json" % osc)
        prov["request"] = {"path": str(req_path.relative_to(REPO_ROOT)), "sha256": _sha256_file(req_path)}
        with open(req_path) as f:
            req = json.load(f)
        prov["request"]["analysis"], prov["request"]["options"] = req["analysis"], req.get("options", {})
        for leg in ("schematic", "extracted"):
            freqs, causes, env = leg_frequencies(osc, rows, leg, path)
            if env:
                prov["nested_%s_report" % leg] = env
            legs[leg] = {"resolved": len(freqs), "unresolved": len(rows) - len(freqs), "causes": causes}
            for cid, f in sorted(freqs.items()):
                p, v, t = _siblings.load("pex", "measure_frequency").parse_corner_id(cid)
                tables[leg].append({"osc": osc, "process": p, "vdd": v, "temp_c": t, "f_hz": f})
        per[osc] = {"corners": len(rows), "legs": legs, "provenance": prov}
    missing = [o for o in _SENS.OSCS if o not in per]
    if missing:
        raise SystemExit("freq: no report for %s (the paired comparison needs all five)" % missing)

    # One solve input per leg, then the same solver, seed and draws on both.
    leg_tables, solves = {}, {}
    for leg in ("schematic", "extracted"):
        tp = out_p.with_name("%s-leg-%s.json" % (stem, leg))
        with open(tp, "w") as f:
            json.dump({"kind": "SIMULATED", "rows": sorted(tables[leg], key=lambda r: (r["osc"], r["process"], r["vdd"], r["temp_c"]))}, f, indent=1, sort_keys=True)
            f.write("\n")
        leg_tables[leg] = tp
        sp = out_p.with_name("%s-rows234-%s.json" % (stem, leg))
        solves[leg] = solve_replay(tp, mc_path, sp, draws)

    # Row-2 classifier-coordinate shift: percent change of ln(f_i/f_osc_hd) from schematic to
    # extracted, per cell common to both legs (the count grader's ratio_space_shift_pct, on frequencies).
    freq = {leg: {(r["osc"], r["process"], r["vdd"], r["temp_c"]): r["f_hz"] for r in tables[leg]} for leg in tables}
    shifts = {}
    base = _SENS.BASELINE
    for osc in _SENS.OSCS:
        if osc == base:
            continue
        pct = {}
        for key, sch in freq["schematic"].items():
            if key[0] != osc:
                continue
            ext = freq["extracted"].get(key)
            sch_hd = freq["schematic"].get((base,) + key[1:])
            ext_hd = freq["extracted"].get((base,) + key[1:])
            if None in (sch, ext, sch_hd, ext_hd) or 0 in (sch, ext, sch_hd, ext_hd):
                continue
            pct["%s/%.2fV/%dC" % key[1:]] = 100 * (math.exp(math.log(ext / ext_hd) - math.log(sch / sch_hd)) - 1)
        vals = sorted(pct.values())
        shifts[osc] = {"cells": len(vals), "min": vals[0] if vals else None,
                       "median": statistics.median(vals) if vals else None, "max": vals[-1] if vals else None,
                       "per_cell_pct": pct}

    res = {"kind": "SIMULATED", "draws": solves["schematic"]["draws"], "seed": solves["schematic"]["seed"],
           "mc": {"path": str(mc_path), "sha256": _sha256_file(mc_path),
                  "pooled_sigma_lnf": solves["schematic"]["mc_pooled_sigma_lnf"],
                  "disclosure": "the pooled mismatch model is schematic-side MC data (nominal V/T, #29 reports), applied unchanged to both legs"},
           "row2_coordinate_shift_pct": shifts,
           "oscillators": per, "solve_replay": {leg: _fold_solve(solves[leg]) for leg in solves}}
    with open(out_p, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=str)
        f.write("\n")
    print(json.dumps({"per_oscillator": {o: {leg: (v["legs"][leg]["resolved"], v["legs"][leg]["unresolved"])
                                             for leg in ("schematic", "extracted")} for o, v in per.items()},
                      "row_verdicts": {leg: {"row1": res["solve_replay"][leg]["row1"]["verdict_target"],
                                             "row2": {k: d["verdict"] for k, d in res["solve_replay"][leg]["row2"].items()},
                                             "row3": res["solve_replay"][leg]["row3"]["grade"],
                                             "row4": res["solve_replay"][leg]["row4"]["grade"]}
                                       for leg in solves}}, indent=1, sort_keys=True))
    return 0


def main(out, paths):
    reports = {}
    res = {"kind": "SIMULATED", "inputs": paths, "min_edges_for_oscillation": MIN_EDGES,
           "row1_extracted_side": {}, "ratio_space_shift_pct": {}}
    for osc, cells, window in map(load, paths):
        reports[osc] = cells
        ext = {c: r["extracted_value"] for c, r in cells.items() if r["extracted_value"] is not None}
        bad = sorted(c for c, n in ext.items() if n < MIN_EDGES)
        res["row1_extracted_side"][osc] = {
            "cells_with_extracted_value": len(ext), "cells_below_min_edges": bad,
            "min_count": min(ext.values()), "max_count": max(ext.values()),
            "window_s": window,
            "f_proxy_hz_min_max": [min(ext.values()) / window, max(ext.values()) / window] if window else None,
            "max_startup_bias_rel": (SKIP_EDGES + 1) / min(ext.values()) if min(ext.values()) else None,
            "cells_without_extracted_value": sorted(c for c in cells if c not in ext)}
    hd = reports["osc_hd"]
    for osc, cells in sorted(reports.items()):
        if osc == "osc_hd":
            continue
        sh = []
        for c, r in cells.items():
            h = hd.get(c)
            vals = (r["schematic_value"], r["extracted_value"], h["schematic_value"], h["extracted_value"])
            if None in vals or 0 in vals:  # a zero count has no log-ratio (e.g. a non-oscillating extraction)
                continue
            sh.append((100 * (math.exp(math.log(r["extracted_value"] / h["extracted_value"])
                                       - math.log(r["schematic_value"] / h["schematic_value"])) - 1), c))
        sh.sort()
        res["ratio_space_shift_pct"][osc] = ({
            "cells": len(sh), "min": sh[0], "median": statistics.median(v for v, _ in sh), "max": sh[-1]}
            if sh else {"cells": 0})
    with open(out, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps(res, indent=1, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "freq":
        argv = sys.argv[2:]
        draws = 2000
        if "--draws" in argv:
            i = argv.index("--draws")
            draws, argv = int(argv[i + 1]), argv[:i] + argv[i + 2:]
        if len(argv) < 3:
            raise SystemExit(__doc__)
        sys.exit(main_freq(argv[0], argv[1], argv[2:], draws))
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2:])
