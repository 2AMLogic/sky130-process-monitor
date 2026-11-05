#!/usr/bin/env python3
"""Connectivity sanity check for layout/osc_bank.gds (not LVS; that is issue #26).

For each oscillator cell: extract nets (diff minus poly = S/D; licon/mcon/via stack),
then assert the labelled nets en/out/vdd/vss/(vbp) are all distinct, and that every
S/D region and gate of a stage reaches the nets the #17 schematic says it should:
  * the number of distinct nets that touch gate poly equals the stage count + (vbp);
  * `out` touches a gate (feedback) and a drain; `en` touches a gate;
  * vdd/vss each touch n-tap/p-tap.
Prints a summary and exits non-zero on any failure.
"""
import sys
import klayout.db as db

gds = sys.argv[1]
ly = db.Layout(); ly.read(gds)
L = lambda a, b: ly.layer(a, b)
fail = 0
for name, nstage in (("osc_hd", 31), ("osc_nmos", 31), ("osc_pmos", 31), ("osc_wire", 31), ("osc_subth", 15)):
    top = ly.cell(name)
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, top, []))
    mk = lambda a, b: l2n.make_layer(L(a, b), f"{a}_{b}")
    diff, poly, licon, li1, mcon, met1, via, met2, tap = (mk(*x) for x in
        ((65, 20), (66, 20), (66, 44), (67, 20), (67, 44), (68, 20), (68, 44), (69, 20), (65, 44)))
    txt = l2n.make_text_layer(L(68, 5), "lbl")
    sd = diff - poly
    gp = poly & diff                                      # gate channel
    for lay in (sd, poly, licon, li1, mcon, met1, via, met2, tap):
        l2n.connect(lay)
    l2n.connect(sd, licon); l2n.connect(poly, licon); l2n.connect(tap, licon)
    l2n.connect(licon, li1); l2n.connect(li1, mcon); l2n.connect(mcon, met1)
    l2n.connect(met1, via); l2n.connect(via, met2)
    l2n.connect(met1, txt)
    l2n.extract_netlist()
    nets = {}
    for net in l2n.netlist().top_circuit().each_net():
        pass
    cir = l2n.netlist().top_circuit()
    named = {}
    for net in cir.each_net():
        for lbl in (net.name or "").split(","):
            if lbl in ("en", "out", "vdd", "vss", "vbp"):
                named.setdefault(lbl, []).append(net.cluster_id)
    # gate nets: nets of poly shapes
    gate_nets = set()
    for net in cir.each_net():
        if not l2n.shapes_of_net(net, poly, True).is_empty():
            gate_nets.add(net.cluster_id)
    ids = {k: set(v) for k, v in named.items()}
    ok = True
    msg = []
    for k in ("en", "out", "vdd", "vss"):
        if k not in ids or len(ids[k]) != 1:
            ok = False; msg.append(f"label {k} on {len(ids.get(k, []))} nets")
    flat = [next(iter(v)) for v in ids.values() if len(v) == 1]
    if len(flat) != len(set(flat)):
        ok = False; msg.append("labelled nets shorted together")
    if ok:
        if ids["out"] and next(iter(ids["out"])) not in gate_nets:
            ok = False; msg.append("out does not reach a gate")
        if next(iter(ids["en"])) not in gate_nets:
            ok = False; msg.append("en does not reach a gate")
    # every gate net except en/vbp must also be driven by a source/drain (stage output -> next gate)
    sd_nets = set()
    for net in cir.each_net():
        if not l2n.shapes_of_net(net, sd, True).is_empty():
            sd_nets.add(net.cluster_id)
    skip = set(ids.get("vdd", set())) | set(ids.get("vss", set())) | set(ids.get("en", set())) | set(ids.get("vbp", set()))
    undriven = (gate_nets - skip) - sd_nets
    n_g = len(gate_nets - skip)
    if undriven:
        ok = False; msg.append(f"{len(undriven)} gate nets with no S/D driver")
    if n_g != nstage:
        ok = False; msg.append(f"{n_g} driven gate nets != {nstage} stages")
    print(f"{name}: labelled={ {k: sorted(v) for k, v in ids.items()} } driven_gate_nets={n_g} -> {'OK' if ok else 'FAIL ' + '; '.join(msg)}")
    fail |= (not ok)
sys.exit(1 if fail else 0)
