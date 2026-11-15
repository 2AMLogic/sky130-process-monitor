#!/usr/bin/env bash
#
# Regenerate evidence/item10.json -- the `klt signoff --attest 10` envelope over
# attest/item10.json -- with the klayout-tools version CI pins, and report
# whether the committed signoff record still reproduces.
#
# Run this from any directory whenever a file in attest/item10.json's `hygiene`
# list changes (README.md, LICENSE, spec/target-spec.md,
# .github/workflows/signoff.yml): their bytes are hashed into the envelope, so
# an edit without a re-attest turns T1 item 10 stale and reds the `klt signoff`
# job (issue #172). Commit the regenerated envelope in the same commit as the
# edit.
#
# The pin is read from .github/workflows/signoff.yml's `pip install
# klayout-tools==X.Y.Z` line -- that is the version CI byte-compares against,
# and it is deliberately not restated here (pin-copy consolidation, #163).
# The parser and the pinned-klt wrapper live in attest/lib/regen-common.sh,
# shared with attest/regen-item9.sh. Regenerating with the host's `klt` writes
# a different `provenance.klt_version` and a non-reproducing envelope, so the
# run always goes through `uvx --from "klayout-tools==<pin>" klt`.
#
# Writes exactly one file: evidence/item10.json. The signoff record is never
# left modified -- see "the circular bootstrap" below.
#
# Exit status:
#   0  envelope up to date (or regenerated) and the committed record reproduces
#   3  envelope regenerated, but the committed signoff record ALSO has to be
#      regenerated and committed (the command is printed)
#   1  nothing was written: the pin is unparseable, uvx is missing, or an
#      inventoried file is genuinely absent / a declared check genuinely fails
#
set -uo pipefail

ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd) || exit 1

# Every path below is relative to $ROOT on purpose: the envelope records its
# inventory path and its audit check's cwd relatively, so a run from anywhere
# else produces different bytes.
REL_INV="attest/item10.json"
REL_ENV="evidence/item10.json"
REL_RECORD="manifests/sky130-process-monitor.signoff.json"
REL_MANIFEST="manifests/sky130-process-monitor.json"
REL_TIERS="manifests/design-evidence-tiers.md"
REL_WORKFLOW=".github/workflows/signoff.yml"

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
    "") ;;
    *)
        echo "regen-item10.sh: unexpected argument '$1' (this script takes no options but --help)" >&2
        exit 1
        ;;
esac

cd "$ROOT" || exit 1

die() {
    echo "regen-item10.sh: $*" >&2
    exit 1
}

for f in "$REL_INV" "$REL_ENV" "$REL_RECORD" "$REL_MANIFEST" "$REL_TIERS" "$REL_WORKFLOW"; do
    [ -f "$f" ] || die "expected $f under $ROOT -- run this from a full checkout"
done

