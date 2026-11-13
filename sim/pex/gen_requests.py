"""Write sim/pex/osc/*.spice and sim/pex/requests/<osc>.json: the klt pex testbenches and requests
(T1 item 7, analog; issue #32).

Each request is the #29 45-cell grid request for the oscillator (sim/sensitivity/requests/grid_<osc>.json,
same analysis window, measurement, solver options and corner box) with only the testbench body
swapped for sim/pex/osc/tb_<osc>.spice (one .include, as klt pex requires). Deterministic.
Usage: python3 -I sim/pex/gen_requests.py

The testbench bodies are derived from the committed sensitivity benches (sim/sensitivity/osc/tb_<osc>.spice)
so no second copy of the circuit exists, the way sim/power/gen_requests.py already does. That is what makes
the pex comparison meaningful: the schematic leg of `klt pex` runs the same bench the #29 grid ran, and an
edit to the enable source or the supplies in sim/sensitivity/osc/ cannot leave these benches behind.

The committed bytes are the contract. Every dated report under records/ names its bench and records its
`netlist_sha256`, so a one-byte change here invalidates recorded evidence: this generator must reproduce
the committed files byte for byte. If a run leaves `git status --porcelain sim/pex` non-empty, that is a
finding to report, not a file to commit. (requests/osc_nmos_coldcell.json and requests/osc_wire_coldcell.json
are hand-written and deliberately not emitted here - see README.md "Cold-cell follow-up".)
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(HERE)
SENS = os.path.join(SIM, "sensitivity", "requests")
SENS_OSC = os.path.join(SIM, "sensitivity", "osc")
DESIGN = os.path.join(os.path.dirname(SIM), "design", "osc_bank")
# `python3 -I` drops the script directory from sys.path, so load the sensitivity generator by path.
_spec = importlib.util.spec_from_file_location(
    "sens_gen_requests", os.path.join(SIM, "sensitivity", "gen_requests.py"))
_SENS_GEN = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_SENS_GEN)
OSCS = list(_SENS_GEN.OSCS)  # the oscillator list lives once, in the sensitivity generator

# Line 2 of a sensitivity bench states what the netlist is. On the pex side the same body is run against
# the klt pex schematic-side DUT, and only the single .include is re-pointed to the extracted netlist for
# the other leg, so that clause is swapped. osc_hd is the exception: its committed bench keeps the
# sensitivity wording and is distinguished by the .include/pin-order rewrite below instead. The committed
# bytes are hashed in the records, so that asymmetry is reproduced, not tidied.
SENS_PROVENANCE = ", no layout, no parasitics."
PEX_PROVENANCE = ", the klt pex schematic-side DUT; the extracted leg re-points the single .include."

# osc_hd: the extracted subcircuit's pin order follows the layout's label order (out en vss vdd) and
# `klt pex --pins` does not reorder it, while the schematic is `en out vdd vss`. klt pex reuses the
# testbench's X line byte-for-byte on both sides, so the schematic-side DUT file is a self-contained
# wrapper that presents the schematic under the extracted pin order. The design netlist is copied
# verbatim except for the subcircuit name (osc_hd -> osc_hd_sch); nothing else is edited. The bench
# therefore carries one .include (the wrapper) in place of the sensitivity bench's two, and the Xdut
# line is written in the extracted pin order.
HD_INCLUDES = ('.include "$PDK_ROOT/sky130A/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice"\n'
               '.include "../../../design/osc_bank/osc_hd.spice"\n')
HD_DUT_INCLUDE = '\n.include "osc_hd_dut.spice"\n'
HD_XDUT = "Xdut en out vdd vss osc_hd\n"
HD_XDUT_PEX = "Xdut out en vss vdd osc_hd\n"

# The cold-cell probe variants: the same bench plus the #69 relaxed solver options, nothing else.
RELAXED = ("osc_nmos", "osc_wire")
RELAXED_TAIL = (
    "* Probe variant (issue #32): same bench plus relaxed solver options, as #69's tb_osc_wire_probe.spice.\n"
    ".options reltol=0.01 gmin=1e-10 method=gear\n")


def tb_text(osc):
    """The pex testbench body for `osc`, derived from the committed sensitivity bench."""
    with open(os.path.join(SENS_OSC, "tb_%s.spice" % osc)) as f:
        body = f.read()
    if osc == "osc_hd":
        assert body.count(HD_INCLUDES) == 1, "the two .include lines were not found in the osc_hd sensitivity bench"
        body = body.replace(HD_INCLUDES, HD_DUT_INCLUDE)
        assert body.count(HD_XDUT) == 1, "the Xdut line was not found in the osc_hd sensitivity bench"
        body = body.replace(HD_XDUT, HD_XDUT_PEX)
    else:
        assert body.count(SENS_PROVENANCE) == 1, "the provenance clause was not found in the %s sensitivity bench" % osc
        body = body.replace(SENS_PROVENANCE, PEX_PROVENANCE)
    return body


def relaxed_text(osc):
    """The cold-cell probe variant of the pex bench for `osc`."""
    return tb_text(osc) + RELAXED_TAIL


def dut_text():
    """The schematic-side DUT wrapper for osc_hd (see the HD_* comment above)."""
    with open(os.path.join(DESIGN, "osc_hd.spice")) as f:
        core = f.read()
    assert core.count(".subckt osc_hd ") == 1, "the osc_hd subcircuit was not found in the design netlist"
    core = core.replace(".subckt osc_hd ", ".subckt osc_hd_sch ")
    return ("* GENERATED by sim/pex/gen_requests.py - do not edit. Schematic-side DUT for klt pex (osc_hd).\n"
            "* design/osc_bank/osc_hd.spice, subckt renamed osc_hd_sch, wrapped under the extracted pin order.\n"
            '.include "$PDK_ROOT/sky130A/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice"\n'
            + core
            + "\n.subckt osc_hd out en vss vdd\nXsch en out vdd vss osc_hd_sch\n.ends osc_hd\n")


def request(osc):
    """The #29 grid request for `osc` with only the testbench body swapped."""
    with open(os.path.join(SENS, "grid_%s.json" % osc)) as f:
        r = json.load(f)
    r["netlist"] = "../osc/tb_%s.spice" % osc
    r["batch"] = dict(r.get("batch", {}), capacity_wait_s=600)
    return r


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "osc"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "requests"), exist_ok=True)
    with open(os.path.join(HERE, "osc", "osc_hd_dut.spice"), "w") as f:
        f.write(dut_text())
    for o in OSCS:
        with open(os.path.join(HERE, "osc", "tb_%s.spice" % o), "w") as f:
            f.write(tb_text(o))
        with open(os.path.join(HERE, "requests", "%s.json" % o), "w") as f:
            json.dump(request(o), f, indent=2)
            f.write("\n")
    for o in RELAXED:
        with open(os.path.join(HERE, "osc", "tb_%s_relaxed.spice" % o), "w") as f:
            f.write(relaxed_text(o))
