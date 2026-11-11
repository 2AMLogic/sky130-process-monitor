#!/usr/bin/env python3
"""Grade the committed `klt pex` reports against the #29 row-1 criterion and summarise the layout shift (issue #32).

    grade_pex.py OUT.json REPORT.pex.report.json [...]

SIMULATED, post-processing only (no simulation). Pure stdlib. Reads each report's per-cell `delta` rows.
The pex scalar is the `t_rise` crossings measurement (rising edges of v(out) at VDD/2 in a fixed 800 ns window);
it is a quantised edge COUNT, not a frequency, and the report carries no crossing times, so #29's
f_osc = (n-1)/(t_last - t_first) (analyze.freq_from_crossings) cannot be reproduced from it.
What this script can state exactly is:
  * row 1 (oscillates): analyze.py drops SKIP_EDGES=3 start-up edges and needs MIN_CYCLES=5 cycles, i.e. at least
    SKIP_EDGES + MIN_CYCLES + 1 = 9 rising edges. A cell passes iff its extracted-side count is >= 9.
  * a frequency proxy f ~ count / 800 ns, with relative bias bounded by (SKIP_EDGES + 1) / count (start-up edges
    included, +/- 1 count quantisation). Reported as a proxy, never as an f_osc.
  * ratio-space shift: #29 row 2 classifies on ln f_i - ln f_osc_hd. The extracted-vs-schematic change of that
    coordinate is ln(ext_i/ext_hd) - ln(sch_i/sch_hd), computed from the counts where both legs exist.
No threshold is applied or changed: rows 2-4 are NOT re-graded (see sim/pex/README.md).
"""
import json
import math
import statistics
import sys

SKIP_EDGES, MIN_CYCLES, WINDOW_S = 3, 5, 800e-9
MIN_EDGES = SKIP_EDGES + MIN_CYCLES + 1


def load(path):
    with open(path) as f:
        d = json.load(f)
    osc = d["testbenches"][0]["request"]["path"].rsplit("/", 1)[-1][:-5]
    return osc, {r["corner_id"]: r for r in d["delta"]}


def main(out, paths):
    reports = dict(load(p) for p in paths)
    res = {"kind": "SIMULATED", "inputs": paths, "min_edges_for_oscillation": MIN_EDGES, "window_s": WINDOW_S,
           "row1_extracted_side": {}, "ratio_space_shift_pct": {}}
    for osc, cells in sorted(reports.items()):
        ext = {c: r["extracted_value"] for c, r in cells.items() if r["extracted_value"] is not None}
        bad = sorted(c for c, n in ext.items() if n < MIN_EDGES)
        res["row1_extracted_side"][osc] = {
            "cells_with_extracted_value": len(ext), "cells_below_min_edges": bad,
            "min_count": min(ext.values()), "max_count": max(ext.values()),
            "f_proxy_hz_min_max": [min(ext.values()) / WINDOW_S, max(ext.values()) / WINDOW_S],
            "max_startup_bias_rel": (SKIP_EDGES + 1) / min(ext.values()),
            "cells_without_extracted_value": sorted(c for c in cells if c not in ext)}
    hd = reports["osc_hd"]
    for osc, cells in sorted(reports.items()):
        if osc == "osc_hd":
            continue
        sh = []
        for c, r in cells.items():
            h = hd.get(c)
            if None in (r["schematic_value"], r["extracted_value"], h["schematic_value"], h["extracted_value"]):
                continue
            sh.append((100 * (math.exp(math.log(r["extracted_value"] / h["extracted_value"])
                                       - math.log(r["schematic_value"] / h["schematic_value"])) - 1), c))
        sh.sort()
        res["ratio_space_shift_pct"][osc] = {
            "cells": len(sh), "min": sh[0], "median": statistics.median(v for v, _ in sh), "max": sh[-1]}
    with open(out, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps(res, indent=1, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
