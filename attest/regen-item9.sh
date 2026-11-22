#!/usr/bin/env bash
#
# Regenerate evidence/item9_<partition>.json -- the `klt signoff --attest 9`
# envelopes over attest/item9_{analog,digital}.json -- with the klayout-tools
# version CI pins, and report whether the committed signoff record still
# reproduces (issue #190).
#
# Item 9 is graded per partition, and both inventories hash testbench sources
# by content: `attest/item9_analog.json` pins every committed deck and
# `klt sim` request, the `sim/solve/` and `sim/sensitivity/` Python modules,
# the PEX grader `sim/pex/grade_pex.py` (issue #267, the item-8 measurement
# path), the shared sibling-module loader those benches import at run time
# (`sim/_siblings.py`), the owner data files those benches load
# (`sim/corner_box.json`, `sim/pdk.json`, `sim/toolchain.json`), and the four
# shell entrypoints (`sim/check_env.sh` plus the three `sim/**/run*.sh`
# runners);
# `attest/item9_digital.json` pins the five `verification/readout/` bench files
# plus the three `sim/` environment files its cold start reads (`check_env.sh`,
# `pdk.json`, `toolchain.json`). An edit to any of them without a
# re-attest turns T1 item 9 stale and reds the `klt signoff` job, so run this
# whenever an inventoried source changes and commit the regenerated envelope
# in the same commit as the edit.
#
# Usage: attest/regen-item9.sh [analog|digital|both]
#
# The declared cold starts are real and local_only (the pinned PDK, ngspice,
# Icarus, Verilator and cocotb, none of which CI has): the analog partition
# runs every one of them for real -- the oscillator-bank and smoke decks as
# single-corner `ngspice -b`, every request as `klt sim --dry-run`, the three
# unittest suites -- which measured ~6 min on a normal worker (issue #193);
# the digital partition runs `make -C verification/readout` (check_env,
# Verilator lint, then the cocotb suite on Icarus; timeout 30 min). This is a
# permitted local single-unit attestation pass -- NOT a batch grid; do not
# reshape it into one, and never send it to a fleet.
#
# The pin is read from .github/workflows/signoff.yml's `pip install
# klayout-tools==X.Y.Z` line -- that is the version CI byte-compares against,
# and it is deliberately not restated here (pin-copy consolidation, #163).
# The parser and the pinned-klt wrapper live in attest/lib/regen-common.sh.
# Regenerating with the host's `klt` writes a different
# `provenance.klt_version` and a non-reproducing envelope.
#
# Writes exactly one file per partition: evidence/item9_<partition>.json.
# The signoff record is never written: an ordinary source edit moves only
# content hashes inside the envelope -- the record cites each item by the
# inventory's sha256, not the envelope's bytes -- so the record reproduces
# unchanged, and this script checks and reports rather than assumes. Only an
# inventory edit (a pinned path added or removed) moves the record; that is
# reported with exit 3 and the record-regeneration command, never written.
#
# Exit status:
#   0  envelope(s) up to date (or regenerated) and the committed record
#      reproduces -- the normal source-edit case
#   3  envelope(s) regenerated, but the committed signoff record ALSO has to
#      be regenerated and committed (the command is printed) -- only after an
#      inventory edit
#   1  nothing was written: bad usage, the pin is unparseable, uvx or a
#      partition toolchain piece is missing, an inventoried file is genuinely
#      absent, or a declared cold start genuinely fails
#
set -uo pipefail

ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd) || exit 1
# Read by attest/lib/regen-common.sh's messages (sourced below).
# shellcheck disable=SC2034
REGEN_NAME=regen-item9.sh
REGEN_WORKFLOW=".github/workflows/signoff.yml"
REL_RECORD="manifests/sky130-process-monitor.signoff.json"
REL_MANIFEST="manifests/sky130-process-monitor.json"
REL_TIERS="manifests/design-evidence-tiers.md"

# The pin parser and the pinned-klt wrapper are shared with
# attest/regen-item10.sh (pin-copy consolidation, #163).
# shellcheck source=attest/lib/regen-common.sh
source "$ROOT/attest/lib/regen-common.sh"

