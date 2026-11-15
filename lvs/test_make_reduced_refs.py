"""Drift check: the committed lvs/osc_wire.ref.spice and lvs/osc_subth.ref.spice must equal what
`make_reduced_refs.py` regenerates (byte-for-byte). The script writes into its own directory, so the
test copies its inputs into a temp tree and runs it there; never touches the working tree (issue #177).
Run: python3 -I lvs/test_make_reduced_refs.py"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

INPUTS = ["lvs/make_reduced_refs.py", "layout/gen/osc_subth_divider.json",
          "design/osc_bank/osc_wire.spice", "design/osc_bank/osc_subth.spice"]
OUTS = ["osc_wire.ref.spice", "osc_subth.ref.spice"]


class ReducedRefsDrift(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="reduced-refs-gen-")
        for rel in INPUTS:
            dst = os.path.join(cls.tmp, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(os.path.join(REPO, rel), dst)
        subprocess.run([sys.executable, "-I", os.path.join(cls.tmp, "lvs", "make_reduced_refs.py")],
                       check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_committed_matches_generator(self):
        for n in OUTS:
            with open(os.path.join(self.tmp, "lvs", n), "rb") as f:
                fresh = f.read()
            with open(os.path.join(REPO, "lvs", n), "rb") as f:
                committed = f.read()
            self.assertEqual(
                fresh, committed,
                n + " drifted from make_reduced_refs.py (regenerate with: python3 -I lvs/make_reduced_refs.py)")


if __name__ == "__main__":
    unittest.main()
