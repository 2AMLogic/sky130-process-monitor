#!/usr/bin/env python3
"""Build the `model-run` evidence envelope for T1 item 5 (analog) from the committed row records (issues #29, #277).

    python3 -I sim/solve/make_envelope.py -o evidence/item5_analog.json

Reads sim/solve/records/2026-11-21-rows1-4-fulltable.json (the full-table re-grade of issue #277; the
2026-11-05 reduced-table record it supersedes remains committed, unedited) and
sim/power/records/2026-11-05-power-grade-complete.json. SIMULATED. Limits are the ratified TARGET bounds
from spec/target-spec.md, copied unchanged; nothing is relaxed. Each measurement is the worst graded
value, so a row that misses its target is recorded failing and the item grades unmet.
"""
import argparse
import hashlib
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
R14 = "sim/solve/records/2026-11-21-rows1-4-fulltable.json"
PWR = "sim/power/records/2026-11-05-power-grade-complete.json"


def sha(p):
    return "sha256:" + hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest()


def meas(name, unit, value, mx, cell, note):
    ok = value <= mx
    return {"name": name, "unit": unit, "limits": {"max": mx}, "status": "pass" if ok else "fail",
            "worst_case": {"corner_id": cell, "value": value, "margin": mx - value}, "note": note}


def build():
    a = json.load(open(os.path.join(ROOT, R14)))
    p = json.load(open(os.path.join(ROOT, PWR)))
    r1 = a["row1"]["target_bank_5"]
    r2 = a["row2_ratio"]["target_5_corner"]
    g3, g4 = a["row3"]["grade"], a["row4"]["grade"]
    lo = a["row1"]["lowest_f_cell"]
    ms = [
        meas("row1_non_oscillating_cells", "cells", len(r1["missing_cells"]), 0,
             "%d of %d cells resolve; lowest f %g Hz at %s %g V/%d C"
             % (r1["cells_checked"] - len(r1["missing_cells"]), r1["cells_checked"], lo["f_hz"],
                lo["cell"][0], lo["cell"][2], lo["cell"][3]),
             "spec row 1 target: oscillates at all 45 cells; two of the fills rest on relaxed-solver values (see record)"),
        meas("row2_unidentified_vt_cells", "cells", r2["total_cells"] - r2["identified_cells"], 0, "1.98 V / 27 C",
             "spec row 2 target: five-corner identification; fallback (slow/fast) passes"),
        meas("row3_p99_abs_dv", "V", a["row3"]["worst_p99_abs_err_v"], 0.020, a["row3"]["binding_cell"],
             "spec row 3 target +-20 mV; fallback +-50 mV %s" % g3["fallback"].lower()),
        meas("row4_p99_abs_dt", "C", a["row4"]["worst_p99_abs_err_c"], 5.0, a["row4"]["binding_cell"],
             "spec row 4 target +-5 C; %d of %d cells graded"
             % (a["row4"]["cells_graded"], a["row4"]["cells_total"])),
        meas("row7_active_power_osc_only", "uW", p["active"]["worst_uW"], 100.0, p["active"]["binding_cell"],
             "oscillator only; COUNTER POWER NOT COVERED; %d of %d cells graded" % (p["active"]["cells_graded"], p["active"]["cells_expected"])),
        meas("row7_idle_power_osc_bank", "uW", p["idle"]["worst_uW"], 1.0, p["idle"]["binding_cell"],
             "oscillator bank only; counter power NOT covered; the binding figure is a suspect osc_nmos DC point (see record); "
             "the verdict holds without it (osc_subth ungated bias alone is 1.8 uW at tt/1.80 V/27 C)"),
    ]
    return {
        "schema_version": 1, "kind": "model-run", "status": "fail",
        "method": "post-processing of the full-table rows 1-4 re-grade (#277; fleet grids plus five single-cell cold runs) "
                  "plus klt sim power benches (row 7); SIMULATED, schematic-level, ngspice-46/47, sky130A",
        "t1_item": 5, "measurements": ms,
        "inputs": {R14: sha(R14), PWR: sha(PWR)},
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", required=True)
    args = ap.parse_args()
    with open(args.o, "w") as f:
        json.dump(build(), f, indent=1, sort_keys=True)
        f.write("\n")
