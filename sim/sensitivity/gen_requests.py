#!/usr/bin/env python3
"""Write the `klt sim` request JSONs for the sensitivity bench (deterministic; re-run to regenerate).

    python3 -I sim/sensitivity/gen_requests.py

Per oscillator: requests/grid_<osc>.json  (5 corners x 3 V x 3 T = the 45-cell box, spec "PVT corner box")
                requests/mc_<osc>.json    (mismatch Monte Carlo, 15 cells x N samples)
Frequency is read from the rising-edge crossing times of v(out) at mid-rail (`crossings`), so
the start-up skip and cycle count are chosen in analyze.py, not frozen into a .meas card.
Submit with: klt sim --batch-set sim/sensitivity/requests/grid_*.json -o <dir> --report-out ...
(multi-unit => batch fleet; never hand-launch ngspice for these).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OSCS = {
    # name: (tran "tstep tstop", n_crossings cap). Windows sized from the single tt records in
    # measurements/osc_bank_records.jsonl with ~8-10x margin for ss / 1.62 V / low-T slowdowns.
    "osc_hd": ("10p 300n", 400),
    "osc_nmos": ("20p 800n", 400),
    "osc_pmos": ("50p 2.5u", 400),
    "osc_wire": ("50p 2.5u", 400),
    "osc_subth": ("20n 2m", 400),
}
PROCESS = ["tt", "ff", "ss", "sf", "fs"]
VDD = [1.62, 1.80, 1.98]
TEMP = [-40, 27, 125]
# mismatch Monte Carlo cells. Issue #8 step 5 asks for five corners x {1.80 V/27 C, 1.62 V/125 C,
# 1.98 V/-40 C}; per-unit wall time on the fleet is ~45 s whatever the window (model load), so 750 units
# per oscillator do not fit a session. Scoped (host rule: scope, land, file the remainder) to the
# nominal cell; the two off-nominal cells are the follow-up issue named in the record.
MC_VT = [(1.80, 27)]
# shorter MC windows, sized from the grid minimum f per oscillator with >=2x margin (records/ grid table)
MC_TRAN = {"osc_hd": "20p 100n", "osc_nmos": "40p 250n", "osc_pmos": "100p 600n", "osc_wire": "100p 500n"}
MC_N = 50
MC_SEED = 20261105


def base(osc, tran, cap):
    return {
        "netlist": "../osc/tb_%s.spice" % osc,
        "engine": "ngspice",
        "models": {"pdk": "sky130A", "lib": "libs.tech/ngspice/sky130.lib.spice"},
        "analysis": {"kind": "tran", "args": tran},
        "measurements": [{
            "name": "t_rise",
            "unit": "s",
            "crossings": {"signal": "v(out)", "level": {"frac_of": "vdd", "fraction": 0.5},
                          "edge": "rise", "max": cap},
        }],
        "options": {"timeout_s": 3000, "retry_on_convergence_error": True}, "batch": {"job_ceiling_check": "warn"},
        "backend": "batch",
    }


def grid(osc, tran, cap):
    r = base(osc, tran, cap)
    r["corners"] = {
        "process": PROCESS,
        "supply_v": {"vdd": VDD},
        "temperature_c": TEMP,
    }
    return r


# osc_subth costs 50-420 s per unit (kHz-scale period), so its MC is scoped to fit a session
# (host rule: scope the run, land it, file the remainder): one (V,T) cell, 20 samples, own window.
SUBTH_MC = {"tran": "10n 500u", "vt": [(1.80, 27)], "n": 20, "timeout_s": 300}


def mc(osc, tran, cap):
    vt, n = MC_VT, MC_N
    tran = MC_TRAN.get(osc, tran)
    if osc == "osc_subth":
        tran, vt, n = SUBTH_MC["tran"], SUBTH_MC["vt"], SUBTH_MC["n"]
    r = base(osc, tran, cap)
    if osc == "osc_subth":
        r["options"]["timeout_s"] = SUBTH_MC["timeout_s"]
    r["corners"] = {"units": [
        {"process": p, "temperature_c": t, "supply_v": {"vdd": v}}
        for p in PROCESS for (v, t) in vt]}
    # mismatch_scale=1 writes `.param mc_mm_switch=1` after the .lib (nominal sigma), per the spec.
    r["monte_carlo"] = {"n": n, "seed": MC_SEED, "vary": "mismatch", "mismatch_scale": 1,
                        "seed_scope": "point"}
    return r


if __name__ == "__main__":
    out = os.path.join(HERE, "requests")
    os.makedirs(out, exist_ok=True)
    for osc, (tran, cap) in OSCS.items():
        for kind, fn in (("grid", grid), ("mc", mc)):
            with open(os.path.join(out, "%s_%s.json" % (kind, osc)), "w") as f:
                json.dump(fn(osc, tran, cap), f, indent=2)
                f.write("\n")
