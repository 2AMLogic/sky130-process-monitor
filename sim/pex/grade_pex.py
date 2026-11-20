#!/usr/bin/env python3
"""Grade the committed `klt pex` reports against the #29 row-1 criterion and summarise the layout shift (issue #32).

    grade_pex.py OUT.json REPORT.pex.report.json [...]

SIMULATED, post-processing only (no simulation). Pure stdlib. Reads each report's per-cell `delta` rows.
The pex scalar is the `t_rise` crossings measurement (rising edges of v(out) at VDD/2 in the request's transient window);
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
No threshold is applied or changed: rows 2-4 are NOT re-graded (see sim/pex/README.md).
"""
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The oscillation rule lives once, in sensitivity/analyze.py (as sim/pex/gen_requests.py already does for
# the oscillator list). `python3 -I` drops the script directory from sys.path, so the module is loaded
# by path via the shared sim/ helper (the bare name `analyze` is ambiguous in the tree).
sys.path.insert(0, os.path.join(HERE, ".."))
import _siblings  # noqa: E402

_SENS = _siblings.load("sensitivity", "analyze")
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
    main(sys.argv[1], sys.argv[2:])
