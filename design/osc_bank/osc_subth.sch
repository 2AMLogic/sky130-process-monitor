v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {osc_subth: subthreshold-starved: subthreshold-biased LVT PMOS header on every inverter after the NAND} -300 -300 0 0 0.4 0.4 {}
T {SIMULATION INTENT ONLY - planning-level sizes, not a layout; see design/osc_bank/README.md} -300 -270 0 0 0.4 0.4 {}
C {devices/ipin.sym} -300 -60 0 0 {name=p1 lab=en}
C {devices/opin.sym} -300 0 0 0 {name=p2 lab=out}
C {devices/iopin.sym} -300 -120 0 0 {name=p3 lab=vdd}
C {devices/iopin.sym} -300 120 0 0 {name=p4 lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 0 -60 0 0 {name=Mp1 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 -60 2 0 {name=l2 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 20 -90 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 20 -30 0 0 {name=l4 sig_type=std_logic lab=n0}
C {devices/lab_pin.sym} 20 -60 0 0 {name=l5 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 80 -60 0 0 {name=Mp6 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 60 -60 2 0 {name=l7 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 100 -90 0 0 {name=l8 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 100 -30 0 0 {name=l9 sig_type=std_logic lab=n0}
C {devices/lab_pin.sym} 100 -60 0 0 {name=l10 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 0 60 0 0 {name=Mn11 W=0.84 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 60 2 0 {name=l12 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 20 30 0 0 {name=l13 sig_type=std_logic lab=n0}
C {devices/lab_pin.sym} 20 90 0 0 {name=l14 sig_type=std_logic lab=mid}
C {devices/lab_pin.sym} 20 60 0 0 {name=l15 sig_type=std_logic lab=vss}
C {sky130_fd_pr/nfet_01v8.sym} 80 150 0 0 {name=Mn16 W=0.84 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 60 150 2 0 {name=l17 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 100 120 0 0 {name=l18 sig_type=std_logic lab=mid}
C {devices/lab_pin.sym} 100 180 0 0 {name=l19 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 100 150 0 0 {name=l20 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 200 -60 0 0 {name=Mp21 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 180 -60 2 0 {name=l22 sig_type=std_logic lab=n0}
C {devices/lab_pin.sym} 220 -90 0 0 {name=l23 sig_type=std_logic lab=vh1}
C {devices/lab_pin.sym} 220 -30 0 0 {name=l24 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 220 -60 0 0 {name=l25 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 200 60 0 0 {name=Mn26 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 180 60 2 0 {name=l27 sig_type=std_logic lab=n0}
C {devices/lab_pin.sym} 220 30 0 0 {name=l28 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 220 90 0 0 {name=l29 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 220 60 0 0 {name=l30 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 280 -150 0 0 {name=Mp31 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 260 -150 2 0 {name=l32 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 300 -180 0 0 {name=l33 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 300 -120 0 0 {name=l34 sig_type=std_logic lab=vh1}
C {devices/lab_pin.sym} 300 -150 0 0 {name=l35 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 400 -60 0 0 {name=Mp36 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 380 -60 2 0 {name=l37 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 420 -90 0 0 {name=l38 sig_type=std_logic lab=vh2}
C {devices/lab_pin.sym} 420 -30 0 0 {name=l39 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 420 -60 0 0 {name=l40 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 400 60 0 0 {name=Mn41 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 380 60 2 0 {name=l42 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 420 30 0 0 {name=l43 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 420 90 0 0 {name=l44 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 420 60 0 0 {name=l45 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 480 -150 0 0 {name=Mp46 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 460 -150 2 0 {name=l47 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 500 -180 0 0 {name=l48 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 500 -120 0 0 {name=l49 sig_type=std_logic lab=vh2}
C {devices/lab_pin.sym} 500 -150 0 0 {name=l50 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 600 -60 0 0 {name=Mp51 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 580 -60 2 0 {name=l52 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 620 -90 0 0 {name=l53 sig_type=std_logic lab=vh3}
C {devices/lab_pin.sym} 620 -30 0 0 {name=l54 sig_type=std_logic lab=n3}
C {devices/lab_pin.sym} 620 -60 0 0 {name=l55 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 600 60 0 0 {name=Mn56 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 580 60 2 0 {name=l57 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 620 30 0 0 {name=l58 sig_type=std_logic lab=n3}
C {devices/lab_pin.sym} 620 90 0 0 {name=l59 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 620 60 0 0 {name=l60 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 680 -150 0 0 {name=Mp61 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 660 -150 2 0 {name=l62 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 700 -180 0 0 {name=l63 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 700 -120 0 0 {name=l64 sig_type=std_logic lab=vh3}
C {devices/lab_pin.sym} 700 -150 0 0 {name=l65 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 800 -60 0 0 {name=Mp66 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 780 -60 2 0 {name=l67 sig_type=std_logic lab=n3}
C {devices/lab_pin.sym} 820 -90 0 0 {name=l68 sig_type=std_logic lab=vh4}
C {devices/lab_pin.sym} 820 -30 0 0 {name=l69 sig_type=std_logic lab=n4}
C {devices/lab_pin.sym} 820 -60 0 0 {name=l70 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 800 60 0 0 {name=Mn71 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 780 60 2 0 {name=l72 sig_type=std_logic lab=n3}
C {devices/lab_pin.sym} 820 30 0 0 {name=l73 sig_type=std_logic lab=n4}
C {devices/lab_pin.sym} 820 90 0 0 {name=l74 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 820 60 0 0 {name=l75 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 880 -150 0 0 {name=Mp76 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 860 -150 2 0 {name=l77 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 900 -180 0 0 {name=l78 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 900 -120 0 0 {name=l79 sig_type=std_logic lab=vh4}
C {devices/lab_pin.sym} 900 -150 0 0 {name=l80 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 1000 -60 0 0 {name=Mp81 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 980 -60 2 0 {name=l82 sig_type=std_logic lab=n4}
C {devices/lab_pin.sym} 1020 -90 0 0 {name=l83 sig_type=std_logic lab=vh5}
C {devices/lab_pin.sym} 1020 -30 0 0 {name=l84 sig_type=std_logic lab=n5}
C {devices/lab_pin.sym} 1020 -60 0 0 {name=l85 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1000 60 0 0 {name=Mn86 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 980 60 2 0 {name=l87 sig_type=std_logic lab=n4}
C {devices/lab_pin.sym} 1020 30 0 0 {name=l88 sig_type=std_logic lab=n5}
C {devices/lab_pin.sym} 1020 90 0 0 {name=l89 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1020 60 0 0 {name=l90 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 1080 -150 0 0 {name=Mp91 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 1060 -150 2 0 {name=l92 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1100 -180 0 0 {name=l93 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1100 -120 0 0 {name=l94 sig_type=std_logic lab=vh5}
C {devices/lab_pin.sym} 1100 -150 0 0 {name=l95 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 1200 -60 0 0 {name=Mp96 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1180 -60 2 0 {name=l97 sig_type=std_logic lab=n5}
C {devices/lab_pin.sym} 1220 -90 0 0 {name=l98 sig_type=std_logic lab=vh6}
C {devices/lab_pin.sym} 1220 -30 0 0 {name=l99 sig_type=std_logic lab=n6}
C {devices/lab_pin.sym} 1220 -60 0 0 {name=l100 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1200 60 0 0 {name=Mn101 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1180 60 2 0 {name=l102 sig_type=std_logic lab=n5}
C {devices/lab_pin.sym} 1220 30 0 0 {name=l103 sig_type=std_logic lab=n6}
C {devices/lab_pin.sym} 1220 90 0 0 {name=l104 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1220 60 0 0 {name=l105 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 1280 -150 0 0 {name=Mp106 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 1260 -150 2 0 {name=l107 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1300 -180 0 0 {name=l108 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1300 -120 0 0 {name=l109 sig_type=std_logic lab=vh6}
C {devices/lab_pin.sym} 1300 -150 0 0 {name=l110 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 1400 -60 0 0 {name=Mp111 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1380 -60 2 0 {name=l112 sig_type=std_logic lab=n6}
C {devices/lab_pin.sym} 1420 -90 0 0 {name=l113 sig_type=std_logic lab=vh7}
C {devices/lab_pin.sym} 1420 -30 0 0 {name=l114 sig_type=std_logic lab=n7}
C {devices/lab_pin.sym} 1420 -60 0 0 {name=l115 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1400 60 0 0 {name=Mn116 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1380 60 2 0 {name=l117 sig_type=std_logic lab=n6}
C {devices/lab_pin.sym} 1420 30 0 0 {name=l118 sig_type=std_logic lab=n7}
C {devices/lab_pin.sym} 1420 90 0 0 {name=l119 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1420 60 0 0 {name=l120 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 1480 -150 0 0 {name=Mp121 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 1460 -150 2 0 {name=l122 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1500 -180 0 0 {name=l123 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1500 -120 0 0 {name=l124 sig_type=std_logic lab=vh7}
C {devices/lab_pin.sym} 1500 -150 0 0 {name=l125 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 1600 -60 0 0 {name=Mp126 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1580 -60 2 0 {name=l127 sig_type=std_logic lab=n7}
C {devices/lab_pin.sym} 1620 -90 0 0 {name=l128 sig_type=std_logic lab=vh8}
C {devices/lab_pin.sym} 1620 -30 0 0 {name=l129 sig_type=std_logic lab=n8}
C {devices/lab_pin.sym} 1620 -60 0 0 {name=l130 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1600 60 0 0 {name=Mn131 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1580 60 2 0 {name=l132 sig_type=std_logic lab=n7}
C {devices/lab_pin.sym} 1620 30 0 0 {name=l133 sig_type=std_logic lab=n8}
C {devices/lab_pin.sym} 1620 90 0 0 {name=l134 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1620 60 0 0 {name=l135 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 1680 -150 0 0 {name=Mp136 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 1660 -150 2 0 {name=l137 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1700 -180 0 0 {name=l138 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1700 -120 0 0 {name=l139 sig_type=std_logic lab=vh8}
C {devices/lab_pin.sym} 1700 -150 0 0 {name=l140 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 1800 -60 0 0 {name=Mp141 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1780 -60 2 0 {name=l142 sig_type=std_logic lab=n8}
C {devices/lab_pin.sym} 1820 -90 0 0 {name=l143 sig_type=std_logic lab=vh9}
C {devices/lab_pin.sym} 1820 -30 0 0 {name=l144 sig_type=std_logic lab=n9}
C {devices/lab_pin.sym} 1820 -60 0 0 {name=l145 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1800 60 0 0 {name=Mn146 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1780 60 2 0 {name=l147 sig_type=std_logic lab=n8}
C {devices/lab_pin.sym} 1820 30 0 0 {name=l148 sig_type=std_logic lab=n9}
C {devices/lab_pin.sym} 1820 90 0 0 {name=l149 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1820 60 0 0 {name=l150 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 1880 -150 0 0 {name=Mp151 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 1860 -150 2 0 {name=l152 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1900 -180 0 0 {name=l153 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1900 -120 0 0 {name=l154 sig_type=std_logic lab=vh9}
C {devices/lab_pin.sym} 1900 -150 0 0 {name=l155 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 2000 -60 0 0 {name=Mp156 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1980 -60 2 0 {name=l157 sig_type=std_logic lab=n9}
C {devices/lab_pin.sym} 2020 -90 0 0 {name=l158 sig_type=std_logic lab=vh10}
C {devices/lab_pin.sym} 2020 -30 0 0 {name=l159 sig_type=std_logic lab=n10}
C {devices/lab_pin.sym} 2020 -60 0 0 {name=l160 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2000 60 0 0 {name=Mn161 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1980 60 2 0 {name=l162 sig_type=std_logic lab=n9}
C {devices/lab_pin.sym} 2020 30 0 0 {name=l163 sig_type=std_logic lab=n10}
C {devices/lab_pin.sym} 2020 90 0 0 {name=l164 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2020 60 0 0 {name=l165 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 2080 -150 0 0 {name=Mp166 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 2060 -150 2 0 {name=l167 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 2100 -180 0 0 {name=l168 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2100 -120 0 0 {name=l169 sig_type=std_logic lab=vh10}
C {devices/lab_pin.sym} 2100 -150 0 0 {name=l170 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 2200 -60 0 0 {name=Mp171 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2180 -60 2 0 {name=l172 sig_type=std_logic lab=n10}
C {devices/lab_pin.sym} 2220 -90 0 0 {name=l173 sig_type=std_logic lab=vh11}
C {devices/lab_pin.sym} 2220 -30 0 0 {name=l174 sig_type=std_logic lab=n11}
C {devices/lab_pin.sym} 2220 -60 0 0 {name=l175 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2200 60 0 0 {name=Mn176 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2180 60 2 0 {name=l177 sig_type=std_logic lab=n10}
C {devices/lab_pin.sym} 2220 30 0 0 {name=l178 sig_type=std_logic lab=n11}
C {devices/lab_pin.sym} 2220 90 0 0 {name=l179 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2220 60 0 0 {name=l180 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 2280 -150 0 0 {name=Mp181 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 2260 -150 2 0 {name=l182 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 2300 -180 0 0 {name=l183 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2300 -120 0 0 {name=l184 sig_type=std_logic lab=vh11}
C {devices/lab_pin.sym} 2300 -150 0 0 {name=l185 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 2400 -60 0 0 {name=Mp186 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2380 -60 2 0 {name=l187 sig_type=std_logic lab=n11}
C {devices/lab_pin.sym} 2420 -90 0 0 {name=l188 sig_type=std_logic lab=vh12}
C {devices/lab_pin.sym} 2420 -30 0 0 {name=l189 sig_type=std_logic lab=n12}
C {devices/lab_pin.sym} 2420 -60 0 0 {name=l190 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2400 60 0 0 {name=Mn191 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2380 60 2 0 {name=l192 sig_type=std_logic lab=n11}
C {devices/lab_pin.sym} 2420 30 0 0 {name=l193 sig_type=std_logic lab=n12}
C {devices/lab_pin.sym} 2420 90 0 0 {name=l194 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2420 60 0 0 {name=l195 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 2480 -150 0 0 {name=Mp196 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 2460 -150 2 0 {name=l197 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 2500 -180 0 0 {name=l198 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2500 -120 0 0 {name=l199 sig_type=std_logic lab=vh12}
C {devices/lab_pin.sym} 2500 -150 0 0 {name=l200 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 2600 -60 0 0 {name=Mp201 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2580 -60 2 0 {name=l202 sig_type=std_logic lab=n12}
C {devices/lab_pin.sym} 2620 -90 0 0 {name=l203 sig_type=std_logic lab=vh13}
C {devices/lab_pin.sym} 2620 -30 0 0 {name=l204 sig_type=std_logic lab=n13}
C {devices/lab_pin.sym} 2620 -60 0 0 {name=l205 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2600 60 0 0 {name=Mn206 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2580 60 2 0 {name=l207 sig_type=std_logic lab=n12}
C {devices/lab_pin.sym} 2620 30 0 0 {name=l208 sig_type=std_logic lab=n13}
C {devices/lab_pin.sym} 2620 90 0 0 {name=l209 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2620 60 0 0 {name=l210 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 2680 -150 0 0 {name=Mp211 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 2660 -150 2 0 {name=l212 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 2700 -180 0 0 {name=l213 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2700 -120 0 0 {name=l214 sig_type=std_logic lab=vh13}
C {devices/lab_pin.sym} 2700 -150 0 0 {name=l215 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 2800 -60 0 0 {name=Mp216 W=0.84 L=0.15 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2780 -60 2 0 {name=l217 sig_type=std_logic lab=n13}
C {devices/lab_pin.sym} 2820 -90 0 0 {name=l218 sig_type=std_logic lab=vh14}
C {devices/lab_pin.sym} 2820 -30 0 0 {name=l219 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 2820 -60 0 0 {name=l220 sig_type=std_logic lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 2800 60 0 0 {name=Mn221 W=0.42 L=0.15 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 2780 60 2 0 {name=l222 sig_type=std_logic lab=n13}
C {devices/lab_pin.sym} 2820 30 0 0 {name=l223 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 2820 90 0 0 {name=l224 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2820 60 0 0 {name=l225 sig_type=std_logic lab=vss}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 2880 -150 0 0 {name=Mp226 W=0.42 L=0.5 nf=1 mult=1 model=pfet_01v8_lvt spiceprefix=X}
C {devices/lab_pin.sym} 2860 -150 2 0 {name=l227 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 2900 -180 0 0 {name=l228 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2900 -120 0 0 {name=l229 sig_type=std_logic lab=vh14}
C {devices/lab_pin.sym} 2900 -150 0 0 {name=l230 sig_type=std_logic lab=vdd}
C {devices/res.sym} -200 300 0 0 {name=Rb0 value=300k m=1}
C {devices/lab_pin.sym} -200 270 0 0 {name=l231 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -200 330 0 0 {name=l232 sig_type=std_logic lab=vbp}
C {devices/res.sym} -140 300 0 0 {name=Rb1 value=1500k m=1}
C {devices/lab_pin.sym} -140 270 0 0 {name=l233 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} -140 330 0 0 {name=l234 sig_type=std_logic lab=vss}
