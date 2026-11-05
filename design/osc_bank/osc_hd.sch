v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {osc_hd: plain sky130_fd_sc_hd chain (NAND2 enable stage + inv_1)} -300 -300 0 0 0.4 0.4 {}
T {SIMULATION INTENT ONLY - stock standard cells, baseline oscillator} -300 -270 0 0 0.4 0.4 {}
C {devices/ipin.sym} -300 -60 0 0 {name=p1 lab=en}
C {devices/opin.sym} -300 0 0 0 {name=p2 lab=out}
C {devices/iopin.sym} -300 -120 0 0 {name=p3 lab=vdd}
C {devices/iopin.sym} -300 120 0 0 {name=p4 lab=vss}
C {sky130_stdcells/nand2_1.sym} 0 0 0 0 {name=x0 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} -60 -20 2 0 {name=l1 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} -60 20 2 0 {name=l2 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 60 0 0 0 {name=l3 sig_type=std_logic lab=n0}
C {sky130_stdcells/inv_1.sym} 200 0 0 0 {name=x1 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 160 0 2 0 {name=l4 sig_type=std_logic lab=n0}
C {devices/lab_pin.sym} 240 0 0 0 {name=l5 sig_type=std_logic lab=n1}
C {sky130_stdcells/inv_1.sym} 400 0 0 0 {name=x2 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 360 0 2 0 {name=l6 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 440 0 0 0 {name=l7 sig_type=std_logic lab=n2}
C {sky130_stdcells/inv_1.sym} 600 0 0 0 {name=x3 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 560 0 2 0 {name=l8 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 640 0 0 0 {name=l9 sig_type=std_logic lab=n3}
C {sky130_stdcells/inv_1.sym} 800 0 0 0 {name=x4 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 760 0 2 0 {name=l10 sig_type=std_logic lab=n3}
C {devices/lab_pin.sym} 840 0 0 0 {name=l11 sig_type=std_logic lab=n4}
C {sky130_stdcells/inv_1.sym} 1000 0 0 0 {name=x5 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 960 0 2 0 {name=l12 sig_type=std_logic lab=n4}
C {devices/lab_pin.sym} 1040 0 0 0 {name=l13 sig_type=std_logic lab=n5}
C {sky130_stdcells/inv_1.sym} 1200 0 0 0 {name=x6 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 1160 0 2 0 {name=l14 sig_type=std_logic lab=n5}
C {devices/lab_pin.sym} 1240 0 0 0 {name=l15 sig_type=std_logic lab=n6}
C {sky130_stdcells/inv_1.sym} 1400 0 0 0 {name=x7 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 1360 0 2 0 {name=l16 sig_type=std_logic lab=n6}
C {devices/lab_pin.sym} 1440 0 0 0 {name=l17 sig_type=std_logic lab=n7}
C {sky130_stdcells/inv_1.sym} 1600 0 0 0 {name=x8 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 1560 0 2 0 {name=l18 sig_type=std_logic lab=n7}
C {devices/lab_pin.sym} 1640 0 0 0 {name=l19 sig_type=std_logic lab=n8}
C {sky130_stdcells/inv_1.sym} 1800 0 0 0 {name=x9 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 1760 0 2 0 {name=l20 sig_type=std_logic lab=n8}
C {devices/lab_pin.sym} 1840 0 0 0 {name=l21 sig_type=std_logic lab=n9}
C {sky130_stdcells/inv_1.sym} 2000 0 0 0 {name=x10 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 1960 0 2 0 {name=l22 sig_type=std_logic lab=n9}
C {devices/lab_pin.sym} 2040 0 0 0 {name=l23 sig_type=std_logic lab=n10}
C {sky130_stdcells/inv_1.sym} 2200 0 0 0 {name=x11 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 2160 0 2 0 {name=l24 sig_type=std_logic lab=n10}
C {devices/lab_pin.sym} 2240 0 0 0 {name=l25 sig_type=std_logic lab=n11}
C {sky130_stdcells/inv_1.sym} 2400 0 0 0 {name=x12 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 2360 0 2 0 {name=l26 sig_type=std_logic lab=n11}
C {devices/lab_pin.sym} 2440 0 0 0 {name=l27 sig_type=std_logic lab=n12}
C {sky130_stdcells/inv_1.sym} 2600 0 0 0 {name=x13 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 2560 0 2 0 {name=l28 sig_type=std_logic lab=n12}
C {devices/lab_pin.sym} 2640 0 0 0 {name=l29 sig_type=std_logic lab=n13}
C {sky130_stdcells/inv_1.sym} 2800 0 0 0 {name=x14 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 2760 0 2 0 {name=l30 sig_type=std_logic lab=n13}
C {devices/lab_pin.sym} 2840 0 0 0 {name=l31 sig_type=std_logic lab=n14}
C {sky130_stdcells/inv_1.sym} 3000 0 0 0 {name=x15 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 2960 0 2 0 {name=l32 sig_type=std_logic lab=n14}
C {devices/lab_pin.sym} 3040 0 0 0 {name=l33 sig_type=std_logic lab=n15}
C {sky130_stdcells/inv_1.sym} 3200 0 0 0 {name=x16 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 3160 0 2 0 {name=l34 sig_type=std_logic lab=n15}
C {devices/lab_pin.sym} 3240 0 0 0 {name=l35 sig_type=std_logic lab=n16}
C {sky130_stdcells/inv_1.sym} 3400 0 0 0 {name=x17 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 3360 0 2 0 {name=l36 sig_type=std_logic lab=n16}
C {devices/lab_pin.sym} 3440 0 0 0 {name=l37 sig_type=std_logic lab=n17}
C {sky130_stdcells/inv_1.sym} 3600 0 0 0 {name=x18 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 3560 0 2 0 {name=l38 sig_type=std_logic lab=n17}
C {devices/lab_pin.sym} 3640 0 0 0 {name=l39 sig_type=std_logic lab=n18}
C {sky130_stdcells/inv_1.sym} 3800 0 0 0 {name=x19 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 3760 0 2 0 {name=l40 sig_type=std_logic lab=n18}
C {devices/lab_pin.sym} 3840 0 0 0 {name=l41 sig_type=std_logic lab=n19}
C {sky130_stdcells/inv_1.sym} 4000 0 0 0 {name=x20 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 3960 0 2 0 {name=l42 sig_type=std_logic lab=n19}
C {devices/lab_pin.sym} 4040 0 0 0 {name=l43 sig_type=std_logic lab=n20}
C {sky130_stdcells/inv_1.sym} 4200 0 0 0 {name=x21 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 4160 0 2 0 {name=l44 sig_type=std_logic lab=n20}
C {devices/lab_pin.sym} 4240 0 0 0 {name=l45 sig_type=std_logic lab=n21}
C {sky130_stdcells/inv_1.sym} 4400 0 0 0 {name=x22 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 4360 0 2 0 {name=l46 sig_type=std_logic lab=n21}
C {devices/lab_pin.sym} 4440 0 0 0 {name=l47 sig_type=std_logic lab=n22}
C {sky130_stdcells/inv_1.sym} 4600 0 0 0 {name=x23 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 4560 0 2 0 {name=l48 sig_type=std_logic lab=n22}
C {devices/lab_pin.sym} 4640 0 0 0 {name=l49 sig_type=std_logic lab=n23}
C {sky130_stdcells/inv_1.sym} 4800 0 0 0 {name=x24 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 4760 0 2 0 {name=l50 sig_type=std_logic lab=n23}
C {devices/lab_pin.sym} 4840 0 0 0 {name=l51 sig_type=std_logic lab=n24}
C {sky130_stdcells/inv_1.sym} 5000 0 0 0 {name=x25 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 4960 0 2 0 {name=l52 sig_type=std_logic lab=n24}
C {devices/lab_pin.sym} 5040 0 0 0 {name=l53 sig_type=std_logic lab=n25}
C {sky130_stdcells/inv_1.sym} 5200 0 0 0 {name=x26 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 5160 0 2 0 {name=l54 sig_type=std_logic lab=n25}
C {devices/lab_pin.sym} 5240 0 0 0 {name=l55 sig_type=std_logic lab=n26}
C {sky130_stdcells/inv_1.sym} 5400 0 0 0 {name=x27 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 5360 0 2 0 {name=l56 sig_type=std_logic lab=n26}
C {devices/lab_pin.sym} 5440 0 0 0 {name=l57 sig_type=std_logic lab=n27}
C {sky130_stdcells/inv_1.sym} 5600 0 0 0 {name=x28 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 5560 0 2 0 {name=l58 sig_type=std_logic lab=n27}
C {devices/lab_pin.sym} 5640 0 0 0 {name=l59 sig_type=std_logic lab=n28}
C {sky130_stdcells/inv_1.sym} 5800 0 0 0 {name=x29 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 5760 0 2 0 {name=l60 sig_type=std_logic lab=n28}
C {devices/lab_pin.sym} 5840 0 0 0 {name=l61 sig_type=std_logic lab=n29}
C {sky130_stdcells/inv_1.sym} 6000 0 0 0 {name=x30 VGND=vss VNB=vss VPB=vdd VPWR=vdd prefix=sky130_fd_sc_hd__}
C {devices/lab_pin.sym} 5960 0 2 0 {name=l62 sig_type=std_logic lab=n29}
C {devices/lab_pin.sym} 6040 0 0 0 {name=l63 sig_type=std_logic lab=out}
