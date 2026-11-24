#!/usr/bin/env bash
#
# Shared pieces of the attest/regen-item*.sh regeneration scripts (issue #190).
#
# Everything drift-prone enough that a second hand-copied version would
# defeat the consolidation they exist for (#163, #330), so the regen scripts
# source it from here instead of restating it:
#
#   REL_RECORD / REL_MANIFEST / REL_TIERS
#       The signoff record, manifest, and tiers doc every regen script
#       checks the committed envelopes against, as repo-relative paths (the
#       envelopes record paths relatively, so callers cd to $ROOT before
#       running the checks). Assign before sourcing to override.
#
#   regen_parse_pin / regen_require_pin
#       The klayout-tools pin parser: reads the version CI pins from
#       .github/workflows/signoff.yml's `pip install klayout-tools==X.Y.Z`
#       line into $PIN. That line is the single source of the pin every
#       regenerated envelope is compared against; a version literal in a
#       regen script would silently drift from it.
#
#   regen_klt
#       The pinned producer: `uvx --from "klayout-tools==$PIN" klt`.
#       Regenerating with the host's `klt` writes a different
#       provenance.klt_version and a non-reproducing envelope.
#
#   regen_refuse_foreign_version
#       The guard that keeps the above honest: refuses to install an
#       envelope whose provenance.klt_version differs from $PIN.
#
#   regen_usage / regen_die / regen_require_files / regen_require_uvx
#       The CLI and preflight boilerplate: the comment-header extractor
#       behind --help, the prefixed error-and-exit helper, the
#       full-checkout file check, and the uvx availability check.
#
#   regen_install_envelope
#       The atomic envelope install: foreign-version refusal, the
#       byte-identical no-op check, the mode-preserving mv.
#
#   regen_check_envelope / regen_check_record
#       The gate's own two checks, re-run on what was installed: the
#       per-item `--attest <item> --check` on the envelope, and the
#       `--manifest ... --check` on the committed record with its exit-3
#       drift report.
#
# Callers set REGEN_NAME (their own script name, used in messages) and
# REGEN_WORKFLOW (the workflow path the pin is parsed from) before sourcing
# this file -- both default to the values every current caller uses -- and
# they compute ROOT and cd there before the preflight helpers run, so its
# messages name the script the user actually ran.

set -uo pipefail

REGEN_NAME=${REGEN_NAME:-regen}
REGEN_WORKFLOW=${REGEN_WORKFLOW:-.github/workflows/signoff.yml}
REL_RECORD=${REL_RECORD:-manifests/sky130-process-monitor.signoff.json}
REL_MANIFEST=${REL_MANIFEST:-manifests/sky130-process-monitor.json}
REL_TIERS=${REL_TIERS:-manifests/design-evidence-tiers.md}

regen_parse_pin() {
    # -> stdout: the pinned klayout-tools version (possibly empty)
    sed -nE 's/^[[:space:]]*(run:[[:space:]]*)?pip install klayout-tools==([0-9][0-9A-Za-z.+!-]*)[[:space:]]*$/\2/p' \
        "$1" | head -n 1
}

regen_require_pin() {
    # $1 = workflow path; sets PIN, or exits 1 with nothing written
    PIN=$(regen_parse_pin "$1")
    if [ -z "$PIN" ]; then
        echo "$REGEN_NAME: could not parse the klayout-tools pin from $1." >&2
        echo "  Expected a line of the form:   run: pip install klayout-tools==X.Y.Z" >&2
        echo "  That line is the single source of the pin these envelopes are compared" >&2
        echo "  against; if the workflow's install step was renamed or reshaped, update the" >&2
        echo "  sed pattern here in attest/lib/regen-common.sh rather than hardcoding a" >&2
        echo "  version in a regen script. Nothing was written." >&2
        exit 1
    fi
}

regen_klt() {
    uvx --quiet --from "klayout-tools==$PIN" klt "$@"
}

regen_refuse_foreign_version() {
    # $1 = candidate envelope file; exits 1 (nothing installed) when its
    # provenance.klt_version differs from $PIN
    local wrote_version
    wrote_version=$(python3 -I -c \
        'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]][sys.argv[3]])' \
        "$1" provenance klt_version) || exit 1
    if [ "$wrote_version" != "$PIN" ]; then
        echo "$REGEN_NAME: refusing to install an envelope stamped klt_version" >&2
        echo "  '$wrote_version' when $REGEN_WORKFLOW pins '$PIN'. CI byte-compares" >&2
        echo "  against the pin, so this envelope would not reproduce. Nothing was written." >&2
        exit 1
    fi
}

