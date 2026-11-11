#!/usr/bin/env bash
# One single-corner probe case = one `ngspice -b`. Usage: run_probe.sh <netlist> <outdir> [force_vbp_volts]
# SIMULATED, tt / 1.80 V / 27 C. If force_vbp_volts is given, `Vforce vbp 0 <V>` is spliced into the DUT subckt.
set -euo pipefail
mkdir -p "$2"; NET=$(readlink -f "$1"); OUT=$(readlink -f "$2"); FORCE=${3:-}
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${SKY130_LIB:-$HOME/.volare/volare/sky130/versions/c6d73a35f524070e85faff4a6a9eef49553ebc2b/sky130A/libs.tech/ngspice/sky130.lib.spice}
mkdir -p "$OUT"
DUT="$OUT/dut.spice"
if [ -n "$FORCE" ]; then
  sed -E "s#^\.(ends|ENDS)( osc_subth)?#Vforce vbp 0 $FORCE\n.ENDS osc_subth#" "$NET" > "$DUT"
  grep -q '^Vforce' "$DUT"
else cp "$NET" "$DUT"; fi
sed -e "s#@PDKLIB@#$LIB#" -e "s#@NET@#$DUT#" -e "s#@OUT@#$OUT/wave.dat#" "$HERE/osc_subth_vbp_probe.cir" > "$OUT/deck.cir"
ngspice -b -o "$OUT/ngspice.log" "$OUT/deck.cir"
python3 -I - "$OUT/wave.dat" <<'PY'
import sys
t=[];o=[];b=[]
for l in open(sys.argv[1]):
    p=l.split()
    t.append(float(p[0]));o.append(float(p[1]));b.append(float(p[3]))
th=0.9;e=sum(1 for i in range(1,len(o)) if o[i-1]<th<=o[i])
print(f"rising_edges={e} vbp_end={b[-1]:.4f} out_min={min(o):.3f} out_max={max(o):.3f} n={len(t)}")
PY
