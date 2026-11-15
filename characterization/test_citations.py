#!/usr/bin/env python3
"""Citation-existence check for the T1 item-8 characterization reports (issue #169).

Run: python3 -I characterization/test_citations.py

Standard library only -- no simulator, no PDK, no `klt`, nothing simulated and nothing
regenerated. This module reads two committed Markdown files and the repository tree, and
nothing else.

Why this exists
---------------
`characterization/analog.md` and `characterization/digital.md` are hand-assembled
aggregations: every verdict in them carries the path of the committed record it rests on.
That is the whole value of the reports, and a path is exactly the kind of claim that rots
silently -- a record renamed or deleted in some later change leaves a citation pointing at
nothing, and a reader cannot tell a dangling citation from a real one without checking each
by hand. T1 item 8 asks for "the evidence record each verdict rests on"
(`manifests/design-evidence-tiers.md`), so a dangling citation is a defect in the evidence,
not a typo. This test turns it into a red CI run.

What it checks
--------------
1. Every repo-path-shaped citation in each report resolves to something that exists.
2. Each report cites a non-empty set of paths -- so a report whose citations were all
   dropped fails rather than passing vacuously.
3. Both reports exist and are non-trivial.

How a citation is recognised
----------------------------
The reports write every record path in backticks, so the extractor takes backtick-quoted
spans and keeps those that look like a repository path:

- contains a "/" (a bare word like `klt` or `osc_hd` is not a path),
- no whitespace, no "://" (so a URL is never treated as a repo path),
- not absolute and not an option (does not start with "/", "-" or "~"),
- and its FIRST path segment names something that exists at the repository root.

That last rule is how "skip anything outside the repo" is implemented: `github.com/foo/bar`
and `docs/cli/signoff.md` (a path inside the klayout-tools package, not this repo) are
skipped because `github.com` and `docs` are not entries at this repo's root. A typo inside a
real top-level directory -- `sim/solve/records/typo.md` -- keeps its first segment, so it is
checked and fails, which is the case this test is for.

Glob and brace forms (`sim/...../grid_*.json.gz`, `reports/{grid,mc}_*.json.gz`) are
expanded and required to match AT LEAST ONE existing path, so a family citation is checked
rather than skipped. The reports as written avoid those forms and cite explicit paths or
directories; the handling is here so a later edit that introduces one is still checked.

Docstring conventions follow `sim/solve/test_records_reproduce.py`.
"""
import os
import re
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPORTS = (
    "characterization/analog.md",
    "characterization/digital.md",
)

# A backtick-quoted span, matched against whitespace-normalised text (see
# extract_citations) so that a span Markdown wrapped across a line break is seen whole
# rather than as two half-spans with misplaced boundaries.
_BACKTICK = re.compile(r"`([^`]+)`")

# Characters a repo path may contain here: path, glob and brace-expansion syntax only.
_PATHISH = re.compile(r"^[A-Za-z0-9_.][A-Za-z0-9._/*?{},+-]*$")


def _read(rel):
    """Read a repo-relative text file. Context-managed: an unclosed handle in a test
    emits a ResourceWarning that buries the real output."""
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def _repo_root_entries():
    """Names present at the repository root -- the gate on a citation's first segment."""
    return set(os.listdir(REPO))


def _expand_braces(token):
    """Expand one level of {a,b,c} alternation, recursively. No brace -> [token]."""
    start = token.find("{")
    if start == -1:
        return [token]
    depth = 0
    for i in range(start, len(token)):
        if token[i] == "{":
            depth += 1
        elif token[i] == "}":
            depth -= 1
            if depth == 0:
                head, body, tail = token[:start], token[start + 1 : i], token[i + 1 :]
                out = []
                for alt in body.split(","):
                    out.extend(_expand_braces(head + alt + tail))
                return out
    return [token]  # unbalanced brace: treat literally


def extract_citations(text, root_entries):
    """Repo-path-shaped citations in `text`, in first-appearance order, deduplicated."""
    seen, out = set(), []
    # Collapse every run of whitespace (including line breaks) to one space, so a
    # backtick span that Markdown wrapped across lines is matched as one token. A span
    # that genuinely contains a space is still rejected below by the no-whitespace rule.
    normalised = re.sub(r"\s+", " ", text)
    for raw in _BACKTICK.findall(normalised):
        token = raw.strip()
        if "/" not in token or "://" in token:
            continue
        if token[0] in "/-~" or not _PATHISH.match(token):
            continue
        if token.split("/", 1)[0] not in root_entries:
            continue  # outside this repository -- skipped, not checked
        if token not in seen:
            seen.add(token)
            out.append(token)
    return out


