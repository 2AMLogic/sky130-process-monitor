#!/usr/bin/env python3
"""Generate layout/osc_bank.gds: the five ring oscillators of the bank + a top cell.

Reproducible from source: `python3 layout/gen/gen_osc_bank.py` rewrites the stream
byte-for-byte (GDS timestamps are not written). Needs the `klayout` Python module
(layout/gen/requirements.txt) and the sky130A PDK pinned by sim/pdk.json.

Drawn (device for device from design/osc_bank/*.spice, issue #17):
  osc_hd    placed row of PDK sky130_fd_sc_hd cells (nand2_1 + 30 x inv_1) + tap cells,
            routed on li1/met1. Cell geometry comes from the pinned PDK GDS, not redrawn.
  osc_nmos / osc_pmos / osc_wire / osc_subth
            transistor-level: single-finger devices; a stage is a pfet over an nfet sharing a
            vertical poly gate; li1 contacts, met1 rails, a substrate/well tap per stage.
            osc_wire draws each res_generic_m1 (W 0.14 um, L 1000 um) as a met1 serpentine.

NOT drawn (ideal placeholders in the #17 schematics; see layout/README.md):
  the 100 fF shunt capacitors of osc_wire, and the Rb0/Rb1 bias divider of osc_subth
  (the divider output `vbp` is a labelled met1 net).

Planning-level geometry: spacing/enclosure values are applied by hand and have NOT been
run through a DRC deck (that is issue #25). Nothing here is measured.
"""
import argparse
import hashlib
import json
import os
import sys

import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

LAYERS = dict(
    nwell=(64, 20), diff=(65, 20), tap=(65, 44), poly=(66, 20), licon=(66, 44),
    li1=(67, 20), mcon=(67, 44), met1=(68, 20), via=(68, 44), met2=(69, 20),
    nsdm=(93, 44), psdm=(94, 44), npc=(95, 20), lvtn=(125, 44),
    li1_lbl=(67, 5), met1_lbl=(68, 5), met1_pin=(68, 16),
)

R = 290            # source/drain column width
LIC = 170
PADX = 500         # left margin of a custom stage (room for the gate-pad bump)
TAPW = 700         # tap column width
STG_GAP = 400
YN0 = 600          # nfet diff bottom
GAP = 1900         # reference nfet top -> pfet bottom
Y_BUS, Y_PADB, Y_OUT, Y_IN = 300, 400, 800, 1400   # gap levels above the reference nfet top
SERP_N, SERP_PITCH = 12, 300      # runs per serpentine; centre pitch (met1 space 160 nm vs 140 nm rule)
SERP_GAP = 700                    # clear gap between one serpentine's last run and the next row's feed


