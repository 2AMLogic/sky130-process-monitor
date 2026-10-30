#!/usr/bin/env bash
# Analog smoke: one ngspice -b run (single corner, local by design).
# Appends a dated record to measurements/inv_smoke_records.jsonl.
# SMOKE_MODEL_LIB overrides the model library path (used by the negative control).
set -eu
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM="$(dirname "$HERE")"
REPO="$(dirname "$SIM")"

envout="$("$SIM/check_env.sh")"
echo "$envout"
ROOT="$(printf '%s\n' "$envout" | sed -n 's/^PDK_ROOT=//p')"
PDK_JSON="$SIM/pdk.json"
rel() { python3 -I -c 'import json,sys;print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$PDK_JSON" "$1"; }
MODEL_LIB="${SMOKE_MODEL_LIB:-$ROOT/$(rel model_lib)}"
CELL_SPICE="$ROOT/$(rel cell_spice)"

BUILD="$SIM/build/smoke"
mkdir -p "$BUILD"
sed -e "s|@MODEL_LIB@|$MODEL_LIB|" -e "s|@CELL_SPICE@|$CELL_SPICE|" \
  "$HERE/inv_smoke.spice" > "$BUILD/inv_smoke.spice"

LOG="$BUILD/inv_smoke.log"
ngspice -b -o "$LOG" "$BUILD/inv_smoke.spice" || true

val() { sed -n "s/^$1 *= *\([-+0-9.e]*\).*/\1/p" "$LOG" | head -1; }
HL="$(val tpd_hl)"; LH="$(val tpd_lh)"
if [ -z "$HL" ] || [ -z "$LH" ]; then
  echo "run.sh: FAIL: propagation delay not measured (see $LOG)" >&2
  exit 1
fi

NGV="$(ngspice --version 2>&1 | sed -n 's/.*ngspice-\([0-9.]*\).*/\1/p' | head -1)"
OPDK="$(python3 -I -c 'import json,sys;print(json.load(open(sys.argv[1]))["open_pdks"])' "$PDK_JSON")"
mkdir -p "$REPO/measurements"
python3 -I - "$REPO/measurements/inv_smoke_records.jsonl" "$HL" "$LH" "$NGV" "$OPDK" "$MODEL_LIB" <<'PY'
import datetime, json, sys
out, hl, lh, ngv, opdk, lib = sys.argv[1:7]
rec = {
    "date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "kind": "SIMULATED",
    "testbench": "sim/smoke/inv_smoke.spice",
    "cell": "sky130_fd_sc_hd__inv_1",
    "corner": "tt", "vdd_V": 1.8, "temp_C": 27, "load_F": 10e-15,
    "tpd_hl_s": float(hl), "tpd_lh_s": float(lh),
    "open_pdks": opdk, "model_file": lib,
    "ngspice": ngv,
    "note": "toolchain smoke: models and cell views load; no design claim",
}
with open(out, "a") as f:        # append-only
    f.write(json.dumps(rec) + "\n")
print("record appended:", json.dumps(rec))
PY