command -v uvx >/dev/null 2>&1 ||
    die "uvx not found on PATH. It runs the pinned klayout-tools in a throwaway
  environment; install uv (https://docs.astral.sh/uv/) or run the commands in
  manifests/README.md by hand with klayout-tools==<pin> on PATH."

# --- the pin -----------------------------------------------------------------
# The parser and the pinned-klt wrapper are shared with attest/regen-item9.sh
# (pin-copy consolidation, #163 -- restating them here is the drift the shared
# file exists to prevent). REGEN_NAME/REGEN_WORKFLOW feed its messages, so a
# refusal still names this script and this workflow.
# Read by attest/lib/regen-common.sh's messages (sourced below).
# shellcheck disable=SC2034
REGEN_NAME=regen-item10.sh
# shellcheck disable=SC2034
REGEN_WORKFLOW="$REL_WORKFLOW"
# shellcheck source=lib/regen-common.sh
source "$ROOT/attest/lib/regen-common.sh"

regen_require_pin "$REL_WORKFLOW"

echo "pin:        klayout-tools==$PIN   (from $REL_WORKFLOW)"
echo "inventory:  $REL_INV"
echo "envelope:   $REL_ENV"
echo

klt() { regen_klt "$@"; }

TMP_REPORT=$(mktemp) || exit 1
TMP_ENV=$(mktemp) || exit 1
TMP_RENDER=$(mktemp) || exit 1
RECORD_BACKUP=$(mktemp) || exit 1
cp "$REL_RECORD" "$RECORD_BACKUP" || exit 1

# The signoff record is an input to this regeneration (the envelope's `audit
# signoff-record-reproduces` check re-renders it) and the bootstrap below
# rewrites it transiently. It is always put back exactly as it was: a verdict
# change is a deliberate, separately reviewed commit, never a side effect.
restore_record() {
    if [ -f "$RECORD_BACKUP" ] && ! cmp -s "$RECORD_BACKUP" "$REL_RECORD"; then
        cp "$RECORD_BACKUP" "$REL_RECORD" || {
            echo "regen-item10.sh: FAILED to restore $REL_RECORD from $RECORD_BACKUP." >&2
            echo "  Restore it by hand (git checkout -- $REL_RECORD) before committing." >&2
            return 1
        }
    fi
}

# shellcheck disable=SC2317,SC2329  # reached through `trap cleanup EXIT` below
cleanup() {
    # Never exit from here: that would mask the script's real status.
    restore_record || :
    rm -f "$TMP_REPORT" "$TMP_ENV" "$TMP_RENDER" "$RECORD_BACKUP"
}
trap cleanup EXIT

# --- helpers -----------------------------------------------------------------

# Classify an attestation report: "pass", "audit-only" (every failing check is
# the circular signoff-record-reproduces audit), or "hygiene" (a real evidence
# failure). A human-readable list of the failing checks goes to stderr.
classify() {
    python3 -I - "$1" <<'PY'
import json, sys

with open(sys.argv[1]) as fh:
    envelope = json.load(fh)
checks = envelope.get("attestation", {}).get("checks", [])
failed = [c for c in checks if not c.get("passed")]

if envelope.get("status") == "pass" and not failed:
    print("pass")
    sys.exit(0)

for c in failed:
    print("  failed check: %s %s %s" % (c.get("check"), c.get("role"),
                                        c.get("name") or c.get("path")),
          file=sys.stderr)

def is_record_audit(c):
    return c.get("role") == "audit" and c.get("name") == "signoff-record-reproduces"

print("audit-only" if failed and all(is_record_audit(c) for c in failed) else "hygiene")
PY
}

# Re-attest into $TMP_ENV (bytes for the committed envelope) and into
# $TMP_REPORT (same envelope on stdout, which klt emits even when the
# attestation fails -- that is what makes the failure classifiable, since klt
# deliberately writes no -o file for a failing attestation).
attest() {
    local rc=0
    klt signoff --attest 10 --inventory "$REL_INV" --format json \
        >"$TMP_REPORT" 2>/dev/null || rc=$?
    if [ ! -s "$TMP_REPORT" ]; then
        echo "regen-item10.sh: klt signoff --attest 10 produced no report (exit $rc)." >&2
        echo "  Re-run it directly to see the error:" >&2
        echo "    uvx --from \"klayout-tools==$PIN\" klt signoff --attest 10 --inventory $REL_INV" >&2
        exit 1
    fi
    if [ "$rc" -ne 0 ] && [ "$rc" -ne 3 ]; then
        echo "regen-item10.sh: klt signoff --attest 10 exited $rc (expected 0 or 3)." >&2
        exit 1
    fi
    return 0
}

# Write the envelope only once the attestation passes, and only via mv, so a
# failed or interrupted run can never leave a partial evidence file.
install_envelope() {
    local rc=0
    klt signoff --attest 10 --inventory "$REL_INV" -o "$TMP_ENV" >/dev/null 2>&1 || rc=$?
    if [ "$rc" -ne 0 ] || [ ! -s "$TMP_ENV" ]; then
        echo "regen-item10.sh: the attestation passed when classified but wrote no envelope (exit $rc)." >&2
        exit 1
    fi

    # The provenance guard is shared with attest/regen-item9.sh
    # (attest/lib/regen-common.sh) and prints the same refusal via
    # REGEN_NAME/REGEN_WORKFLOW.
    regen_refuse_foreign_version "$TMP_ENV"

    if cmp -s "$TMP_ENV" "$REL_ENV"; then
        echo "$REL_ENV is already up to date (byte-identical); not rewritten."
        return 0
    fi
    # mktemp makes the scratch file 0600; carry the envelope's own mode over so
    # the replacement is not left more restrictive than the file it replaces.
    chmod --reference="$REL_ENV" "$TMP_ENV" 2>/dev/null || chmod 0644 "$TMP_ENV"
    mv "$TMP_ENV" "$REL_ENV" || exit 1
    echo "wrote $REL_ENV (5/5 checks passed, klt_version $PIN)."
}

render_record() { # -> $TMP_RENDER
    local rc=0
    klt signoff --manifest "$REL_MANIFEST" --tiers-doc "$REL_TIERS" --format json \
        >"$TMP_RENDER" 2>/dev/null || rc=$?
    # 0 = every T1 item met, 3 = graded clean with items unmet. Both are real
    # renders; anything else means the manifest or a cited envelope is broken.
    if [ "$rc" -ne 0 ] && [ "$rc" -ne 3 ]; then
        echo "regen-item10.sh: rendering the tier verdict exited $rc (expected 0 or 3):" >&2
        echo "  the manifest, the vendored tier doc, or a cited envelope is unreadable." >&2
        exit 1
    fi
    [ -s "$TMP_RENDER" ] || die "rendering the tier verdict produced no output"
}

# --- regenerate --------------------------------------------------------------
attest
verdict=$(classify "$TMP_REPORT")

case "$verdict" in
pass)
    install_envelope
    ;;
