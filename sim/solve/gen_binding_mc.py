#!/usr/bin/env python3
"""Write the `klt sim` mismatch-MC requests for the three binding cells of rows 2-4 (issue #31).

    python3 -I sim/solve/gen_binding_mc.py

Binding cells (sim/solve/records/2026-11-05-rows1-4.md): row 2 at 1.98 V/27 C (all 5 corners),
row 3 at tt 1.62 V/-40 C, row 4 at ff 1.62 V/27 C. Same testbenches, mismatch_scale=1 (`mc_mm_switch=1`),
seed and windows as sim/sensitivity/gen_requests.py; only the cells and n change. SIMULATED requests;
submit with `klt sim --batch-set` (fleet), never hand-launched ngspice. The osc_subth cold cell has its own
longer-window request. Run-scoped n (host rule: scope the run, land it, file the remainder) is stated in the record.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "sensitivity"))
import gen_requests as G  # noqa: E402

# (process, vdd, temp_c, row)
CELLS = [(p, 1.98, 27) for p in G.PROCESS] + [("tt", 1.62, -40), ("ff", 1.62, 27)]
N = {"osc_hd": 30, "osc_nmos": 30, "osc_pmos": 30, "osc_wire": 30, "osc_subth": 10}
SPLIT_PER_CELL = ("osc_nmos", "osc_wire")
SUBTH_TRAN = {"warm": ("10n 500u", 300), "cold": ("10n 4m", 1800)}


def request(osc, cells, tran=None, timeout=None):
    tran0, cap = G.OSCS[osc]
    r = G.base(osc, tran or G.MC_TRAN.get(osc, tran0), cap)
    r["netlist"] = "../../../sensitivity/osc/tb_%s.spice" % osc  # requests live in sim/solve/mc/requests/
    if timeout:
        r["options"]["timeout_s"] = timeout
    r["corners"] = {"units": [{"process": p, "temperature_c": t, "supply_v": {"vdd": v}} for p, v, t in cells]}
    r["monte_carlo"] = {"n": N[osc], "seed": G.MC_SEED, "vary": "mismatch", "mismatch_scale": 1, "seed_scope": "point"}
    return r


def all_requests():
    out = {}
    for osc in G.OSCS:
        if osc in SPLIT_PER_CELL:  # the 7-unit jobs failed on the fleet (#31 record); one request per cell
            for c in CELLS:
                out["mc_bind_%s_%s_%gV_%gC.json" % (osc, c[0], c[1], c[2])] = request(osc, [c])
            continue
        if osc != "osc_subth":
            out["mc_bind_%s.json" % osc] = request(osc, CELLS)
            continue
        warm = [c for c in CELLS if c[2] == 27]
        cold = [c for c in CELLS if c[2] == -40]
        out["mc_bind_osc_subth_27C.json"] = request(osc, warm, *SUBTH_TRAN["warm"])
        out["mc_bind_osc_subth_-40C.json"] = request(osc, cold, *SUBTH_TRAN["cold"])
    return out


# --- sized campaign (issue #31, rev. 2026-11-06): n >= 183 (rows 2, 4) per binding cell, chunked ---------
# One request per (oscillator, cell, chunk) so an errored draw or a failed job loses one chunk only. Each
# chunk has its own seed (SIZED_SEED + 1000 * chunk) so chunks are independent draws and pool by concatenation
# (analyze.extract_mc appends per cell key). Requests live in sim/solve/mc/requests-sized/.
SIZED_SEED = 20261106
SIZED_CHUNK = 50
SIZED_CHUNKS = 4   # 4 x 50 = 200 >= 183 (rows 2, 4 sample-size verdict at as-of 1f3e1a7)


def sized_request(osc, cell, chunk, n=SIZED_CHUNK):
    cold = cell[2] < 0
    tran = timeout = None
    if osc == "osc_subth":
        tran, timeout = SUBTH_TRAN["cold" if cold else "warm"]
    r = request(osc, [cell], tran, timeout)
    r["monte_carlo"]["n"] = n
    r["monte_carlo"]["seed"] = SIZED_SEED + 1000 * chunk
    return r


def sized_requests(oscs=None, chunks=SIZED_CHUNKS, cells=None, n=SIZED_CHUNK):
    out = {}
    for osc in oscs or list(G.OSCS):
        for c in cells or CELLS:
            for k in range(chunks):
                out["mc_sized_%s_%s_%gV_%gC_c%d.json" % (osc, c[0], c[1], c[2], k)] = sized_request(osc, c, k, n)
    return out


if __name__ == "__main__" and "--sized" in sys.argv:
    d = os.path.join(HERE, "mc", "requests-sized")
    os.makedirs(d, exist_ok=True)
    for name, req in sized_requests().items():
        with open(os.path.join(d, name), "w") as f:
            json.dump(req, f, indent=2)
            f.write("\n")
    sys.exit(0)

if __name__ == "__main__":
    d = os.path.join(HERE, "mc", "requests")
    os.makedirs(d, exist_ok=True)
    for name, req in all_requests().items():
        with open(os.path.join(d, name), "w") as f:
            json.dump(req, f, indent=2)
            f.write("\n")
