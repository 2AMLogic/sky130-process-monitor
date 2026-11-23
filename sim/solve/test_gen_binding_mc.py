"""Drift check: the committed sim/solve/mc/requests-sized/ and sim/solve/mc/requests/
sets must equal what `gen_binding_mc.py` generates (byte-for-byte; no missing, extra or
altered files). Recorded yield results cite these request files as inputs (issue #71);
the binding set is checked since issue #183. Generates into a temp dir; never touches
the working tree.
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
COMMITTED_BINDING = os.path.join(HERE, "mc", "requests")


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


class RequestsDriftMixin:
    """The six drift checks shared by every committed request set. A concrete class
    subclasses this plus unittest.TestCase and supplies: tmp_prefix, generate (a
    callable writing the fresh set into a directory), committed_dir, the
    sample_count / sample_count_perturbed bytes for the altered-file control,
    extra_name, and regen_command."""

    tmp_prefix = None
    generate = None
    committed_dir = None
    sample_count = None
    sample_count_perturbed = None
    extra_name = None
    regen_command = None

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix=cls.tmp_prefix)
        cls.fresh_dir = os.path.join(cls.tmp, "fresh")
        cls.generate(cls.fresh_dir)
        cls.fresh = read_dir(cls.fresh_dir)
        cls.committed = read_dir(cls.committed_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_committed_matches_generator(self):
        self.assertEqual(diff(self.committed, self.fresh), [], "regenerate with: " + self.regen_command)

    def test_nonempty(self):
        self.assertGreater(len(self.fresh), 0)

    # --- negative controls: perturbed copies must be detected ---
    def test_detects_altered_file(self):
        c = dict(self.committed)
        k = sorted(c)[0]
        c[k] = c[k].replace(self.sample_count, self.sample_count_perturbed, 1)
        self.assertNotEqual(c[k], self.committed[k])
        self.assertEqual(diff(c, self.fresh), ["content differs: " + k])

    def test_detects_missing_file(self):
        c = dict(self.committed)
        k = sorted(c)[0]
        del c[k]
        self.assertEqual(diff(c, self.fresh), ["missing from committed set: " + k])

    def test_detects_extra_file(self):
        c = dict(self.committed)
        c[self.extra_name] = b"{}\n"
        self.assertEqual(diff(c, self.fresh), ["extra in committed set: " + self.extra_name])

    def test_detects_trailing_newline_difference(self):
        c = dict(self.committed)
        k = sorted(c)[0]
        c[k] = c[k].rstrip(b"\n")
        self.assertEqual(diff(c, self.fresh), ["content differs: " + k])


class SizedRequestsDrift(RequestsDriftMixin, unittest.TestCase):
    tmp_prefix = "sized-gen-"
    generate = staticmethod(G.write_sized)
    committed_dir = COMMITTED
    sample_count = b'"n": 50'
    sample_count_perturbed = b'"n": 51'
    extra_name = "mc_sized_extra.json"
    regen_command = "python3 -I sim/solve/gen_binding_mc.py --sized"


class BindingRequestsDrift(RequestsDriftMixin, unittest.TestCase):
    tmp_prefix = "binding-gen-"
    generate = staticmethod(G.write_all)
    committed_dir = COMMITTED_BINDING
    sample_count = b'"n": 30'
    sample_count_perturbed = b'"n": 31'
    extra_name = "mc_bind_extra.json"
    regen_command = "python3 -I sim/solve/gen_binding_mc.py"


if __name__ == "__main__":
    unittest.main()
