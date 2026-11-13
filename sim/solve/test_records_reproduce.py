#!/usr/bin/env python3
"""Pinned-input reproduction check for the committed sim/solve outputs (issue #140).

Run: python3 -I sim/solve/test_records_reproduce.py

Post-processing only: every input here is a committed `klt sim` report, no simulator and no PDK are
needed, and nothing is simulated. SIMULATED evidence is re-derived, never regenerated in place --
each pipeline writes into a temp dir and is compared byte-for-byte with the committed file.

Why this exists
---------------
The records' own `Reproduce:` lines abbreviate their inputs as a glob over a reports directory
(`sim/sensitivity/records/reports/{grid,mc_osc}_*.json.gz`, `sim/solve/mc/reports{,-sized}/*.json.gz`).
Reports added to those directories afterwards match the same glob, so the obvious reading of a
reproduce line stops regenerating its record and a reader cannot tell a stale record from a wrong
input set (#140). The input sets below are therefore PINNED as explicit file lists: this module
contains no glob, so a new report landing in any of those directories cannot change its result.

The same pinned lists are quoted in a dated, appended note at the foot of each record; the records
themselves, and every committed JSON, are append-only evidence and are not edited.

Interpreter requirement (measured, #140)
----------------------------------------
`sim/solve/records/2026-11-05-rows1-4.json` is byte-reproducible only on CPython >= 3.12: it writes
`mc_pooled_sigma_lnf` at full float repr, CPython 3.12 changed `sum()` of floats to Neumaier
compensated summation (gh-100425), and two of its five sigmas move by 1 ULP on 3.10/3.11. No row
2/3/4 number changes. The record is evidence and is not regenerated to hide this; `.github/
workflows/tests.yml` runs 3.12 and `test_ci_python_satisfies_every_min_python` keeps it there. The
samples files below round to 6 decimals and reproduce on every version tried (3.10, 3.11, 3.12, 3.13).

Not covered here
----------------
`sim/solve/mc/RECORD-2026-11-06-item6.md` (the reduced-bank run). Its output was written to
`sim/solve/mc/samples-binding-cells.json` and then superseded at that path by the full-bank run of
`RECORD-2026-11-06-item6-full-bank.md`, so there is no committed file left to diff it against. Its
input set is still identified and pinned in that record's appended note; it reproduces the file as
committed at `63392bd`, which only `git show` can supply and a shallow CI checkout does not have.
"""
import filecmp
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

ANALYZE = "sim/sensitivity/analyze.py"
SOLVE = "sim/solve/solve.py"
YIELD_SAMPLES = "sim/solve/yield_samples.py"

R = "sim/sensitivity/records/reports"          # #8 grid / nominal-MC reports
B = "sim/solve/mc/reports"                     # #31 binding-cell MC reports
Z = "sim/solve/mc/reports-sized"               # #31 sized (chunked) binding-cell MC reports

# ---------------------------------------------------------------- pinned input sets
#
# Each list is the set the matching record's glob resolved to at the commit that wrote the record
# (`git ls-tree <commit> <dir>`), in the order the shell expands it -- the order matters, because
# `analyze.py extract-mc` pools same-cell samples by concatenation.

# `{grid,mc_osc}_*.json.gz` at e57415f (2026-11-05), the rows 1-4 record.
GRID_5 = ["%s/grid_osc_%s.json.gz" % (R, o) for o in ("hd", "nmos", "pmos", "wire", "subth")]
MCNOM_5 = ["%s/mc_osc_%s.json.gz" % (R, o) for o in ("hd", "nmos", "pmos", "wire", "subth")]

# `grid_*.json.gz` / `mc_osc_*.json.gz` at f1026ec (2026-11-06), the full-bank item 6 record.
# `grid_osc_hd_5p.json.gz` / `mc_osc_hd_5p.json.gz` are a variant `analyze._osc_of` attributes to
# osc_hd; they were already in the directory and are part of this record's input set.
_SIX = ("hd", "hd_5p", "nmos", "pmos", "subth", "wire")
GRID_6 = ["%s/grid_osc_%s.json.gz" % (R, o) for o in _SIX]
MCNOM_6 = ["%s/mc_osc_%s.json.gz" % (R, o) for o in _SIX]

