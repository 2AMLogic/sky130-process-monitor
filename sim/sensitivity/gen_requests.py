#!/usr/bin/env python3
"""Write the `klt sim` request JSONs for the sensitivity bench (deterministic; re-run to regenerate).

    python3 -I sim/sensitivity/gen_requests.py

Per oscillator: requests/grid_<osc>.json  (5 corners x 3 V x 3 T = the 45-cell box, spec "PVT corner box")
                requests/mc_<osc>.json    (mismatch Monte Carlo, nominal 1.80 V/27 C cell, 5 corners x N samples;
                                           off-nominal cells are requests/mc_offnom_*.json)
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
# (host rule: scope the run, land it, file the remainder): 20 samples and its own window/timeout.
# The (V,T) cell is MC_VT for every oscillator.
MC_OVERRIDE = {"osc_subth": {"tran": "10n 500u", "n": 20, "timeout_s": 300}}


def mc(osc, tran, cap):
    ov = MC_OVERRIDE.get(osc, {})
    tran = ov.get("tran", MC_TRAN.get(osc, tran))
    n = ov.get("n", MC_N)
    r = base(osc, tran, cap)
    r["options"]["timeout_s"] = ov.get("timeout_s", r["options"]["timeout_s"])
    r["corners"] = {"units": [
        {"process": p, "temperature_c": t, "supply_v": {"vdd": v}}
        for p in PROCESS for (v, t) in MC_VT]}
    # mismatch_scale=1 writes `.param mc_mm_switch=1` after the .lib (nominal sigma), per the spec.
    r["monte_carlo"] = {"n": n, "seed": MC_SEED, "vary": "mismatch", "mismatch_scale": 1,
                        "seed_scope": "point"}
    return r


# Off-nominal MC (issue #48): the 1.62 V/125 C and 1.98 V/-40 C cells, 5 corners each. 500 units per
# oscillator did not fit a session on the fleet (~45 s/unit model load), so n is scoped per oscillator
# (stated in the record). osc_subth gets one request per cell because the cold cell needs a longer window.
OFFNOM_VT = [(1.62, 125), (1.98, -40)]
OFFNOM_N = {"osc_hd": 30, "osc_nmos": 20, "osc_pmos": 30, "osc_wire": 30, "osc_subth": 10}
OFFNOM_SUBTH = {(1.62, 125): ("10n 500u", 300), (1.98, -40): ("10n 2m", 900)}


def mc_offnom(osc, tran, cap, vt_cells=OFFNOM_VT, subth_cell=None):
    """Same request shape as mc() (same seed, mismatch_scale=1) on the off-nominal (V,T) cells."""
    tran = MC_TRAN.get(osc, tran)
    n = OFFNOM_N[osc]
    timeout = 3000
    if osc == "osc_subth":
        tran, timeout = OFFNOM_SUBTH[subth_cell]
        vt_cells = [subth_cell]
    r = base(osc, tran, cap)
    r["options"]["timeout_s"] = timeout
    r["corners"] = {"units": [
        {"process": p, "temperature_c": t, "supply_v": {"vdd": v}}
        for p in PROCESS for (v, t) in vt_cells]}
    r["monte_carlo"] = {"n": n, "seed": MC_SEED, "vary": "mismatch", "mismatch_scale": 1,
                        "seed_scope": "point"}
    return r


# Step-refined osc_hd (issue #54): the 20 ps (MC) / 10 ps (grid) tran step biases osc_hd and locks the
# ff period to the step grid (records/2026-11-05-mc-offnom-partial.md section 1). These requests cap the
# max step at 5 ps ("tstep tstop tstart tmax"), keep the coarse windows, n and seed, and are written
# under NEW names (*_5p.json); the coarse requests are never rewritten with these.
HD_5P_GRID_TRAN = "5p 300n 0 5p"
HD_5P_MC_TRAN = "5p 100n 0 5p"


def hd_5p_requests():
    """name -> request for the three step-refined osc_hd runs (same corners/units/n/seed as the coarse ones)."""
    cap = OSCS["osc_hd"][1]
    g = grid("osc_hd", HD_5P_GRID_TRAN, cap)
    m = mc("osc_hd", "", cap)
    m["analysis"]["args"] = HD_5P_MC_TRAN
    o = mc_offnom("osc_hd", "", cap)
    o["analysis"]["args"] = HD_5P_MC_TRAN
    return {"grid_osc_hd_5p.json": g, "mc_osc_hd_5p.json": m, "mc_offnom_osc_hd_5p.json": o}


# Cold-cell completion (issue #48): the 1.98 V/-40 C sf grid cells for osc_subth / osc_wire were missing from
# the 2026-11-05 grid (sf osc_subth shows <2.5 kHz, i.e. fewer than 5 cycles in 2 ms; osc_wire hit
# `timestep too small`), and the sf osc_subth MC samples were all lost to the 2 ms window. These are new
# requests under new names; the existing requests are never rewritten with these.
COLD = (1.98, -40)
COLD_SF_SUBTH_TRAN = "10n 10m"
COLD_SF_WIRE_TRAN = "50p 2.5u 0 20p"  # tmax capped at 20 ps (the 2.5u grid request used the default step)


def cold_sf_requests():
    """name -> request for the sf cold-cell grid points (osc_subth, osc_wire) and the osc_subth sf cold MC."""
    v, t = COLD
    unit = [{"process": "sf", "temperature_c": t, "supply_v": {"vdd": v}}]
    g_sub = base("osc_subth", COLD_SF_SUBTH_TRAN, OSCS["osc_subth"][1])
    g_sub["options"]["timeout_s"] = 3480  # fleet whole-job ceiling is 3600 s
    g_sub["corners"] = {"units": unit}
    g_wire = base("osc_wire", COLD_SF_WIRE_TRAN, OSCS["osc_wire"][1])
    g_wire["corners"] = {"units": unit}
    m_sub = mc_offnom("osc_subth", "", OSCS["osc_subth"][1], subth_cell=COLD)
    m_sub["analysis"]["args"] = COLD_SF_SUBTH_TRAN
    m_sub["options"]["timeout_s"] = 3480  # fleet whole-job ceiling is 3600 s
    m_sub["corners"] = {"units": unit}
    return {"grid_osc_subth_sf_cold.json": g_sub, "grid_osc_wire_sf_cold.json": g_wire,
            "mc_offnom_osc_subth_sf_1.98V_-40C.json": m_sub}


if __name__ == "__main__":
    out = os.path.join(HERE, "requests")
    os.makedirs(out, exist_ok=True)
    for name, req in list(hd_5p_requests().items()) + list(cold_sf_requests().items()):
        with open(os.path.join(out, name), "w") as f:
            json.dump(req, f, indent=2)
            f.write("\n")
    for osc, (tran, cap) in OSCS.items():
        for kind, fn in (("grid", grid), ("mc", mc)):
            with open(os.path.join(out, "%s_%s.json" % (kind, osc)), "w") as f:
                json.dump(fn(osc, tran, cap), f, indent=2)
                f.write("\n")
        # off-nominal MC requests (issue #48)
        if osc == "osc_subth":
            for cell in OFFNOM_VT:
                name = "mc_offnom_%s_%gV_%dC.json" % (osc, cell[0], cell[1])
                with open(os.path.join(out, name), "w") as f:
                    json.dump(mc_offnom(osc, tran, cap, subth_cell=cell), f, indent=2)
                    f.write("\n")
        else:
            with open(os.path.join(out, "mc_offnom_%s.json" % osc), "w") as f:
                json.dump(mc_offnom(osc, tran, cap), f, indent=2)
                f.write("\n")
