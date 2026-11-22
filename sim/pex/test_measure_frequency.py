"""Offline tests for the --measure-command callback (sim/pex/measure_frequency.py, issue #282).

No klt, no simulator: the nested `klt sim` runner is patched, so these check the bench/request
derivation and the crossing-time reduction (the shared estimator's own suite is
sim/sensitivity/test_analyze.py).
"""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import measure_frequency as mf  # noqa: E402

SPACING = 10e-9  # 100 MHz


def edges(n, spacing=SPACING, start=1e-8):
    return [start + i * spacing for i in range(n)]


def sim_report(rows):
    """rows: {corner_id: (unit_status, measurement_status, times)} -> a klt sim report body."""
    corners = []
    for cid, (unit, meas, times) in rows.items():
        corners.append({"corner_id": cid, "status": unit,
                        "measurements": [{"name": "t_rise", "value": len(times), "status": meas,
                                          "crossings": {"times": times}}]})
    return {"corners": corners}


class CornerId(unittest.TestCase):
    def test_round_trip(self):
        for p, v, t in [("tt", 1.80, 27), ("ss", 1.62, -40), ("ff", 1.98, 125)]:
            self.assertEqual(mf.parse_corner_id(mf.corner_id(p, v, t)), (p, v, t))
        with self.assertRaises(ValueError):
            mf.parse_corner_id("tt/1.8V/27C-x")


class Bench(unittest.TestCase):
    def test_single_include_repointed(self):
        for osc in ("osc_nmos", "osc_subth"):
            text = mf.bench_text(osc, "/tmp/handed.spice")
            self.assertEqual([l for l in text.splitlines() if l.lstrip().startswith(".include")],
                             ['.include "/tmp/handed.spice"'])
            committed = (HERE / "osc" / ("tb_%s.spice" % osc)).read_text().splitlines()
            self.assertEqual([l for l in text.splitlines() if not l.lstrip().startswith(".include")],
                             [l for l in committed if not l.lstrip().startswith(".include")])

    def test_osc_hd_keeps_extracted_pin_order(self):
        text = mf.bench_text("osc_hd", "/tmp/handed.spice")
        self.assertIn("Xdut out en vss vdd osc_hd\n", text)  # the extracted pin order, unchanged
        self.assertEqual([l for l in text.splitlines() if l.lstrip().startswith(".include")],
                         ['.include "/tmp/handed.spice"'])

    def test_two_includes_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "osc"))
            with open(os.path.join(tmp, "osc", "tb_bad.spice"), "w") as f:
                f.write(".include \"a.spice\"\n.include \"b.spice\"\n")
            with patch.object(mf, "HERE", tmp):
                with self.assertRaises(SystemExit):
                    mf.bench_text("bad", "/tmp/x.spice")


class Request(unittest.TestCase):
    def load_committed(self, osc):
        return json.loads((HERE / "requests" / ("%s.json" % osc)).read_bytes())

    def test_netlist_swapped_only(self):
        r = mf.request_json("osc_nmos", "/tmp/bench.spice", None)
        committed = self.load_committed("osc_nmos")
        self.assertEqual(r["netlist"], "/tmp/bench.spice")
        r["netlist"] = committed["netlist"]
        self.assertEqual(r, committed)

    def test_corner_scoping(self):
        r = mf.request_json("osc_hd", "/tmp/bench.spice", ("tt", 1.8, 27))
        self.assertEqual(r["corners"], {"process": ["tt"], "supply_v": {"vdd": [1.8]}, "temperature_c": [27]})
        self.assertEqual(list(mf.expected_corners(r)), ["tt/1.800V/27C"])