# Every path below is relative to $ROOT on purpose: the envelope records its
# inventory path relatively, so a run from anywhere else produces different
# bytes. The script cd's to $ROOT first for the same reason.

# Print the comment header above (from line 3 to the first non-comment line),
# so --help cannot drift out of sync with it.
usage() {
    awk 'NR > 2 && /^#/ { sub(/^# ?/, ""); print; next } NR > 2 { exit }' "${BASH_SOURCE[0]}"
}

case "${1-}" in
    -h | --help)
        usage
        exit 0
        ;;
    analog | digital)
        PARTITIONS=("$1")
        ;;
    both)
        PARTITIONS=(analog digital)
        ;;
    "")
        usage >&2
        echo >&2
        echo "regen-item9.sh: a partition argument is required: analog | digital | both" >&2
        exit 1
        ;;
    *)
        echo "regen-item9.sh: unexpected argument '$1' (expected analog | digital | both, or --help)" >&2
        exit 1
        ;;
esac

cd "$ROOT" || exit 1

die() {
    echo "regen-item9.sh: $*" >&2
    exit 1
}

for f in "$REGEN_WORKFLOW" "$REL_RECORD" "$REL_MANIFEST" "$REL_TIERS"; do
    [ -f "$f" ] || die "expected $f under $ROOT -- run this from a full checkout"
done

command -v uvx >/dev/null 2>&1 ||
    die "uvx not found on PATH. It runs the pinned klayout-tools in a throwaway
  environment; install uv (https://docs.astral.sh/uv/) or run the commands in
  manifests/README.md by hand with klayout-tools==<pin> on PATH."

regen_require_pin "$REGEN_WORKFLOW"

# --- pre-flight: fail before spending minutes on the cold starts --------------
# The analog decks resolve models against the pinned PDK, and check_env -- the
# inventory-level cold start, run again by every sim/ bench wrapper -- pins the
# whole toolchain including cocotb, so both partitions need it resolvable. The
# PDK root is reached the way sim/pdk.json declares: the PDK_ROOT_SKY130A
# override, else the ~/.volare/sky130A default.

pdk_root() {
    python3 -I - <<'PY'
import json, os
pdk = json.load(open("sim/pdk.json"))
print(os.path.realpath(os.path.expanduser(
    os.environ.get(pdk["root_override_env"], pdk["default_root"]))))
PY
}

preflight() {
    local p=$1 inv="attest/item9_${1}.json" env="evidence/item9_${1}.json"
    local missing=()

    [ -f "$inv" ] || missing+=("$inv (run this from a full checkout)")
    [ -f "$env" ] || missing+=("$env (the committed envelope this script refreshes)")

    command -v ngspice >/dev/null 2>&1 ||
        missing+=("ngspice on PATH (the decks run real single-corner ngspice -b; provisioned tools live in ~/.local/bin)")
    command -v python3 >/dev/null 2>&1 || missing+=("python3 on PATH")
    python3 -c 'import cocotb' >/dev/null 2>&1 ||
        missing+=("cocotb importable by python3 -- check_env pins it for both partitions (put a venv with the cocotb pin first on PATH)")

    case "$p" in
        digital)
            command -v iverilog >/dev/null 2>&1 ||
                missing+=("iverilog on PATH (Icarus runs the cocotb suite)")
            command -v verilator >/dev/null 2>&1 ||
                missing+=("verilator on PATH (the bench lints -Wall)")
            ;;
    esac

    local root
    root=$(pdk_root) || exit 1
    [ -d "$root" ] ||
        missing+=("the pinned PDK at $root (sim/pdk.json: set PDK_ROOT_SKY130A or install sky130A there)")

    if [ "${#missing[@]}" -gt 0 ]; then
        echo "regen-item9.sh: the '$p' toolchain is incomplete; attesting now would waste a run." >&2
        local m
        for m in "${missing[@]}"; do echo "  missing: $m" >&2; done
        echo "  Fallback (documented in manifests/README.md, \"Item 9 (testbenches shipped)\"):" >&2
        echo "  install the toolchain pins in a worktree venv and invoke the producer" >&2
        echo "  through a throwaway environment, so klt and the pinned benches do not" >&2
        echo "  share one venv:" >&2
        echo >&2
        echo "    python3 -m venv .venv && .venv/bin/pip install cocotb==2.1.0 klayout-tools==$PIN" >&2
        echo "    PATH=\"\$PWD/.venv/bin:\$PATH\" uvx --from \"klayout-tools==$PIN\" klt signoff --attest 9 \\" >&2
        echo "        --inventory attest/item9_<partition>.json -o evidence/item9_<partition>.json" >&2
        echo >&2
        echo "  Nothing was written." >&2
        exit 1
    fi
}

