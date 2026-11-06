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
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SENS = os.path.join(HERE, "..", "sensitivity")


def _load_sensitivity():
    """The corner box and windows are defined once, in the sensitivity generator. `python3 -I` drops the
    script directory from sys.path, so load it by path."""
    spec = importlib.util.spec_from_file_location("sens_gen_requests", os.path.join(SENS, "gen_requests.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_SENS_GEN = _load_sensitivity()
PROCESS, VDD, TEMP = _SENS_GEN.PROCESS, _SENS_GEN.VDD, _SENS_GEN.TEMP
_UNIT_NS = {"p": 1e-3, "n": 1.0, "u": 1e3, "m": 1e6}


def _ns(tok):
    return int(round(float(tok[:-1]) * _UNIT_NS[tok[-1]]))


# osc -> (tstop in ns, tran step string), parsed from the sensitivity "tstep tstop" window strings
WINDOWS = {}
for _osc, (_tran, _cap) in _SENS_GEN.OSCS.items():
    _step, _tstop = _tran.split()
    WINDOWS[_osc] = (_ns(_tstop), _step)
EN_RE = re.compile(r"^Ben en 0 .*$", re.M)
# Oscillators whose first fleet run left a few -40 C cells with `timestep too small` / failed gmin stepping
# (floating nodes with the ring gated off). A 1e12 ohm shunt on every node gives them a DC path; it adds ~2 pA per
# node at 1.8 V, negligible against the uA-scale active and nA-scale idle currents it is compared to. Recorded in the
# power record as a bench option, not a model change.
RSHUNT = {"osc_nmos", "osc_wire"}


def tb_text(osc, idle):
    body = open(os.path.join(SENS, "osc", "tb_%s.spice" % osc)).read()
    assert EN_RE.search(body), "enable source line not found in the sensitivity bench"
    if idle:
        body = EN_RE.sub("Ven en 0 0", body)
        head = "* Power bench (IDLE): %s with the enable tied to vss; supply leakage current. SIMULATION, schematic-level.\n" % osc
    else:
        head = "* Power bench (ACTIVE): %s enabled; mean supply current. SIMULATION, schematic-level.\n" % osc
    if osc in RSHUNT:
        body = re.sub(r"^(\.include)", ".options rshunt=1e12\n\\1", body, count=1, flags=re.M)
    return head + body


def request(osc, idle):
    tstop_ns, step = WINDOWS[osc]
    b = _SENS_GEN.base(osc, "%s %dn" % (step, tstop_ns), 0)
    r = {
        "netlist": "../tb/%s_%s.spice" % ("idle" if idle else "active", osc),
        "engine": b["engine"],
        "models": b["models"],
        "options": b["options"],
        "batch": b["batch"],
        "backend": b["backend"],
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
