#!/usr/bin/env python3
"""Issue #117: classify the osc_subth `vh` split as layout vs extraction defect. SIMULATED/extraction evidence only.

usage: <klayout-python> -I sim/pex/diag/vh_split.py <layout.gds> <out.json>   (needs `klt` on PATH)

1. Layout side: merge `diff` (65/20) and report the merged polygons that carry the diffusion step (one per stage).
2. Extraction side: `klt extract` the cell; for each header (`pfet_01v8_lvt`) take its non-vdd source/drain net, and
   count how many are the same net as a stage-PFET terminal (a split means none are).
3. Control: delete `lvtn` (125/44) from a scratch copy and repeat; the header drain and the PFET source then share a net.
"""
import json, os, re, subprocess, sys, tempfile
import klayout.db as db

def merged_step_polys(path, top):
    ly = db.Layout(); ly.read(path)
    r = db.Region(ly.cell(top).begin_shapes_rec(ly.layer(65, 20))).merged()
    return [p for p in r.each() if p.num_points() > 4]

def extract(path, top):
    out = tempfile.mktemp(suffix=".spice")
    subprocess.run(["klt", "extract", path, "--deck", "sky130", "--pdk", "sky130A", "--top", top,
                    "--pins", "en,out,vdd,vss", "-o", out, "--format", "json"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return open(out).read()

def pairs(spice):
    """(header S/D net, stage-pfet S/D nets) -> number of headers whose non-vdd terminal is shared with a stage pfet."""
    hdr, pf = [], []
    for ln in spice.splitlines():
        t = ln.split()
        if not t or not t[0].startswith("X"): continue
        if "pfet_01v8" not in ln: continue
        if "L=0.5 " in ln:      # series header (LVT when the marker is present, plain pfet in the control)
            hdr.append(t[3] if t[1] == "vdd" else t[1])
        elif "L=0.15 " in ln: pf += [t[1], t[3]]
    return len(hdr), sum(1 for h in hdr if h in pf)

def main(gds, out):
    top = "osc_subth"
    res = {"layout": {"step_diff_merged_polygons": len(merged_step_polys(gds, top))}}
    res["extracted"] = dict(zip(("headers", "headers_sharing_a_net_with_stage_pfet"), pairs(extract(gds, top))))
    ly = db.Layout(); ly.read(gds); li = ly.layer(125, 44)
    for c in ly.each_cell(): c.shapes(li).clear()
    scratch = tempfile.mktemp(suffix=".gds"); ly.write(scratch)
    res["control_no_lvtn"] = dict(zip(("headers", "headers_sharing_a_net_with_stage_pfet"), pairs(extract(scratch, top))))
    json.dump(res, open(out, "w"), indent=2); print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main(*sys.argv[1:3])
