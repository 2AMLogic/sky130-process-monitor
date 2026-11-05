"""Unit tests with synthetic data (no simulator). Run: python3 -I sim/sensitivity/test_analyze.py"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A  # noqa: E402


def synth(model, drop=()):
    """Frequency table from model(osc, process, v, t) -> ln f; drop = cells to make MISSING."""
    rows = []
    for o in A.OSCS:
        for p in A.PROCESS:
            for v in A.VDD:
                for t in A.TEMP:
                    f = None if (o, p, v, t) in drop else math.exp(model(o, p, v, t))
                    rows.append({"osc": o, "process": p, "vdd": v, "temp_c": t, "f_hz": f})
    return A.table(rows)


COEF_WELL = {  # d ln f / d{V(per 0.18 V), T(per 82.5 C), Pn, Pp}: independent directions
    "osc_hd": (0.30, -0.05, 0.10, 0.10),
    "osc_nmos": (0.20, -0.20, 0.30, 0.02),
    "osc_pmos": (0.25, -0.02, 0.02, 0.30),
    "osc_wire": (0.10, 0.10, 0.03, 0.03),
    "osc_subth": (0.60, 0.50, 0.12, 0.15),
}


def linear(coef):
    def m(o, p, v, t):
        c = coef[o]
        pn, pp = A.PCOORD[p]
        return 18.0 + c[0] * (v - 1.8) / A.V_HALF + c[1] * (t - 27) / A.T_HALF + c[2] * pn + c[3] * pp
    return m


class Tests(unittest.TestCase):
    def test_svd_known(self):
        sv, k, rk = A.conditioning([[3, 0], [0, 1]])
        self.assertAlmostEqual(sv[0], 3.0)
        self.assertAlmostEqual(k, 3.0)
        self.assertEqual(rk, 2)

    def test_svd_rotated(self):
        # orthogonal rotation of diag(5, 0.5): same singular values
        c, s = math.cos(0.7), math.sin(0.7)
        a = [[5 * c, -0.5 * s], [5 * s, 0.5 * c]]
        sv, k, _ = A.conditioning(a)
        self.assertAlmostEqual(sv[0], 5.0, places=9)
        self.assertAlmostEqual(sv[1], 0.5, places=9)
        self.assertAlmostEqual(k, 10.0, places=7)

    def test_identical_oscillators_huge_kappa(self):
        coef = dict(COEF_WELL)
        coef["osc_wire"] = coef["osc_nmos"]
        coef["osc_pmos"] = coef["osc_nmos"]
        absm, _, miss = A.matrices(synth(linear(coef)), 1, 1)
        self.assertFalse(miss)
        sv, k, rk = A.conditioning(absm)
        self.assertGreater(k, 1e6)
        self.assertLess(rk, 4)

    def test_well_conditioned_recovers_coefficients(self):
        absm, ratio, _ = A.matrices(synth(linear(COEF_WELL)), 1, 1)
        for row, o in zip(absm, A.OSCS):
            for got, want in zip(row, COEF_WELL[o]):
                self.assertAlmostEqual(got, want, places=9)
        sv, k, rk = A.conditioning(absm)
        self.assertEqual(rk, 4)
        self.assertLess(k, 20)

    def test_ratio_form_drops_a_dimension_when_only_a_common_mode_differs(self):
        # all oscillators share a common mode (same V,T,P sensitivities) plus one private direction
        coef = {o: (0.3, 0.1, 0.1, 0.1) for o in A.OSCS}
        coef["osc_nmos"] = (0.3, 0.1, 0.4, 0.1)
        absm, ratio, _ = A.matrices(synth(linear(coef)), 1, 1)
        _, _, rk_abs = A.conditioning(absm)
        _, _, rk_ratio = A.conditioning(ratio)
        self.assertEqual(rk_abs, 2)    # common mode + the Pn direction
        self.assertEqual(rk_ratio, 1)  # common mode removed: only the Pn direction left

    def test_missing_cell_reported_never_interpolated(self):
        tab = synth(linear(COEF_WELL), drop={("osc_subth", "ss", 1.8, 27)})
        absm, ratio, miss = A.matrices(tab, 1, 1)
        self.assertEqual(miss, ["osc_subth"])
        self.assertIsNone(absm)
        self.assertIsNone(ratio)  # subth row missing, so the 4x4 ratio form is unavailable too
        m, pair = A.margin(tab, 1, 1, None)
        self.assertIsNone(m)

    def test_margin_needs_mc_sigma_for_every_oscillator(self):
        tab = synth(linear(COEF_WELL))
        m, _ = A.margin(tab, 1, 1, {"osc_hd": 0.01})   # others lack MC data: not assumed noiseless
        self.assertIsNone(m)
        m, _ = A.margin(tab, 1, 1, None)               # quantization only is allowed explicitly
        self.assertIsNotNone(m)

    def test_freq_extraction_and_short_run(self):
        times = [1e-9 * k for k in range(1, 30)]  # 1 GHz
        self.assertAlmostEqual(A.freq_from_crossings(times), 1e9, delta=1.0)
        self.assertIsNone(A.freq_from_crossings(times[:8]))   # too few cycles after skipping start-up
        self.assertIsNone(A.freq_from_crossings([]))

    def test_margin_scales_with_noise(self):
        tab = synth(linear(COEF_WELL))
        m0, _ = A.margin(tab, 1, 1, {o: 0.0 for o in A.OSCS})
        m1, _ = A.margin(tab, 1, 1, {o: 0.05 for o in A.OSCS})
        self.assertGreater(m0, m1)
        m2, _ = A.margin(tab, 1, 1, {o: 0.10 for o in A.OSCS})
        self.assertAlmostEqual(m1 / m2, 2.0, delta=0.15)  # sigma-dominated regime: halves when sigma doubles

    def test_quantization_sigma(self):
        # 1 MHz over 102.4 us = 102.4 counts -> 1/(102.4*sqrt(12))
        self.assertAlmostEqual(A.sigma_quant(1e6), 1 / (102.4 * math.sqrt(12)), places=9)


if __name__ == "__main__":
    unittest.main()