# `grid_*.json.gz` at 0930916 / 6d7a431 (2026-11-06), the sized item 6 records: the two off-nominal
# cold-margin grids landed in between. `mc_osc_*.json.gz` is unchanged from the full-bank record.
GRID_8 = ["%s/grid_osc_%s.json.gz" % (R, o) for o in
          ("hd", "hd_5p", "nmos", "pmos", "subth", "subth_sf_cold", "wire", "wire_sf_cold")]

# `sim/solve/mc/reports/*.json.gz` from f1026ec onwards: osc_hd / osc_pmos / osc_subth in one report
# each, osc_nmos / osc_wire one report per binding cell (the per-cell resubmission of that record).
_BIND_CELLS = ["ff_1.62V_27C", "ff_1.98V_27C", "fs_1.98V_27C", "sf_1.98V_27C",
               "ss_1.98V_27C", "tt_1.62V_-40C", "tt_1.98V_27C"]
MCBIND_18 = (["%s/mc_bind_osc_hd.json.gz" % B]
             + ["%s/mc_bind_osc_nmos_%s.json.gz" % (B, c) for c in _BIND_CELLS]
             + ["%s/mc_bind_osc_pmos.json.gz" % B,
                "%s/mc_bind_osc_subth_-40C.json.gz" % B,
                "%s/mc_bind_osc_subth_27C.json.gz" % B]
             + ["%s/mc_bind_osc_wire_%s.json.gz" % (B, c) for c in _BIND_CELLS])

# `sim/solve/mc/reports-sized/*.json.gz`: 4 chunks of n=50 per (oscillator, row-2/4 binding cell).
_SIZED_CELLS = [("ff", "1.62V", "27C"), ("ff", "1.98V", "27C"), ("fs", "1.98V", "27C"),
                ("sf", "1.98V", "27C"), ("ss", "1.98V", "27C"), ("tt", "1.98V", "27C")]


def _sized(oscs):
    return ["%s/mc_sized_osc_%s_%s_%s_%s_c%d.json.gz" % (Z, o, p, v, t, c)
            for o in oscs for (p, v, t) in _SIZED_CELLS for c in range(4)]


MCSIZED_SUBTH_24 = _sized(("subth",))                                  # at 0930916
MCSIZED_ALL_120 = _sized(("hd", "nmos", "pmos", "subth", "wire"))      # at 6d7a431

# ---------------------------------------------------------------- pinned outputs
#
# Each committed output maps to the exact command steps that regenerate it. A "@name" token is a
# temp-dir artifact; any other token containing "/" is a repo-relative path. The last step's "-o"
# artifact is the one compared with the committed file. Steps repeated across entries are identical
# tuples and are executed once.

_ROWS14 = [
    (ANALYZE, ["extract"] + GRID_5 + ["-o", "@freq_5.json"]),
    (ANALYZE, ["extract-mc"] + MCNOM_5 + ["-o", "@mcnom_5.json"]),
    (SOLVE, ["grade", "@freq_5.json", "@mcnom_5.json", "--json", "@rows1-4.json"]),
]
_FULL_BANK = [
    (ANALYZE, ["extract"] + GRID_6 + ["-o", "@freq_6.json"]),
    (ANALYZE, ["extract-mc"] + MCNOM_6 + ["-o", "@mcnom_6.json"]),
    (ANALYZE, ["extract-mc"] + MCBIND_18 + ["-o", "@mcbind_18.json"]),
    (YIELD_SAMPLES, ["build", "@freq_6.json", "@mcnom_6.json", "@mcbind_18.json",
                     "-o", "@samples-binding-cells.json"]),
]
_SIZED_COMMON = [
    (ANALYZE, ["extract"] + GRID_8 + ["-o", "@freq_8.json"]),
    (ANALYZE, ["extract-mc"] + MCNOM_6 + ["-o", "@mcnom_6.json"]),
]
_SIZED = _SIZED_COMMON + [
    (ANALYZE, ["extract-mc"] + MCBIND_18 + MCSIZED_SUBTH_24 + ["-o", "@mcbind_sized.json"]),
]
_SIZED_BANK = _SIZED_COMMON + [
    (ANALYZE, ["extract-mc"] + MCBIND_18 + MCSIZED_ALL_120 + ["-o", "@mcbind_sized_bank.json"]),
]

