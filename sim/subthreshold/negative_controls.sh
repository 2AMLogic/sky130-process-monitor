#!/usr/bin/env bash
# Negative controls for the subthreshold benches: a wrong model path or a wrong corner name must
# make the bench FAIL for its own specific reason -- non-zero exit, the matching diagnostic, and no
# measurement value in the report -- never produce numbers. Local, single unit each. The pass rule
# and the baseline check_env.sh pass come from sim/neg_control_common.sh; without that baseline a
# host with no `klt` on PATH reported both controls as passing on exit 127 (issue #159).
# Usage: sim/subthreshold/negative_controls.sh   (exits 0 only if every control failed as required)
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=sim/neg_control_common.sh
. "$(dirname "$HERE")/neg_control_common.sh"
cd "$HERE" || exit 1
T="$(mktemp -d "$HERE/.nc.XXXXXX")"; trap 'rm -rf "$T"' EXIT
mk() {  # $1 = python expression mutating request r; $2 = where to write it (inside $T)
  python3 -I -c '
import json,sys
r=json.load(open("osc_grid.request.json")); exec(sys.argv[1])
r["corners"]={"units":[{"process":r.get("_p","tt"),"supply_v":{"vdd":1.8},"temperature_c":27}]}
# klt resolves a relative netlist against the request file, and the request goes one level down
# into $T so the trap cleans it up, so the testbench reference has to climb back out.
r["netlist"]="../"+r["netlist"]
r.pop("_p",None); json.dump(r,open(sys.argv[2],"w"))' "$1" "$2"
}
# A produced number appears in the report as `"value": <number>`; a run that measured nothing has
# only `"value": null`, or no measurements block at all. This is the "no frequency" condition, and
# it is checked on top of the diagnostic, not instead of it.
NUMBER='"value": -?[0-9]'

mk 'r["models"]["lib"]="libs.tech/ngspice/no_such_models.spice"' "$T/nc_badlib.json"
expect_fail "wrong model path" 'model library not found: .*/libs\.tech/ngspice/no_such_models\.spice' \
  klt sim "$T/nc_badlib.json" --backend local --format json
expect_absent "wrong model path (no measurement value)" "$NUMBER"

mk 'r["_p"]="zz"' "$T/nc_badcorner.json"
expect_fail "unknown corner name" 'section definition zz not found' \
  klt sim "$T/nc_badcorner.json" --backend local --format json
expect_absent "unknown corner name (no measurement value)" "$NUMBER"
exit $rc
