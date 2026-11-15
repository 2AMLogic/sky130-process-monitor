#!/usr/bin/env bash
#
# Shared pieces of the attest/regen-item*.sh regeneration scripts (issue #190).
#
# Two pieces are drift-prone enough that a second hand-copied version would
# defeat the consolidation they exist for (#163), so the regen scripts source
# them from here instead of restating them:
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
# Callers set REGEN_NAME (their own script name, used in messages) and
# REGEN_WORKFLOW (the workflow path the pin is parsed from) before sourcing
# this file, so its messages name the script the user actually ran.

set -uo pipefail

REGEN_NAME=${REGEN_NAME:-regen}
REGEN_WORKFLOW=${REGEN_WORKFLOW:-.github/workflows/signoff.yml}

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
