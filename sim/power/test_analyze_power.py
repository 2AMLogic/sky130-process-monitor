"""Unit tests with synthetic reports (no simulator). Run: python3 -I sim/power/test_analyze_power.py

The subject is the ONE thing the power grader decides on its own data: which active cells are gradable.
That must be the #8 rule and nothing else — a cell the #8 frequency surface records as MISSING must not
have its mean supply current folded into the row-7 "worst oscillator, worst cell" binding figure.
"""
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze_power as P  # noqa: E402

_SENS = P._SENS


def _load_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def crossings(n, period_s=1e-9):
    """n rising-crossing times, evenly spaced (a ring that ran exactly n edges into the window)."""
    return [(k + 1) * period_s for k in range(n)]


def report(cells, kind="active", osc="osc_hd", i_a=1.5e-4, status="pass"):
    """A synthetic `klt sim` report. cells = {(process, vdd, temp_c): n_crossings or None}."""
    corners = []
    for (p, v, t), n in sorted(cells.items(), key=lambda kv: str(kv[0])):
        meas = []
        if kind == "active":
            meas.append({"name": "i_avg", "value": i_a, "unit": "A"})
            if n is not None:
                meas.append({"name": "t_rise", "value": n, "unit": "s", "crossings": {"times": crossings(n)}})
        else:
            meas.append({"name": "i_vdd", "value": i_a, "unit": "A"})
        corners.append({"process": p, "supply_v": {"vdd": v}, "temperature_c": t,
                        "status": status, "measurements": meas})
    return {"netlist": {"path": "sim/power/tb/%s_%s.spice" % (kind, osc), "scope": "repo"},
            "corners": corners, "environment": {}}


def extract_one(module=None, **kw):
    """Run extract() over one synthetic report; returns {(osc, process, vdd, temp_c): i_a}."""
    rep = report(**kw)
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "r.json")
        with open(path, "w") as f:
            json.dump(rep, f)
        tab = (module or P).extract([path])
    return {(r["osc"], r["process"], r["vdd"], r["temp_c"]): r["i_a"] for r in tab["rows"]}


class GradabilityBoundary(unittest.TestCase):
    def test_eight_crossings_is_missing_nine_is_graded(self):
        # The off-by-one this file exists to pin down: 8 crossings is 4 full cycles after the 3 dropped
        # start-up edges, which #8 reports as MISSING. It must not be graded for power.
        got = extract_one(cells={("tt", 1.80, 27): 8, ("ff", 1.80, 27): 9})
        self.assertIsNone(got[("osc_hd", "tt", 1.8, 27)])
        self.assertEqual(got[("osc_hd", "ff", 1.8, 27)], 1.5e-4)

    def test_boundary_matches_freq_from_crossings_exactly(self):
        # The invariant, not the number: gradable here iff #8 yields a frequency there.
        cells = {("tt", 1.80, t): n for t, n in zip(range(0, 15), range(0, 15))}
        got = extract_one(cells=cells)
        for t, n in zip(range(0, 15), range(0, 15)):
            sens_has_f = _SENS.freq_from_crossings(crossings(n)) is not None
            power_graded = got[("osc_hd", "tt", 1.8, t)] is not None
            self.assertEqual(power_graded, sens_has_f,
                             "n=%d: power graded=%s but #8 frequency=%s" % (n, power_graded, sens_has_f))

    def test_min_edges_is_derived_not_restated(self):
        self.assertEqual(P.MIN_EDGES, _SENS.SKIP_EDGES + _SENS.MIN_CYCLES + 1)
        self.assertIs(P._SENS.SKIP_EDGES, _SENS.SKIP_EDGES)

    def test_min_edges_follows_a_change_to_the_sensitivity_constants(self):
        """The grader must TRACK sim/sensitivity/analyze.py, not agree with it by coincidence.

        Load an unmodified copy of analyze_power.py beside a sensitivity module whose SKIP_EDGES and
        MIN_CYCLES are 4 and 7, and the boundary must move to 12. A grader holding its own literal would
        keep admitting cells at 8 (or at 9) and fail here — which is what this repo had before issue #173.
        """
        real_sens = os.path.abspath(os.path.join(HERE, "..", "sensitivity", "analyze.py"))
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "sensitivity"))
            os.makedirs(os.path.join(d, "power"))
            with open(os.path.join(d, "sensitivity", "analyze.py"), "w") as f:
                f.write("import importlib.util\n"
                        "_s = importlib.util.spec_from_file_location('real_sens', %r)\n"
                        "_m = importlib.util.module_from_spec(_s)\n"
                        "_s.loader.exec_module(_m)\n"
                        "OSCS, _load, _remote = _m.OSCS, _m._load, _m._remote\n"
                        "SKIP_EDGES, MIN_CYCLES = 4, 7\n" % real_sens)
            shutil.copyfile(os.path.join(HERE, "analyze_power.py"),
                            os.path.join(d, "power", "analyze_power.py"))
            moved = _load_by_path("analyze_power_moved", os.path.join(d, "power", "analyze_power.py"))
        self.assertEqual(moved.MIN_EDGES, 12)
        got = extract_one(cells={("tt", 1.80, 27): 11, ("ff", 1.80, 27): 12}, module=moved)
        self.assertIsNone(got[("osc_hd", "tt", 1.8, 27)])
        self.assertEqual(got[("osc_hd", "ff", 1.8, 27)], 1.5e-4)

    def test_pex_grader_uses_the_same_threshold(self):
        pex = _load_by_path("grade_pex", os.path.join(HERE, "..", "pex", "grade_pex.py"))
        self.assertEqual(pex.MIN_EDGES, P.MIN_EDGES)
        self.assertEqual(pex.MIN_EDGES, 9)  # the committed value; the records are graded at 9


class NeverGradedWithoutData(unittest.TestCase):
    def test_enough_crossings_but_no_mean_current(self):
        got = extract_one(cells={("tt", 1.80, 27): 20}, i_a=None)
        self.assertIsNone(got[("osc_hd", "tt", 1.8, 27)])

    def test_failed_unit_is_never_graded(self):
        got = extract_one(cells={("tt", 1.80, 27): 20}, status="fail")
        self.assertIsNone(got[("osc_hd", "tt", 1.8, 27)])

    def test_no_t_rise_measurement_at_all(self):
        got = extract_one(cells={("tt", 1.80, 27): None})
        self.assertIsNone(got[("osc_hd", "tt", 1.8, 27)])

    def test_idle_does_not_apply_the_oscillation_rule(self):
        # Idle is an `op` analysis with the ring gated off: there are no crossings and none are required.
        got = extract_one(cells={("tt", 1.80, 27): None}, kind="idle", i_a=-3e-7)
        self.assertEqual(got[("osc_hd", "tt", 1.8, 27)], 3e-7)


class GradeDoesNotMoveTheRecordedVerdict(unittest.TestCase):
    def test_committed_row7_grade_reproduces_from_the_committed_table(self):
        # grade() reads i_a only, so the threshold correction cannot re-grade the 2026-11-05 record.
        rec = os.path.join(HERE, "records", "2026-11-05-power-table-complete.json")
        want = os.path.join(HERE, "records", "2026-11-05-power-grade-complete.json")
        with open(rec) as f:
            got = P.grade(json.load(f))
        with open(want) as f:
            self.assertEqual(json.loads(json.dumps(got, sort_keys=True)), json.load(f))


if __name__ == "__main__":
    unittest.main()
