#!/usr/bin/env python3 -I
"""Generate the five oscillator-bank xschem schematics (design/osc_bank/*.sch).

The schematics are committed; this script is how they were drawn, so a stage
count or a device size changes in one place.  Stage counts are the ratified
planning figures of spec/target-spec.md section 1 (31 / 31 / 31 / 15 / 31):
changing them needs a new decision record, not an edit here.

Every ring is a chain of inverting stages whose FIRST stage is a NAND2 with the
enable on its second input, so each ring has an odd inversion count and
`en`=0 parks it in a defined state.  Ports: en (in), out (out), vdd, vss.

Connectivity is by net-name stubs (a 10-unit wire carrying lab=NET on every
pin), so the files are readable in xschem without long wires.

Usage: python3 -I design/osc_bank/gen_schematics.py   (rewrites the .sch files)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PITCH = 200

NFET, PFET = "sky130_fd_pr/nfet_01v8.sym", "sky130_fd_pr/pfet_01v8.sym"
RES, CAP = "sky130_fd_pr/res_generic_m1.sym", "devices/capa.sym"
INV, NAND2 = "sky130_stdcells/inv_1.sym", "sky130_stdcells/nand2_1.sym"


class Sheet:
    def __init__(self, title):
        self.items = []
        self.n = 0
        self.title = title

    def uid(self, p):
        self.n += 1
        return f"{p}{self.n}"

    def stub(self, x, y, dx, net):
        rot = 0 if dx > 0 else 2
        self.n += 1
        self.items.append(f"C {{devices/lab_pin.sym}} {x} {y} {rot} 0 {{name=l{self.n} sig_type=std_logic lab={net}}}")

    def inst(self, sym, x, y, props, rot=0, flip=0):
        self.items.append(f"C {{{sym}}} {x} {y} {rot} {flip} {{{props}}}")

    def text(self, x, y, s, size=0.4):
        self.items.append(f"T {{{s}}} {x} {y} 0 0 {size} {size} {{}}")

    def fet(self, kind, x, y, d, g, s, b, w, l, lvt=False):
        suffix = "_lvt" if lvt else ""
        model = ("nfet_01v8" if kind == "n" else "pfet_01v8") + suffix
        sym = "sky130_fd_pr/" + model + ".sym"
        nm = self.uid("M" + kind)
        self.inst(sym, x, y, f"name={nm} W={w} L={l} nf=1 mult=1 model={model} spiceprefix=X")
        # pin offsets: nfet D(20,-30) S(20,30); pfet S(20,-30) D(20,30); G(-20,0) B(20,0)
        top, bot = (d, s) if kind == "n" else (s, d)
        self.stub(x - 20, y, -10, g)
        self.stub(x + 20, y - 30, 10, top)
        self.stub(x + 20, y + 30, 10, bot)
        self.stub(x + 20, y, 10, b)

    def render(self):
        head = ["v {xschem version=3.4.4 file_version=1.2", "}", "G {}", "K {}", "V {}", "S {}", "E {}"]
        return "\n".join(head + self.items) + "\n"


def ports(sh, ymid):
    for i, (nm, sym, y) in enumerate((("en", "devices/ipin.sym", ymid - 60),
                                      ("out", "devices/opin.sym", ymid),
                                      ("vdd", "devices/iopin.sym", ymid - 120),
                                      ("vss", "devices/iopin.sym", ymid + 120))):
        sh.inst(sym, -300, y, f"name=p{i + 1} lab={nm}")


def inv_custom(sh, x, nin, nout, wn, ln, wp, lp, vp="vdd", vn="vss"):
    sh.fet("p", x, -60, nout, nin, vp, "vdd", wp, lp)
    sh.fet("n", x, 60, nout, nin, vn, "vss", wn, ln)


def nand_custom(sh, x, nin, en, nout, wn, ln, wp, lp):
    sh.fet("p", x, -60, nout, nin, "vdd", "vdd", wp, lp)
    sh.fet("p", x + 80, -60, nout, en, "vdd", "vdd", wp, lp)
    sh.fet("n", x, 60, nout, nin, "mid", "vss", wn, ln)
    sh.fet("n", x + 80, 60 + 90, "mid", en, "vss", "vss", wn, ln)


def ring(name, stages, stage_fn, first_fn, title, extra=None):
    sh = Sheet(title)
    sh.text(-300, -300, f"{name}: {title}")
    sh.text(-300, -270, "SIMULATION INTENT ONLY - planning-level sizes, not a layout; see design/osc_bank/README.md")
    ports(sh, 0)
    for stage in range(stages):
        x = stage * PITCH
        nin = f"n{stage - 1}" if stage else "out"
        nout = "out" if stage == stages - 1 else f"n{stage}"
        if stage == 0:
            first_fn(sh, x, nin, nout)
        else:
            stage_fn(sh, x, nin, nout, stage)
        if extra:
            extra(sh, x, nout, stage)
    # ring closure: the last stage drives net "out", which stage 0 reads.
    return sh


def bias_divider(sh):
    """vdd -Rt- vbp -Rb- vss : vbp ~ 1.5 V at 1.8 V (header Vsg ~ 0.3 V).
    Ideal resistors: a ratiometric simulation placeholder for the starving-device
    bias, NOT a bias-generator design (no tempco, no mismatch)."""
    for i, (top, bot, val) in enumerate((("vdd", "vbp", "300k"), ("vbp", "vss", "1500k"))):
        x = -200 + 60 * i
        sh.inst("devices/res.sym", x, 300, f"name=Rb{i} value={val} m=1")
        sh.stub(x, 270, 10, top)
        sh.stub(x, 330, 10, bot)


def make(name, stages, title, wn, ln, wp, lp, wire=None, starve=None):
    """wn/ln/wp/lp: inverter (and NAND) sizes. wire=(L_um, C_fF): series metal-1
    resistor + shunt C at every stage output. starve=(wh,lh): subthreshold-biased LVT PMOS header
    in each inverting stage after the NAND."""
    def first(sh, x, nin, nout):
        outnet = f"s{0}" if wire else nout
        nand_custom(sh, x, nin, "en", outnet, wn * 2, ln, wp, lp)

    def stage(sh, x, nin, nout, i):
        outnet = f"s{i}" if wire else nout
        if starve:
            wh, lh = starve
            vh = f"vh{i}"
            inv_custom(sh, x, nin, outnet, wn, ln, wp, lp, vp=vh)
            # header only: LVT PMOS S=vdd, G=vbp, D=vh. Its gate is held 0.3 V inside
            # the rail by a shared divider, so it runs in subthreshold and sets the
            # rising-edge delay; the falling edge stays regenerative (a header AND a
            # footer left every stage in a stable low-gain equilibrium: no oscillation).
            sh.fet("p", x + 80, -150, vh, "vbp", "vdd", "vdd", wh, lh, lvt=True)
        else:
            inv_custom(sh, x, nin, outnet, wn, ln, wp, lp)

    def extra(sh, x, nout, i):
        if not wire:
            return
        L, C = wire
        # wire: R from stage output s{i} to the next stage input net
        dest = nout
        rn = sh.uid("R")
        sh.inst(RES, x + 100, 0, f"name={rn} W=0.14 L={L} model=res_generic_m1 mult=1", rot=1)
        # rot=1 puts pins on the horizontal axis; stub them to the two nets
        sh.stub(x + 70, 0, -10, f"s{i}")
        sh.stub(x + 130, 0, 10, dest)
        cn = sh.uid("C")
        sh.inst(CAP, x + 160, 100, f"name={cn} m=1 value={C}f")
        sh.stub(x + 160, 70, 10, dest)
        sh.stub(x + 160, 130, 10, "vss")

    sh = ring(name, stages, stage, first, title, extra)
    if starve:
        bias_divider(sh)
    return sh


SPECS = {
    # name: (stages, title, kwargs)
    "osc_hd": None,
    "osc_nmos": (31, "NMOS-dominated: long-L min-W pull-down, wide fast pull-up",
                 dict(wn=0.42, ln=0.5, wp=3.0, lp=0.15)),
    "osc_pmos": (31, "PMOS-dominated: long-L min-W pull-up, wide fast pull-down",
                 dict(wn=3.0, ln=0.15, wp=0.42, lp=0.5)),
    "osc_wire": (31, "wire-dominated: strong inverters driving a lumped metal-1 RC wire",
                 dict(wn=4.0, ln=0.15, wp=8.0, lp=0.15, wire=(1000, 100))),
    "osc_subth": (15, "subthreshold-starved: subthreshold-biased LVT PMOS header on every inverter after the NAND",
                  dict(wn=0.42, ln=0.15, wp=0.84, lp=0.15, starve=(0.42, 0.5))),
}


def hd(stages=31):
    sh = Sheet("hd baseline")
    sh.text(-300, -300, "osc_hd: plain sky130_fd_sc_hd chain (NAND2 enable stage + inv_1)")
    sh.text(-300, -270, "SIMULATION INTENT ONLY - stock standard cells, baseline oscillator")
    ports(sh, 0)
    extra = "VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__"
    for i in range(stages):
        x = i * PITCH
        nin = f"n{i - 1}" if i else "out"
        nout = "out" if i == stages - 1 else f"n{i}"
        if i == 0:
            sh.inst(NAND2, x, 0, f"name=x{i} {extra}")
            sh.stub(x - 60, -20, -10, nin)
            sh.stub(x - 60, 20, -10, "en")
            sh.stub(x + 60, 0, 10, nout)
        else:
            sh.inst(INV, x, 0, f"name=x{i} {extra}")
            sh.stub(x - 40, 0, -10, nin)
            sh.stub(x + 40, 0, 10, nout)
    return sh


def main():
    out = {"osc_hd": hd()}
    for name, spec in SPECS.items():
        if spec:
            stages, title, kw = spec
            out[name] = make(name, stages, title, **kw)
    for name, sh in out.items():
        with open(os.path.join(HERE, name + ".sch"), "w") as f:
            f.write(sh.render())
        print("wrote", name + ".sch")


if __name__ == "__main__":
    main()