class Ctx:
    def __init__(self, ly):
        self.ly = ly
        self.li = {k: ly.layer(*v) for k, v in LAYERS.items()}

    def rect(self, cell, lay, x0, y0, x1, y1):
        cell.shapes(self.li[lay]).insert(db.Box(int(x0), int(y0), int(x1), int(y1)))

    def cr(self, cell, lay, cx, cy, w):
        self.rect(cell, lay, cx - w // 2, cy - w // 2, cx - w // 2 + w, cy - w // 2 + w)

    def text(self, cell, lay, x, y, s):
        cell.shapes(self.li[lay]).insert(db.Text(s, int(x), int(y)))

    def label(self, cell, x, y, s):
        self.text(cell, "met1_lbl", x, y, s)
        self.text(cell, "met1_pin", x, y, s)

    def li_v(self, cell, x, y0, y1):
        self.rect(cell, "li1", x - 125, min(y0, y1), x + 125, max(y0, y1))

    def li_h(self, cell, y, x0, x1):
        self.rect(cell, "li1", min(x0, x1), y - 85, max(x0, x1), y + 85)

    def mcon_pad(self, cell, x, y, m1=350):
        self.cr(cell, "li1", x, y, 250)
        self.cr(cell, "mcon", x, y, LIC)
        self.cr(cell, "met1", x, y, m1)

    def via_pad(self, cell, x, y):
        self.cr(cell, "met1", x, y, 350)
        self.cr(cell, "via", x, y, 150)
        self.cr(cell, "met2", x, y, 350)

    def m2_v(self, cell, x, y0, y1):
        self.rect(cell, "met2", x - 115, min(y0, y1), x + 115, max(y0, y1))

    def m2_h(self, cell, y, x0, x1):
        self.rect(cell, "met2", min(x0, x1), y - 115, max(x0, x1), y + 115)

    def m1_v(self, cell, x, y0, y1):
        self.rect(cell, "met1", x - 70, min(y0, y1), x + 70, max(y0, y1))

    def m1_h(self, cell, y, x0, x1):
        self.rect(cell, "met1", min(x0, x1), y - 70, max(x0, x1), y + 70)

    def poly_pad(self, cell, xpad, ypad, xgate):
        self.rect(cell, "poly", xpad - 165, ypad - 165, xgate, ypad + 165)
        self.cr(cell, "npc", xpad, ypad, 430)
        self.cr(cell, "licon", xpad, ypad, LIC)
        self.cr(cell, "li1", xpad, ypad, 250)


def contact_ys(W):
    n = (W - 120 + 170) // 340
    total = n * LIC + (n - 1) * LIC
    y0 = (W - total) // 2
    return [y0 + i * 340 for i in range(n)]


# ----------------------------- stage descriptions ---------------------------------
def inv_stage(Wn, Wp, Ln, Lp):
    G = max(Ln, Lp)
    return dict(Wn=Wn, Wp=Wp, cols=["R", G, "R"], ocol=2, nand=False,
                n=(0, ["vss", ("in", Ln), "out"]), p=(0, ["vdd", ("in", Lp), "out"]))


def nand_stage(Wn, Wp, Ln, Lp):
    G = max(Ln, Lp)
    return dict(Wn=Wn, Wp=Wp, cols=["R", G, "R700", G, "R"], ocol=4, nand=True,
                n=(0, ["vss", ("en", Ln), "float", ("out", Ln), "n0"]),
                p=(0, ["vdd", ("en", Lp), "n0", ("out", Lp), "vdd"]))


def subth_stage(Wn, Wp, Ln, Lp, Lh):
    G = max(Ln, Lp)
    return dict(Wn=Wn, Wp=Wp, Whdr=420, cols=["R", Lh, "R700", G, "R"], ocol=4, nand=False,
                n=(2, ["vss", ("in", Ln), "out"]),
                p=(0, ["vdd", ("vbp", Lh, "lvt"), "float", ("in", Lp), "out"]))


def stages_for(kind):
    if kind == "osc_nmos":
        return [nand_stage(840, 3000, 500, 150)] + [inv_stage(420, 3000, 500, 150) for _ in range(30)]
    if kind == "osc_pmos":
        return [nand_stage(6000, 420, 150, 500)] + [inv_stage(3000, 420, 150, 500) for _ in range(30)]
    if kind == "osc_wire":
        return [nand_stage(8000, 8000, 150, 150)] + [inv_stage(4000, 8000, 150, 150) for _ in range(30)]
    if kind == "osc_subth":
        return [nand_stage(840, 840, 150, 150)] + [subth_stage(420, 840, 150, 150, 500) for _ in range(14)]
    raise SystemExit("unknown oscillator " + kind)


def build_custom(ctx, name, sts, wire=False, vbp=False):
    cell = ctx.ly.create_cell(name)
    WNM = max(s["Wn"] for s in sts)
    WPM = max(s["Wp"] for s in sts)
    YREF = YN0 + WNM                  # reference nfet top
    YP0 = YREF + GAP
    YP1 = YP0 + WPM
    YRV = YP1 + 600                   # vdd rail centre
    geo = []
    x = 0
    for st in sts:
        xs, cx = [], x + PADX
        for c in st["cols"]:
            w = (R if c == "R" else int(c[1:])) if isinstance(c, str) else c
            xs.append((cx, cx + w))
            cx += w
        xT = cx + TAPW // 2
        g = dict(x0=x, x1=cx + TAPW, xs=xs, xT=xT, gates={}, regs={}, pads={})
        colc = lambda i: (xs[i][0] + xs[i][1]) // 2
        for kind, (c0, items), W, y0 in (("n", st["n"], st["Wn"], YN0),
                                         ("p", st["p"], st["Wp"], YP1 - st["Wp"])):
            xl, xr = xs[c0][0], xs[c0 + len(items) - 1][1]
            Wh = st.get("Whdr") if kind == "p" else None
            if Wh:      # series header is narrower than the inverter pfet: step the diffusion mid-"float" column
                xstep = (xs[c0 + 2][0] + xs[c0 + 2][1]) // 2
                ctx.rect(cell, "diff", xl, y0 + W - Wh, xstep, y0 + W)
                ctx.rect(cell, "diff", xstep, y0, xr, y0 + W)
            else:
                ctx.rect(cell, "diff", xl, y0, xr, y0 + W)
            ctx.rect(cell, "nsdm" if kind == "n" else "psdm", xl - 125, y0 - 125, xr + 125, y0 + W + 125)
            for k, it in enumerate(items):
                col = c0 + k
                if isinstance(it, tuple):
                    g["gates"][(kind, col)] = (it[0], colc(col), it[1])
                    if len(it) > 2:      # LVT header: lvtn spans its channel up to the shared region centre
                        ctx.rect(cell, "lvtn", xs[col - 1][0] - 100, y0 - 100, colc(col + 1), y0 + W + 100)
                elif it != "float":
                    Wc, yc = (Wh, y0 + W - Wh) if (Wh and k == 0) else (W, y0)
                    ys = contact_ys(Wc)
                    for yy in ys:
                        ctx.cr(cell, "licon", colc(col), yc + yy + LIC // 2, LIC)
                    g["regs"][(kind, col)] = (it, colc(col), yc + ys[0] - 80, yc + ys[-1] + LIC + 80)
        for (kind, col), (gnet, gx, L) in g["gates"].items():
            ymid = YREF + GAP // 2      # poly steps between the nfet and pfet gate widths here
            if kind == "n":
                ytop = ymid if ("p", col) in g["gates"] else YP1 + 130
                ctx.rect(cell, "poly", gx - L // 2, YN0 - 130, gx - L // 2 + L, ytop)
            elif ("n", col) in g["gates"]:
                ctx.rect(cell, "poly", gx - L // 2, ymid, gx - L // 2 + L, YP1 + 130)
            else:
                ctx.rect(cell, "poly", gx - L // 2, YREF + Y_BUS - 165, gx - L // 2 + L, YP1 + 130)
        for (kind, col), (net, rx, lo, hi) in g["regs"].items():
            if net == "vss":
                ctx.li_v(cell, rx, 0, hi)
                ctx.cr(cell, "mcon", rx, 0, LIC)
            elif net == "vdd":
                ctx.li_v(cell, rx, lo, YRV)
                ctx.cr(cell, "mcon", rx, YRV, LIC)
        for ty, sd in ((0, "psdm"), (YRV, "nsdm")):
            ctx.cr(cell, "tap", xT, ty, 340)
            ctx.cr(cell, sd, xT, ty, 600)
            ctx.cr(cell, "licon", xT, ty, LIC)
            ctx.cr(cell, "li1", xT, ty, 250)
            ctx.cr(cell, "mcon", xT, ty, LIC)
        # drain column(s)
        oc = st["ocol"]
        rn = g["regs"][("n", oc)]
        if st["nand"]:
            rp = g["regs"][("p", oc - 2)]
            ctx.li_v(cell, rn[1], rn[2], YREF + Y_IN + 85)
            ctx.li_v(cell, rp[1], YREF + Y_OUT - 85, rp[3])
            ctx.li_h(cell, YREF + Y_OUT, rp[1], rn[1])
        else:
            rp = g["regs"][("p", oc)]
            ctx.li_v(cell, rn[1], rn[2], rp[3])
        g["xd"] = rn[1]
        # gate pads (placed left of the gate, over the left-hand source column's gap)
        for (kind, col), (gnet, gx, L) in g["gates"].items():
            if kind != "p":
                continue
            ypad = YREF + {"vbp": Y_BUS, "out": Y_PADB}.get(gnet, Y_IN)
            xpad = gx - L // 2 - 250
            ctx.poly_pad(cell, xpad, ypad, gx)
            g["pads"][gnet] = (xpad, ypad)
        geo.append(g)
        x = g["x1"] + STG_GAP

    xmax = x - STG_GAP
    ctx.rect(cell, "met1", 0, -240, xmax, 240)
    ctx.rect(cell, "met1", 0, YRV - 240, xmax, YRV + 240)
    ctx.label(cell, 100, 0, "vss")
    ctx.label(cell, 100, YRV, "vdd")
    for g in geo:
        ctx.rect(cell, "nwell", g["x0"] - 150, YP0 - 250, g["x1"] + 150, YRV + 400)

    # stage output -> next stage input (direct li1; osc_wire goes through a serpentine instead)
    if not wire:
        for g, gn in zip(geo, geo[1:]):
            xp, yp = gn["pads"]["in"]
            ctx.li_h(cell, yp, g["xd"], xp)

    # enable
    xen, yen = geo[0]["pads"]["en"]
    ctx.li_h(cell, yen, -600, xen)
    ctx.mcon_pad(cell, -600, yen)
    ctx.label(cell, -600, yen, "en")

    # vbp bus
    if vbp:
        pts = [g["pads"]["vbp"] for g in geo if "vbp" in g["pads"]]
        for (xp, yp) in pts:
            ctx.mcon_pad(cell, xp, yp)
        ctx.m1_h(cell, pts[0][1], pts[0][0], pts[-1][0])
        ctx.label(cell, pts[0][0], pts[0][1], "vbp")

    yret = YRV + 1400
    pbx, pby = geo[0]["pads"]["out"]
    ctx.mcon_pad(cell, pbx, pby)
    ctx.via_pad(cell, pbx, pby)
    last = geo[-1]
    xo, yo = last["xd"], YREF + Y_OUT
    if not wire:
        ctx.mcon_pad(cell, xo, yo)
        ctx.via_pad(cell, xo, yo)
        ctx.label(cell, xo, yo, "out")
        ctx.m2_v(cell, xo, yo, yret)
        ctx.m2_h(cell, yret, pbx, xo)
        ctx.m2_v(cell, pbx, pby, yret)
        return cell, xmax, yret

    # osc_wire: one met1 serpentine (W 140 nm, centreline 1000 um) per stage output.
    # The band sits under the stage column (not beside it). Each serpentine's two ends are
    # brought out on met2 to a feed column xL at the band's left edge, left of every stage x,
    # so a feed never crosses a serpentine run. Rows run top to bottom in stage order.
    seg = (1_000_000 - (SERP_N - 1) * SERP_PITCH) // SERP_N
    xout = xmax + 1500
    links = []
    for i, g in enumerate(geo):
        a = (g["xd"], YREF + Y_OUT)
        b = geo[i + 1]["pads"]["in"] if i + 1 < len(geo) else (xout, None)
        links.append((a, b))
    xmin = min(min(a[0], b[0]) for a, b in links)
    xL = min(xmin, 0) - 600
    xS = xL + 600
    # stage x must increase with the row index, else an m2 feed would cross another row's
    xs_a = [a[0] for a, b in links]
    xs_b = [b[0] for a, b in links]
    assert xs_a == sorted(xs_a) and xs_b == sorted(xs_b) and all(p < q for p, q in zip(xs_a, xs_b))
    ROW = (SERP_N - 1) * SERP_PITCH + SERP_GAP
    for j, (a, b) in enumerate(links):
        yc0 = -2000 - j * ROW
        ctx.mcon_pad(cell, a[0], a[1])
        ctx.via_pad(cell, a[0], a[1])
        ctx.m2_v(cell, a[0], a[1], yc0)
        ctx.m2_h(cell, yc0, xL, a[0])
        ctx.via_pad(cell, xL, yc0)
        ctx.m1_h(cell, yc0, xL, xS)
        for s in range(SERP_N):
            yy = yc0 - s * SERP_PITCH
            ctx.rect(cell, "met1", xS, yy - 70, xS + seg, yy + 70)
            if s < SERP_N - 1:
                xj = xS + seg if s % 2 == 0 else xS
                ctx.rect(cell, "met1", xj - 70, yy - SERP_PITCH - 70, xj + 70, yy + 70)
        ybe = yc0 - (SERP_N - 1) * SERP_PITCH
        # odd run count ends on the right edge; even (SERP_N) ends back on the left edge
        assert SERP_N % 2 == 0
        ctx.m1_h(cell, ybe, xL, xS)
        ctx.via_pad(cell, xL, ybe)
        ctx.m2_h(cell, ybe, xL, b[0])
        if b[1] is None:
            ctx.label(cell, xL, ybe, "out")
            ctx.m2_v(cell, b[0], ybe, yret)
            ctx.m2_h(cell, yret, pbx, b[0])
            ctx.m2_v(cell, pbx, pby, yret)
        else:
            ctx.m2_v(cell, b[0], ybe, b[1])
            ctx.mcon_pad(cell, b[0], b[1])
            ctx.via_pad(cell, b[0], b[1])
    return cell, max(xmax, xS + seg), yret


# ------------------------------- osc_hd (PDK cells) --------------------------------
def build_hd(ctx, pdk):
    ly = ctx.ly
    cell = ly.create_cell("osc_hd")
    nm = lambda n: ly.cell("sky130_fd_sc_hd__" + n).cell_index()
    NAND, INV, TAP = nm("nand2_1"), nm("inv_1"), nm("tapvpwrvgnd_1")
    plan = ["tap", "nand"] + ["inv"] * 8 + ["tap"] + ["inv"] * 8 + ["tap"] + ["inv"] * 8 + ["tap"] \
        + ["inv"] * 6 + ["tap"]
    x, xs = 0, []
    for p in plan:
        idx = {"tap": TAP, "nand": NAND, "inv": INV}[p]
        cell.insert(db.CellInstArray(idx, db.Trans(x, 0)))
        xs.append((p, x))
        x += 460 if p == "tap" else 1380
    xend = x
    cells = [(p, x0) for p, x0 in xs if p != "tap"]
    assert len(cells) == 31 and cells[0][0] == "nand"
    M = 260
    xn = cells[0][1]
    # enable at nand B, feedback to nand A, nand Y -> first inverter
    ctx.mcon_pad(cell, xn + 225, 1190, M)
    ctx.label(cell, xn + 225, 1190, "en")
    ctx.mcon_pad(cell, xn + 1145, 1190, M)
    ctx.mcon_pad(cell, xn + 685, 850, M)
    x1 = cells[1][1]
    ctx.m1_h(cell, 850, xn + 685, x1 + 445)
    ctx.m1_v(cell, x1 + 445, 850, 1190)
    ctx.mcon_pad(cell, x1 + 445, 1190, M)
    # inverter chain on li1
    for (_, xa), (_, xb) in zip(cells[1:-1], cells[2:]):
        ctx.rect(cell, "li1", xa + 900, 1105, xb + 400, 1275)
    xl = cells[-1][1]
    ctx.mcon_pad(cell, xl + 905, 1190, M)
    ctx.label(cell, xl + 905, 1190, "out")
    ctx.m1_v(cell, xl + 905, 1190, 1700)
    ctx.m1_h(cell, 1700, xn + 1145, xl + 905)
    ctx.m1_v(cell, xn + 1145, 1190, 1700)
    ctx.label(cell, 230, 0, "vss")
    ctx.label(cell, 230, 2720, "vdd")
    return cell, xend, 2960


# ------------------------------------- main ---------------------------------------
def pdk_gds():
    pj = json.load(open(os.path.join(REPO, "sim", "pdk.json")))
    root = os.path.realpath(os.path.expanduser(
        os.environ.get(pj["root_override_env"], pj["default_root"])))
    path = os.path.join(root, "libs.ref/sky130_fd_sc_hd/gds/sky130_fd_sc_hd.gds")
    pin = json.load(open(os.path.join(HERE, "pdk_cells.json")))
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if sha != pin["sky130_fd_sc_hd_gds_sha256"]:
        raise SystemExit(f"PDK cell GDS {path} sha256 {sha} != pinned {pin['sky130_fd_sc_hd_gds_sha256']}")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=os.path.join(REPO, "layout", "osc_bank.gds"))
    args = ap.parse_args()
    ly = db.Layout()
    ly.dbu = 0.001
    ly.read(pdk_gds())
    ctx = Ctx(ly)
    built = {}
    built["osc_hd"] = build_hd(ctx, None)
    for kind in ("osc_nmos", "osc_pmos", "osc_wire", "osc_subth"):
        built[kind] = build_custom(ctx, kind, stages_for(kind), wire=(kind == "osc_wire"),
                                   vbp=(kind == "osc_subth"))
    top = ly.create_cell("osc_bank")
    y = 0
    for kind in ("osc_hd", "osc_nmos", "osc_pmos", "osc_wire", "osc_subth"):
        c = built[kind][0]
        bb = c.bbox()
        top.insert(db.CellInstArray(c.cell_index(), db.Trans(-bb.left, y - bb.bottom)))
        y += bb.height() + 5000
    keep = {top.cell_index()} | set(top.called_cells())
    for ci in [c.cell_index() for c in ly.each_cell() if c.cell_index() not in keep]:
        if ly.is_valid_cell_index(ci):
            ly.delete_cell(ci)
    ly.top_cell()
    opt = db.SaveLayoutOptions()
    opt.format = "GDS2"
    opt.gds2_write_timestamps = False
    opt.gds2_libname = "osc_bank"
    ly.write(args.out, opt)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