for p in "${PARTITIONS[@]}"; do preflight "$p"; done

# --- announce the cost before spending it -------------------------------------
# Counted live from the inventory so the numbers cannot drift from it. This is
# what stops a reader from assuming the script is a cheap hash pass -- or from
# reaching for the batch fleet, which a bounded local pass must not become.

cost_line() {
    python3 -I - "$1" <<'PY'
import json, sys

inv = json.load(open(sys.argv[1]))
ng = dry = suites = other = 0
for m in inv.get("testbenches", []):
    cs = m.get("cold_start") if isinstance(m, dict) else None
    if not cs:
        continue
    a = cs.get("argv", [])
    if a[:1] == ["ngspice"] or (a and str(a[0]).endswith("run.sh") and "--no-record" in a):
        # the oscillator-bank and smoke wrappers: each runs one real
        # single-corner ngspice -b deck
        ng += 1
    elif a[:2] == ["klt", "sim"]:
        dry += 1
    elif a[:1] == ["python3"]:
        suites += 1
    else:
        other += 1
level = inv.get("cold_start") or None
total = ng + dry + suites + other + (1 if level else 0)

parts = []
if ng:
    parts.append("%d single-corner ngspice -b decks" % ng)
if dry:
    parts.append("%d klt sim --dry-run" % dry)
if suites:
    parts.append("%d unittest suites" % suites)
if other:
    parts.append("%d other commands" % other)
if level:
    parts.append("the inventory-level %s" % " ".join(level.get("argv", ["?"])))
    if level.get("timeout_s"):
        parts.append("timeout %d s" % level["timeout_s"])
print("%d declared cold starts for real (%s)" % (total, ", ".join(parts)))
PY
}

echo "== item 9 re-attest: partitions: ${PARTITIONS[*]} =="
echo "pin:        klayout-tools==$PIN   (from $REGEN_WORKFLOW)"
for p in "${PARTITIONS[@]}"; do
    echo "cost ($p):  $(cost_line "attest/item9_${p}.json")"
done
echo
echo "This is a permitted local single-unit attestation pass -- NOT a batch grid;"
echo "do not reshape it into one, and never send it to a fleet."
echo

# --- regenerate ----------------------------------------------------------------

TMP_REPORT=$(mktemp) || exit 1
TMP_ENV=$(mktemp) || exit 1
trap 'rm -f "$TMP_REPORT" "$TMP_ENV"' EXIT

INSTALLED_ANY=0
ENV_FILES=""

# Human-readable list of the failing checks, to stderr. Returns non-zero when
# the report is missing or unparsable, so the caller can point at the direct
# command instead.
classify_report() {
    python3 -I - "$1" <<'PY' >&2
import json, sys

try:
    env = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(1)
failed = [c for c in env.get("attestation", {}).get("checks", []) if not c.get("passed")]
for c in failed:
    where = c.get("path") or c.get("testbench") or c.get("name") or " ".join(c.get("argv", []))
    print("  failed check: %s %s" % (c.get("check"), where))
    tail = [l for l in (c.get("output_tail") or "").strip().splitlines() if l.strip()]
    if tail:
        print("    last output line: %s" % tail[-1])
sys.exit(1 if not failed else 0)
PY
}

