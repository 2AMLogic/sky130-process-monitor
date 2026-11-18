#!/usr/bin/env python3
"""Work-plan generated-region suffix guard (issue #250).

Run: python3 -I attest/test_work_plan_region.py

Standard library only -- no forge access, no re-render, nothing simulated. This
module reads the bytes of `WORK_PLAN.md` and nothing else.

Why this exists
---------------
The generated region of `WORK_PLAN.md` (between `<!-- guide:plan-body:start -->`
and `<!-- guide:plan-body:end -->`) is compared byte-for-byte against the Guide
role's `render_plan_body()`. A hand-written token inside it -- e.g. a trailing
`*(held)*` on a bullet, which re-appeared nine times in PR #249 -- forces a
no-op churn PR on every Guide pass, and until now no check saw it: the Guide
regenerates the region from live forge state, so the token survives until a
human notices the diff noise.

What it checks
--------------
Every bullet line inside the marker region that ends in an italic parenthesised
tag `*(word)*` must use a word `render_plan_body()` actually emits:
`curated`, `architect`, or `hermit` (allowlist, not a `held` grep -- the next
invented token is caught too). Suffixes outside the region are prose, not
generated output, and are ignored; a missing marker is a clear failure rather
than a silent pass, since a moved or deleted marker would otherwise disable the
whole guard.
"""
import os
import re
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORK_PLAN = os.path.join(REPO, "WORK_PLAN.md")

START_MARKER = "<!-- guide:plan-body:start -->"
END_MARKER = "<!-- guide:plan-body:end -->"

# The only italic bullet suffixes `render_plan_body()` (.loom/roles/guide.md)
# emits; anything else in the generated region is a hand-edit that will churn
# the next Guide pass.
ALLOWED_SUFFIXES = {"curated", "architect", "hermit"}

# A bullet line whose trailing text is an italic parenthesised tag, e.g.
# `- **#12**: title *(held)*`. Trailing whitespace tolerated; the tag must sit
# at end of line -- `*(held)*` mid-sentence is prose, not the generated format.
_BULLET_SUFFIX = re.compile(r"^- .*\*\(([^()]+)\)\*\s*$")


class MissingMarkerError(ValueError):
    """One of the two plan-body markers is absent from WORK_PLAN.md."""


def check_file(text):
    """Violations (human-readable strings) for one WORK_PLAN.md content string.

    Raises MissingMarkerError if either marker is missing, so a moved or
    deleted marker cannot silently disable the guard.
    """
    start = text.find(START_MARKER)
    if start == -1:
        raise MissingMarkerError(
            "no start marker %s found -- the generated region cannot be delimited"
            % START_MARKER
        )
    region_start = start + len(START_MARKER)
    end = text.find(END_MARKER, region_start)
    if end == -1:
        raise MissingMarkerError(
            "no end marker %s after the start marker -- the generated region is unterminated"
            % END_MARKER
        )
    region = text[region_start:end]
    first_line = text.count("\n", 0, region_start) + 1
    violations = []
    for offset, line in enumerate(region.splitlines()):
        match = _BULLET_SUFFIX.match(line)
        if match and match.group(1) not in ALLOWED_SUFFIXES:
            violations.append(
                "WORK_PLAN.md:%d: bullet suffix *(%s)* is not allowlisted %s -- %s"
                % (
                    first_line + offset,
                    match.group(1),
                    sorted(ALLOWED_SUFFIXES),
                    line.strip(),
                )
            )
    return violations


def _fixture(body):
    """A WORK_PLAN.md-shaped document with `body` as the generated region."""
    return (
        "# Work Plan\n"
        "\n"
        "Prioritized roadmap from current GitHub label state.\n"
        "\n"
        + START_MARKER
        + "\n"
        + body
        + "\n"
        + END_MARKER
        + "\n"
        "| Issues open | 5 |\n"
    )


class TestRegionExtraction(unittest.TestCase):
    def test_violation_reports_whole_file_line_number(self):
        # Header (1) + blank (2) + intro (3) + blank (4) + start marker (5):
        # the offending bullet is line 6 of the document.
        text = _fixture("- **#1**: x *(held)*")
        violations = check_file(text)
        self.assertEqual(1, len(violations))
        self.assertTrue(violations[0].startswith("WORK_PLAN.md:6:"), violations[0])

    def test_missing_start_marker_is_a_clear_failure(self):
        text = _fixture("- **#1**: title").replace(START_MARKER + "\n", "")
        with self.assertRaises(MissingMarkerError) as ctx:
            check_file(text)
        self.assertIn("start marker", str(ctx.exception))

    def test_missing_end_marker_is_a_clear_failure(self):
        text = _fixture("- **#1**: title").replace("\n" + END_MARKER, "")
        with self.assertRaises(MissingMarkerError) as ctx:
            check_file(text)
        self.assertIn("end marker", str(ctx.exception))


class TestSuffixGuard(unittest.TestCase):
    def test_current_committed_work_plan_passes(self):
        with open(WORK_PLAN, "r", encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn(START_MARKER, text)
        self.assertIn(END_MARKER, text)
        self.assertEqual([], check_file(text))

    def test_held_suffix_fails(self):
        text = _fixture("- **#1**: x *(held)*")
        violations = check_file(text)
        self.assertEqual(1, len(violations))
        self.assertIn("*(held)*", violations[0])

    def test_any_unknown_suffix_fails(self):
        text = _fixture("- **#2**: y *(urgent)*")
        violations = check_file(text)
        self.assertEqual(1, len(violations))
        self.assertIn("*(urgent)*", violations[0])

    def test_all_allowlisted_suffixes_pass(self):
        text = _fixture(
            "- **#1**: a *(curated)*\n"
            "- **#2**: b *(architect)*\n"
            "- **#3**: c *(hermit)*"
        )
        self.assertEqual([], check_file(text))

    def test_suffix_outside_markers_is_ignored(self):
        text = (
            "# Work Plan\n"
            + START_MARKER
            + "\n- **#1**: a *(curated)*\n"
            + END_MARKER
            + "\n"
            "## Notes\n\n"
            "- **#9**: hand-written note *(held)*\n"
        )
        self.assertEqual([], check_file(text))

    def test_prose_held_mention_inside_region_is_not_flagged(self):
        text = _fixture(
            "- **#4**: merge risk (held) for operator decision\n"
            "- **#5**: status *(held)* until a human reviews it"
        )
        self.assertEqual([], check_file(text))


if __name__ == "__main__":
    unittest.main(verbosity=2)
