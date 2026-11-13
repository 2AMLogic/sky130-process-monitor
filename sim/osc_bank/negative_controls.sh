#!/usr/bin/env bash
# Negative controls for the oscillator bank. Each must FAIL for its own specific reason (the
# diagnostic is grepped), after a baseline check_env pass; both rules come from
# sim/neg_control_common.sh. Exit 0 = all controls behaved; exit 2 = the environment itself is broken.
#  1. enable tied off  -> run.sh exits non-zero, "did not oscillate", and appends no record.
#  2. a drifted schematic -> `klt netlist --check` reports 'drifted' (exit 3), not 'match'.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM="$(dirname "$HERE")"
# shellcheck source=sim/neg_control_common.sh
. "$SIM/neg_control_common.sh"
REPO="$(dirname "$SIM")"
REC="$REPO/measurements/osc_bank_records.jsonl"
DES="$REPO/design/osc_bank"

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
    --rcfile "$T/xschemrc" --pdk sky130A --pdk-root "$NEG_PDK_ROOT"
exit $rc
