"""Regression tests for frequency proxies derived from PEX reports and their requests."""
import contextlib
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import grade_pex as grade  # noqa: E402

HD = HERE / "records/2026-11-10-osc_hd.pex.report.json"
SUBTH = HERE / "records/2026-11-20-osc_subth-dev2493.pex.report.json"

# the corner box's single source is sim/corner_box.json (issue #191: no literal restatement)
_BOX = json.loads((HERE.parent / "corner_box.json").read_bytes())
PROCS, VDDS, TEMPS = tuple(_BOX["process"]), tuple(_BOX["vdd"]), tuple(_BOX["temp_c"])
CELLS = ["%s/%.3fV/%dC" % (p, v, t) for p in PROCS for v in VDDS for t in TEMPS]
BASE_F = {"osc_hd": 600e6, "osc_nmos": 400e6, "osc_pmos": 300e6, "osc_wire": 200e6, "osc_subth": 5e6}
EXT_F = {"osc_hd": 0.90, "osc_nmos": 0.80, "osc_pmos": 0.85, "osc_wire": 0.95, "osc_subth": 0.70}


def cell_f(osc, i, ext=False):
    """A deterministic, distinct frequency per (osc, cell); ext scales per oscillator so the
    row-2 ratio coordinates move by ln(EXT_F[osc]/EXT_F[osc_hd]), not by a cancelling constant."""
    return BASE_F[osc] * (1.0 + 0.001 * i) * (EXT_F[osc] if ext else 1.0)


def freq_report(path, osc, cells, error_message="unresolved"):
    """Write one synthetic --measure-command pex report; cells: {corner_id: (schematic, extracted)}."""
    delta = []
    for cid, (s, e) in cells.items():
        row = {"spec_row": "f_hz", "corner_id": cid, "schematic_value": s, "extracted_value": e,
               "schematic_status": "pass" if s is not None else "error",
               "extracted_status": "pass" if e is not None else "error",
               "status": "pass" if s is not None and e is not None else "error"}
        if s is None or e is None:
            row["error"] = {"stage": "execute", "message": error_message}
        delta.append(row)
    doc = {"schema_version": 1, "status": "pass",
           "netlist": {"path": "sim/pex/extracted/%s.spice" % osc, "scope": "repo", "sha256": "sha256:" + "e" * 64},
           "reference_netlist": {"path": "design/osc_bank/%s.spice" % osc, "scope": "repo",
                                 "sha256": "sha256:" + "r" * 64},
           "measurement": {"mode": "command",
                           "command": ["python3", "-I", "sim/pex/measure_frequency.py", "--osc", osc],
                           "timeout_s": 60, "sides": None},
           "delta": delta,
           "provenance": {"klt_version": "test", "input": {"content_hash": "sha256:" + "0" * 64}, "pdk": {}}}
    Path(path).write_text(json.dumps(doc))
    return Path(path)


def mc_table(path):
    samples = {"%s|tt|1.80|27" % o: [BASE_F[o], BASE_F[o] * 1.001, BASE_F[o] * 0.999] for o in BASE_F}
    Path(path).write_text(json.dumps({"kind": "SIMULATED", "samples": samples, "environment": []}))
    return Path(path)


