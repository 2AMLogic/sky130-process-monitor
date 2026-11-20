"""Regression tests for frequency proxies derived from PEX reports and their requests."""
import contextlib
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


if __name__ == "__main__":
    unittest.main()
