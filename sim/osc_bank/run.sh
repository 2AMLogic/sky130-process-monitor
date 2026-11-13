#!/usr/bin/env bash
# Oscillator-bank bench: one ngspice -b per oscillator (tt, 1.8 V, 27 C; single-unit, local by design).
# Appends one dated SIMULATED record per oscillator to measurements/osc_bank_records.jsonl, but only
# if EVERY ring oscillated (all-or-nothing: a failed run appends nothing).
# Usage: sim/osc_bank/run.sh [--no-record] [osc_name ...]   (default: all five)
# --no-record runs the benches and prints the results but appends nothing: the repeatable
#   cold-start invocation (attest/item9_analog.json) must not grow the append-only record.
# OSC_EN_SRC overrides the enable source (negative control: enable tied off).
set -eu
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM="$(dirname "$HERE")"
REPO="$(dirname "$SIM")"
DESIGN="$REPO/design/osc_bank"
RECORD=1
if [ "${1:-}" = "--no-record" ]; then RECORD=0; shift; fi
OSCS=("$@"); [ ${#OSCS[@]} -gt 0 ] || OSCS=(osc_hd osc_nmos osc_pmos osc_wire osc_subth)

envout="$("$SIM/check_env.sh")"
echo "$envout"
ROOT="$(printf '%s\n' "$envout" | sed -n 's/^PDK_ROOT=//p')"
PDK_JSON="$SIM/pdk.json"
rel() { python3 -I -c 'import json,sys;print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$PDK_JSON" "$1"; }
MODEL_LIB="$ROOT/$(rel model_lib)"
CELL_SPICE="$ROOT/$(rel cell_spice)"
EN_SRC="${OSC_EN_SRC:-Ven en 0 PULSE(0 1.8 1n 100p 100p 1 2)}"
BUILD="$SIM/build/osc_bank"
mkdir -p "$BUILD"
NGV="$(ngspice --version 2>&1 | sed -n 's/.*ngspice-\([0-9.]*\).*/\1/p' | head -1)"
OPDK="$(rel open_pdks)"

fail=0; results=""
for o in "${OSCS[@]}"; do
  sed -e "s|@MODEL_LIB@|$MODEL_LIB|" -e "s|@CELL_SPICE@|$CELL_SPICE|" \
      -e "s|@NETLIST@|$DESIGN/$o.spice|" -e "s|@EN_SRC@|$EN_SRC|" \
      "$HERE/bench_$o.spice" > "$BUILD/$o.spice"
  LOG="$BUILD/$o.log"
  ngspice -b -o "$LOG" "$BUILD/$o.spice" || true
  val() { sed -n "s/^RESULT $1 *= *\([-+0-9.eE]*\).*/\1/p" "$LOG" | head -1; }
  F="$(val f_osc_hz)"; I="$(val i_avg_ua)"
  if [ -z "$F" ] || [ -z "$I" ]; then
    echo "run.sh: FAIL: $o did not oscillate (no frequency measured; see $LOG)" >&2
    fail=1; continue
  fi
  echo "$o: f_osc_hz=$F i_avg_ua=$I"
  results="$results$o $F $I"$'\n'
done
[ "$fail" = 0 ] || exit 1
if [ "$RECORD" = 0 ]; then echo "run.sh: --no-record: all rings oscillated; no record appended"; exit 0; fi

mkdir -p "$REPO/measurements"
printf '%s' "$results" | python3 -I -c '
import datetime, json, sys
out, ngv, opdk, lib = sys.argv[1:5]
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
with open(out, "a") as f:   # append-only
    for line in sys.stdin.read().splitlines():
        o, fo, ia = line.split()
        rec = {"date_utc": now, "kind": "SIMULATED", "oscillator": o,
               "f_osc_hz": float(fo), "i_avg_ua": float(ia),
               "corner": "tt", "vdd_V": 1.8, "temp_C": 27,
               "testbench": "sim/osc_bank/bench_%s.spice" % o,
               "netlist": "design/osc_bank/%s.spice" % o,
               "open_pdks": opdk, "model_file": lib, "ngspice": ngv,
               "note": "single-corner start-up-skipped measurement; no PVT claim"}
        f.write(json.dumps(rec) + "\n")
        print("record appended:", json.dumps(rec))
' "$REPO/measurements/osc_bank_records.jsonl" "$NGV" "$OPDK" "$MODEL_LIB"
