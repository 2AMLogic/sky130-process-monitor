#!/usr/bin/env python3
"""Write the testbenches and `klt sim` requests for the oscillator-bank power bench (issue #29, spec row 7).

    python3 -I sim/power/gen_requests.py

SIMULATED, schematic-level, oscillator bank only (the counter has no SPICE netlist: its power is NOT covered).
Per oscillator, over the 45-cell box (5 corners x 3 V x 3 T):
  requests/active_<osc>.json  one ring enabled; tran; mean supply current over the second half of the window
  requests/idle_<osc>.json    enable tied to vss; op; supply leakage current
The testbench bodies are derived from the committed sensitivity benches (same oscillator netlists,
same enable convention) so no second copy of the circuit exists. Multi-unit => batch fleet via `klt sim`.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SENS = os.path.join(HERE, "..", "sensitivity")
# (tstop in ns, tran step string) copied from sim/sensitivity/gen_requests.py windows
WINDOWS = {
    "osc_hd": (300, "10p"),
    "osc_nmos": (800, "20p"),
    "osc_pmos": (2500, "50p"),
    "osc_wire": (2500, "50p"),
    "osc_subth": (2000000, "20n"),
}
PROCESS = ["tt", "ff", "ss", "sf", "fs"]
VDD = [1.62, 1.80, 1.98]
TEMP = [-40, 27, 125]
EN_RE = re.compile(r"^Ben en 0 .*$", re.M)


def tb_text(osc, idle):
    body = open(os.path.join(SENS, "osc", "tb_%s.spice" % osc)).read()
    assert EN_RE.search(body), "enable source line not found in the sensitivity bench"
    if idle:
        body = EN_RE.sub("Ven en 0 0", body)
        head = "* Power bench (IDLE): %s with the enable tied to vss; supply leakage current. SIMULATION, schematic-level.\n" % osc
    else:
        head = "* Power bench (ACTIVE): %s enabled; mean supply current. SIMULATION, schematic-level.\n" % osc
    return head + body


def request(osc, idle):
    tstop_ns, step = WINDOWS[osc]
    r = {
        "netlist": "../tb/%s_%s.spice" % ("idle" if idle else "active", osc),
        "engine": "ngspice",
        "models": {"pdk": "sky130A", "lib": "libs.tech/ngspice/sky130.lib.spice"},
        "options": {"timeout_s": 3000, "retry_on_convergence_error": True},
        "batch": {"job_ceiling_check": "warn"},
        "backend": "batch",
        "corners": {"process": PROCESS, "supply_v": {"vdd": VDD}, "temperature_c": TEMP},
    }
    if idle:
        r["analysis"] = {"kind": "op", "args": ""}
        r["measurements"] = [{"name": "i_vdd", "expr": "i(Vdd)", "unit": "A"}]
    else:
        r["analysis"] = {"kind": "tran", "args": "%s %dn" % (step, tstop_ns)}
        r["measurements"] = [
            {"name": "i_avg", "spice": ".meas tran i_avg avg i(Vdd) from=%dn to=%dn" % (tstop_ns // 2, tstop_ns), "unit": "A"},
            {"name": "t_rise", "unit": "s",
             "crossings": {"signal": "v(out)", "level": {"frac_of": "vdd", "fraction": 0.5}, "edge": "rise", "max": 400}},
        ]
    return r


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "tb"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "requests"), exist_ok=True)
    for osc in WINDOWS:
        for idle in (False, True):
            kind = "idle" if idle else "active"
            with open(os.path.join(HERE, "tb", "%s_%s.spice" % (kind, osc)), "w") as f:
                f.write(tb_text(osc, idle))
            with open(os.path.join(HERE, "requests", "%s_%s.json" % (kind, osc)), "w") as f:
                json.dump(request(osc, idle), f, indent=2)
                f.write("\n")