regen_usage() {
    # $1 = script path; prints its comment header (line 3 to the first
    # non-comment line), so --help cannot drift out of sync with it.
    awk 'NR > 2 && /^#/ { sub(/^# ?/, ""); print; next } NR > 2 { exit }' "$1"
}

regen_die() {
    # Prefixed with REGEN_NAME so a failure names the script the user
    # actually ran; exits 1 with nothing written.
    echo "$REGEN_NAME: $*" >&2
    exit 1
}

regen_require_files() {
    # $1 = the checkout root (the caller's $ROOT); each remaining argument
    # must exist as a file under it (callers cd there first and pass the
    # same repo-relative paths the envelopes record), else exit 1.
    local root=$1
    shift
    local f
    for f in "$@"; do
        [ -f "$f" ] || regen_die "expected $f under $root -- run this from a full checkout"
    done
}

regen_require_uvx() {
    command -v uvx >/dev/null 2>&1 ||
        regen_die "uvx not found on PATH. It runs the pinned klayout-tools in a throwaway
  environment; install uv (https://docs.astral.sh/uv/) or run the commands in
  manifests/README.md by hand with klayout-tools==<pin> on PATH."
}

regen_install_envelope() {
    # $1 = candidate envelope (a mktemp scratch file), $2 = the committed
    # envelope it replaces, $3 = extra success label ("" or "5/5 checks
    # passed, "). Returns 0 when it wrote $2, 1 when $2 was already
    # byte-identical; exits 1 (nothing installed) on a foreign klt_version
    # or a failed mv.
    regen_refuse_foreign_version "$1"
    if cmp -s "$1" "$2"; then
        echo "$2 is already up to date (byte-identical); not rewritten."
        return 1
    fi
    # mktemp makes the scratch file 0600; carry the envelope's own mode
    # over so the replacement is not left more restrictive than the file
    # it replaces. mv, never a write in place: a failed or interrupted run
    # can never leave a partial evidence file.
    chmod --reference="$2" "$1" 2>/dev/null || chmod 0644 "$1"
    mv "$1" "$2" || exit 1
    echo "wrote $2 ($3klt_version $PIN)."
    return 0
}

regen_check_envelope() {
    # $1 = attest item, $2 = inventory, $3 = the envelope now on disk,
    # $4 = how to name it in the failure message (defaults to its path;
    # item 10 passes "envelope"), $5 = trailing failure clause ("", or
    # ", even though the record reproduces"). Exits 1 when the freshly
    # installed envelope does not --check clean.
    local label=${4:-$3} rc=0
    regen_klt signoff --attest "$1" --inventory "$2" --check "$3" || rc=$?
    if [ "$rc" -ne 0 ]; then
        echo >&2
        echo "$REGEN_NAME: the freshly written $label does not --check clean (exit $rc)${5:-}." >&2
        echo "  Re-run the commands in manifests/README.md by hand to see what disagrees." >&2
        exit 1
    fi
}

regen_check_record() {
    # $1 = why the tier verdict moved (worded per item; may span lines to
    # keep the wrap), $2 = what was regenerated (the envelope path or
    # list), $3 = "" or "(s)" after "envelope". Exits 3 when the record
    # must be regenerated and committed (the command is printed), 1 on an
    # unexpected status; returns 0 when the record reproduces.
    local record_rc=0
    regen_klt signoff --manifest "$REL_MANIFEST" --tiers-doc "$REL_TIERS" --check "$REL_RECORD" || record_rc=$?
    echo

    if [ "$record_rc" -eq 3 ]; then
        cat <<MSG
The committed signoff record has ALSO drifted (status above). The tier verdict
itself moved -- $1

$2 has been regenerated and is correct, but a verdict change is a
deliberate, separately reviewed commit, so this script does not write one.
Regenerate and commit the record alongside the envelope$3:

  uvx --from "klayout-tools==$PIN" klt signoff \\
      --manifest $REL_MANIFEST \\
      --tiers-doc $REL_TIERS \\
      --format json > $REL_RECORD

Then re-run this script; it should report a reproducing record.
MSG
        exit 3
    fi

    if [ "$record_rc" -ne 0 ]; then
        regen_die "checking the record exited $record_rc (expected 0 or 3): the manifest, the vendored tier doc, or a cited envelope is unreadable."
    fi
}
