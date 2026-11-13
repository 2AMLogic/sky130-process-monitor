#!/usr/bin/env bash
# Each control must make the flow FAIL for its own specific reason; this script
# exits 0 only if all do. The pass rule (non-zero exit AND a matching diagnostic)
# and the baseline check_env.sh pass come from sim/neg_control_common.sh, which
# every negative-control script in this tree sources.
set -u
SIM="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=sim/neg_control_common.sh
. "$SIM/neg_control_common.sh"
REC="$(dirname "$SIM")/measurements/inv_smoke_records.jsonl"
before="$(wc -l < "$REC" 2>/dev/null || echo 0)"
# run.sh's own message only says the delay was not measured; the cause (missing
# library) is in the ngspice log, so print it after the failure.
model_path_control() {
  SMOKE_MODEL_LIB=/nonexistent/sky130.lib.spice "$SIM/smoke/run.sh"; local r=$?
  grep -h 'library file' "$SIM/build/smoke/inv_smoke.log"; return $r
}
expect_fail "wrong model path" 'library file .* not found' model_path_control
after="$(wc -l < "$REC" 2>/dev/null || echo 0)"
[ "$before" = "$after" ] || { echo "NEG-CONTROL FAIL: failed run appended a record"; rc=1; }
# Edited pin: point at a temp copy of the pins with a wrong open_pdks hash.
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cp "$SIM/check_env.sh" "$SIM/toolchain.json" "$T/"
sed 's/"open_pdks": "[0-9a-f]*"/"open_pdks": "0000000000000000000000000000000000000000"/' "$SIM/pdk.json" > "$T/pdk.json"
expect_fail "edited PDK pin" 'open_pdks revision [0-9a-f]+ != pinned 0{40}' "$T/check_env.sh"
sed 's/"min": "46"/"min": "9999"/' "$SIM/toolchain.json" > "$T/toolchain.json"
cp "$SIM/pdk.json" "$T/pdk.json"
expect_fail "edited tool floor" 'ngspice: version [0-9.]+ < floor 9999 ' "$T/check_env.sh"
expect_fail "pinned PDK absent" 'PDK root not found: /nonexistent' env PDK_ROOT_SKY130A=/nonexistent "$SIM/check_env.sh"
exit $rc
