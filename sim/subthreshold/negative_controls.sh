#!/usr/bin/env bash
# Negative controls for the subthreshold benches: a wrong model path or corner name must make the
# bench FAIL (non-zero exit, no frequency), never produce numbers. Local, single unit each.
# Usage: sim/subthreshold/negative_controls.sh   (exits 0 only if every control failed as required)
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"
T="$(mktemp -d "$HERE/.nc.XXXXXX")"; trap 'rm -rf "$T"' EXIT
mk() {  # $1 = python expression mutating request r
  python3 -I -c '
import json,sys
r=json.load(open("osc_grid.request.json")); exec(sys.argv[1])
r["corners"]={"units":[{"process":r.get("_p","tt"),"supply_v":{"vdd":1.8},"temperature_c":27}]}
r.pop("_p",None); json.dump(r,open(sys.argv[2],"w"))' "$1" "$2"
}
rc=0
mk 'r["models"]["lib"]="libs.tech/ngspice/no_such_models.spice"' "$T/../.nc_badlib.json"
mk 'r["_p"]="zz"' "$T/../.nc_badcorner.json"
for c in badlib badcorner; do
  out="$(klt sim ".nc_$c.json" --backend local --format json 2>&1)"; code=$?
  has_f="$(printf '%s' "$out" | grep -c '"f_osc_hz"[^}]*"value": [0-9]')"
  if [ "$code" -ne 0 ] && [ "$has_f" = 0 ]; then echo "negative control $c: PASS (exit $code, no frequency)"
  else echo "negative control $c: FAIL (exit $code, frequency present=$has_f)"; rc=1; fi
  rm -f ".nc_$c.json"
done
exit $rc
