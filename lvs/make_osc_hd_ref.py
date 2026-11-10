#!/usr/bin/env python3
"""Write lvs/osc_hd.ref.spice: design/osc_bank/osc_hd.spice plus the transistor-level
`.subckt` bodies of the PDK cells it instantiates, copied verbatim from the PDK cell SPICE
named in sim/pdk.json. `osc_hd.spice` calls the cells by name; the layout is extracted at
transistor level, so the reference needs their bodies for a device-level compare."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
pj = json.load(open(os.path.join(REPO, "sim", "pdk.json")))
root = os.path.expanduser(os.environ.get(pj["root_override_env"], pj["default_root"]))
lib = open(os.path.join(root, pj["cell_spice"])).read()
src = open(os.path.join(REPO, "design/osc_bank/osc_hd.spice")).read()
need = sorted(set(re.findall(r"\b(sky130_fd_sc_hd__\w+)\s*$", src, re.M)))
out = [src.rstrip("\n"), ""]
for cell in need:
    m = re.search(r"^\.subckt %s\b.*?^\.ends\b[^\n]*\n" % cell, lib, re.M | re.S | re.I)
    if not m:
        sys.exit("cell %s not in %s" % (cell, pj["cell_spice"]))
    body = m.group(0).rstrip("\n")
    # PDK cell SPICE writes geometry as `w=650000u` meaning 0.65 (um) under its own scale;
    # the klt reference reader takes bare micrometres, so divide the mantissa by 1e6.
    body = re.sub(r"\b([wl])=([0-9.e+]+)u\b", lambda k: "%s=%g" % (k.group(1), float(k.group(2)) / 1e6), body)
    out.append(body)
open(os.path.join(HERE, "osc_hd.ref.spice"), "w").write("\n".join(out) + "\n")
print("cells:", ", ".join(need))