PINNED = {
    "sim/solve/records/2026-11-05-rows1-4.json": {
        "record": "sim/solve/records/2026-11-05-rows1-4.md",
        "steps": _ROWS14,
        # MEASURED (2026-11-13, #140), not a workaround: this record writes
        # `mc_pooled_sigma_lnf` at full float repr, and those values come out of
        # `sum()` over floats in `analyze.mc_sigmas`. CPython 3.12 changed `sum()`
        # of floats to Neumaier compensated summation (gh-100425), so on 3.10/3.11
        # the osc_pmos and osc_wire sigmas differ from the committed record in the
        # last ULP (0.006711570064586324 vs ...23, 0.0014583321231023284 vs ...86).
        # Every row 2/3/4 number in the record is unaffected. The record is
        # evidence and is NOT regenerated to paper over this; CI runs 3.12, and an
        # older interpreter skips this one check with the reason above.
        "min_python": (3, 12),
    },
    "sim/solve/mc/samples-binding-cells.json": {
        "record": "sim/solve/mc/RECORD-2026-11-06-item6-full-bank.md",
        "steps": _FULL_BANK,
    },
    "sim/solve/mc/samples-sized.json": {
        "record": "sim/solve/mc/RECORD-2026-11-06-item6-sized.md",
        "steps": _SIZED + [
            (YIELD_SAMPLES, ["build", "@freq_8.json", "@mcnom_6.json", "@mcbind_sized.json",
                             "-o", "@samples-sized.json"]),
        ],
    },
    "sim/solve/mc/samples-sized-negctl-hd0.3.json": {
        "record": "sim/solve/mc/RECORD-2026-11-06-item6-sized.md",
        "steps": _SIZED + [
            (YIELD_SAMPLES, ["build", "@freq_8.json", "@mcnom_6.json", "@mcbind_sized.json",
                             "--defect", "0.3", "-o", "@samples-sized-negctl.json"]),
        ],
    },
    "sim/solve/mc/samples-sized-bank.json": {
        "record": "sim/solve/mc/RECORD-2026-11-06-item6-sized-bank.md",
        "steps": _SIZED_BANK + [
            (YIELD_SAMPLES, ["build", "@freq_8.json", "@mcnom_6.json", "@mcbind_sized_bank.json",
                             "-o", "@samples-sized-bank.json"]),
        ],
    },
    "sim/solve/mc/samples-sized-bank-negctl-hd0.3.json": {
        "record": "sim/solve/mc/RECORD-2026-11-06-item6-sized-bank.md",
        "steps": _SIZED_BANK + [
            (YIELD_SAMPLES, ["build", "@freq_8.json", "@mcnom_6.json", "@mcbind_sized_bank.json",
                             "--defect", "0.3", "--defect-osc", "osc_hd",
                             "-o", "@samples-sized-bank-negctl.json"]),
        ],
    },
}


# ---------------------------------------------------------------- runner