class GradePex(unittest.TestCase):
    def grade_rows(self, hd, subth):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            out = Path(tmp) / "grades.json"
            grade.main(out, [str(hd), str(subth)])
            return json.loads(out.read_bytes())["row1_extracted_side"]

    def test_each_proxy_uses_its_own_request(self):
        rows = self.grade_rows(HD, SUBTH)
        self.assertEqual(rows["osc_hd"]["window_s"], 300e-9)
        self.assertEqual(rows["osc_hd"]["f_proxy_hz_min_max"], [83 / 300e-9, 260 / 300e-9])
        self.assertEqual(rows["osc_subth"]["window_s"], 2e-3)
        self.assertEqual(rows["osc_subth"]["f_proxy_hz_min_max"], [0, 77523 / 2e-3])

    def test_stale_request_preserves_edge_grades(self):
        report = json.loads(SUBTH.read_bytes())
        report["testbenches"][0]["request_sha256"] = "sha256:" + "0" * 64
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "subth.report.json"
            path.write_text(json.dumps(report))
            rows = self.grade_rows(HD, path)
        row = rows["osc_subth"]
        self.assertIsNone(row["window_s"])
        self.assertIsNone(row["f_proxy_hz_min_max"])
        self.assertEqual(row["cells_with_extracted_value"], 45)
        self.assertEqual(len(row["cells_below_min_edges"]), 5)
        self.assertEqual(rows["osc_hd"]["window_s"], 300e-9)

    def test_missing_request_and_transient_arguments(self):
        bench = {"request": {"scope": "repo", "path": "request.json"}}
        with tempfile.TemporaryDirectory() as tmp, patch.object(grade, "REPO_ROOT", Path(tmp)):
            self.assertIsNone(grade.verified_window_s(bench))
            for args, expected in [("20p 2u 1u 10p", 1e-6), ("20p unknown", None), ("10p 0", None)]:
                with self.subTest(args=args):
                    raw = json.dumps({"analysis": {"kind": "tran", "args": args}}).encode()
                    (Path(tmp) / "request.json").write_bytes(raw)
                    bench["request_sha256"] = "sha256:" + hashlib.sha256(raw).hexdigest()
                    self.assertEqual(grade.verified_window_s(bench), expected)