audit-only)
    # The circular bootstrap. attest/item10.json's one declared check re-renders
    # the tier verdict and compares it against the committed record -- and the
    # record grades T1 item 10 from this very envelope. So while the envelope is
    # stale the render disagrees with the committed record, the check fails, and
    # klt (correctly) refuses to write a failing envelope: the envelope cannot be
    # refreshed in one pass. manifests/README.md calls this out; the way through
    # is to render the record against the stale envelope, re-attest against that,
    # then re-render. The record ends where it started unless some other item
    # genuinely moved, which is reported below.
    echo "The envelope is stale: an inventoried file changed, so the record it"
    echo "vouches for no longer reproduces. Running the documented bootstrap"
    echo "(render record -> re-attest -> re-render); the record is restored"
    echo "afterwards either way."
    echo
    render_record
    cp "$TMP_RENDER" "$REL_RECORD" || exit 1

    attest
    verdict=$(classify "$TMP_REPORT")
    if [ "$verdict" != "pass" ]; then
        echo "regen-item10.sh: the attestation still fails after the bootstrap render." >&2
        echo "  This is not the stale-evidence case -- see the failing checks above." >&2
        echo "  Nothing was written; $REL_RECORD is restored." >&2
        exit 1
    fi
    install_envelope
    ;;
*)
    echo "regen-item10.sh: the attestation fails on an inventoried file, not on the" >&2
    echo "  circular record check. A file in $REL_INV's hygiene list is missing or" >&2
    echo "  renamed, or a declared check genuinely fails -- klt writes no envelope for" >&2
    echo "  a failing attestation, so there is nothing to regenerate here." >&2
    echo "  Restore the file, or change what item 10 attests through a spec/ decision" >&2
    echo "  record (CLAUDE.md: do not narrow an attestation to make a gate pass)." >&2
    echo "  Nothing was written." >&2
    exit 1
    ;;
esac

# --- report the gate's own two checks ----------------------------------------
# The record goes back to its committed bytes FIRST: the bootstrap above may
# have left the interim render in place, and both checks below re-render the
# verdict against whatever is on disk. Checking against the interim record
# would report drift for a tree that is in fact consistent.
restore_record || exit 1

echo
echo "== re-running the two checks .github/workflows/signoff.yml asserts =="
echo
# The record is checked first: it is the one of the two that can legitimately
# still be stale after a successful re-attest (the envelope's own audit check
# re-renders the verdict, so a drifted record also fails the envelope check --
# reporting that as an envelope problem would name the wrong file).
record_rc=0
klt signoff --manifest "$REL_MANIFEST" --tiers-doc "$REL_TIERS" --check "$REL_RECORD" || record_rc=$?
echo

if [ "$record_rc" -eq 3 ]; then
    cat <<MSG
The committed signoff record has ALSO drifted (status above). The tier verdict
itself moved -- the envelope's summary or passed_count changed (an inventoried
file removed, a declared check flipped), or some other item's evidence did.

$REL_ENV has been regenerated and is correct, but a verdict change is a
deliberate, separately reviewed commit, so this script does not write one.
Regenerate and commit the record alongside the envelope:

  uvx --from "klayout-tools==$PIN" klt signoff \\
      --manifest $REL_MANIFEST \\
      --tiers-doc $REL_TIERS \\
      --format json > $REL_RECORD

Then re-run this script; it should report a reproducing record.
MSG
    exit 3
fi

if [ "$record_rc" -ne 0 ]; then
    echo "regen-item10.sh: checking the record exited $record_rc (expected 0 or 3):" >&2
    echo "  the manifest, the vendored tier doc, or a cited envelope is unreadable." >&2
    exit 1
fi

env_rc=0
klt signoff --attest 10 --inventory "$REL_INV" --check "$REL_ENV" || env_rc=$?
if [ "$env_rc" -ne 0 ]; then
    echo >&2
    echo "regen-item10.sh: the freshly written envelope does not --check clean (exit $env_rc)," >&2
    echo "  even though the record reproduces. Re-run the commands in manifests/README.md" >&2
    echo "  by hand to see what disagrees." >&2
    exit 1
fi

echo
echo "The committed signoff record still reproduces: $REL_RECORD needs no change."
echo "Commit $REL_ENV with the edit that changed an inventoried file."
exit 0