def resolve(token):
    """True if `token` names an existing path, or (if a glob/brace form) matches >= 1."""
    import glob as _glob

    candidates = _expand_braces(token)
    if not any(c in token for c in "*?") and len(candidates) == 1:
        return os.path.exists(os.path.join(REPO, candidates[0].rstrip("/")))
    for cand in candidates:
        if _glob.glob(os.path.join(REPO, cand)):
            return True
    return False


class TestReportsExist(unittest.TestCase):
    def test_both_reports_present_and_substantial(self):
        for rel in REPORTS:
            path = os.path.join(REPO, rel)
            self.assertTrue(os.path.isfile(path), f"{rel} is missing")
            self.assertGreater(len(_read(rel)), 2000, f"{rel} is implausibly short")


class TestCitationsExist(unittest.TestCase):
    """Every record path the two reports cite must exist at HEAD."""

    def test_citations_resolve(self):
        root_entries = _repo_root_entries()
        for rel in REPORTS:
            with self.subTest(report=rel):
                citations = extract_citations(_read(rel), root_entries)
                # Guard against vacuous success: a report whose citations were all
                # removed must fail here rather than trivially pass the loop below.
                self.assertGreater(
                    len(citations),
                    10,
                    f"{rel} cites {len(citations)} repo paths; a characterization report "
                    "must carry the record path behind each verdict",
                )
                missing = sorted(c for c in citations if not resolve(c))
                self.assertEqual(
                    [],
                    missing,
                    f"{rel} cites {len(missing)} path(s) that do not exist at HEAD: "
                    f"{missing}. Either the record moved (update the citation) or the "
                    "citation is wrong.",
                )

    def test_each_report_cites_its_own_partition_records(self):
        """A smoke check that the extractor is finding real citations, not noise."""
        root_entries = _repo_root_entries()
        analog = extract_citations(_read(REPORTS[0]), root_entries)
        digital = extract_citations(_read(REPORTS[1]), root_entries)
        self.assertIn("sim/solve/records/2026-11-05-rows1-4.md", analog)
        self.assertIn("sta/readout.osc-corner.sta.report.json", digital)


class TestExtractor(unittest.TestCase):
    """The recogniser's own rules, so a future edit cannot silently widen or narrow it."""

    def setUp(self):
        self.root = _repo_root_entries()

    def test_skips_non_paths_and_outside_repo(self):
        text = (
            "`klt sta` `osc_hd` `--format json` `https://example.invalid/a/b` "
            "`/etc/passwd` `docs/cli/signoff.md` `github.com/o/r`"
        )
        self.assertEqual([], extract_citations(text, self.root))

    def test_keeps_repo_paths(self):
        text = "see `sim/pdk.json` and `spec/target-spec.md` and `measurements`"
        self.assertEqual(
            ["sim/pdk.json", "spec/target-spec.md"], extract_citations(text, self.root)
        )

    def test_missing_path_in_real_top_level_dir_is_reported(self):
        text = "`sim/solve/records/does-not-exist.md`"
        found = extract_citations(text, self.root)
        self.assertEqual(["sim/solve/records/does-not-exist.md"], found)
        self.assertFalse(resolve(found[0]))

    def test_line_wrapped_spans_are_matched_whole(self):
        """A backtick span wrapped across lines is one token, not two half-spans.

        A path itself can never be split by a reflow -- Markdown wraps at whitespace and a
        repository path contains none -- so this is about span BOUNDARIES, not about
        rescuing a split path. The reports do wrap multi-word spans
        (`status: "pass"`, `klt extract --abstract-cells ...`); matching those whole means
        their tails cannot be mistaken for a path, and a real citation either side of the
        wrap is still found.
        """
        text = 'the report reads `status:\n"pass"` -- see `sim/pdk.json`\nand `spec/target-spec.md`'
        self.assertEqual(
            ["sim/pdk.json", "spec/target-spec.md"], extract_citations(text, self.root)
        )
        # A multi-word span stays rejected whether or not it wrapped.
        self.assertEqual([], extract_citations("`klt extract\n--def-net-names`", self.root))

    def test_brace_and_glob_forms_resolve(self):
        self.assertTrue(resolve("sim/sensitivity/records/reports/grid_*.json.gz"))
        self.assertTrue(resolve("evidence/item8_{analog,digital}.json"))
        self.assertFalse(resolve("sim/nope/*.json"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