class _Pipelines:
    """Runs the pinned command steps into one shared temp dir, each distinct step at most once."""

    def __init__(self, tmp):
        self.tmp = tmp
        self.done = set()

    def _resolve(self, tok):
        if tok.startswith("@"):
            return os.path.join(self.tmp, tok[1:])
        if "/" in tok:
            return os.path.join(REPO, tok)
        return tok

    @staticmethod
    def _output_token(argv):
        """The artifact a step writes: `-o OUT` for analyze.py / yield_samples.py, `--json OUT`
        for solve.py grade."""
        for flag in ("-o", "--json"):
            if flag in argv:
                return argv[argv.index(flag) + 1]
        raise AssertionError("step names no output artifact: %r" % (argv,))

    def run(self, steps):
        """Run every step; return the path of the artifact the last step writes."""
        for script, argv in steps:
            key = (script, tuple(argv))
            if key in self.done:
                continue
            cmd = [sys.executable, "-I", os.path.join(REPO, script)] + [self._resolve(a) for a in argv]
            p = subprocess.run(cmd, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
            if p.returncode != 0:
                raise AssertionError("step failed (%d): %s\n%s" % (p.returncode, " ".join(cmd), p.stdout))
            self.done.add(key)
        return self._resolve(self._output_token(steps[-1][1]))


class ReproducePinnedRecords(unittest.TestCase):
    """Every committed output regenerates byte-identically from its pinned input list."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="records-reproduce-")
        cls.pipelines = _Pipelines(cls._tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def _check(self, committed):
        spec = PINNED[committed]
        need = spec.get("min_python")
        if need and sys.version_info[:2] < need:
            self.skipTest(
                "%s is byte-reproducible only on CPython >= %d.%d (running %d.%d): CPython 3.12 "
                "changed sum() of floats to compensated summation (gh-100425), which moves this "
                "record's full-precision mc_pooled_sigma_lnf by 1 ULP. See the note in %s. CI "
                "runs the required version, so this check is never skipped there."
                % ((committed,) + need + sys.version_info[:2] + (spec["record"],)))
        got = self.pipelines.run(spec["steps"])
        want = os.path.join(REPO, committed)
        self.assertTrue(
            filecmp.cmp(got, want, shallow=False),
            "%s is no longer byte-identical to the output of the input list pinned in %s.\n"
            "Nothing committed may be regenerated to make this pass: either the pinned list is "
            "wrong, or a change to the post-processing code altered recorded evidence (#140)."
            % (committed, spec["record"]))

    def test_rows1_4_grade(self):
        self._check("sim/solve/records/2026-11-05-rows1-4.json")

    def test_samples_binding_cells(self):
        self._check("sim/solve/mc/samples-binding-cells.json")

    def test_samples_sized(self):
        self._check("sim/solve/mc/samples-sized.json")

    def test_samples_sized_negative_control(self):
        self._check("sim/solve/mc/samples-sized-negctl-hd0.3.json")

    def test_samples_sized_bank(self):
        self._check("sim/solve/mc/samples-sized-bank.json")

    def test_samples_sized_bank_negative_control(self):
        self._check("sim/solve/mc/samples-sized-bank-negctl-hd0.3.json")


class PinnedListsAreLiteral(unittest.TestCase):
    """The pinned lists are explicit files: a report landing in a reports directory cannot move them."""

    def test_no_glob_in_any_pinned_input(self):
        for committed, spec in PINNED.items():
            for script, argv in spec["steps"]:
                for tok in argv:
                    self.assertNotRegex(tok, r"[*?\[]", "%s: glob in a pinned input: %r"
                                        % (committed, tok))

    def test_every_pinned_input_exists(self):
        for committed, spec in PINNED.items():
            self.assertTrue(os.path.exists(os.path.join(REPO, committed)), committed)
            self.assertTrue(os.path.exists(os.path.join(REPO, spec["record"])), spec["record"])
            for script, argv in spec["steps"]:
                self.assertTrue(os.path.exists(os.path.join(REPO, script)), script)
                for tok in argv:
                    if tok.startswith("@") or "/" not in tok:
                        continue
                    self.assertTrue(os.path.exists(os.path.join(REPO, tok)),
                                    "%s: pinned input is missing: %s" % (committed, tok))

    def test_ci_python_satisfies_every_min_python(self):
        """CI must run an interpreter that can actually execute every pinned check.

        Structural, not advisory: lowering `python-version` in the workflow below the version a
        record reproduces on would otherwise turn a byte-identity gate into a silent skip.
        """
        need = max([s["min_python"] for s in PINNED.values() if "min_python" in s] or [(0, 0)])
        workflow = os.path.join(REPO, ".github", "workflows", "tests.yml")
        with open(workflow) as f:
            found = re.findall(r'python-version:\s*"?([0-9]+)\.([0-9]+)"?', f.read())
        self.assertTrue(found, "no python-version pinned in %s" % workflow)
        for major, minor in found:
            self.assertGreaterEqual(
                (int(major), int(minor)), need,
                "tests.yml pins Python %s.%s, below the %d.%d a pinned record needs (#140)"
                % ((major, minor) + need))

    def test_pinned_list_sizes(self):
        """The counts the record notes quote, so a silently shortened list fails here too."""
        self.assertEqual((len(GRID_5), len(MCNOM_5)), (5, 5))
        self.assertEqual((len(GRID_6), len(MCNOM_6), len(GRID_8)), (6, 6, 8))
        self.assertEqual(len(MCBIND_18), 18)
        self.assertEqual((len(MCSIZED_SUBTH_24), len(MCSIZED_ALL_120)), (24, 120))


if __name__ == "__main__":
    unittest.main()
