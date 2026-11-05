#!/usr/bin/env bash
# Negative controls for the oscillator bank. Each must FAIL for its own specific reason (the
# diagnostic is grepped), after a baseline check_env pass, so a broken environment is not read
# as a control passing. Exit 0 = all controls behaved; exit 2 = the environment itself is broken.
#  1. enable tied off  -> run.sh exits non-zero, "did not oscillate", and appends no record.
#  2. a drifted schematic -> `klt netlist --check` reports 'drifted' (exit 3), not 'match'.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM="$(dirname "$HERE")"
REPO="$(dirname "$SIM")"
REC="$REPO/measurements/osc_bank_records.jsonl"
DES="$REPO/design/osc_bank"
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
if ! "$SIM/check_env.sh" >/dev/null; then
  echo "NEG-CONTROL ABORT: environment check failed; fix it first:" >&2
  "$SIM/check_env.sh" >/dev/null; exit 2
fi

before="$(wc -l < "$REC" 2>/dev/null || echo 0)"
expect_fail "enable tied off (ring cannot start)" 'run.sh: FAIL: osc_hd did not oscillate' \
  env OSC_EN_SRC='Ven en 0 0' "$HERE/run.sh" osc_hd
after="$(wc -l < "$REC" 2>/dev/null || echo 0)"
[ "$before" = "$after" ] || { echo "NEG-CONTROL FAIL: failed run appended a record"; rc=1; }

T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cp "$DES/xschemrc" "$DES/osc_hd.sch" "$DES/osc_hd.spice" "$T/"
# drop one inverter instance from the schematic copy: the committed netlist no longer matches it
sed -i '/name=x7 /d' "$T/osc_hd.sch"
expect_fail "drifted schematic vs committed netlist" 'drifted' \
  klt netlist "$T/osc_hd.sch" -o "$T/osc_hd.spice" --check --ignore-comments --block \
    --rcfile "$T/xschemrc" --pdk sky130A --pdk-root "$(sed -n 's/^PDK_ROOT=//p' <("$SIM/check_env.sh"))"
exit $rc
