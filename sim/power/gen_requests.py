#!/usr/bin/env python3
"""Write the testbenches and `klt sim` requests for the oscillator-bank power bench (issues #29, #279).

    python3 -I sim/power/gen_requests.py

SIMULATED, schematic-level, oscillator bank only (the counter has no SPICE netlist: its power is NOT covered).
Per oscillator, over the 45-cell box (5 corners x 3 V x 3 T):
  requests/active_<osc>.json  one ring enabled; tran; mean supply current over the second half of the window
  requests/idle_<osc>.json    enable tied to vss; op; supply leakage current
The testbench bodies are derived from the committed sensitivity benches (same oscillator netlists,
same enable convention) so no second copy of the circuit exists. Multi-unit => batch fleet via `klt sim`.

Issue #279 adds the idle re-bench and the gated-divider candidate (records/2026-11-21-idle-settle.md):
  requests/idle_<osc>_settle.json        osc_nmos/osc_wire idle via transient settle (the op-form bench has
                                         a non-unique DC solve on the gated-off ring; see the record)
  requests/xcheck_settle_<osc>_*.json    norshunt / .ic cross-checks on the nine flagged op cells
  cand/osc_subth_gated.spice             en-gated bias-divider candidate, derived from the design netlist
  requests/gated_subth_idle.json         its 45-cell idle grid (op + rshunt), with a tran cross-check set
  requests/gated_subth_active_cells.json its vbp / frequency / start-up A/B at the nominal and cold cells,
                                         against requests/active_osc_subth_cells.json on the unchanged bench
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SENS = os.path.join(HERE, "..", "sensitivity")

# The corner box and windows are defined once, in the sensitivity generator. `python3 -I` drops the
# script directory from sys.path, so the module is loaded by path via the shared sim/ helper.
sys.path.insert(0, os.path.join(HERE, ".."))
import _siblings  # noqa: E402

_SENS_GEN = _siblings.load("sensitivity", "gen_requests")
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


# --- issue #279: idle re-bench (transient settle) -------------------------------------------
#
# The op-form idle bench on the gated-off osc_nmos / osc_wire rings has a non-unique DC solve: after
# "Dynamic gmin stepping failed" ngspice may accept a spurious high-current solution that is not the
# state the circuit reaches from any defined initial state (nine 2026-11-05 cells; see
# records/2026-11-21-idle-settle.md). The settle benches hold `en` at vss for a transient from t=0
# (caps at 0: the ring is powered up gated off, a fully defined initial state) and average i(Vdd)
# over the final half-window. rshunt=1e12 is kept for robustness; the norshunt and .ic cross-check
# requests below agree with it at the nA scale on every flagged cell.
SETTLE = {"osc_nmos": 1000, "osc_wire": 5000}  # tstop ns; flat by ~100 ns (nmos) / ~2 us (wire)
# The nine 2026-11-05 op cells the power record flagged SUSPECT (issue #279 table 1); the cross-check
# requests run only on these.
SUSPECT = {
    "osc_nmos": [("sf", 1.62, 27), ("ff", 1.62, -40), ("ff", 1.80, -40),
                 ("sf", 1.98, -40), ("sf", 1.80, -40)],
    "osc_wire": [("ss", 1.98, -40), ("ss", 1.80, -40), ("ss", 1.62, -40), ("sf", 1.80, -40)],
}
# Every ring node of each bench's DUT, for the .ic cross-check deck (a deliberately "wrong" start:
# all nodes charged to 1.8 V whatever the corner's supply, to show the settled current is the same).
IC_NODES = {
    "osc_nmos": ["n%d" % k for k in range(30)] + ["out"],
    "osc_wire": (["s%d" % k for k in range(31)] + ["n%d" % k for k in range(30)] + ["out"]),
}


def settle_tb_text(osc):
    """Idle settle deck: the idle deck with the settle header (the measurement lives in the request)."""
    body = open(os.path.join(HERE, "tb", "idle_%s.spice" % osc)).read()
    head = ("* Power bench (IDLE, settle): %s with the enable held at vss for the whole window; transient\n"
            "* from t=0 (caps at 0, a defined powered-up-gated-off state); mean supply current over the final\n"
            "* half-window (request .meas). Replaces the op-form idle bench, whose DC solve on the gated-off\n"
            "* ring is non-unique (issue #279; records/2026-11-21-idle-settle.md). SIMULATION, schematic-level.\n") % osc
    return head + body[len("* Power bench (IDLE): %s with the enable tied to vss; supply leakage current. "
                           "SIMULATION, schematic-level.\n" % osc):]


def settle_request(osc):
    tstop = SETTLE[osc]
    r = request(osc, True)
    r["netlist"] = "../tb/idle_%s_settle.spice" % osc
    r["analysis"] = {"kind": "tran", "args": "10n %dn" % tstop}
    r["measurements"] = [
        {"name": "i_vdd", "spice": ".meas tran i_vdd avg i(Vdd) from=%dn to=%dn" % (tstop // 2, tstop), "unit": "A"},
        {"name": "i_vdd_early", "spice": ".meas tran i_vdd_early avg i(Vdd) from=%dn to=%dn"
                                          % (tstop // 4, tstop // 2), "unit": "A"},
    ]
    return r


def xcheck_request(osc, variant):
    """Cross-check the settle bench on the flagged cells: norshunt (rshunt removed) or ic (all ring
    nodes started at 1.8 V). Same window and measurement as the settle request it checks."""
    r = settle_request(osc)
    r["netlist"] = "../tb/xcheck_settle_%s_%s.spice" % (osc, variant)
    if variant == "norshunt":
        body = re.sub(r"^\.options rshunt=1e12\n", "", open(os.path.join(HERE, "tb", "idle_%s_settle.spice" % osc)).read(),
                      count=1, flags=re.M)
    else:
        body = open(os.path.join(HERE, "tb", "idle_%s_settle.spice" % osc)).read()
        body += ".ic " + " ".join("v(%s)=1.8" % ("out" if n == "out" else "xdut." + n) for n in IC_NODES[osc]) + "\n"
    with open(os.path.join(HERE, "tb", "xcheck_settle_%s_%s.spice" % (osc, variant)), "w") as f:
        f.write(body)
    del r["measurements"][1]  # one window is enough for a cross-check
    r["corners"] = {"units": [{"process": p, "temperature_c": t, "supply_v": {"vdd": v}}
                              for p, v, t in SUSPECT[osc]]}
    return r


# Review follow-up (PR #295, findings 2 and 6): a defined ZERO start (`uic`, every ring node 0 V) at the nine
# suspect cells, and a converged shunt-sensitivity check at the two ss / -40 C osc_wire cells whose norshunt
# cross-check failed. The plain settle bench starts from the DC operating point, which is exactly the
# non-unique solve under suspicion, so it cannot establish a zero start; `uic` skips the DC solve.
SHUNT_CELLS = {"osc_wire": [("ss", 1.62, -40), ("ss", 1.80, -40)]}
SHUNT_VARIANTS = {"shunt13": "1e13", "shunt14": "1e14"}


def xcheck2_text(osc, variant):
    body = open(os.path.join(HERE, "tb", "idle_%s_settle.spice" % osc)).read()
    if variant == "zero":
        body += ".ic " + " ".join("v(%s)=0" % ("out" if n == "out" else "xdut." + n) for n in IC_NODES[osc]) + "\n"
    else:
        body = body.replace(".options rshunt=1e12\n", ".options rshunt=%s\n" % SHUNT_VARIANTS[variant], 1)
        assert ".options rshunt=%s" % SHUNT_VARIANTS[variant] in body
    return body


def xcheck2_request(osc, variant):
    """`zero`: tran with `uic` and every ring node at 0 V, on the suspect cells. `shunt13`/`shunt14`: the
    settle bench with a larger shunt resistance (less shunt current), on the cells the norshunt run lost."""
    r = settle_request(osc)
    r["netlist"] = "../tb/xcheck_settle_%s_%s.spice" % (osc, variant)
    del r["measurements"][1]
    if variant == "zero":
        r["analysis"] = {"kind": "tran", "args": "10n %dn uic" % SETTLE[osc]}
        cells = SUSPECT[osc]
    else:
        cells = SHUNT_CELLS[osc]
    r["corners"] = {"units": [{"process": p, "temperature_c": t, "supply_v": {"vdd": v}} for p, v, t in cells]}
    return r


# --- issue #279: isolated OFF-device probes (PR #295 finding 6) ---------------------------------
#
# One deck, one instance per probed device geometry, each with its own source so a single .meas per
# device reports the OFF current at Vgs=0, |Vds|=vdd: the numbers the idle record cites for the dominant
# leakage devices and for the candidate's switch. Instances use the ring geometries (design/osc_bank/).
PROBE_DEVICES = [  # (label, model, W, L)
    ("p_wire_stage", "pfet_01v8", 8.0, 0.15), ("p_nmos_stage", "pfet_01v8", 3.0, 0.15),
    ("p_subth_stage", "pfet_01v8", 0.84, 0.15), ("p_subth_lvt", "pfet_01v8_lvt", 0.42, 0.5),
    ("n_stage", "nfet_01v8", 4.0, 0.15), ("n_enstack", "nfet_01v8", 0.84, 0.5),
    ("n_long", "nfet_01v8", 0.42, 0.5), ("n_gate_switch", "nfet_01v8", 1.0, 0.15),
]
PROBE_CELLS = [("fs", 1.98, 125), ("ff", 1.98, 125), ("ss", 1.98, 125), ("fs", 1.98, -40)]


def probe_tb_text():
    ln = ["* Isolated OFF-device probes (PR #295 finding 6): each device at Vgs=0, |Vds|=vdd, body at its rail;",
          "* a 0 V sense source per device so one .meas per device reports its OFF current (positive out of",
          "* the supply). SIMULATION, schematic-level single devices; geometries are the ring/candidate ones.",
          "Vdd vdd 0 1.8", "Vss vss 0 0"]
    for lab, mod, w, l in PROBE_DEVICES:
        ln.append("Vm_%s vdd m_%s 0" % (lab, lab))
        if mod.startswith("pfet"):  # source=m, gate=vdd (Vgs=0), drain=vss, body=vdd
            ln.append("XM_%s vss vdd m_%s vdd sky130_fd_pr__%s L=%s W=%s nf=1 mult=1 m=1" % (lab, lab, mod, l, w))
        else:  # drain=m, gate=vss, source=vss, body=vss
            ln.append("XM_%s m_%s vss vss vss sky130_fd_pr__%s L=%s W=%s nf=1 mult=1 m=1" % (lab, lab, mod, l, w))
    return "\n".join(ln) + "\n"


def probe_request():
    b = request("osc_subth", True)
    r = {"netlist": "../tb/probe_off_devices.spice", "engine": b["engine"], "models": b["models"],
         "options": b["options"], "batch": b["batch"], "backend": b["backend"],
         "corners": {"units": [{"process": p, "temperature_c": t, "supply_v": {"vdd": v}} for p, v, t in PROBE_CELLS]},
         "analysis": {"kind": "op", "args": ""},
         "measurements": [{"name": "i_%s" % lab, "expr": "i(Vm_%s)" % lab, "unit": "A"} for lab, *_ in PROBE_DEVICES]}
    return r


def op_probe_request(variant):
    """Single-unit op probe of the 2026-11-05 suspect cell osc_nmos sf / 1.62 V / 27 C on the committed
    op-form idle deck. `a`: i(Vdd) only; `b`: i(Vdd) plus three node voltages (a different measurement
    set on the identical deck). One unit, so `klt sim` keeps it local."""
    r = request("osc_nmos", True)
    r["corners"] = {"units": [{"process": "sf", "temperature_c": 27, "supply_v": {"vdd": 1.62}}]}
    if variant == "b":
        r["measurements"] += [{"name": "v_out", "expr": "v(out)", "unit": "V"},
                              {"name": "v_n0", "expr": "v(xdut.n0)", "unit": "V"},
                              {"name": "v_n1", "expr": "v(xdut.n1)", "unit": "V"}]
    return r


# --- issue #279: en-gated osc_subth bias-divider candidate ----------------------------------
#
# Candidate netlist only (adoption is a follow-up issue): the design netlist with the divider return
# Rb1 routed to vss through an en-gated nfet (W=1.0/L=0.15; ~1-2 kOhm against the 1.8 MOhm string).
# design/osc_bank/ is NOT touched (item-1 / LVS / pex evidence depends on it).
GATED_HEADER = [
    "* CANDIDATE netlist for issue #279 -- NOT a design file, NOT item-1 evidence, never adopted here.",
    "* Derived from design/osc_bank/osc_subth.spice (left untouched) by exactly one edit: the bias",
    "* divider return Rb1 goes to vss through en-gated nfet switch XMsw1 (W=1.0/L=0.15; on-resistance",
    "* ~1-2 kOhm against the 1.8 MOhm divider string, ~1-2 mV drop), cutting the ~1 uA divider",
    "* current when en is low. SIMULATED, schematic-level, no layout. Adoption is a follow-up",
    "* issue: it invalidates the osc_subth rows 1-4 / Monte Carlo / layout / LVS / pex evidence.",
]


def gated_subth_text():
    src = open(os.path.join(HERE, "..", "..", "design", "osc_bank", "osc_subth.spice")).read().splitlines()
    out = []
    for ln in src:
        if ln.startswith("** sch_path:"):
            out.extend(GATED_HEADER)
        elif ln.startswith(".subckt osc_subth "):
            out.append(ln.replace(".subckt osc_subth ", ".subckt osc_subth_gated "))
        elif ln.startswith("Rb1 vbp vss 1500k m=1"):
            out.append("Rb1 vbp vsw 1500k m=1")
            out.append("XMsw1 vsw en vss vss sky130_fd_pr__nfet_01v8 L=0.15 W=1.0 nf=1 ad=0.29 as=0.29 pd=2.58 ps=2.58")
            out.append("+ nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 mult=1 m=1")
        else:
            out.append(ln)
    return "\n".join(out) + "\n"


GATED_IDLE_BODY = """* Power bench (IDLE, candidate): osc_subth_gated with the enable tied to vss; supply leakage current.
* op + rshunt=1e12 (with the divider gated off, vbp has no DC path); tran cross-checked in
* requests/gated_subth_idle_tran_xcheck.json. SIMULATION, schematic-level, candidate netlist.
.options rshunt=1e12
.include "../cand/osc_subth_gated.spice"
Vdd vdd 0 1.8
Vss vss 0 0
Ven en 0 0
Xdut en out vdd vss osc_subth_gated
"""

GATED_ACTIVE_BODY = """* Power bench (ACTIVE, candidate): osc_subth_gated enabled; mean supply current, vbp bias and
* start-up after en rises. SIMULATION, schematic-level, candidate netlist (issue #279).
* Enable is the sensitivity benches' behavioural source (off for 1 ns, ramp 100 ps).
.include "../cand/osc_subth_gated.spice"
Vdd vdd 0 1.8
Vss vss 0 0
Ben en 0 V='v(vdd)*min(max((time-1n)/100p,0),1)'
Xdut en out vdd vss osc_subth_gated
"""


def gated_units():
    """Nominal cell + the cold cells: 5 corners x 3 V at -40 C, tt/1.80/27 first (16 units)."""
    cells = [("tt", 1.80, 27)]
    for p in PROCESS:
        for v in VDD:
            cells.append((p, v, -40))
    return [{"process": p, "temperature_c": t, "supply_v": {"vdd": v}} for p, v, t in cells]


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
    # issue #279: settle idle benches + cross-checks + the gated-divider candidate benches
    os.makedirs(os.path.join(HERE, "cand"), exist_ok=True)
    with open(os.path.join(HERE, "cand", "osc_subth_gated.spice"), "w") as f:
        f.write(gated_subth_text())
    for osc in SETTLE:
        with open(os.path.join(HERE, "tb", "idle_%s_settle.spice" % osc), "w") as f:
            f.write(settle_tb_text(osc))
        with open(os.path.join(HERE, "requests", "idle_%s_settle.json" % osc), "w") as f:
            json.dump(settle_request(osc), f, indent=2)
            f.write("\n")
        for variant in ("norshunt", "ic"):
            with open(os.path.join(HERE, "requests", "xcheck_settle_%s_%s.json" % (osc, variant)), "w") as f:
                json.dump(xcheck_request(osc, variant), f, indent=2)
                f.write("\n")
    variants = [(o, "zero") for o in SETTLE] + [(o, v) for o in SHUNT_CELLS for v in SHUNT_VARIANTS]
    for osc, variant in variants:
        with open(os.path.join(HERE, "tb", "xcheck_settle_%s_%s.spice" % (osc, variant)), "w") as f:
            f.write(xcheck2_text(osc, variant))
        with open(os.path.join(HERE, "requests", "xcheck_settle_%s_%s.json" % (osc, variant)), "w") as f:
            json.dump(xcheck2_request(osc, variant), f, indent=2)
            f.write("\n")
    for v in ("a", "b"):
        with open(os.path.join(HERE, "requests", "probe_op_osc_nmos_sf162_%s.json" % v), "w") as f:
            json.dump(op_probe_request(v), f, indent=2)
            f.write("\n")
    with open(os.path.join(HERE, "tb", "probe_off_devices.spice"), "w") as f:
        f.write(probe_tb_text())
    with open(os.path.join(HERE, "requests", "probe_off_devices.json"), "w") as f:
        json.dump(probe_request(), f, indent=2)
        f.write("\n")
    with open(os.path.join(HERE, "tb", "gated_subth_idle.spice"), "w") as f:
        f.write(GATED_IDLE_BODY)
    with open(os.path.join(HERE, "tb", "gated_subth_active.spice"), "w") as f:
        f.write(GATED_ACTIVE_BODY)
    with open(os.path.join(HERE, "tb", "gated_subth_idle_tran.spice"), "w") as f:
        f.write(GATED_IDLE_BODY.replace("op + rshunt=1e12 (with the divider gated off, vbp has no DC path); tran cross-checked in\n"
                                        "* requests/gated_subth_idle_tran_xcheck.json.",
                                        "transient settle form (rshunt=1e12 kept): en held at vss from t=0; final-half mean.")
                 .replace("(IDLE, candidate)", "(IDLE, candidate, tran settle)"))
    # gated idle: 45-cell op grid + a 16-cell tran cross-check (nominal + 5 corners x cold/room/hot)
    r = request("osc_subth", True)
    r["netlist"] = "../tb/gated_subth_idle.spice"
    with open(os.path.join(HERE, "requests", "gated_subth_idle.json"), "w") as f:
        json.dump(r, f, indent=2)
        f.write("\n")
    cells = [{"process": "tt", "temperature_c": 27, "supply_v": {"vdd": 1.80}}]
    for p in PROCESS:
        for v, t in ((1.62, -40), (1.80, 27), (1.98, 125)):
            if (p, v, t) != ("tt", 1.80, 27):
                cells.append({"process": p, "temperature_c": t, "supply_v": {"vdd": v}})
    r = {"netlist": "../tb/gated_subth_idle_tran.spice", "engine": "ngspice",
         "models": r["models"], "options": r["options"], "batch": r["batch"], "backend": r["backend"],
         "corners": {"units": cells},
         "analysis": {"kind": "tran", "args": "10n 500000n"},
         "measurements": [
             {"name": "i_vdd", "spice": ".meas tran i_vdd avg i(Vdd) from=250000n to=500000n", "unit": "A"},
             {"name": "vbp_f", "spice": ".meas tran vbp_f find v(xdut.vbp) at=500000n", "unit": "V"}]}
    with open(os.path.join(HERE, "requests", "gated_subth_idle_tran_xcheck.json"), "w") as f:
        json.dump(r, f, indent=2)
        f.write("\n")
    # active A/B on the nominal + cold cells: gated candidate vs the unchanged design bench
    r = request("osc_subth", False)
    r["corners"] = {"units": gated_units()}
    # The same measurement set on BOTH benches. Edge timestamps (`t_rise` crossings, cap 400) give the
    # oscillator frequency and first output edge via sensitivity/analyze.py freq_from_crossings; the vbp
    # samples give bias settling separately (PR #295 finding 4): vbp_avg is the settled reference, the
    # timed samples show when vbp is within tolerance of it.
    r["measurements"] = r["measurements"] + [
        {"name": "vbp_avg", "spice": ".meas tran vbp_avg avg v(xdut.vbp) from=1000000n to=2000000n", "unit": "V"}] + [
        {"name": "vbp_%s" % t, "spice": ".meas tran vbp_%s find v(xdut.vbp) at=%s" % (t, t), "unit": "V"}
        for t in ("2n", "5n", "10n", "20n", "50n", "100n", "1u")]
    with open(os.path.join(HERE, "requests", "active_osc_subth_cells.json"), "w") as f:
        json.dump(r, f, indent=2)
        f.write("\n")
    r["netlist"] = "../tb/gated_subth_active.spice"
    with open(os.path.join(HERE, "requests", "gated_subth_active_cells.json"), "w") as f:
        json.dump(r, f, indent=2)
        f.write("\n")
