#!/usr/bin/env bash
# Each control must make the flow FAIL for its own specific reason; this script
# exits 0 only if all do. A control passes only if the command exits non-zero AND
# its output matches the expected diagnostic, so a broken environment (wrong tool
# version, missing PATH) cannot be read as a control passing.
set -u
SIM="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REC="$(dirname "$SIM")/measurements/inv_smoke_records.jsonl"
rc=0
expect_fail() { # name, expected-diagnostic regex, command...
  local name="$1" pat="$2"; shift 2
  local out
  if out="$("$@" 2>&1)"; then echo "NEG-CONTROL FAIL (unexpectedly passed): $name"; rc=1
  elif printf '%s\n' "$out" | grep -Eq -- "$pat"; then
    echo "neg-control ok (failed as required, diagnostic matched): $name"
  else
    echo "NEG-CONTROL FAIL (failed for the wrong reason, no match for /$pat/): $name"
    printf '%s\n' "$out" | tail -5 | sed 's/^/    /'; rc=1
  fi
}
# Baseline: the environment must be sound, else a control "failing" proves nothing.
if ! "$SIM/check_env.sh" >/dev/null; then
  echo "NEG-CONTROL ABORT: environment check failed; fix it first:" >&2
  "$SIM/check_env.sh" >/dev/null; exit 2
fi
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
sed 's/"expect": "46"/"expect": "1"/' "$SIM/toolchain.json" > "$T/toolchain.json"
cp "$SIM/pdk.json" "$T/pdk.json"
expect_fail "edited tool pin" 'ngspice: version 46 != pinned 1 ' "$T/check_env.sh"
expect_fail "pinned PDK absent" 'PDK root not found: /nonexistent' env PDK_ROOT_SKY130A=/nonexistent "$SIM/check_env.sh"
exit $rc
