"""Drift check: the committed lvs/osc_wire.ref.spice and lvs/osc_subth.ref.spice must equal what
`make_reduced_refs.py` regenerates (byte-for-byte). The script writes into its own directory, so the
test copies its inputs into a temp tree and runs it there; never touches the working tree (issue #177).
Also checks the res_high_po width-variant pairing (issue #208): the PDK device name is derived from
the owner file's poly_w_nm, so a matching width emits its variant and an unmatched width fails
without emitting. Run: python3 -I lvs/test_make_reduced_refs.py"""
import json
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


def run_generator_with(poly_w_nm):
    """Copy the inputs into a fresh temp tree, patch poly_w_nm in the owner JSON copy and run the
    generator there. The class fixture runs the generator once at the committed width, so each
    perturbed width gets its own temp tree (never the working tree; issue #177's constraint)."""
    tmp = tempfile.mkdtemp(prefix="reduced-refs-w%d-" % poly_w_nm)
    for rel in INPUTS:
        dst = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(REPO, rel), dst)
    owner = os.path.join(tmp, "layout", "gen", "osc_subth_divider.json")
    with open(owner) as f:
        cfg = json.load(f)
    cfg["poly_w_nm"] = poly_w_nm
    with open(owner, "w") as f:
        json.dump(cfg, f)
    run = subprocess.run([sys.executable, "-I", os.path.join(tmp, "lvs", "make_reduced_refs.py")],
                         capture_output=True, text=True)
    return tmp, run


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

    def test_350nm_emits_0p35_device(self):
        with open(os.path.join(self.tmp, "lvs", "osc_subth.ref.spice")) as f:
            fresh = f.read()
        self.assertIn("XRb0 vdd vbp vss sky130_fd_pr__res_high_po_0p35 L=270 W=0.35", fresh)
        self.assertIn("XRb1 vbp vss vss sky130_fd_pr__res_high_po_0p35 L=1360 W=0.35", fresh)

    def test_690nm_emits_0p69_device(self):
        tmp, run = run_generator_with(690)
        try:
            self.assertEqual(run.returncode, 0, run.stderr)
            with open(os.path.join(tmp, "lvs", "osc_subth.ref.spice")) as f:
                fresh = f.read()
            self.assertIn("sky130_fd_pr__res_high_po_0p69 L=270 W=0.69", fresh)
            self.assertIn("sky130_fd_pr__res_high_po_0p69 L=1360 W=0.69", fresh)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_unmatched_width_fails_without_emitting(self):
        tmp, run = run_generator_with(400)
        try:
            self.assertNotEqual(run.returncode, 0, run.stdout)
            self.assertIn("400", run.stderr)
            for w in (350, 690, 1410, 2850, 5730):
                self.assertIn(str(w), run.stderr)
            self.assertFalse(os.path.exists(os.path.join(tmp, "lvs", "osc_subth.ref.spice")))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
