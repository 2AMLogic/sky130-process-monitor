#!/usr/bin/env python3
"""Generate the osc_subth cold-corner design-iteration decks, testbench bodies and
`klt sim` requests (issue #278; deterministic -- re-run to regenerate, `--check` to
verify the committed files).

    python3 -I sim/subthreshold/variants/gen_variants.py           # write everything
    python3 -I sim/subthreshold/variants/gen_variants.py --check   # verify no drift

Every variant deck is a text transformation of the committed baseline
`design/osc_bank/osc_subth.spice` (15 stages: enable NAND + 14 starved inverters, each
starved through a series `pfet_01v8_lvt` L=0.5 W=0.42 header gated at `vbp`, biased from
the Rb0/Rb1 resistive divider) with exactly ONE factor changed, so the per-lever sweeps
of the record compare like against like:

    vbp_2_3  divider ratio  Rb0 300k->600k, Rb1 1500k->1200k (vbp 0.8333->0.6667 VDD);
             total divider resistance stays 1.8 M, isolating the bias point from the
             divider current
    vbp_1_2  divider ratio  Rb0 900k, Rb1 900k (vbp 0.5 VDD); total still 1.8 M
    hw3      header W/L     header W 0.42->1.26 (x3), L=0.5 unchanged
    hl35     header W/L     header L 0.5->0.35 (the model bin floor: the pfet_01v8_lvt
             discrete bins in this open_pdks install have no L below 0.35 -- L=0.25 and
             L=0.15 fail with ngspice "could not find a valid modelname", verified
             locally on the pinned models), W=0.42 unchanged
    st11     stage count    15->11 stages (NAND + 10 starved; stage 10 drives `out`);
             odd stage count preserved including the enable NAND

The testbench bodies are the sensitivity bench's `tb_osc_subth.spice` verbatim except
the include line, so the VDD/2-crossing extraction of `sim/sensitivity/analyze.py`
applies unchanged. Grid requests use the baseline grid window (`20n 2m`, cap 400); the
mismatch MC follows `sim/subthreshold/osc_mc.request.json` (30 draws, seed 20261105,
mismatch_scale 1) at the single nominal cell tt/1.80 V/27 C through the sensitivity
measurement path. `probe_hdr_tb.spice` + `requests/probe_hdr.json` extend the #44 device
probe to the header geometries and |Vgs| drives the levers actually reach (the committed
probe stops at |Vgs| = 0.30 V, W <= 0.86, L = 0.5).

COLD_FILL / FAST_FILL are filled in after the round-1 grids: one single-cell request per
(variant, cell) the 2 ms window under-resolves (longer window, like #277) or the hot
cells it cannot integrate in budget (shorter window, like `osc_grid_fast`). They are
declarative here so the committed requests stay generator-owned.

Multi-unit runs go to the batch fleet through `klt sim` (never hand-launched ngspice).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE = os.path.join(HERE, "..", "..", "..", "design", "osc_bank", "osc_subth.spice")
TB_SRC = os.path.join(HERE, "..", "..", "sensitivity", "osc", "tb_osc_subth.spice")
REQ_DIR = os.path.join(HERE, "requests")

with open(os.path.join(HERE, "..", "..", "corner_box.json")) as _f:
    _BOX = json.load(_f)
PROCESS, VDD, TEMP = _BOX["process"], _BOX["vdd"], _BOX["temp_c"]

MC_CELL = {"process": "tt", "temperature_c": 27, "supply_v": {"vdd": 1.8}}
MC_N, MC_SEED = 30, 20261105
# Grid window per variant. The baseline grid (requests/grid_osc_subth.json) uses "20n 2m",
# sized for the baseline's dynamics; the vbp variants run the ring tens of times faster
# (local single-corner probes: vbp_2_3 ~85 MHz vs baseline 2.84 MHz at tt/1.80/27 C), so
# 2 ms cannot be integrated inside the fleet per-unit timeout at the hot cells. Windows
# are sized from those probes to keep a unit under ~300k cycles; the extraction RULE
# (skip 3 edges, >= 5 cycles, VDD/2 crossings) is identical everywhere, and cells the
# window under-resolves are re-run as single-cell fills (COLD_FILL below), the #277 method.
GRID_TRAN = {"vbp_2_3": "20n 200u", "vbp_1_2": "20n 50u", "hw3": "20n 500u",
             "hl35": "20n 1m", "st11": "20n 1m"}
GRID_TIMEOUT = 3000
# MC windows sized the same way from the local probes (the committed sensitivity MC used
# "10n 500u" for the 2.84 MHz baseline; the fast variants only need ~9+ edges per draw).
MC_TRAN = {"vbp_2_3": "10n 50u", "vbp_1_2": "10n 20u", "hw3": "10n 100u",
           "hl35": "10n 100u", "st11": "10n 200u"}
MC_TIMEOUT = 300

VARIANTS = [
    ("vbp_2_3", "divider ratio: Rb0 300k->600k, Rb1 1500k->1200k (vbp 0.8333->0.6667 of VDD; total 1.8 M unchanged)"),
    ("vbp_1_2", "divider ratio: Rb0 300k->900k, Rb1 1500k->900k (vbp 0.5 of VDD; total 1.8 M unchanged)"),
    ("hw3", "header W/L: pfet_01v8_lvt header W 0.42->1.26 (x3), L=0.5 unchanged"),
    ("hl35", "header W/L: pfet_01v8_lvt header L 0.5->0.35 (the lvt model bin floor), W=0.42 unchanged"),
    ("st11", "stage count: 15->11 stages (enable NAND + 10 starved; stage 10 drives out)"),
]

# Single-cell re-runs declared after inspecting the round-1 grids (issue #277 method:
# window sized with >= 2x margin over the ~9 edges the estimator needs; max step sized
# per window so a fleet job stays ~1M internal steps). (variant, process, vdd, temp) ->
# tran args. timeout is the fleet whole-job ceiling minus margin.
COLD_FILL = {
    # hw3: the five historical cold cells stay under the 500 us grid window; windows sized
    # from the grid's own partial edge evidence (ss/1.80: 5 edges in 500 us ~ 9 kHz) and
    # the baseline cells scaled by this variant's ~4.5x tt/-40 speedup, with >= 2x margin.
    ("hw3", "sf", 1.62, -40): "10n 10m",
    ("hw3", "sf", 1.80, -40): "10n 10m",
    ("hw3", "sf", 1.98, -40): "10n 10m",
    ("hw3", "ss", 1.62, -40): "10n 10m",
    ("hw3", "ss", 1.80, -40): "10n 10m",
    # st11: only ~1.36x faster, so the cold cells are near-baseline (437-3044 Hz):
    # 40 ms for the three slowest, 20 ms for the ss pair (>= 2x margin over 9 edges).
    ("st11", "sf", 1.62, -40): "40n 40m",
    ("st11", "sf", 1.80, -40): "40n 40m",
    ("st11", "sf", 1.98, -40): "40n 40m",
    ("st11", "ss", 1.62, -40): "20n 20m",
    ("st11", "ss", 1.80, -40): "20n 20m",
}
FAST_FILL = {}

# Header device probe: (name, L, W) for the baseline header and the two geometry levers.
# L stops at 0.35: the lvt discrete model bins have no L below that (see the hl35 note).
HDR_DEVS = [("l050_w042", 0.5, 0.42), ("l050_w126", 0.5, 1.26), ("l035_w042", 0.35, 0.42)]
VG_POINTS = [0.0, 0.05, 0.15, 0.30, 0.45, 0.54, 0.60, 0.66, 0.75, 0.81, 0.90, 0.99]
PROBE_CELLS = [{"process": p, "temperature_c": t, "supply_v": {"vdd": 1.8}}
               for p, t in [("tt", 27), ("tt", -40), ("ff", -40), ("ss", -40),
                            ("sf", -40), ("fs", -40)]]


# ---------------------------------------------------------------- baseline deck transformation

def _chunks(path):
    """Baseline deck -> (header comment lines, [element chunks], trailer lines).

    A chunk is one element card plus its continuation line(s); comments and the
    .subckt/.ends/.ipin lines stay in order around them.
    """
    with open(path) as f:
        lines = [l.rstrip("\n") for l in f]
    lines = [l for l in lines if not l.startswith("** sch_path:")]  # xschem artifact
    pre, chunks, post = [], [], []
    cur = None
    for l in lines:
        if cur is not None and l.startswith("+"):
            cur.append(l)
            continue
        if cur is not None:
            chunks.append(cur)
            cur = None
        if l.startswith("+"):
            raise ValueError("continuation without a card: %r" % l)
        if l.startswith(".") or l.startswith("*.") or l.startswith("*"):
            (post if chunks else pre).append(l)
            continue
        if l.strip():
            cur = [l]
    if cur is not None:
        chunks.append(cur)
    return pre, chunks, post


def _hdr_w(w):
    return {"ad": "%.10g" % (0.29 * w), "pd": "%.10g" % (2 * w + 0.58),
            "nrd": "%.14g" % (0.29 / w)}


def variant_deck(name):
    pre, chunks, post = _chunks(BASELINE)
    if name == "vbp_2_3":
        rb0, rb1 = "600k", "1200k"
    elif name == "vbp_1_2":
        rb0, rb1 = "900k", "900k"
    else:
        rb0 = rb1 = None
    keep = []
    for ch in chunks:
        text = ch[0]
        if name in ("vbp_2_3", "vbp_1_2") and text.startswith("Rb0 "):
            ch = ["Rb0 vdd vbp %s m=1" % rb0]
        elif name in ("vbp_2_3", "vbp_1_2") and text.startswith("Rb1 "):
            ch = ["Rb1 vbp vss %s m=1" % rb1]
        elif name == "hw3" and "pfet_01v8_lvt" in text:
            g = _hdr_w(1.26)
            ch = [text.replace("L=0.5 W=0.42", "L=0.5 W=1.26")
                      .replace("ad=0.1218 as=0.1218 pd=1.42 ps=1.42",
                               "ad=%(ad)s as=%(ad)s pd=%(pd)s ps=%(pd)s" % g)
                      .replace("nrd=0.69047619047619", "nrd=%(nrd)s" % g),
                  ch[1].replace("nrs=0.69047619047619", "nrs=%(nrd)s" % g)]
        elif name == "hl35" and "pfet_01v8_lvt" in text:
            ch = [text.replace("L=0.5", "L=0.35")] + ch[1:]
        else:
            keep.append(ch)
            continue
        keep.append(ch)
    chunks = keep
    if name == "st11":
        # A starved stage k element is identifiable by its connections: the header and
        # pull-up name vh<k>, and every stage element's gate is n<k-1> (the NAND gates on
        # out/en instead). The last stage's pull-down drains `out`, so vh/gate are the
        # reliable keys, never the drain.
        import re

        def stage_of(chunk_lines):
            t = chunk_lines[0]
            m = re.search(r" vh(\d+) ", t + " ")
            if m:
                return int(m.group(1))
            toks = t.split()
            if len(toks) > 2 and toks[2].startswith("n") and toks[2][1:].isdigit():
                return int(toks[2][1:]) + 1   # gate n<k-1> -> stage k
            return None

        kept = []
        for ch in chunks:
            k = stage_of(ch)
            if k is not None and k > 10:
                continue  # drop starved stages 11..14
            if k == 10:
                ch = [c.replace(" n10 n9 ", " out n9 ") for c in ch]
            kept.append(ch)
        chunks = kept
    desc = dict(VARIANTS)[name]
    head = ["* osc_subth variant %s -- cold-corner design iteration (issue #278)." % name,
            "* SIMULATION ONLY. Schematic-level deck generated by gen_variants.py from the",
            "* committed design/osc_bank/osc_subth.spice by a one-factor text transformation:",
            "* %s. Not a design/ file: adoption is a spec/decisions/ record, not this deck." % desc]
    out = head + pre + [l for ch in chunks for l in ch] + post
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- testbench bodies

def variant_tb(name):
    with open(TB_SRC) as f:
        lines = [l.rstrip("\n") for l in f]
    out = []
    for l in lines:
        if l.startswith("** sch_path:"):
            continue
        if l.startswith(".include"):
            l = '.include "osc_subth_%s.spice"' % name
        elif l.startswith("* Sensitivity-grade testbench body"):
            l = ("* Sensitivity-grade testbench body for the osc_subth variant %s "
                 "(circuit body only: klt sim owns .control/.end)." % name)
        elif l.startswith("* SIMULATION: schematic-level netlist"):
            l = ("* SIMULATION: schematic-level netlist sim/subthreshold/variants/osc_subth_%s.spice "
                 "(issue #278 variant deck), no layout, no parasitics." % name)
        out.append(l)
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- requests

def _base(netlist, tran, timeout):
    return {
        "netlist": netlist,
        "engine": "ngspice",
        "models": {"pdk": "sky130A", "lib": "libs.tech/ngspice/sky130.lib.spice"},
        "analysis": {"kind": "tran", "args": tran},
        "measurements": [{
            "name": "t_rise", "unit": "s",
            "crossings": {"signal": "v(out)", "level": {"frac_of": "vdd", "fraction": 0.5},
                          "edge": "rise", "max": 400},
        }],
        "options": {"timeout_s": timeout, "retry_on_convergence_error": True},
        "batch": {"job_ceiling_check": "warn"},
        "backend": "batch",
    }


def grid_request(name):
    r = _base("../tb_osc_subth_%s.spice" % name, GRID_TRAN[name], GRID_TIMEOUT)
    r["corners"] = {"process": PROCESS, "supply_v": {"vdd": VDD}, "temperature_c": TEMP}
    return r


def mc_request(name):
    r = _base("../tb_osc_subth_%s.spice" % name, MC_TRAN[name], MC_TIMEOUT)
    r["corners"] = {"units": [dict(MC_CELL)]}
    r["monte_carlo"] = {"n": MC_N, "seed": MC_SEED, "vary": "mismatch",
                        "mismatch_scale": 1, "seed_scope": "point"}
    return r


def cell_request(name, stem, process, vdd, temp, tran, timeout):
    r = _base("../tb_osc_subth_%s.spice" % name, tran, timeout)
    r["corners"] = {"units": [{"process": process, "temperature_c": temp,
                               "supply_v": {"vdd": vdd}}]}
    return {"requests/%s_osc_subth_%s_%s_%gV_%dC.json" % (stem, name, process, vdd, temp): r}


def probe_hdr_tb():
    o = ["* HEADER DEVICE PROBE for the osc_subth cold-corner iteration (circuit body for `klt sim`;",
         "* generated by gen_variants.py; the gen_probe.py convention: |Vgs| swept by Vg,",
         "* |Vds| = 0.90 V on every device, Vdd fixed 1.8 V). SIMULATION ONLY.",
         "Vdd vdd 0 1.8", "Vg vg 0 0", "Egp gp vdd vg 0 -1", "Bdp dpref 0 V=V(vdd)-0.90"]
    for nm, L, W in HDR_DEVS:
        o += ["Vd_%s d_%s dpref 0" % (nm, nm),
              "XM_%s d_%s gp vdd vdd sky130_fd_pr__pfet_01v8_lvt W=%g L=%g nf=1 mult=1" % (nm, nm, W, L)]
    return "\n".join(o) + "\n"


def probe_hdr_request():
    ms = []
    for nm, _L, _W in HDR_DEVS:
        for vg in VG_POINTS:
            ms.append({"name": "i%03d_%s" % (round(vg * 100), nm), "unit": "A",
                       "spice": ".meas dc i%03d_%s find i(Vd_%s) at=%g"
                                % (round(vg * 100), nm, nm, vg)})
    return {
        "netlist": "../probe_hdr_tb.spice",
        "engine": "ngspice",
        "models": {"pdk": "sky130A", "lib": "libs.tech/ngspice/sky130.lib.spice"},
        "analysis": {"kind": "dc", "args": "Vg 0 1.0 0.01"},
        "measurements": ms,
        "options": {"timeout_s": 200, "keep_artifacts": False, "ngspice_options": {"gmin": 1e-15}},
        "corners": {"units": PROBE_CELLS},
    }


def all_files():
    files = {}
    for name, _desc in VARIANTS:
        files["osc_subth_%s.spice" % name] = variant_deck(name)
        files["tb_osc_subth_%s.spice" % name] = variant_tb(name)
        files["requests/grid_osc_subth_%s.json" % name] = json.dumps(grid_request(name), indent=2) + "\n"
        files["requests/mc_osc_subth_%s.json" % name] = json.dumps(mc_request(name), indent=2) + "\n"
    files["probe_hdr_tb.spice"] = probe_hdr_tb()
    files["requests/probe_hdr.json"] = json.dumps(probe_hdr_request(), indent=2) + "\n"
    for (name, proc, vdd, temp), tran in sorted(COLD_FILL.items()):
        for fn, r in cell_request(name, "cold", proc, vdd, temp, tran, 3480).items():
            files[fn] = json.dumps(r, indent=2) + "\n"
    for (name, proc, vdd, temp), tran in sorted(FAST_FILL.items()):
        for fn, r in cell_request(name, "fast", proc, vdd, temp, tran, 3000).items():
            files[fn] = json.dumps(r, indent=2) + "\n"
    return files


def main():
    check = "--check" in sys.argv[1:]
    files = all_files()
    bad = []
    for rel, text in sorted(files.items()):
        path = os.path.join(HERE, rel)
        if check:
            try:
                with open(path) as f:
                    if f.read() != text:
                        bad.append(rel)
            except FileNotFoundError:
                bad.append(rel)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(text)
    stale = []
    # A --check pass also fails if committed generated files exist that the generator
    # no longer produces (drift in the other direction).
    produced = set(files)
    for sub in (".", "requests"):
        d = os.path.join(HERE, sub)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.endswith((".spice", ".json")) and fn not in ("gen_variants.py",):
                rel = fn if sub == "." else os.path.join(sub, fn)
                if rel not in produced and not fn.startswith("cold_") \
                        and not fn.startswith("fast_") and fn != "README.md":
                    stale.append(fn)
    if bad or stale:
        print("DRIFT: mismatched=%s unknown=%s" % (bad, stale))
        return 1
    print("OK: %d generated files %s" % (len(files), "match" if check else "written"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
