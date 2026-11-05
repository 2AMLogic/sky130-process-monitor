#!/usr/bin/env bash
# Local single-corner probe (one ngspice -b per corner, DC op point, allowed locally): which of the
# sky130 `sf` / `fs` sections is NMOS-slow? Prints Id of a W/L = 1/0.15 um nfet and pfet at
# |Vgs| = |Vds| = 0.9 V, 27 C. Usage: probe_skew.sh <pdk_root_containing_libs.tech> [corner ...]
set -eu
ROOT="$1"; shift
CORNERS=("$@"); [ ${#CORNERS[@]} -gt 0 ] || CORNERS=(tt sf fs)
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
for C in "${CORNERS[@]}"; do
  cat > "$T/probe_$C.spice" <<DECK
* skew probe $C
.lib "$ROOT/libs.tech/ngspice/sky130.lib.spice" $C
.temp 27
Vn dn 0 0.9
Vgn gn 0 0.9
XN dn gn 0 0 sky130_fd_pr__nfet_01v8 L=0.15 W=1
Vp dp 0 -0.9
Vgp gp 0 -0.9
XP dp gp 0 0 sky130_fd_pr__pfet_01v8 L=0.15 W=1
.control
op
let idn = -i(Vn)*1e6
let idp = i(Vp)*1e6
echo "RESULT idn_ua = \$&idn"
echo "RESULT idp_ua = \$&idp"
quit
.endc
.end
DECK
  echo "$C: $(timeout 60 ngspice -b "$T/probe_$C.spice" < /dev/null 2>&1 | grep RESULT | tr '\n' ' ')"
done
