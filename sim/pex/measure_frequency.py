#!/usr/bin/env python3
"""The --measure-command callback for the klt pex frequency pass (issue #282).

`klt pex` runs this command TWICE, once per leg, appending the leg's DUT netlist
path as the final argument and exporting $KLT_PEX_SIDE / $KLT_PEX_NETLIST /
$KLT_PEX_ARTIFACTS_DIR (plus $KLT_PEX_BACKEND when klt pex was given --backend).
Each invocation must print one measurement document on stdout:

    {"corners": [{"corner_id": ..., "measurements": [{"name": "f_hz", ...}]}]}

What one invocation does:

  1. derive a bench body from the committed sim/pex/osc/tb_<osc>.spice (the
     same generated bench the testbench-mode reports record) with its single
     DUT .include re-pointed at the netlist it was handed -- for osc_hd that is
     the extracted pin order the committed bench already carries, so the
     schematic leg is measured on the osc_hd_dut.spice wrapper passed as
     klt pex's --reference-netlist, never on a re-ordered copy;
  2. derive a request from the committed sim/pex/requests/<osc>.json with only
     the netlist (and, for a --corner pilot, the corner set) changed;
  3. run that request through `klt sim` -- the batch fleet on any host that
     defaults KLT_SIM_BACKEND=batch, never a hand-rolled ngspice grid -- with
     the committed request's own capacity_wait_s and any --hosts sharding
     given on the measure command;
  4. reduce each corner's crossings times to f_hz with
     sensitivity/analyze.py::freq_from_crossings (SKIP_EDGES start-up edges
     dropped, MIN_CYCLES complete cycles required -- the same estimator and
     the same constants the schematic #29 frequencies use, loaded through
     sim/_siblings.py so no copy exists), emitting null with the cause for
     unresolved cells (too few edges / solver error / missing result).

The derived bench and request, and a copy of the nested `klt sim` report (the
crossing times the frequencies were reduced from), are kept in
$KLT_PEX_ARTIFACTS_DIR for provenance. The nested report itself is written
outside that tree, as docs/cli/pex.md requires.

Pilot (one paired corner, local single-unit run):

    klt pex layout/osc_bank.gds --deck sky130 --pdk sky130A --top osc_hd \
        --pins en,out,vdd,vss --rename-declared-pins --backend local \
        --measure-command 'python3 -I sim/pex/measure_frequency.py --osc osc_hd --corner tt/1.800V/27C' \
        --reference-netlist sim/pex/osc/osc_hd_dut.spice ...

Grid (fleet; the nested klt sim routes to batch through KLT_SIM_BACKEND):

    klt pex layout/osc_bank.gds --deck sky130 --pdk sky130A --top osc_subth \
        --pins en,out,vdd,vss --backend batch \
        --measure-command 'python3 -I sim/pex/measure_frequency.py --osc osc_subth --hosts 45' \
        --reference-netlist design/osc_bank/osc_subth.spice ...
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(HERE)
sys.path.insert(0, SIM)
import _siblings  # noqa: E402

# One frequency definition, owned by the sensitivity analysis: SKIP_EDGES / MIN_CYCLES and
# freq_from_crossings itself. The measurement name stays t_rise so the nested report's first
# corner measurement is the crossings measurement analyze.extract() reads.
_SENS = _siblings.load("sensitivity", "analyze")
FREQ_NAME = "f_hz"
MIN_EDGES = _SENS.SKIP_EDGES + _SENS.MIN_CYCLES + 1
CORNER_ID = re.compile(r"^([a-z]+)/([0-9.]+)V/(-?[0-9]+)C$")


def corner_id(process, vdd, temp_c):
    """klt's own corner_id spelling (never parsed back here; both legs share it)."""
    return "%s/%.3fV/%dC" % (process, vdd, temp_c)


def parse_corner_id(cid):
    m = CORNER_ID.match(cid)
    if not m:
        raise ValueError("not a corner id: %r" % cid)
    return m.group(1), float(m.group(2)), int(m.group(3))


def bench_text(osc, dut_path):
    """The committed pex bench for `osc` with its single DUT .include re-pointed at `dut_path`.

    The committed bench bodies are GENERATED (sim/pex/gen_requests.py) and byte-hashed in the
    testbench-mode records, so they are read, not re-derived: the only change is the include
    target, exactly the line klt pex itself swaps in testbench mode. osc_hd's committed bench
    already instantiates the DUT in the extracted pin order, so both legs keep one bench.
    """
    with open(os.path.join(HERE, "osc", "tb_%s.spice" % osc)) as f:
        lines = f.readlines()
    idx = [i for i, l in enumerate(lines) if l.lstrip().lower().startswith((".include", ".inc"))]
    if len(idx) != 1:
        raise SystemExit("expected exactly one .include in tb_%s.spice, found %d" % (osc, len(idx)))
    lines[idx[0]] = '.include "%s"\n' % dut_path
    return "".join(lines)


def request_json(osc, bench_path, corner):
    """The committed pex request for `osc` with the netlist (and optionally the corner set) swapped."""
    with open(os.path.join(HERE, "requests", "%s.json" % osc)) as f:
        r = json.load(f)
    r["netlist"] = bench_path
    if corner:
        p, v, t = corner
        c = r["corners"]
        c["process"], c["supply_v"]["vdd"], c["temperature_c"] = [p], [v], [t]
    return r