class MeasurementDocument(unittest.TestCase):
    def doc(self, rows, expected=("tt/1.800V/27C",)):
        return mf.measurement_document(sim_report(rows), list(expected))

    def m(self, doc, cid="tt/1.800V/27C"):
        c = doc["corners"][0] if len(doc["corners"]) == 1 else \
            next(c for c in doc["corners"] if c["corner_id"] == cid)
        return c["measurements"][0]

    def test_nine_edges_known_spacing_is_finite(self):
        doc = self.doc({"tt/1.800V/27C": ("pass", "pass", edges(9))})
        m = self.m(doc)
        self.assertEqual(m["value"], 5 / (5 * SPACING))  # 100 MHz over the 5 post-start-up cycles
        self.assertEqual(m["status"], "pass")
        self.assertNotIn("message", m)

    def test_eight_edges_unresolved_with_cause(self):
        doc = self.doc({"tt/1.800V/27C": ("pass", "pass", edges(8))})
        m = self.m(doc)
        self.assertIsNone(m["value"])
        self.assertEqual(m["status"], "error")
        self.assertIn("too few edges: 8", m["message"])

    def test_startup_spacing_cannot_change_result(self):
        irregular = [0.0, 1e-12, 5e-10]  # three start-up edges, dropped by SKIP_EDGES
        doc = self.doc({"tt/1.800V/27C": ("pass", "pass", irregular + edges(9))})
        self.assertEqual(self.m(doc)["value"], 5 / (5 * SPACING))

    def test_solver_error_reported_with_status(self):
        doc = self.doc({"tt/1.800V/27C": ("timestep_too_small", "fail", edges(30))})
        m = self.m(doc)
        self.assertIsNone(m["value"])
        self.assertIn("solver error: unit timestep_too_small", m["message"])

    def test_missing_result_for_absent_corner(self):
        doc = self.doc({})
        m = self.m(doc)
        self.assertIsNone(m["value"])
        self.assertEqual(m["message"], "missing result")

    def test_first_measurement_must_be_t_rise(self):
        rep = sim_report({"tt/1.800V/27C": ("pass", "pass", edges(9))})
        rep["corners"][0]["measurements"][0]["name"] = "other"
        with self.assertRaises(SystemExit):
            mf.measurement_document(rep, ["tt/1.800V/27C"])

    def test_duplicate_corner_refused(self):
        rep = sim_report({"tt/1.800V/27C": ("pass", "pass", edges(9))})
        rep["corners"].append(dict(rep["corners"][0]))
        with self.assertRaises(SystemExit):
            mf.measurement_document(rep, ["tt/1.800V/27C", "tt/1.620V/-40C"])


class Main(unittest.TestCase):
    def run_main(self, argv, report_rows):
        """main() with klt sim patched out; returns (doc, artifacts dir contents)."""
        with tempfile.TemporaryDirectory() as tmp:
            def fake_run_sim(req, out, backend, hosts, wait):
                Path(out).write_text(json.dumps(sim_report(report_rows)))
                return 0, ""
            env = {"KLT_PEX_SIDE": "schematic", "KLT_PEX_ARTIFACTS_DIR": tmp,
                   "KLT_PEX_NETLIST": str(Path(HERE).parent.parent / "design/osc_bank/osc_nmos.spice")}
            out = io.StringIO()
            with patch.object(mf, "run_sim", fake_run_sim), patch.dict(os.environ, env), \
                    contextlib.redirect_stdout(out):
                rc = mf.main(argv + [env["KLT_PEX_NETLIST"]])
            self.assertEqual(rc, 0)
            return json.loads(out.getvalue()), sorted(os.listdir(tmp))

    def test_full_grid_document_and_artifacts(self):
        doc, files = self.run_main(["--osc", "osc_nmos"],
                                   {"%s/%.3fV/%dC" % (p, v, t): ("pass", "pass", edges(9))
                                    for p in ("tt", "ff") for v in (1.8,) for t in (27,)})
        # every corner of the committed request's box is accounted for, resolved or not
        self.assertEqual(len(doc["corners"]), 45)
        self.assertTrue(all(c["measurements"][0]["name"] == "f_hz" for c in doc["corners"]))
        for name in ("tb_osc_nmos_freq.spice", "request-schematic.json", "sim.report.schematic.json",
                     "measurement.schematic.json"):
            self.assertIn(name, files)

    def test_pilot_corner_scope(self):
        doc, _ = self.run_main(["--osc", "osc_hd", "--corner", "tt/1.800V/27C"],
                               {"tt/1.800V/27C": ("pass", "pass", edges(9))})
        self.assertEqual([c["corner_id"] for c in doc["corners"]], ["tt/1.800V/27C"])
        self.assertEqual(doc["corners"][0]["measurements"][0]["value"], 5 / (5 * SPACING))


if __name__ == "__main__":
    unittest.main()