class GradePexFreq(unittest.TestCase):
    """The measured-frequency path: pairing guards, unresolved accounting and the solve replay."""

    def reports(self, tmp, ext_nulls=(), sch_nulls=(), dup=None):
        paths = []
        for osc in BASE_F:
            cells = {}
            for i, cid in enumerate(CELLS):
                s, e = cell_f(osc, i), cell_f(osc, i, ext=True)
                if cid in sch_nulls:
                    s = None
                if cid in ext_nulls:
                    e = None
                cells[cid] = (s, e)
            paths.append(freq_report(Path(tmp) / ("freq-%s.pex.report.json" % osc), osc, cells))
        return paths

    def run_freq(self, tmp, paths, draws=20):
        mc = mc_table(Path(tmp) / "mc.json")
        out = Path(tmp) / "compare.json"
        with contextlib.redirect_stdout(io.StringIO()):
            grade.main_freq(mc, out, [str(p) for p in paths], draws)
        return json.loads(out.read_bytes()), out

    def test_all_cells_paired_and_graded(self):
        with tempfile.TemporaryDirectory() as tmp:
            res, out = self.run_freq(tmp, self.reports(tmp))
            self.assertEqual(res["kind"], "SIMULATED")
            for osc in BASE_F:
                legs = res["oscillators"][osc]["legs"]
                self.assertEqual((legs["schematic"]["resolved"], legs["schematic"]["unresolved"]), (45, 0))
                self.assertEqual((legs["extracted"]["resolved"], legs["extracted"]["unresolved"]), (45, 0))
            for leg in ("schematic", "extracted"):
                tab = json.loads((out.parent / ("compare-leg-%s.json" % leg)).read_bytes())
                self.assertEqual(len(tab["rows"]), 225)
                self.assertTrue(all(r["f_hz"] for r in tab["rows"]))
                self.assertTrue((out.parent / ("compare-rows234-%s.json" % leg)).exists())
            # every oscillator's ratio coordinate moves by exactly ln(EXT_F[osc]/EXT_F[osc_hd]) - 1
            for osc, d in res["row2_coordinate_shift_pct"].items():
                want = 100 * (EXT_F[osc] / EXT_F["osc_hd"] - 1)
                self.assertEqual(d["cells"], 45)
                self.assertAlmostEqual(d["min"], want, places=6)
                self.assertAlmostEqual(d["max"], want, places=6)

    def test_null_leg_cell_accounted_not_paired(self):
        cold = "tt/1.800V/27C"
        with tempfile.TemporaryDirectory() as tmp:
            res, out = self.run_freq(tmp, self.reports(tmp, ext_nulls=(cold,), sch_nulls=(cold,)))
            legs = res["oscillators"]["osc_hd"]["legs"]
            self.assertEqual(legs["schematic"]["unresolved"], 1)
            self.assertEqual(legs["extracted"]["unresolved"], 1)
            self.assertEqual(legs["schematic"]["causes"][cold], "unresolved")
            for leg in ("schematic", "extracted"):
                tab = json.loads((out.parent / ("compare-leg-%s.json" % leg)).read_bytes())
                self.assertEqual(len([r for r in tab["rows"] if r["osc"] == "osc_hd"]), 44)
            # no shift at the cold cell for any oscillator: the leg is missing there
            for d in res["row2_coordinate_shift_pct"].values():
                self.assertEqual(d["cells"], 44)
                self.assertNotIn(cold.replace("1.800V", "1.80V"), d["per_cell_pct"])
            # and the solver sees it: one missing cell on both legs
            self.assertEqual(len(res["solve_replay"]["schematic"]["row1"]["missing_cells"]), 5)

    def test_missing_leg_reported_not_dropped(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self.reports(tmp)
            freq_report(paths[0], "osc_hd", {cid: (cell_f("osc_hd", i), None) for i, cid in enumerate(CELLS)})
            res, _ = self.run_freq(tmp, paths)
            legs = res["oscillators"]["osc_hd"]["legs"]
            self.assertEqual((legs["extracted"]["resolved"], legs["extracted"]["unresolved"]), (0, 45))
            self.assertEqual(res["row2_coordinate_shift_pct"]["osc_nmos"]["cells"], 0)
            self.assertEqual(len(res["solve_replay"]["extracted"]["row1"]["missing_cells"]), 45)

    def test_duplicate_corner_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self.reports(tmp)
            d = json.loads(paths[0].read_bytes())
            d["delta"].append(d["delta"][0])
            paths[0].write_text(json.dumps(d))
            with self.assertRaises(SystemExit):
                self.run_freq(tmp, paths)

    def test_oscillator_missing_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self.reports(tmp)
            with self.assertRaises(SystemExit):
                self.run_freq(tmp, paths[:4])

    def test_nested_report_crosscheck(self):
        import measure_frequency as mf
        with tempfile.TemporaryDirectory() as tmp:
            paths = self.reports(tmp)
            hd = paths[0]
            # nested leg reports beside the pex report; the delta values are then rewritten to the
            # frequencies the shared estimator rebuilds from those crossing times (the callback's
            # own contract: the delta value IS freq_from_crossings(times) of the nested report)
            for leg in ("schematic", "extracted"):
                corners, vals = [], {}
                for i, cid in enumerate(CELLS):
                    f = cell_f("osc_hd", i, ext=(leg == "extracted"))
                    times = [1e-8 + k / f for k in range(12)]
                    vals[cid] = mf._SENS.freq_from_crossings(times)
                    corners.append({"corner_id": cid, "status": "pass",
                                    "measurements": [{"name": "t_rise", "value": 12, "status": "pass",
                                                      "crossings": {"times": times}}]})
                nested = str(hd).replace(".pex.report.json", "") + "-%s.sim.report.json.gz" % leg
                with gzip.open(nested, "wt") as g:
                    json.dump({"corners": corners}, g)
                d = json.loads(hd.read_bytes())
                for row in d["delta"]:
                    row["%s_value" % ("schematic" if leg == "schematic" else "extracted")] = vals[row["corner_id"]]
                hd.write_text(json.dumps(d))
            # delta values equal to the rebuilt frequencies pass and cross-check
            res, _ = self.run_freq(tmp, [hd] + paths[1:])
            self.assertEqual(res["oscillators"]["osc_hd"]["legs"]["schematic"]["resolved"], 45)
            self.assertIn("runner_pdk", json.dumps(res))  # the nested env (worker PDK stamp) is recorded
            # a delta value that disagrees with the committed crossing times is refused
            d = json.loads(hd.read_bytes())
            d["delta"][0]["schematic_value"] *= 1.01
            hd.write_text(json.dumps(d))
            with self.assertRaises(SystemExit):
                self.run_freq(tmp, [hd] + paths[1:])


if __name__ == "__main__":
    unittest.main()
