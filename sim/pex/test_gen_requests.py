"""Unit tests for the pex testbench derivation (no simulator, no PDK).
Run: python3 -I sim/pex/test_gen_requests.py

The pex comparison (T1 item 7, issue #32) is only evidence if its bench is the #29 sensitivity bench.
These tests hold that: every committed file under sim/pex/osc/ and sim/pex/requests/ must equal what
gen_requests.py derives from sim/sensitivity/, byte for byte, because the dated reports under
sim/pex/records/ record each bench's `netlist_sha256`. An edit to a sensitivity bench therefore fails
here until the pex benches are regenerated under a new dated record, instead of silently leaving the
pex leg running a different circuit.
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_requests as G  # noqa: E402

OSC_DIR = os.path.join(G.HERE, "osc")


def read(path):
    with open(path) as f:
        return f.read()


def circuit_lines(text):
    """The bench's circuit, i.e. everything that is not a comment or a blank line."""
    return [ln for ln in text.splitlines() if ln.strip() and not ln.startswith("*")]


class Committed(unittest.TestCase):
    """The committed bytes are the contract: a difference is a finding, never a file to commit."""

    def test_benches_match_committed(self):
        for osc in G.OSCS:
            with self.subTest(osc=osc):
                self.assertEqual(read(os.path.join(OSC_DIR, "tb_%s.spice" % osc)), G.tb_text(osc))

    def test_relaxed_variants_match_committed(self):
        for osc in G.RELAXED:
            with self.subTest(osc=osc):
                self.assertEqual(read(os.path.join(OSC_DIR, "tb_%s_relaxed.spice" % osc)), G.relaxed_text(osc))

    def test_hd_dut_matches_committed(self):
        self.assertEqual(read(os.path.join(OSC_DIR, "osc_hd_dut.spice")), G.dut_text())

    def test_requests_match_committed(self):
        for osc in G.OSCS:
            with self.subTest(osc=osc):
                committed = read(os.path.join(G.HERE, "requests", "%s.json" % osc))
                self.assertEqual(committed, json.dumps(G.request(osc), indent=2) + "\n")

    def test_no_stray_generated_benches(self):
        """Everything in osc/ is accounted for by the generator, so no hand-kept copy can creep back."""
        expected = {"osc_hd_dut.spice"}
        expected |= {"tb_%s.spice" % o for o in G.OSCS}
        expected |= {"tb_%s_relaxed.spice" % o for o in G.RELAXED}
        self.assertEqual(set(os.listdir(OSC_DIR)), expected)


class Derivation(unittest.TestCase):
    """What the derivation is allowed to change: comments, and for osc_hd the include and pin order."""

    def test_circuit_is_the_sensitivity_circuit(self):
        for osc in G.OSCS:
            if osc == "osc_hd":
                continue  # covered by test_hd_rewrites_include_and_pin_order
            with self.subTest(osc=osc):
                sens = read(os.path.join(G.SENS_OSC, "tb_%s.spice" % osc))
                self.assertEqual(circuit_lines(G.tb_text(osc)), circuit_lines(sens))

    def test_provenance_comment_is_swapped(self):
        for osc in G.OSCS:
            if osc == "osc_hd":
                continue
            with self.subTest(osc=osc):
                body = G.tb_text(osc)
                self.assertIn(G.PEX_PROVENANCE, body)
                self.assertNotIn(G.SENS_PROVENANCE, body)

    def test_hd_rewrites_include_and_pin_order(self):
        sens = read(os.path.join(G.SENS_OSC, "tb_osc_hd.spice"))
        body = G.tb_text("osc_hd")
        # Undoing exactly the two documented edits must give the sensitivity bench back.
        self.assertEqual(body.replace(G.HD_DUT_INCLUDE, G.HD_INCLUDES).replace(G.HD_XDUT_PEX, G.HD_XDUT), sens)
        # klt pex requires a single .include in the bench.
        self.assertEqual(sum(1 for ln in circuit_lines(body) if ln.startswith(".include")), 1)
        # The pin order is reordered, not renamed: the same four nets on the same subcircuit.
        self.assertEqual(sorted(G.HD_XDUT.split()[1:5]), sorted(G.HD_XDUT_PEX.split()[1:5]))
        self.assertEqual(G.HD_XDUT.split()[5], G.HD_XDUT_PEX.split()[5])

    def test_relaxed_is_the_bench_plus_options(self):
        for osc in G.RELAXED:
            with self.subTest(osc=osc):
                base, relaxed = G.tb_text(osc), G.relaxed_text(osc)
                self.assertTrue(relaxed.startswith(base))
                self.assertEqual(circuit_lines(relaxed), circuit_lines(base) + [
                    ".options reltol=0.01 gmin=1e-10 method=gear"])

    def test_missing_pattern_is_an_error(self):
        """A sensitivity bench that no longer carries a pattern fails loudly, it is not passed through.

        tb_text reads a committed path, so point it at a temporary bench that is missing the clause."""
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "tb_osc_nmos.spice"), "w") as f:
                f.write("* a bench whose provenance comment has been reworded\n.include \"x.spice\"\n")
            real, G.SENS_OSC = G.SENS_OSC, d
            try:
                with self.assertRaises(AssertionError):
                    G.tb_text("osc_nmos")
            finally:
                G.SENS_OSC = real

    def test_hd_missing_pattern_is_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            sens = read(os.path.join(G.SENS_OSC, "tb_osc_hd.spice"))
            with open(os.path.join(d, "tb_osc_hd.spice"), "w") as f:
                f.write(sens.replace(G.HD_XDUT, "Xdut en out vdd vss osc_hd_renamed\n"))
            real, G.SENS_OSC = G.SENS_OSC, d
            try:
                with self.assertRaises(AssertionError):
                    G.tb_text("osc_hd")
            finally:
                G.SENS_OSC = real


class Requests(unittest.TestCase):
    def test_request_is_the_grid_request_with_only_the_bench_swapped(self):
        """Same analysis window, measurement, solver options and corner box as #29 - nothing else may drift."""
        for osc in G.OSCS:
            with self.subTest(osc=osc):
                with open(os.path.join(G.SENS, "grid_%s.json" % osc)) as f:
                    grid = json.load(f)
                r = G.request(osc)
                # `../osc/tb_<osc>.spice` is the same string in both, but resolves against
                # sim/sensitivity/requests/ there and sim/pex/requests/ here - that is the swap.
                self.assertEqual(r["netlist"], "../osc/tb_%s.spice" % osc)
                self.assertEqual(r["batch"]["capacity_wait_s"], 600)  # host rule: wait for fleet capacity
                self.assertEqual(dict(r, batch=grid["batch"]), grid,
                                 "the pex request differs from the #29 grid request by more than the batch wait")


if __name__ == "__main__":
    unittest.main()
