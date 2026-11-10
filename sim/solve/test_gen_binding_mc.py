"""Drift check: the committed sim/solve/mc/requests-sized/ set must equal what
`gen_binding_mc.py --sized` generates (byte-for-byte; no missing, extra or altered files).
Recorded yield results cite these request files as inputs (issue #71).
Generates into a temp dir; never touches the working tree.
Run: python3 -I sim/solve/test_gen_binding_mc.py"""
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_binding_mc as G  # noqa: E402

COMMITTED = os.path.join(HERE, "mc", "requests-sized")


def read_dir(d):
    out = {}
    for n in sorted(os.listdir(d)):
        with open(os.path.join(d, n), "rb") as f:
            out[n] = f.read()
    return out


def diff(committed, fresh):
    """Human-readable list of drift between two {name: bytes} maps; empty if identical."""
    msgs = ["missing from committed set: " + n for n in sorted(fresh.keys() - committed.keys())]
    msgs += ["extra in committed set: " + n for n in sorted(committed.keys() - fresh.keys())]
    msgs += ["content differs: " + n for n in sorted(committed.keys() & fresh.keys()) if committed[n] != fresh[n]]
    return msgs


class SizedRequestsDrift(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="sized-gen-")
        cls.fresh_dir = os.path.join(cls.tmp, "fresh")
        G.write_sized(cls.fresh_dir)
        cls.fresh = read_dir(cls.fresh_dir)
        cls.committed = read_dir(COMMITTED)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_committed_matches_generator(self):
        self.assertEqual(diff(self.committed, self.fresh), [], "regenerate with: python3 -I sim/solve/gen_binding_mc.py --sized")

    def test_nonempty(self):
        self.assertGreater(len(self.fresh), 0)

    # --- negative controls: perturbed copies must be detected ---
    def test_detects_altered_file(self):
        c = dict(self.committed)
        k = sorted(c)[0]
        c[k] = c[k].replace(b'"n": 50', b'"n": 51', 1)
        self.assertNotEqual(c[k], self.committed[k])
        self.assertEqual(diff(c, self.fresh), ["content differs: " + k])

    def test_detects_missing_file(self):
        c = dict(self.committed)
        k = sorted(c)[0]
        del c[k]
        self.assertEqual(diff(c, self.fresh), ["missing from committed set: " + k])

    def test_detects_extra_file(self):
        c = dict(self.committed)
        c["mc_sized_extra.json"] = b"{}\n"
        self.assertEqual(diff(c, self.fresh), ["extra in committed set: mc_sized_extra.json"])

    def test_detects_trailing_newline_difference(self):
        c = dict(self.committed)
        k = sorted(c)[0]
        c[k] = c[k].rstrip(b"\n")
        self.assertEqual(diff(c, self.fresh), ["content differs: " + k])


if __name__ == "__main__":
    unittest.main()