def expected_corners(r):
    for p in r["corners"]["process"]:
        for v in r["corners"]["supply_v"]["vdd"]:
            for t in r["corners"]["temperature_c"]:
                yield corner_id(p, v, t)


def run_sim(request_path, out_path, backend, hosts, capacity_wait_s):
    """Run the derived request through klt sim; returns (exit_status, stdout+stderr tail)."""
    cmd = ["klt", "sim", request_path, "-o", out_path]
    if backend:
        cmd += ["--backend", backend]
    if hosts:
        cmd += ["--hosts", str(hosts)]
    if capacity_wait_s is not None:
        cmd += ["--wait-for-capacity", str(capacity_wait_s)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    tail = (p.stdout + p.stderr)[-4000:]
    return p.returncode, tail


def measurement_document(report, expected):
    """{"corners": [...]} for every expected corner id, null f_hz with the cause when unresolved."""
    by_id = {c["corner_id"]: c for c in report.get("corners", [])}
    dupes = sorted(c for c, n in
                   ((c, sum(1 for x in report.get("corners", []) if x["corner_id"] == c))
                    for c in by_id) if n > 1)
    if dupes:
        raise SystemExit("nested report has duplicate corner ids: %s" % dupes)
    doc = {"kind": "SIMULATED", "measurement": FREQ_NAME, "corners": []}
    for cid in expected:
        c = by_id.get(cid)
        if c is None:
            row = {"corner_id": cid,
                   "measurements": [{"name": FREQ_NAME, "value": None, "status": "error",
                                     "message": "missing result"}]}
            doc["corners"].append(row)
            continue
        m = c["measurements"][0]
        if m.get("name") != "t_rise":
            raise SystemExit("first measurement of corner %s is %r, not t_rise" % (cid, m.get("name")))
        times = (m.get("crossings") or {}).get("times") or []
        failed = c["status"] != "pass" or m.get("status") not in (None, "pass")
        f = None if failed else _SENS.freq_from_crossings(times)
        if f is not None:
            meas = {"name": FREQ_NAME, "value": f, "status": "pass"}
            row = {"corner_id": cid, "measurements": [meas], "n_edges": len(times)}
        else:
            why = "solver error: unit %s, measurement %s" % (c["status"], m.get("status")) if failed else \
                  "too few edges: %d rising edges < %d (SKIP_EDGES=%d, MIN_CYCLES=%d)" % (
                      len(times), MIN_EDGES, _SENS.SKIP_EDGES, _SENS.MIN_CYCLES)
            meas = {"name": FREQ_NAME, "value": None, "status": "error", "message": why}
            row = {"corner_id": cid, "measurements": [meas], "n_edges": len(times), "unit_status": c["status"]}
        doc["corners"].append(row)
    return doc


def main(argv):
    osc = corner = hosts = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--osc":
            osc, i = argv[i + 1], i + 2
        elif a == "--corner":
            corner, i = parse_corner_id(argv[i + 1]), i + 2
        elif a == "--hosts":
            hosts, i = int(argv[i + 1]), i + 2
        elif a.startswith("--"):
            raise SystemExit("unknown option %r" % a)
        else:
            break
    dut = argv[i]
    if not osc:
        raise SystemExit("--osc is required")
    if os.environ.get("KLT_PEX_NETLIST") and os.path.realpath(os.environ["KLT_PEX_NETLIST"]) != os.path.realpath(dut):
        raise SystemExit("$KLT_PEX_NETLIST and the final argument disagree")
    side = os.environ.get("KLT_PEX_SIDE", "schematic")
    art = os.environ.get("KLT_PEX_ARTIFACTS_DIR") or tempfile.mkdtemp(prefix="pex-freq-%s-" % side)
    os.makedirs(art, exist_ok=True)

    bench = os.path.join(art, "tb_%s_freq.spice" % osc)
    with open(bench, "w") as f:
        f.write(bench_text(osc, os.path.abspath(dut)))
    req = os.path.join(art, "request-%s.json" % side)
    r = request_json(osc, bench, corner)
    with open(req, "w") as f:
        json.dump(r, f, indent=2)
        f.write("\n")

    # The nested report must be written OUTSIDE $KLT_PEX_ARTIFACTS_DIR (docs/cli/pex.md, outdir_locked);
    # a copy is kept inside it afterwards, next to the bench and request it came from.
    with tempfile.TemporaryDirectory(prefix="pex-freq-sim-") as tmp:
        out = os.path.join(tmp, "sim.report.json")
        status, tail = run_sim(req, out, os.environ.get("KLT_PEX_BACKEND"),
                               hosts, (r.get("batch") or {}).get("capacity_wait_s"))
        if status != 0 or not os.path.exists(out):
            sys.stderr.write("klt sim failed (exit %d):\n%s\n" % (status, tail))
            return 1
        with open(out) as f:
            report = json.load(f)
        shutil.copyfile(out, os.path.join(art, "sim.report.%s.json" % side))

    doc = measurement_document(report, list(expected_corners(r)))
    with open(os.path.join(art, "measurement.%s.json" % side), "w") as f:
        json.dump(doc, f, indent=1)
    json.dump(doc, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
