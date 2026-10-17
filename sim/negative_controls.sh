#!/usr/bin/env bash
# Each control must make the flow FAIL; this script exits 0 only if all do.
set -u
SIM="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REC="$(dirname "$SIM")/measurements/inv_smoke_records.jsonl"
rc=0
expect_fail() { # name, command...
  local name="$1"; shift
  if "$@" >/dev/null 2>&1; then echo "NEG-CONTROL FAIL (unexpectedly passed): $name"; rc=1
  else echo "neg-control ok (failed as required): $name"; fi
}
before="$(wc -l < "$REC" 2>/dev/null || echo 0)"
expect_fail "wrong model path" env SMOKE_MODEL_LIB=/nonexistent/sky130.lib.spice "$SIM/smoke/run.sh"
after="$(wc -l < "$REC" 2>/dev/null || echo 0)"
[ "$before" = "$after" ] || { echo "NEG-CONTROL FAIL: failed run appended a record"; rc=1; }
# Edited pin: point at a temp copy of the pins with a wrong open_pdks hash.
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cp "$SIM/check_env.sh" "$SIM/toolchain.json" "$T/"
sed 's/"open_pdks": "[0-9a-f]*"/"open_pdks": "0000000000000000000000000000000000000000"/' "$SIM/pdk.json" > "$T/pdk.json"
expect_fail "edited PDK pin" "$T/check_env.sh"
sed 's/"expect": "46"/"expect": "1"/' "$SIM/toolchain.json" > "$T/toolchain.json"
cp "$SIM/pdk.json" "$T/pdk.json"
expect_fail "edited tool pin" "$T/check_env.sh"
expect_fail "pinned PDK absent" env PDK_ROOT_SKY130A=/nonexistent "$SIM/check_env.sh"
exit $rc
