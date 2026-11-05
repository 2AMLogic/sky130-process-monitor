v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {osc_wire: wire-dominated: strong inverters driving a lumped metal-1 RC wire} -300 -300 0 0 0.4 0.4 {}
T {SIMULATION INTENT ONLY - planning-level sizes, not a layout; see design/osc_bank/README.md} -300 -270 0 0 0.4 0.4 {}
C {devices/ipin.sym} -300 -60 0 0 {name=p1 lab=en}
C {devices/opin.sym} -300 0 0 0 {name=p2 lab=out}
C {devices/iopin.sym} -300 -120 0 0 {name=p3 lab=vdd}
C {devices/iopin.sym} -300 120 0 0 {name=p4 lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 0 -60 0 0 {name=Mp1 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 -60 2 0 {name=l2 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 20 -90 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 20 -30 0 0 {name=l4 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 20 -60 0 0 {name=l5 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 80 -60 0 0 {name=Mp6 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 60 -60 2 0 {name=l7 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 100 -90 0 0 {name=l8 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 100 -30 0 0 {name=l9 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 100 -60 0 0 {name=l10 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 0 60 0 0 {name=Mn11 W=8.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 60 2 0 {name=l12 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 20 30 0 0 {name=l13 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 20 90 0 0 {name=l14 sig_type=std_logic lab=mid}
C {devices/lab_pin.sym} 20 60 0 0 {name=l15 sig_type=std_logic lab=vss}
C {sky130_fd_pr/nfet_01v8.sym} 80 150 0 0 {name=Mn16 W=8.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 60 150 2 0 {name=l17 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 100 120 0 0 {name=l18 sig_type=std_logic lab=mid}
C {devices/lab_pin.sym} 100 180 0 0 {name=l19 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 100 150 0 0 {name=l20 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 100 0 1 0 {name=R21 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 70 0 2 0 {name=l22 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 130 0 0 0 {name=l23 sig_type=std_logic lab=n0}
C {devices/capa.sym} 160 100 0 0 {name=C24 m=1 value=100f}
C {devices/lab_pin.sym} 160 70 0 0 {name=l25 sig_type=std_logic lab=n0}
C {devices/lab_pin.sym} 160 130 0 0 {name=l26 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 200 -60 0 0 {name=Mp27 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 180 -60 2 0 {name=l28 sig_type=std_logic lab=n0}
C {devices/lab_pin.sym} 220 -90 0 0 {name=l29 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 220 -30 0 0 {name=l30 sig_type=std_logic lab=s1}
C {devices/lab_pin.sym} 220 -60 0 0 {name=l31 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 200 60 0 0 {name=Mn32 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 180 60 2 0 {name=l33 sig_type=std_logic lab=n0}
C {devices/lab_pin.sym} 220 30 0 0 {name=l34 sig_type=std_logic lab=s1}
C {devices/lab_pin.sym} 220 90 0 0 {name=l35 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 220 60 0 0 {name=l36 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 300 0 1 0 {name=R37 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 270 0 2 0 {name=l38 sig_type=std_logic lab=s1}
C {devices/lab_pin.sym} 330 0 0 0 {name=l39 sig_type=std_logic lab=n1}
C {devices/capa.sym} 360 100 0 0 {name=C40 m=1 value=100f}
C {devices/lab_pin.sym} 360 70 0 0 {name=l41 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 360 130 0 0 {name=l42 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 400 -60 0 0 {name=Mp43 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 380 -60 2 0 {name=l44 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 420 -90 0 0 {name=l45 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 420 -30 0 0 {name=l46 sig_type=std_logic lab=s2}
C {devices/lab_pin.sym} 420 -60 0 0 {name=l47 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 400 60 0 0 {name=Mn48 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 380 60 2 0 {name=l49 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 420 30 0 0 {name=l50 sig_type=std_logic lab=s2}
C {devices/lab_pin.sym} 420 90 0 0 {name=l51 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 420 60 0 0 {name=l52 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 500 0 1 0 {name=R53 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 470 0 2 0 {name=l54 sig_type=std_logic lab=s2}
C {devices/lab_pin.sym} 530 0 0 0 {name=l55 sig_type=std_logic lab=n2}
C {devices/capa.sym} 560 100 0 0 {name=C56 m=1 value=100f}
C {devices/lab_pin.sym} 560 70 0 0 {name=l57 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 560 130 0 0 {name=l58 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 600 -60 0 0 {name=Mp59 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 580 -60 2 0 {name=l60 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 620 -90 0 0 {name=l61 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 620 -30 0 0 {name=l62 sig_type=std_logic lab=s3}
C {devices/lab_pin.sym} 620 -60 0 0 {name=l63 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 600 60 0 0 {name=Mn64 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 580 60 2 0 {name=l65 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 620 30 0 0 {name=l66 sig_type=std_logic lab=s3}
C {devices/lab_pin.sym} 620 90 0 0 {name=l67 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 620 60 0 0 {name=l68 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 700 0 1 0 {name=R69 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 670 0 2 0 {name=l70 sig_type=std_logic lab=s3}
C {devices/lab_pin.sym} 730 0 0 0 {name=l71 sig_type=std_logic lab=n3}
C {devices/capa.sym} 760 100 0 0 {name=C72 m=1 value=100f}
C {devices/lab_pin.sym} 760 70 0 0 {name=l73 sig_type=std_logic lab=n3}
C {devices/lab_pin.sym} 760 130 0 0 {name=l74 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 800 -60 0 0 {name=Mp75 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 780 -60 2 0 {name=l76 sig_type=std_logic lab=n3}
C {devices/lab_pin.sym} 820 -90 0 0 {name=l77 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 820 -30 0 0 {name=l78 sig_type=std_logic lab=s4}
C {devices/lab_pin.sym} 820 -60 0 0 {name=l79 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 800 60 0 0 {name=Mn80 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 780 60 2 0 {name=l81 sig_type=std_logic lab=n3}
C {devices/lab_pin.sym} 820 30 0 0 {name=l82 sig_type=std_logic lab=s4}
C {devices/lab_pin.sym} 820 90 0 0 {name=l83 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 820 60 0 0 {name=l84 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 900 0 1 0 {name=R85 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 870 0 2 0 {name=l86 sig_type=std_logic lab=s4}
C {devices/lab_pin.sym} 930 0 0 0 {name=l87 sig_type=std_logic lab=n4}
C {devices/capa.sym} 960 100 0 0 {name=C88 m=1 value=100f}
C {devices/lab_pin.sym} 960 70 0 0 {name=l89 sig_type=std_logic lab=n4}
C {devices/lab_pin.sym} 960 130 0 0 {name=l90 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 1000 -60 0 0 {name=Mp91 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 980 -60 2 0 {name=l92 sig_type=std_logic lab=n4}
C {devices/lab_pin.sym} 1020 -90 0 0 {name=l93 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1020 -30 0 0 {name=l94 sig_type=std_logic lab=s5}
C {devices/lab_pin.sym} 1020 -60 0 0 {name=l95 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1000 60 0 0 {name=Mn96 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 980 60 2 0 {name=l97 sig_type=std_logic lab=n4}
C {devices/lab_pin.sym} 1020 30 0 0 {name=l98 sig_type=std_logic lab=s5}
C {devices/lab_pin.sym} 1020 90 0 0 {name=l99 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1020 60 0 0 {name=l100 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 1100 0 1 0 {name=R101 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 1070 0 2 0 {name=l102 sig_type=std_logic lab=s5}
C {devices/lab_pin.sym} 1130 0 0 0 {name=l103 sig_type=std_logic lab=n5}
C {devices/capa.sym} 1160 100 0 0 {name=C104 m=1 value=100f}
C {devices/lab_pin.sym} 1160 70 0 0 {name=l105 sig_type=std_logic lab=n5}
C {devices/lab_pin.sym} 1160 130 0 0 {name=l106 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 1200 -60 0 0 {name=Mp107 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1180 -60 2 0 {name=l108 sig_type=std_logic lab=n5}
C {devices/lab_pin.sym} 1220 -90 0 0 {name=l109 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1220 -30 0 0 {name=l110 sig_type=std_logic lab=s6}
C {devices/lab_pin.sym} 1220 -60 0 0 {name=l111 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1200 60 0 0 {name=Mn112 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1180 60 2 0 {name=l113 sig_type=std_logic lab=n5}
C {devices/lab_pin.sym} 1220 30 0 0 {name=l114 sig_type=std_logic lab=s6}
C {devices/lab_pin.sym} 1220 90 0 0 {name=l115 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1220 60 0 0 {name=l116 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 1300 0 1 0 {name=R117 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 1270 0 2 0 {name=l118 sig_type=std_logic lab=s6}
C {devices/lab_pin.sym} 1330 0 0 0 {name=l119 sig_type=std_logic lab=n6}
C {devices/capa.sym} 1360 100 0 0 {name=C120 m=1 value=100f}
C {devices/lab_pin.sym} 1360 70 0 0 {name=l121 sig_type=std_logic lab=n6}
C {devices/lab_pin.sym} 1360 130 0 0 {name=l122 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 1400 -60 0 0 {name=Mp123 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1380 -60 2 0 {name=l124 sig_type=std_logic lab=n6}
C {devices/lab_pin.sym} 1420 -90 0 0 {name=l125 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1420 -30 0 0 {name=l126 sig_type=std_logic lab=s7}
C {devices/lab_pin.sym} 1420 -60 0 0 {name=l127 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1400 60 0 0 {name=Mn128 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1380 60 2 0 {name=l129 sig_type=std_logic lab=n6}
C {devices/lab_pin.sym} 1420 30 0 0 {name=l130 sig_type=std_logic lab=s7}
C {devices/lab_pin.sym} 1420 90 0 0 {name=l131 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1420 60 0 0 {name=l132 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 1500 0 1 0 {name=R133 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 1470 0 2 0 {name=l134 sig_type=std_logic lab=s7}
C {devices/lab_pin.sym} 1530 0 0 0 {name=l135 sig_type=std_logic lab=n7}
C {devices/capa.sym} 1560 100 0 0 {name=C136 m=1 value=100f}
C {devices/lab_pin.sym} 1560 70 0 0 {name=l137 sig_type=std_logic lab=n7}
C {devices/lab_pin.sym} 1560 130 0 0 {name=l138 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 1600 -60 0 0 {name=Mp139 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1580 -60 2 0 {name=l140 sig_type=std_logic lab=n7}
C {devices/lab_pin.sym} 1620 -90 0 0 {name=l141 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1620 -30 0 0 {name=l142 sig_type=std_logic lab=s8}
C {devices/lab_pin.sym} 1620 -60 0 0 {name=l143 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1600 60 0 0 {name=Mn144 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1580 60 2 0 {name=l145 sig_type=std_logic lab=n7}
C {devices/lab_pin.sym} 1620 30 0 0 {name=l146 sig_type=std_logic lab=s8}
C {devices/lab_pin.sym} 1620 90 0 0 {name=l147 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1620 60 0 0 {name=l148 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 1700 0 1 0 {name=R149 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 1670 0 2 0 {name=l150 sig_type=std_logic lab=s8}
C {devices/lab_pin.sym} 1730 0 0 0 {name=l151 sig_type=std_logic lab=n8}
C {devices/capa.sym} 1760 100 0 0 {name=C152 m=1 value=100f}
C {devices/lab_pin.sym} 1760 70 0 0 {name=l153 sig_type=std_logic lab=n8}
C {devices/lab_pin.sym} 1760 130 0 0 {name=l154 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 1800 -60 0 0 {name=Mp155 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1780 -60 2 0 {name=l156 sig_type=std_logic lab=n8}
C {devices/lab_pin.sym} 1820 -90 0 0 {name=l157 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1820 -30 0 0 {name=l158 sig_type=std_logic lab=s9}
C {devices/lab_pin.sym} 1820 -60 0 0 {name=l159 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1800 60 0 0 {name=Mn160 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1780 60 2 0 {name=l161 sig_type=std_logic lab=n8}
C {devices/lab_pin.sym} 1820 30 0 0 {name=l162 sig_type=std_logic lab=s9}
C {devices/lab_pin.sym} 1820 90 0 0 {name=l163 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1820 60 0 0 {name=l164 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 1900 0 1 0 {name=R165 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 1870 0 2 0 {name=l166 sig_type=std_logic lab=s9}
C {devices/lab_pin.sym} 1930 0 0 0 {name=l167 sig_type=std_logic lab=n9}
C {devices/capa.sym} 1960 100 0 0 {name=C168 m=1 value=100f}
C {devices/lab_pin.sym} 1960 70 0 0 {name=l169 sig_type=std_logic lab=n9}
C {devices/lab_pin.sym} 1960 130 0 0 {name=l170 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 2000 -60 0 0 {name=Mp171 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1980 -60 2 0 {name=l172 sig_type=std_logic lab=n9}
C {devices/lab_pin.sym} 2020 -90 0 0 {name=l173 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2020 -30 0 0 {name=l174 sig_type=std_logic lab=s10}
C {devices/lab_pin.sym} 2020 -60 0 0 {name=l175 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2000 60 0 0 {name=Mn176 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1980 60 2 0 {name=l177 sig_type=std_logic lab=n9}
C {devices/lab_pin.sym} 2020 30 0 0 {name=l178 sig_type=std_logic lab=s10}
C {devices/lab_pin.sym} 2020 90 0 0 {name=l179 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2020 60 0 0 {name=l180 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 2100 0 1 0 {name=R181 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 2070 0 2 0 {name=l182 sig_type=std_logic lab=s10}
C {devices/lab_pin.sym} 2130 0 0 0 {name=l183 sig_type=std_logic lab=n10}
C {devices/capa.sym} 2160 100 0 0 {name=C184 m=1 value=100f}
C {devices/lab_pin.sym} 2160 70 0 0 {name=l185 sig_type=std_logic lab=n10}
C {devices/lab_pin.sym} 2160 130 0 0 {name=l186 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 2200 -60 0 0 {name=Mp187 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2180 -60 2 0 {name=l188 sig_type=std_logic lab=n10}
C {devices/lab_pin.sym} 2220 -90 0 0 {name=l189 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2220 -30 0 0 {name=l190 sig_type=std_logic lab=s11}
C {devices/lab_pin.sym} 2220 -60 0 0 {name=l191 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2200 60 0 0 {name=Mn192 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2180 60 2 0 {name=l193 sig_type=std_logic lab=n10}
C {devices/lab_pin.sym} 2220 30 0 0 {name=l194 sig_type=std_logic lab=s11}
C {devices/lab_pin.sym} 2220 90 0 0 {name=l195 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2220 60 0 0 {name=l196 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 2300 0 1 0 {name=R197 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 2270 0 2 0 {name=l198 sig_type=std_logic lab=s11}
C {devices/lab_pin.sym} 2330 0 0 0 {name=l199 sig_type=std_logic lab=n11}
C {devices/capa.sym} 2360 100 0 0 {name=C200 m=1 value=100f}
C {devices/lab_pin.sym} 2360 70 0 0 {name=l201 sig_type=std_logic lab=n11}
C {devices/lab_pin.sym} 2360 130 0 0 {name=l202 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 2400 -60 0 0 {name=Mp203 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2380 -60 2 0 {name=l204 sig_type=std_logic lab=n11}
C {devices/lab_pin.sym} 2420 -90 0 0 {name=l205 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2420 -30 0 0 {name=l206 sig_type=std_logic lab=s12}
C {devices/lab_pin.sym} 2420 -60 0 0 {name=l207 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2400 60 0 0 {name=Mn208 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2380 60 2 0 {name=l209 sig_type=std_logic lab=n11}
C {devices/lab_pin.sym} 2420 30 0 0 {name=l210 sig_type=std_logic lab=s12}
C {devices/lab_pin.sym} 2420 90 0 0 {name=l211 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2420 60 0 0 {name=l212 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 2500 0 1 0 {name=R213 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 2470 0 2 0 {name=l214 sig_type=std_logic lab=s12}
C {devices/lab_pin.sym} 2530 0 0 0 {name=l215 sig_type=std_logic lab=n12}
C {devices/capa.sym} 2560 100 0 0 {name=C216 m=1 value=100f}
C {devices/lab_pin.sym} 2560 70 0 0 {name=l217 sig_type=std_logic lab=n12}
C {devices/lab_pin.sym} 2560 130 0 0 {name=l218 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 2600 -60 0 0 {name=Mp219 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2580 -60 2 0 {name=l220 sig_type=std_logic lab=n12}
C {devices/lab_pin.sym} 2620 -90 0 0 {name=l221 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2620 -30 0 0 {name=l222 sig_type=std_logic lab=s13}
C {devices/lab_pin.sym} 2620 -60 0 0 {name=l223 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2600 60 0 0 {name=Mn224 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2580 60 2 0 {name=l225 sig_type=std_logic lab=n12}
C {devices/lab_pin.sym} 2620 30 0 0 {name=l226 sig_type=std_logic lab=s13}
C {devices/lab_pin.sym} 2620 90 0 0 {name=l227 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2620 60 0 0 {name=l228 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 2700 0 1 0 {name=R229 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 2670 0 2 0 {name=l230 sig_type=std_logic lab=s13}
C {devices/lab_pin.sym} 2730 0 0 0 {name=l231 sig_type=std_logic lab=n13}
C {devices/capa.sym} 2760 100 0 0 {name=C232 m=1 value=100f}
C {devices/lab_pin.sym} 2760 70 0 0 {name=l233 sig_type=std_logic lab=n13}
C {devices/lab_pin.sym} 2760 130 0 0 {name=l234 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 2800 -60 0 0 {name=Mp235 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2780 -60 2 0 {name=l236 sig_type=std_logic lab=n13}
C {devices/lab_pin.sym} 2820 -90 0 0 {name=l237 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2820 -30 0 0 {name=l238 sig_type=std_logic lab=s14}
C {devices/lab_pin.sym} 2820 -60 0 0 {name=l239 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2800 60 0 0 {name=Mn240 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2780 60 2 0 {name=l241 sig_type=std_logic lab=n13}
C {devices/lab_pin.sym} 2820 30 0 0 {name=l242 sig_type=std_logic lab=s14}
C {devices/lab_pin.sym} 2820 90 0 0 {name=l243 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2820 60 0 0 {name=l244 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 2900 0 1 0 {name=R245 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 2870 0 2 0 {name=l246 sig_type=std_logic lab=s14}
C {devices/lab_pin.sym} 2930 0 0 0 {name=l247 sig_type=std_logic lab=n14}
C {devices/capa.sym} 2960 100 0 0 {name=C248 m=1 value=100f}
C {devices/lab_pin.sym} 2960 70 0 0 {name=l249 sig_type=std_logic lab=n14}
C {devices/lab_pin.sym} 2960 130 0 0 {name=l250 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 3000 -60 0 0 {name=Mp251 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2980 -60 2 0 {name=l252 sig_type=std_logic lab=n14}
C {devices/lab_pin.sym} 3020 -90 0 0 {name=l253 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 3020 -30 0 0 {name=l254 sig_type=std_logic lab=s15}
C {devices/lab_pin.sym} 3020 -60 0 0 {name=l255 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 3000 60 0 0 {name=Mn256 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2980 60 2 0 {name=l257 sig_type=std_logic lab=n14}
C {devices/lab_pin.sym} 3020 30 0 0 {name=l258 sig_type=std_logic lab=s15}
C {devices/lab_pin.sym} 3020 90 0 0 {name=l259 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 3020 60 0 0 {name=l260 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 3100 0 1 0 {name=R261 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 3070 0 2 0 {name=l262 sig_type=std_logic lab=s15}
C {devices/lab_pin.sym} 3130 0 0 0 {name=l263 sig_type=std_logic lab=n15}
C {devices/capa.sym} 3160 100 0 0 {name=C264 m=1 value=100f}
C {devices/lab_pin.sym} 3160 70 0 0 {name=l265 sig_type=std_logic lab=n15}
C {devices/lab_pin.sym} 3160 130 0 0 {name=l266 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 3200 -60 0 0 {name=Mp267 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3180 -60 2 0 {name=l268 sig_type=std_logic lab=n15}
C {devices/lab_pin.sym} 3220 -90 0 0 {name=l269 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 3220 -30 0 0 {name=l270 sig_type=std_logic lab=s16}
C {devices/lab_pin.sym} 3220 -60 0 0 {name=l271 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 3200 60 0 0 {name=Mn272 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3180 60 2 0 {name=l273 sig_type=std_logic lab=n15}
C {devices/lab_pin.sym} 3220 30 0 0 {name=l274 sig_type=std_logic lab=s16}
C {devices/lab_pin.sym} 3220 90 0 0 {name=l275 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 3220 60 0 0 {name=l276 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 3300 0 1 0 {name=R277 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 3270 0 2 0 {name=l278 sig_type=std_logic lab=s16}
C {devices/lab_pin.sym} 3330 0 0 0 {name=l279 sig_type=std_logic lab=n16}
C {devices/capa.sym} 3360 100 0 0 {name=C280 m=1 value=100f}
C {devices/lab_pin.sym} 3360 70 0 0 {name=l281 sig_type=std_logic lab=n16}
C {devices/lab_pin.sym} 3360 130 0 0 {name=l282 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 3400 -60 0 0 {name=Mp283 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3380 -60 2 0 {name=l284 sig_type=std_logic lab=n16}
C {devices/lab_pin.sym} 3420 -90 0 0 {name=l285 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 3420 -30 0 0 {name=l286 sig_type=std_logic lab=s17}
C {devices/lab_pin.sym} 3420 -60 0 0 {name=l287 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 3400 60 0 0 {name=Mn288 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3380 60 2 0 {name=l289 sig_type=std_logic lab=n16}
C {devices/lab_pin.sym} 3420 30 0 0 {name=l290 sig_type=std_logic lab=s17}
C {devices/lab_pin.sym} 3420 90 0 0 {name=l291 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 3420 60 0 0 {name=l292 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 3500 0 1 0 {name=R293 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 3470 0 2 0 {name=l294 sig_type=std_logic lab=s17}
C {devices/lab_pin.sym} 3530 0 0 0 {name=l295 sig_type=std_logic lab=n17}
C {devices/capa.sym} 3560 100 0 0 {name=C296 m=1 value=100f}
C {devices/lab_pin.sym} 3560 70 0 0 {name=l297 sig_type=std_logic lab=n17}
C {devices/lab_pin.sym} 3560 130 0 0 {name=l298 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 3600 -60 0 0 {name=Mp299 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3580 -60 2 0 {name=l300 sig_type=std_logic lab=n17}
C {devices/lab_pin.sym} 3620 -90 0 0 {name=l301 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 3620 -30 0 0 {name=l302 sig_type=std_logic lab=s18}
C {devices/lab_pin.sym} 3620 -60 0 0 {name=l303 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 3600 60 0 0 {name=Mn304 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3580 60 2 0 {name=l305 sig_type=std_logic lab=n17}
C {devices/lab_pin.sym} 3620 30 0 0 {name=l306 sig_type=std_logic lab=s18}
C {devices/lab_pin.sym} 3620 90 0 0 {name=l307 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 3620 60 0 0 {name=l308 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 3700 0 1 0 {name=R309 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 3670 0 2 0 {name=l310 sig_type=std_logic lab=s18}
C {devices/lab_pin.sym} 3730 0 0 0 {name=l311 sig_type=std_logic lab=n18}
C {devices/capa.sym} 3760 100 0 0 {name=C312 m=1 value=100f}
C {devices/lab_pin.sym} 3760 70 0 0 {name=l313 sig_type=std_logic lab=n18}
C {devices/lab_pin.sym} 3760 130 0 0 {name=l314 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 3800 -60 0 0 {name=Mp315 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3780 -60 2 0 {name=l316 sig_type=std_logic lab=n18}
C {devices/lab_pin.sym} 3820 -90 0 0 {name=l317 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 3820 -30 0 0 {name=l318 sig_type=std_logic lab=s19}
C {devices/lab_pin.sym} 3820 -60 0 0 {name=l319 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 3800 60 0 0 {name=Mn320 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3780 60 2 0 {name=l321 sig_type=std_logic lab=n18}
C {devices/lab_pin.sym} 3820 30 0 0 {name=l322 sig_type=std_logic lab=s19}
C {devices/lab_pin.sym} 3820 90 0 0 {name=l323 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 3820 60 0 0 {name=l324 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 3900 0 1 0 {name=R325 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 3870 0 2 0 {name=l326 sig_type=std_logic lab=s19}
C {devices/lab_pin.sym} 3930 0 0 0 {name=l327 sig_type=std_logic lab=n19}
C {devices/capa.sym} 3960 100 0 0 {name=C328 m=1 value=100f}
C {devices/lab_pin.sym} 3960 70 0 0 {name=l329 sig_type=std_logic lab=n19}
C {devices/lab_pin.sym} 3960 130 0 0 {name=l330 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 4000 -60 0 0 {name=Mp331 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3980 -60 2 0 {name=l332 sig_type=std_logic lab=n19}
C {devices/lab_pin.sym} 4020 -90 0 0 {name=l333 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 4020 -30 0 0 {name=l334 sig_type=std_logic lab=s20}
C {devices/lab_pin.sym} 4020 -60 0 0 {name=l335 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 4000 60 0 0 {name=Mn336 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 3980 60 2 0 {name=l337 sig_type=std_logic lab=n19}
C {devices/lab_pin.sym} 4020 30 0 0 {name=l338 sig_type=std_logic lab=s20}
C {devices/lab_pin.sym} 4020 90 0 0 {name=l339 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 4020 60 0 0 {name=l340 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 4100 0 1 0 {name=R341 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 4070 0 2 0 {name=l342 sig_type=std_logic lab=s20}
C {devices/lab_pin.sym} 4130 0 0 0 {name=l343 sig_type=std_logic lab=n20}
C {devices/capa.sym} 4160 100 0 0 {name=C344 m=1 value=100f}
C {devices/lab_pin.sym} 4160 70 0 0 {name=l345 sig_type=std_logic lab=n20}
C {devices/lab_pin.sym} 4160 130 0 0 {name=l346 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 4200 -60 0 0 {name=Mp347 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4180 -60 2 0 {name=l348 sig_type=std_logic lab=n20}
C {devices/lab_pin.sym} 4220 -90 0 0 {name=l349 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 4220 -30 0 0 {name=l350 sig_type=std_logic lab=s21}
C {devices/lab_pin.sym} 4220 -60 0 0 {name=l351 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 4200 60 0 0 {name=Mn352 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4180 60 2 0 {name=l353 sig_type=std_logic lab=n20}
C {devices/lab_pin.sym} 4220 30 0 0 {name=l354 sig_type=std_logic lab=s21}
C {devices/lab_pin.sym} 4220 90 0 0 {name=l355 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 4220 60 0 0 {name=l356 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 4300 0 1 0 {name=R357 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 4270 0 2 0 {name=l358 sig_type=std_logic lab=s21}
C {devices/lab_pin.sym} 4330 0 0 0 {name=l359 sig_type=std_logic lab=n21}
C {devices/capa.sym} 4360 100 0 0 {name=C360 m=1 value=100f}
C {devices/lab_pin.sym} 4360 70 0 0 {name=l361 sig_type=std_logic lab=n21}
C {devices/lab_pin.sym} 4360 130 0 0 {name=l362 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 4400 -60 0 0 {name=Mp363 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4380 -60 2 0 {name=l364 sig_type=std_logic lab=n21}
C {devices/lab_pin.sym} 4420 -90 0 0 {name=l365 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 4420 -30 0 0 {name=l366 sig_type=std_logic lab=s22}
C {devices/lab_pin.sym} 4420 -60 0 0 {name=l367 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 4400 60 0 0 {name=Mn368 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4380 60 2 0 {name=l369 sig_type=std_logic lab=n21}
C {devices/lab_pin.sym} 4420 30 0 0 {name=l370 sig_type=std_logic lab=s22}
C {devices/lab_pin.sym} 4420 90 0 0 {name=l371 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 4420 60 0 0 {name=l372 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 4500 0 1 0 {name=R373 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 4470 0 2 0 {name=l374 sig_type=std_logic lab=s22}
C {devices/lab_pin.sym} 4530 0 0 0 {name=l375 sig_type=std_logic lab=n22}
C {devices/capa.sym} 4560 100 0 0 {name=C376 m=1 value=100f}
C {devices/lab_pin.sym} 4560 70 0 0 {name=l377 sig_type=std_logic lab=n22}
C {devices/lab_pin.sym} 4560 130 0 0 {name=l378 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 4600 -60 0 0 {name=Mp379 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4580 -60 2 0 {name=l380 sig_type=std_logic lab=n22}
C {devices/lab_pin.sym} 4620 -90 0 0 {name=l381 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 4620 -30 0 0 {name=l382 sig_type=std_logic lab=s23}
C {devices/lab_pin.sym} 4620 -60 0 0 {name=l383 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 4600 60 0 0 {name=Mn384 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4580 60 2 0 {name=l385 sig_type=std_logic lab=n22}
C {devices/lab_pin.sym} 4620 30 0 0 {name=l386 sig_type=std_logic lab=s23}
C {devices/lab_pin.sym} 4620 90 0 0 {name=l387 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 4620 60 0 0 {name=l388 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 4700 0 1 0 {name=R389 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 4670 0 2 0 {name=l390 sig_type=std_logic lab=s23}
C {devices/lab_pin.sym} 4730 0 0 0 {name=l391 sig_type=std_logic lab=n23}
C {devices/capa.sym} 4760 100 0 0 {name=C392 m=1 value=100f}
C {devices/lab_pin.sym} 4760 70 0 0 {name=l393 sig_type=std_logic lab=n23}
C {devices/lab_pin.sym} 4760 130 0 0 {name=l394 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 4800 -60 0 0 {name=Mp395 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4780 -60 2 0 {name=l396 sig_type=std_logic lab=n23}
C {devices/lab_pin.sym} 4820 -90 0 0 {name=l397 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 4820 -30 0 0 {name=l398 sig_type=std_logic lab=s24}
C {devices/lab_pin.sym} 4820 -60 0 0 {name=l399 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 4800 60 0 0 {name=Mn400 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4780 60 2 0 {name=l401 sig_type=std_logic lab=n23}
C {devices/lab_pin.sym} 4820 30 0 0 {name=l402 sig_type=std_logic lab=s24}
C {devices/lab_pin.sym} 4820 90 0 0 {name=l403 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 4820 60 0 0 {name=l404 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 4900 0 1 0 {name=R405 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 4870 0 2 0 {name=l406 sig_type=std_logic lab=s24}
C {devices/lab_pin.sym} 4930 0 0 0 {name=l407 sig_type=std_logic lab=n24}
C {devices/capa.sym} 4960 100 0 0 {name=C408 m=1 value=100f}
C {devices/lab_pin.sym} 4960 70 0 0 {name=l409 sig_type=std_logic lab=n24}
C {devices/lab_pin.sym} 4960 130 0 0 {name=l410 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 5000 -60 0 0 {name=Mp411 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4980 -60 2 0 {name=l412 sig_type=std_logic lab=n24}
C {devices/lab_pin.sym} 5020 -90 0 0 {name=l413 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 5020 -30 0 0 {name=l414 sig_type=std_logic lab=s25}
C {devices/lab_pin.sym} 5020 -60 0 0 {name=l415 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 5000 60 0 0 {name=Mn416 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 4980 60 2 0 {name=l417 sig_type=std_logic lab=n24}
C {devices/lab_pin.sym} 5020 30 0 0 {name=l418 sig_type=std_logic lab=s25}
C {devices/lab_pin.sym} 5020 90 0 0 {name=l419 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 5020 60 0 0 {name=l420 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 5100 0 1 0 {name=R421 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 5070 0 2 0 {name=l422 sig_type=std_logic lab=s25}
C {devices/lab_pin.sym} 5130 0 0 0 {name=l423 sig_type=std_logic lab=n25}
C {devices/capa.sym} 5160 100 0 0 {name=C424 m=1 value=100f}
C {devices/lab_pin.sym} 5160 70 0 0 {name=l425 sig_type=std_logic lab=n25}
C {devices/lab_pin.sym} 5160 130 0 0 {name=l426 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 5200 -60 0 0 {name=Mp427 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5180 -60 2 0 {name=l428 sig_type=std_logic lab=n25}
C {devices/lab_pin.sym} 5220 -90 0 0 {name=l429 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 5220 -30 0 0 {name=l430 sig_type=std_logic lab=s26}
C {devices/lab_pin.sym} 5220 -60 0 0 {name=l431 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 5200 60 0 0 {name=Mn432 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5180 60 2 0 {name=l433 sig_type=std_logic lab=n25}
C {devices/lab_pin.sym} 5220 30 0 0 {name=l434 sig_type=std_logic lab=s26}
C {devices/lab_pin.sym} 5220 90 0 0 {name=l435 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 5220 60 0 0 {name=l436 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 5300 0 1 0 {name=R437 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 5270 0 2 0 {name=l438 sig_type=std_logic lab=s26}
C {devices/lab_pin.sym} 5330 0 0 0 {name=l439 sig_type=std_logic lab=n26}
C {devices/capa.sym} 5360 100 0 0 {name=C440 m=1 value=100f}
C {devices/lab_pin.sym} 5360 70 0 0 {name=l441 sig_type=std_logic lab=n26}
C {devices/lab_pin.sym} 5360 130 0 0 {name=l442 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 5400 -60 0 0 {name=Mp443 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5380 -60 2 0 {name=l444 sig_type=std_logic lab=n26}
C {devices/lab_pin.sym} 5420 -90 0 0 {name=l445 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 5420 -30 0 0 {name=l446 sig_type=std_logic lab=s27}
C {devices/lab_pin.sym} 5420 -60 0 0 {name=l447 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 5400 60 0 0 {name=Mn448 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5380 60 2 0 {name=l449 sig_type=std_logic lab=n26}
C {devices/lab_pin.sym} 5420 30 0 0 {name=l450 sig_type=std_logic lab=s27}
C {devices/lab_pin.sym} 5420 90 0 0 {name=l451 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 5420 60 0 0 {name=l452 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 5500 0 1 0 {name=R453 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 5470 0 2 0 {name=l454 sig_type=std_logic lab=s27}
C {devices/lab_pin.sym} 5530 0 0 0 {name=l455 sig_type=std_logic lab=n27}
C {devices/capa.sym} 5560 100 0 0 {name=C456 m=1 value=100f}
C {devices/lab_pin.sym} 5560 70 0 0 {name=l457 sig_type=std_logic lab=n27}
C {devices/lab_pin.sym} 5560 130 0 0 {name=l458 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 5600 -60 0 0 {name=Mp459 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5580 -60 2 0 {name=l460 sig_type=std_logic lab=n27}
C {devices/lab_pin.sym} 5620 -90 0 0 {name=l461 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 5620 -30 0 0 {name=l462 sig_type=std_logic lab=s28}
C {devices/lab_pin.sym} 5620 -60 0 0 {name=l463 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 5600 60 0 0 {name=Mn464 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5580 60 2 0 {name=l465 sig_type=std_logic lab=n27}
C {devices/lab_pin.sym} 5620 30 0 0 {name=l466 sig_type=std_logic lab=s28}
C {devices/lab_pin.sym} 5620 90 0 0 {name=l467 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 5620 60 0 0 {name=l468 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 5700 0 1 0 {name=R469 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 5670 0 2 0 {name=l470 sig_type=std_logic lab=s28}
C {devices/lab_pin.sym} 5730 0 0 0 {name=l471 sig_type=std_logic lab=n28}
C {devices/capa.sym} 5760 100 0 0 {name=C472 m=1 value=100f}
C {devices/lab_pin.sym} 5760 70 0 0 {name=l473 sig_type=std_logic lab=n28}
C {devices/lab_pin.sym} 5760 130 0 0 {name=l474 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 5800 -60 0 0 {name=Mp475 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5780 -60 2 0 {name=l476 sig_type=std_logic lab=n28}
C {devices/lab_pin.sym} 5820 -90 0 0 {name=l477 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 5820 -30 0 0 {name=l478 sig_type=std_logic lab=s29}
C {devices/lab_pin.sym} 5820 -60 0 0 {name=l479 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 5800 60 0 0 {name=Mn480 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5780 60 2 0 {name=l481 sig_type=std_logic lab=n28}
C {devices/lab_pin.sym} 5820 30 0 0 {name=l482 sig_type=std_logic lab=s29}
C {devices/lab_pin.sym} 5820 90 0 0 {name=l483 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 5820 60 0 0 {name=l484 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 5900 0 1 0 {name=R485 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 5870 0 2 0 {name=l486 sig_type=std_logic lab=s29}
C {devices/lab_pin.sym} 5930 0 0 0 {name=l487 sig_type=std_logic lab=n29}
C {devices/capa.sym} 5960 100 0 0 {name=C488 m=1 value=100f}
C {devices/lab_pin.sym} 5960 70 0 0 {name=l489 sig_type=std_logic lab=n29}
C {devices/lab_pin.sym} 5960 130 0 0 {name=l490 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 6000 -60 0 0 {name=Mp491 W=8.0 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5980 -60 2 0 {name=l492 sig_type=std_logic lab=n29}
C {devices/lab_pin.sym} 6020 -90 0 0 {name=l493 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 6020 -30 0 0 {name=l494 sig_type=std_logic lab=s30}
C {devices/lab_pin.sym} 6020 -60 0 0 {name=l495 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 6000 60 0 0 {name=Mn496 W=4.0 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 5980 60 2 0 {name=l497 sig_type=std_logic lab=n29}
C {devices/lab_pin.sym} 6020 30 0 0 {name=l498 sig_type=std_logic lab=s30}
C {devices/lab_pin.sym} 6020 90 0 0 {name=l499 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 6020 60 0 0 {name=l500 sig_type=std_logic lab=vss}
C {sky130_fd_pr/res_generic_m1.sym} 6100 0 1 0 {name=R501 W=0.14 L=1000 model=res_generic_m1 mult=1}
C {devices/lab_pin.sym} 6070 0 2 0 {name=l502 sig_type=std_logic lab=s30}
C {devices/lab_pin.sym} 6130 0 0 0 {name=l503 sig_type=std_logic lab=out}
C {devices/capa.sym} 6160 100 0 0 {name=C504 m=1 value=100f}
C {devices/lab_pin.sym} 6160 70 0 0 {name=l505 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 6160 130 0 0 {name=l506 sig_type=std_logic lab=vss}
