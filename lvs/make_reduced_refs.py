#!/usr/bin/env python3
"""Derive DISCLOSED reduced references for the two oscillators whose layout does not draw every
schematic element (layout/README.md "Not drawn"). These are NOT item-1 netlists; a match against
them is a transistor-topology result only and is not T1 item 4 evidence for those cells.
  osc_wire : drop the 31 ideal 100 fF shunt caps (C*); short each wire resistor (R*) -- the met1
             serpentine is drawn as plain metal, so the extractor sees one net across it.
  osc_subth: the ideal bias divider Rb0/Rb1 (300k / 1500k) is drawn as two sky130 high-resistance poly
             resistors (res_high_po_0p35); the reference swaps each ideal R for that PDK device at the poly
             length that realises the ideal value in the PDK model (lengths and width read from
             layout/gen/osc_subth_divider.json, the owner layout/gen/gen_osc_bank.py also draws from;
             tt/27C, 1.8 V divider). The item-1 schematic keeps the ideal R.
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(os.path.dirname(HERE), "design/osc_bank")

def lines(name):
    txt = open(os.path.join(D, name + ".spice")).read().replace("\n+", " ")
    return [l for l in txt.splitlines() if l.strip() and not l.startswith("*")]

# osc_wire
ls = lines("osc_wire"); alias = {}
for l in ls:
    t = l.split()
    if t[0].startswith("R"):
        alias[t[2]] = t[1]
out = []
for l in ls:
    t = l.split()
    if t[0].startswith(("R", "C")):
        continue
    if t[0].startswith("X") or t[0].startswith("M"):
        n = [alias.get(x, x) for x in t[1:5]]
        t = [t[0]] + n + t[5:]
    out.append(" ".join(t))
open(os.path.join(HERE, "osc_wire.ref.spice"), "w").write("\n".join(out) + "\n")
# osc_subth
divider = json.load(open(os.path.join(os.path.dirname(HERE), "layout", "gen", "osc_subth_divider.json")))
RB_L = {k: r["L_um"] for k, r in divider["resistors"].items()}   # um; owner: layout/gen/osc_subth_divider.json
W_UM = divider["poly_w_nm"] / 1000
ls = []
for l in lines("osc_subth"):
    t = l.split()
    if t[0] in RB_L:                   # Rb* a b value ... -> PDK resistor, body on vss
        l = f"X{t[0]} {t[1]} {t[2]} vss sky130_fd_pr__res_high_po_0p35 L={RB_L[t[0]]} W={W_UM}"
    ls.append(l)
open(os.path.join(HERE, "osc_subth.ref.spice"), "w").write("\n".join(ls) + "\n")
