# shellcheck shell=bash
# Shared preamble for every negative-control script in this tree. Sourced, not executed.
#
# ONE PASS RULE, enforced here so no script can invent its own: a control passes only if the
# command exits non-zero AND its output matches the expected diagnostic, so a broken environment
# (wrong tool version, missing PATH) cannot be read as a control passing.
#
# SOURCING THIS FILE RUNS THE ENVIRONMENT BASELINE and exits 2 if it fails -- a control that
# "fails" on a host whose tools or PDK do not match the pins proves nothing. The baseline is part
# of the source, not a separate call, so it cannot be left out of a new script.
#
# Provides to the sourcing script:
#   rc             initialised to 0; the helpers set it to 1. The script ends with `exit $rc`.
#   expect_fail <name> <diagnostic-regex> <command...>
#                  Runs the command with stdout+stderr captured, and fails the control unless it
#                  exited non-zero with output matching the regex. Leaves the captured output in
#                  NEG_CONTROL_OUT so a caller can assert more about the same run.
#   expect_absent <name> <forbidden-regex>
#                  An extra condition on the output expect_fail just captured: fails the control
#                  if it matches. Use for "and it produced no number", which exit status alone
#                  does not establish.
#   NEG_SIM_DIR    absolute path of sim/
#   NEG_PDK_ROOT   the PDK root check_env.sh resolved during the baseline (its PDK_ROOT= line),
#                  so a script needing it does not re-run check_env.sh a third time.

# shellcheck disable=SC2034  # rc, NEG_SIM_DIR and NEG_PDK_ROOT are read by the sourcing script
NEG_SIM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEG_CONTROL_OUT=""
rc=0

expect_fail() { # name, expected-diagnostic regex, command...
  local name="$1" pat="$2"; shift 2
  if NEG_CONTROL_OUT="$("$@" 2>&1)"; then
    echo "NEG-CONTROL FAIL (unexpectedly passed): $name"; rc=1
  elif printf '%s\n' "$NEG_CONTROL_OUT" | grep -Eq -- "$pat"; then
    echo "neg-control ok (failed as required, diagnostic matched): $name"
  else
    echo "NEG-CONTROL FAIL (failed for the wrong reason, no match for /$pat/): $name"
    printf '%s\n' "$NEG_CONTROL_OUT" | tail -5 | sed 's/^/    /'; rc=1
  fi
}

expect_absent() { # name, regex the output captured by the preceding expect_fail must NOT match
  local name="$1" pat="$2"
  if printf '%s\n' "$NEG_CONTROL_OUT" | grep -Eq -- "$pat"; then
    echo "NEG-CONTROL FAIL (output matched /$pat/, which it must not): $name"
    printf '%s\n' "$NEG_CONTROL_OUT" | grep -E -- "$pat" | tail -5 | sed 's/^/    /'; rc=1
  fi
}

# Baseline: the environment must be sound, else a control "failing" proves nothing.
if ! _neg_env_out="$("$NEG_SIM_DIR/check_env.sh" 2>&1)"; then
  echo "NEG-CONTROL ABORT: environment check failed; fix it first:" >&2
  printf '%s\n' "$_neg_env_out" >&2
  exit 2
fi
# shellcheck disable=SC2034  # read by the sourcing script (sim/osc_bank/negative_controls.sh)
NEG_PDK_ROOT="$(printf '%s\n' "$_neg_env_out" | sed -n 's/^PDK_ROOT=//p')"
unset _neg_env_out
