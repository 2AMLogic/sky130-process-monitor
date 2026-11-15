"""Drift check: the committed sim/sensitivity/requests/ set must equal what
`gen_requests.py` generates (byte-for-byte; no missing, extra or altered files).
The two hand-written probe_*.json are not generator output; they are excluded by
explicit name, so a new unexplained file still fails the check. Recorded evidence
cites these request files as inputs (issue #183). Generates into a temp dir;
never touches the working tree.
Run: python3 -I sim/sensitivity/test_gen_requests.py"""
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_requests as G  # noqa: E402

COMMITTED = os.path.join(HERE, "requests")
# Not generator output (they reference ../osc/tb_osc_wire_probe.spice); excluded by
# explicit name so any *new* unexplained file still fails as an extra.
HAND_WRITTEN = ("probe_wire_sf.json", "probe_wire_val.json")


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


class SensitivityRequestsDrift(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="sens-gen-")
        cls.fresh_dir = os.path.join(cls.tmp, "fresh")
        G.write_requests(cls.fresh_dir)
        cls.fresh = read_dir(cls.fresh_dir)
        cls.committed = read_dir(COMMITTED)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_committed_matches_generator(self):
        self.assertEqual(diff(self.committed, self.fresh),
                         ["extra in committed set: " + n for n in HAND_WRITTEN],
                         "regenerate with: python3 -I sim/sensitivity/gen_requests.py")

    def test_covers_full_generated_set(self):
        # 22 generated files: the 6 import-reachable before issue #183 plus the 16 that
        # were only written by __main__ (curator correction, verified against the committed dir).
        self.assertEqual(len(self.fresh), 22)

    def test_nonempty(self):
        self.assertGreater(len(self.fresh), 0)

    # --- negative controls: perturbed copies must be detected ---
    def test_detects_altered_file(self):
        c = dict(self.committed)
        k = "mc_osc_hd.json"
        c[k] = c[k].replace(b'"n": 50', b'"n": 51', 1)
        self.assertNotEqual(c[k], self.committed[k])
        expected = ["extra in committed set: " + n for n in HAND_WRITTEN] + ["content differs: " + k]
        self.assertEqual(diff(c, self.fresh), expected)

    def test_detects_missing_file(self):
        c = dict(self.committed)
        k = sorted(c)[0]
        del c[k]
        expected = ["missing from committed set: " + k] + ["extra in committed set: " + n for n in HAND_WRITTEN]
        self.assertEqual(diff(c, self.fresh), expected)

    def test_detects_unexplained_new_file(self):
        # A third probe-like name is NOT covered by the allowlist and must fail.
        c = dict(self.committed)
        c["probe_bogus.json"] = b"{}\n"
        expected = ["extra in committed set: probe_bogus.json"] + \
            ["extra in committed set: " + n for n in HAND_WRITTEN]
        self.assertEqual(diff(c, self.fresh), expected)

    def test_detects_trailing_newline_difference(self):
        c = dict(self.committed)
        k = sorted(c)[0]
        c[k] = c[k].rstrip(b"\n")
        expected = ["extra in committed set: " + n for n in HAND_WRITTEN] + ["content differs: " + k]
        self.assertEqual(diff(c, self.fresh), expected)


if __name__ == "__main__":
    unittest.main()
