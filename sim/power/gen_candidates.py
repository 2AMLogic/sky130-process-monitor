#!/usr/bin/env python3
"""Write the ACTIVE-power iteration benches and requests (issue #280, spec row 7 active power).

    python3 -I sim/power/gen_candidates.py [carried-candidate ...]

Everything here is SIMULATED, schematic-level, oscillator-only (no counter netlist). The committed
design netlists are NOT edited: a sizing or stage-count change lands only through a spec/decisions/
record. This generator writes bench-side EXPERIMENT VARIANTS so the levers can be measured first:

  tb/cand/<name>.spice           variant `.subckt` (one lever moved from the committed design point;
                                 the base parameters reproduce the committed netlist -- asserted)
  tb/active_cand_<name>.spice    deck body for a variant (same bench shape as tb/active_osc_*.spice)
  requests/probe_<osc>.json      single-corner decomposition probe at the oscillator's binding cell
                                 (supply energy, frequency, stage-node swing, and for the wire ring
                                 driver-output vs post-RC crossings)
  requests/cand_<name>.json      single-corner screen of one candidate at its oscillator's binding cell
  requests/candgrid_<name>.json  the 45-cell active power + frequency box for a carried candidate
  requests/gap_*.json            fresh single-cell runs for the six ungraded active cells

Bench conventions (window, enable, rshunt, request envelope) come from gen_requests.py, which stays
the owner of the committed 2026-11-05 bench; nothing it writes is rewritten here.
Grid and gap requests go to the batch fleet via `klt sim --batch-set --wait-for-capacity 600`;
single-corner probes/screens run locally (`klt sim <req> --backend local`).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.join(HERE, "..", "..", "design", "osc_bank")

sys.path.insert(0, os.path.join(HERE, ".."))
import _siblings  # noqa: E402

_POWER = _siblings.load("power", "gen_requests")
WINDOWS = _POWER.WINDOWS  # osc -> (tstop_ns, step)
PROCESS, VDD, TEMP = _POWER.PROCESS, _POWER.VDD, _POWER.TEMP
RSHUNT = _POWER.RSHUNT

# Binding cell per oscillator: the worst graded active cell in the committed table
# sim/power/records/2026-11-05-power-table-complete.json (re-verified by analyze_iteration.py).
BINDING = {
    "osc_hd": ("ff", 1.98, 125),
    "osc_nmos": ("ff", 1.98, -40),
    "osc_pmos": ("ff", 1.98, 125),
    "osc_wire": ("ff", 1.98, -40),
    "osc_subth": ("ff", 1.98, 125),
}

# ---------------------------------------------------------------------------
# sky130 discrete-FET geometry as emitted by the committed xschem netlists
# (verified against design/osc_bank/*.spice for every W they contain):
#   ad = as = 0.29*W   pd = ps = 2*W + 0.58   nrd = nrs = 0.29/W


def _g(x):
    return "%.12g" % x


def fet(inst, nodes, model, w, l):
    ad = 0.29 * w
    pd = 2 * w + 0.58
    nrd = 0.29 / w
    return ("%s %s sky130_fd_pr__%s L=%s W=%s nf=1 ad=%s as=%s pd=%s ps=%s nrd=%s nrs=%s sd=0 mult=1 m=1"
            % (inst, " ".join(nodes), model, _g(l), _g(w), _g(ad), _g(ad), _g(pd), _g(pd), _g(nrd), _g(nrd)))


def pfet(inst, nodes, w, l=0.15):
    return fet(inst, nodes, "pfet_01v8", w, l)


def nfet(inst, nodes, w, l=0.15):
    return fet(inst, nodes, "nfet_01v8", w, l)


# ---------------------------------------------------------------------------
# Variant netlists, mirroring the committed topology stage for stage:
#   osc_wire  NAND(en,out)->s0, then per stage R into a node with a shunt C; the LAST stage's RC node
#             IS `out` (R501 s30 out / C504 out vss). n counts the RC stages (NAND + n-1 inverters).
#   osc_nmos / osc_pmos  NAND(en,out)->n0 then n-1 inverters, the last driving `out` directly (no RC).
#   osc_hd   nand2_1(en,out)->n0 then n-1 inv_1, the last driving `out`.
# The enable NAND (stage 0) keeps its committed geometry in every variant; the levers move only the
# n-1 identical inverter stages (and their R/C), so one lever at a time changes exactly one thing.

def wire_variant(name, wp=8.0, wn=4.0, r_l=1000, c_f=100.0, n=31):
    out = [".subckt %s en out vdd vss" % name,
           pfet("XMp1", ["s0", "out", "vdd", "vdd"], 8.0),
           pfet("XMp6", ["s0", "en", "vdd", "vdd"], 8.0),
           nfet("XMn11", ["s0", "out", "mid", "vss"], 8.0),
           nfet("XMn16", ["mid", "en", "vss", "vss"], 8.0),
           "R21 s0 n0 sky130_fd_pr__res_generic_m1 W=0.14 L=%s m=1" % _g(r_l),
           "C24 n0 vss %sf m=1" % _g(c_f)]
    for k in range(1, n):
        drv, nxt = "s%d" % k, ("n%d" % k if k < n - 1 else "out")
        out += [pfet("XMp%d" % (100 + 4 * k), [drv, "n%d" % (k - 1), "vdd", "vdd"], wp),
                nfet("XMn%d" % (110 + 4 * k), [drv, "n%d" % (k - 1), "vss", "vss"], wn),
                "R%d %s %s sky130_fd_pr__res_generic_m1 W=0.14 L=%s m=1" % (200 + 4 * k, drv, nxt, _g(r_l)),
                "C%d %s vss %sf m=1" % (300 + 4 * k, nxt, _g(c_f))]
    out.append(".ends")
    return out


def fet_ring_variant(name, kind, weak_w=0.42, weak_l=0.5, strong_w=3.0, n=31):
    """osc_nmos (kind='nmos'): strong pfet pull-up (strong_w, L=0.15) over a weak long nfet pull-down
    (weak_w, weak_l); committed point 3.0 / 0.42 / 0.5. osc_pmos is the mirror."""
    out = [".subckt %s en out vdd vss" % name]
    if kind == "nmos":
        out += [pfet("XMp1", ["n0", "out", "vdd", "vdd"], 3.0),
                pfet("XMp6", ["n0", "en", "vdd", "vdd"], 3.0),
                nfet("XMn11", ["n0", "out", "mid", "vss"], 0.84, 0.5),
                nfet("XMn16", ["mid", "en", "vss", "vss"], 0.84, 0.5)]
    else:
        out += [pfet("XMp1", ["n0", "out", "vdd", "vdd"], 0.42, 0.5),
                pfet("XMp6", ["n0", "en", "vdd", "vdd"], 0.42, 0.5),
                nfet("XMn11", ["n0", "out", "mid", "vss"], 6.0),
                nfet("XMn16", ["mid", "en", "vss", "vss"], 6.0)]
    for k in range(1, n):
        drv = "n%d" % k if k < n - 1 else "out"
        if kind == "nmos":
            out += [pfet("XMp%d" % (100 + 2 * k), [drv, "n%d" % (k - 1), "vdd", "vdd"], strong_w),
                    nfet("XMn%d" % (110 + 2 * k), [drv, "n%d" % (k - 1), "vss", "vss"], weak_w, weak_l)]
        else:
            out += [pfet("XMp%d" % (100 + 2 * k), [drv, "n%d" % (k - 1), "vdd", "vdd"], weak_w, weak_l),
                    nfet("XMn%d" % (110 + 2 * k), [drv, "n%d" % (k - 1), "vss", "vss"], strong_w)]
    out.append(".ends")
    return out


def hd_variant(name, n=31):
    out = [".subckt %s en out vdd vss" % name,
           "x0 out en vss vss vdd vdd n0 sky130_fd_sc_hd__nand2_1"]
    for k in range(1, n):
        nxt = "n%d" % k if k < n - 1 else "out"
        out.append("x%d n%d vss vss vdd vdd %s sky130_fd_sc_hd__inv_1" % (k, k - 1, nxt))
    out.append(".ends")
    return out


# The candidate list: one lever at a time from the committed design point. The base entry regenerates
# the committed netlist and exists so the parity assertion covers every generator, not just levers.
CANDIDATES = {
    "wire": {"osc": "osc_wire",
             "levers": {"base": {}, "c050": {"c_f": 50.0}, "c025": {"c_f": 25.0},
                        "r005": {"r_l": 500}, "r002": {"r_l": 2000},
                        "w04": {"wp": 4.0, "wn": 2.0}, "w02": {"wp": 2.0, "wn": 1.0},
                        "n021": {"n": 21}, "n061": {"n": 61},
                        "r004": {"r_l": 4000},
                        "r002w02": {"r_l": 2000, "wp": 2.0, "wn": 1.0},
                        "r004w02": {"r_l": 4000, "wp": 2.0, "wn": 1.0}},
             "make": wire_variant},
    "nmos": {"osc": "osc_nmos",
             "levers": {"base": {}, "l10": {"weak_l": 1.0}, "l20": {"weak_l": 2.0},
                        "l30": {"weak_l": 3.0},
                        "wp015": {"strong_w": 1.5}, "n021": {"n": 21}},
             "make": lambda tag: fet_ring_variant("osc_nmos_%s" % tag, "nmos", **LEVERS["nmos"][tag])},
    "pmos": {"osc": "osc_pmos",
             "levers": {"base": {}, "l10": {"weak_l": 1.0}, "l20": {"weak_l": 2.0},
                        "wn015": {"strong_w": 1.5}, "n021": {"n": 21}},
             "make": lambda tag: fet_ring_variant("osc_pmos_%s" % tag, "pmos", **LEVERS["pmos"][tag])},
    "hd": {"osc": "osc_hd",
           "levers": {"base": {}, "n021": {"n": 21}, "n061": {"n": 61}},
           "make": hd_variant},
}
LEVERS = {k: v["levers"] for k, v in CANDIDATES.items()}


def make_variant(fam, tag):
    spec = CANDIDATES[fam]
    if fam in ("wire", "hd"):
        return spec["make"]("osc_%s_%s" % (fam, tag), **spec["levers"][tag])
    return spec["make"](tag)


# ---------------------------------------------------------------------------
# Canonical device comparison: proves the base variant of each generator is device-for-device the
# committed design netlist (instance names / whitespace / line wrapping aside), so every candidate
# differs from the design by exactly its lever.

def canonical_devices(text):
    """Sorted multiset of canonical device entries: (kind, positional tokens lowercased, sorted numeric params)."""
    entries, cur = [], []

    def flush():
        if not cur:
            return
        positional = tuple(t.lower() for t in cur[1:] if "=" not in t)
        params = dict((kv.split("=", 1)[0].lower(), round(float(kv.split("=", 1)[1]), 9))
                      for kv in cur if "=" in kv)
        # sa/sb (and sd) default to 0 in the sky130 fd_pr wrappers; the committed netlists state
        # them inconsistently (hand-edited stages carry sa=0 sb=0, generated ones omit them), so
        # the parity check compares them as their electrical value, absent == 0.
        for k in ("sa", "sb"):
            params.setdefault(k, 0.0)
        entries.append((cur[0][0].lower(), positional, tuple(sorted(params.items()))))
        del cur[:]

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("*") or line.startswith("."):
            flush()
            continue
        if line.startswith("+"):
            cur.extend(line[1:].split())
        else:
            flush()
            cur.extend(line.split())
    flush()
    return sorted(entries)


def assert_parity():
    for fam, spec in CANDIDATES.items():
        osc = spec["osc"]
        gen = make_variant(fam, "base")
        want = open(os.path.join(DESIGN, "%s.spice" % osc)).read()
        a, b = canonical_devices("\n".join(gen)), canonical_devices(want)
        if a != b:
            raise AssertionError("%s base variant != design %s.spice\n only in variant: %s\n only in design: %s"
                                 % (fam, osc, [e for e in a if e not in b][:3], [e for e in b if e not in a][:3]))


# ---------------------------------------------------------------------------
# Requests

def _meas_common(osc, half_ns):
    """Probes/screens: supply energy over the settled half window, mean current (the committed
    convention), output frequency, internal stage-node swing; the wire family additionally gets the
    driver-output and post-RC crossing series for the RC-fraction-of-stage-delay measurement."""
    tstop_ns = 2 * half_ns
    m = [{"name": "e_vdd", "energy": {"source": "Vdd", "voltage": "v(vdd)",
                                      "from": "%dn" % half_ns, "to": "%dn" % tstop_ns}},
         {"name": "i_avg", "spice": ".meas tran i_avg avg i(Vdd) from=%dn to=%dn" % (half_ns, tstop_ns), "unit": "A"},
         {"name": "t_rise", "unit": "s",
          "crossings": {"signal": "v(out)", "level": {"frac_of": "vdd", "fraction": 0.5},
                        "edge": "rise", "max": 400}},
         {"name": "t_n1", "unit": "s",
          "crossings": {"signal": "v(xdut.n1)", "level": {"frac_of": "vdd", "fraction": 0.5},
                        "edge": "rise", "max": 400}},
         {"name": "vhi_n1", "spice": ".meas tran vhi_n1 max v(xdut.n1) from=%dn to=%dn" % (half_ns, tstop_ns), "unit": "V"},
         {"name": "vlo_n1", "spice": ".meas tran vlo_n1 min v(xdut.n1) from=%dn to=%dn" % (half_ns, tstop_ns), "unit": "V"}]
    if osc == "osc_wire":
        m += [{"name": "t_s1", "unit": "s",
               "crossings": {"signal": "v(xdut.s1)", "level": {"frac_of": "vdd", "fraction": 0.5},
                             "edge": "rise", "max": 400}},
              {"name": "vhi_s1", "spice": ".meas tran vhi_s1 max v(xdut.s1) from=%dn to=%dn" % (half_ns, tstop_ns), "unit": "V"},
              {"name": "vlo_s1", "spice": ".meas tran vlo_s1 min v(xdut.s1) from=%dn to=%dn" % (half_ns, tstop_ns), "unit": "V"}]
    return m


def _grid_meas(osc, half_ns):
    """Grid requests keep the committed active measurements (i_avg + t_rise crossings) and add the
    wire driver/post-RC crossings and driver swing so the RC fraction stays visible per cell."""
    tstop_ns = 2 * half_ns
    m = [{"name": "i_avg", "spice": ".meas tran i_avg avg i(Vdd) from=%dn to=%dn" % (half_ns, tstop_ns), "unit": "A"},
         {"name": "t_rise", "unit": "s",
          "crossings": {"signal": "v(out)", "level": {"frac_of": "vdd", "fraction": 0.5},
                        "edge": "rise", "max": 400}}]
    if osc == "osc_wire":
        m += [{"name": "t_s1", "unit": "s",
               "crossings": {"signal": "v(xdut.s1)", "level": {"frac_of": "vdd", "fraction": 0.5},
                             "edge": "rise", "max": 400}},
              {"name": "t_n1", "unit": "s",
               "crossings": {"signal": "v(xdut.n1)", "level": {"frac_of": "vdd", "fraction": 0.5},
                             "edge": "rise", "max": 400}},
              {"name": "vhi_s1", "spice": ".meas tran vhi_s1 max v(xdut.s1) from=%dn to=%dn" % (half_ns, tstop_ns), "unit": "V"},
              {"name": "vlo_s1", "spice": ".meas tran vlo_s1 min v(xdut.s1) from=%dn to=%dn" % (half_ns, tstop_ns), "unit": "V"}]
    return m


def _request(netlist, tran, corners, meas, timeout_s=3000):
    return {"netlist": netlist, "engine": "ngspice",
            "models": {"pdk": "sky130A", "lib": "libs.tech/ngspice/sky130.lib.spice"},
            "options": {"timeout_s": timeout_s, "retry_on_convergence_error": True},
            "batch": {"job_ceiling_check": "warn"}, "backend": "batch",
            "corners": corners,
            "analysis": {"kind": "tran", "args": tran},
            "measurements": meas}


def _units(cells):
    return {"units": [{"process": p, "temperature_c": t, "supply_v": {"vdd": v}} for p, v, t in cells]}


def _box():
    return {"process": PROCESS, "supply_v": {"vdd": VDD}, "temperature_c": TEMP}


def all_requests():
    """name -> request for the probes, screens and gap cells (grids are added by write_all)."""
    out = {}
    for osc, (p, v, t) in BINDING.items():
        tstop_ns, step = WINDOWS[osc]
        out["probe_%s.json" % osc] = _request(
            "../tb/active_%s.spice" % osc, "%s %dn" % (step, tstop_ns),
            _units([(p, v, t)]), _meas_common(osc, tstop_ns // 2))
    for fam, spec in CANDIDATES.items():
        osc = spec["osc"]
        p, v, t = BINDING[osc]
        tstop_ns, step = WINDOWS[osc]
        for tag in spec["levers"]:
            if tag == "base":
                continue
            name = "%s_%s" % (fam, tag)
            out["cand_%s.json" % name] = _request(
                "../tb/active_cand_%s.spice" % name, "%s %dn" % (step, tstop_ns),
                _units([(p, v, t)]), _meas_common(osc, tstop_ns // 2))
    out.update(gap_requests())
    return out


def grid_requests(carried):
    out = {}
    for name in carried:
        fam = name.split("_", 1)[0]
        osc = CANDIDATES[fam]["osc"]
        tstop_ns, step = WINDOWS[osc]
        out["candgrid_%s.json" % name] = _request(
            "../tb/active_cand_%s.spice" % name, "%s %dn" % (step, tstop_ns),
            _box(), _grid_meas(osc, tstop_ns // 2))
    return out


# The six ungraded active cells (record 2026-11-05-power-complete.md). Windows sized from the
# committed sensitivity surface (grid_osc_subth*.json.gz: the cold slow cells run at ~0.2-2.5 kHz;
# the committed 2 ms window resolved at most 6 edges) with >=2x margin over 9 crossings at each
# cell's measured or extrapolated frequency; tstep is coarser than the committed 20n because these
# rings have ms-scale periods (>=90 samples/period). The wire cell re-runs the committed bench with
# tmax capped at 20p -- the fix that resolved the same abort at sf/1.98 V/-40 C
# (sim/sensitivity/gen_requests.py COLD_SF_WIRE_TRAN).
GAPS = {
    "gap_osc_wire_sf_1.62V_-40C.json": ("../tb/active_osc_wire.spice", "50p 2500n 0 20p",
                                        [("sf", 1.62, -40)], 3000),
    "gap_osc_subth_ss_1.62V_-40C.json": ("../tb/active_osc_subth.spice", "10u 20m",
                                         [("ss", 1.62, -40)], 3480),
    "gap_osc_subth_ss_1.80V_-40C.json": ("../tb/active_osc_subth.spice", "10u 10m",
                                         [("ss", 1.80, -40)], 3480),
    "gap_osc_subth_sf_1.62V_-40C.json": ("../tb/active_osc_subth.spice", "20u 100m",
                                         [("sf", 1.62, -40)], 3480),
    "gap_osc_subth_sf_1.80V_-40C.json": ("../tb/active_osc_subth.spice", "10u 40m",
                                         [("sf", 1.80, -40)], 3480),
    "gap_osc_subth_sf_1.98V_-40C.json": ("../tb/active_osc_subth.spice", "10u 20m",
                                         [("sf", 1.98, -40)], 3480),
}

_UNIT_NS = {"p": 1e-3, "n": 1.0, "u": 1e3, "m": 1e6}


def _half(tok):
    """Half of a SPICE time literal, as a same-scale literal (i_avg measures the settled half)."""
    val, suf = float(tok[:-1]), tok[-1]
    half_ns = val * _UNIT_NS[suf] / 2.0
    for s, scale in (("m", 1e6), ("u", 1e3)):
        if half_ns / scale >= 1:
            return "%g%s" % (half_ns / scale, s)
    return "%gn" % half_ns


def gap_requests():
    out = {}
    for name, (netlist, tran, cells, tmo) in GAPS.items():
        tstop_tok = tran.split()[1]
        out[name] = _request(
            netlist, tran, _units(cells),
            [{"name": "i_avg", "spice": ".meas tran i_avg avg i(Vdd) from=%s to=%s"
              % (_half(tstop_tok), tstop_tok), "unit": "A"},
             {"name": "t_rise", "unit": "s",
              "crossings": {"signal": "v(out)", "level": {"frac_of": "vdd", "fraction": 0.5},
                            "edge": "rise", "max": 400}}],
            timeout_s=tmo)
    return out


def deck_text(name, osc):
    subckt = "osc_%s" % name
    body = ["* ACTIVE-power candidate bench: %s (EXPERIMENT VARIANT, not the committed design)." % name,
            "* Same bench shape as tb/active_%s.spice; the variant subckt differs from" % osc,
            "* design/osc_bank/%s.spice by exactly the lever recorded in the iteration record." % osc]
    if osc == "osc_hd":
        body.append('.include "$PDK_ROOT/sky130A/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice"')
    if osc in RSHUNT:
        body.append(".options rshunt=1e12")
    body += ['.include "cand/%s.spice"' % name,
             "Vdd vdd 0 1.8",
             "Vss vss 0 0",
             "Ben en 0 V='v(vdd)*min(max((time-1n)/100p,0),1)'",
             "Xdut en out vdd vss %s" % subckt]
    return "\n".join(body) + "\n"


def write_all(carried=None):
    assert_parity()
    os.makedirs(os.path.join(HERE, "tb", "cand"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "requests"), exist_ok=True)
    written = []
    for fam, spec in CANDIDATES.items():
        for tag in spec["levers"]:
            name = "%s_%s" % (fam, tag)
            with open(os.path.join(HERE, "tb", "cand", "%s.spice" % name), "w") as f:
                f.write("* EXPERIMENT VARIANT subckt for the row-7 active-power iteration (issue #280).\n")
                f.write("* Lever %s from the committed design point (the empty lever is the base, which\n"
                        "* reproduces design/osc_bank/%s.spice; asserted by gen_candidates.py).\n"
                        % (json.dumps(spec["levers"][tag], sort_keys=True), spec["osc"]))
                f.write("\n".join(make_variant(fam, tag)) + "\n")
            if tag != "base":
                with open(os.path.join(HERE, "tb", "active_cand_%s.spice" % name), "w") as f:
                    f.write(deck_text(name, spec["osc"]))
                written.append("tb/active_cand_%s.spice" % name)
    reqs = all_requests()
    if carried:
        reqs.update(grid_requests(carried))
    for name, req in sorted(reqs.items()):
        with open(os.path.join(HERE, "requests", name), "w") as f:
            json.dump(req, f, indent=2)
            f.write("\n")
        written.append("requests/%s" % name)
    return written


if __name__ == "__main__":
    carried = sys.argv[1:] or None
    for w in write_all(carried):
        print(w)