regen_partition() {
    local p=$1 inv="attest/item9_${1}.json" env="evidence/item9_${1}.json"

    echo "== partition: $p =="

    # One attestation pass per partition: the cold starts are the cost, so
    # the same pass captures the envelope for installation AND the report
    # that classifies a failure. --format json only shapes stdout (measured:
    # the -o envelope bytes are identical either way, item 10), and klt
    # deliberately writes no -o file for a failing attestation, which is what
    # the emptiness check below detects. regen-item10.sh runs the same
    # single-pass pattern (issue #310).
    local rc=0
    regen_klt signoff --attest 9 --inventory "$inv" --format json -o "$TMP_ENV" \
        >"$TMP_REPORT" 2>/dev/null || rc=$?
    if [ "$rc" -ne 0 ] || [ ! -s "$TMP_ENV" ]; then
        echo "regen-item9.sh: the '$p' attestation failed (exit $rc); nothing was written." >&2
        classify_report "$TMP_REPORT" ||
            echo "  klt produced no parsable report; re-run it directly to see the error:" >&2
        echo "  An inventoried file is missing or renamed, or a declared cold start failed." >&2
        echo "  Item 9 inventories declare no checks, so there is no record-audit case here:" >&2
        echo "  any failing check is a real evidence failure. Restore the file or fix the" >&2
        echo "  bench; narrowing the inventory to quiet the gate is a spec/ decision" >&2
        echo "  record, not a CI fix (CLAUDE.md)." >&2
        exit 1
    fi

    regen_refuse_foreign_version "$TMP_ENV"

    if cmp -s "$TMP_ENV" "$env"; then
        echo "$env is already up to date (byte-identical); not rewritten."
    else
        # mktemp makes the scratch file 0600; carry the envelope's own mode
        # over so the replacement is not left more restrictive than the file
        # it replaces. mv, never a write in place: a failed or interrupted run
        # can never leave a partial evidence file.
        chmod --reference="$env" "$TMP_ENV" 2>/dev/null || chmod 0644 "$TMP_ENV"
        mv "$TMP_ENV" "$env" || exit 1
        echo "wrote $env (klt_version $PIN)."
        INSTALLED_ANY=1
    fi
    ENV_FILES="$ENV_FILES $env"

    # The gate's own envelope check, on the bytes now on disk.
    local check_rc=0
    regen_klt signoff --attest 9 --inventory "$inv" --check "$env" || check_rc=$?
    if [ "$check_rc" -ne 0 ]; then
        echo >&2
        echo "regen-item9.sh: the freshly written $env does not --check clean (exit $check_rc)." >&2
        echo "  Re-run the commands in manifests/README.md by hand to see what disagrees." >&2
        exit 1
    fi
    echo
}

for p in "${PARTITIONS[@]}"; do regen_partition "$p"; done

# --- the record check, once, over all selected partitions ----------------------
record_rc=0
regen_klt signoff --manifest "$REL_MANIFEST" --tiers-doc "$REL_TIERS" --check "$REL_RECORD" || record_rc=$?
echo

if [ "$record_rc" -eq 3 ]; then
    cat <<MSG
The committed signoff record has ALSO drifted (status above). The tier verdict
itself moved -- an item-9 inventory changed (a pinned path added or removed),
or some other item's evidence did.

$ENV_FILES has been regenerated and is correct, but a verdict change is a
deliberate, separately reviewed commit, so this script does not write one.
Regenerate and commit the record alongside the envelope(s):

  uvx --from "klayout-tools==$PIN" klt signoff \\
      --manifest $REL_MANIFEST \\
      --tiers-doc $REL_TIERS \\
      --format json > $REL_RECORD

Then re-run this script; it should report a reproducing record.
MSG
    exit 3
fi

if [ "$record_rc" -ne 0 ]; then
    die "checking the record exited $record_rc (expected 0 or 3): the manifest, the vendored tier doc, or a cited envelope is unreadable."
fi

echo "The committed signoff record still reproduces: $REL_RECORD needs no change."
echo "(An ordinary source edit moves only hashes inside the envelope -- the record"
echo "cites the inventory, not the envelope's bytes -- so this is the expected case.)"
if [ "$INSTALLED_ANY" -eq 1 ]; then
    echo "Commit the regenerated envelope(s) with the edit that changed an inventoried file."
else
    echo "Nothing to commit: every selected envelope already matches its inventory."
fi
exit 0
