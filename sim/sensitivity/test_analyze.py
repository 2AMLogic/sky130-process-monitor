"""Unit tests with synthetic data (no simulator). Run: python3 -I sim/sensitivity/test_analyze.py"""
import io
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

    # ------------------------------------------------------------ gate parameter (issue #170)

    def test_default_gate_is_the_spec_default_and_sigma_quant_default_is_unchanged(self):
        # the module constant must stay one value in one place: 2^10 reference cycles at 10 MHz
        self.assertEqual(A.GATE_S, 2 ** 10 / 10e6)
        self.assertEqual(A.GATE_EXP, 10)
        self.assertEqual(A.COUNTER_MAX, 2 ** 24 - 1)
        # no gate argument, and an explicit default gate, are the same number
        self.assertEqual(A.sigma_quant(1e6), A.sigma_quant(1e6, A.GATE_S))
        self.assertEqual(A.sigma_quant(1e6), A.sigma_quant(1e6, None))

    def test_sigma_quant_halves_when_the_gate_doubles(self):
        # sigma_quant = 1/(f*gate*sqrt(12)): twice the gate is twice the counts is half the sigma.
        # Fails if the gate_s argument is accepted and then ignored.
        self.assertAlmostEqual(A.sigma_quant(1e6, gate_s=2 * A.GATE_S),
                               0.5 * A.sigma_quant(1e6), places=15)
        self.assertAlmostEqual(A.sigma_quant(1e6, gate_s=2 ** 14 / A.REF_HZ),
                               1 / (1e6 * 2 ** 14 / A.REF_HZ * math.sqrt(12)), places=15)
        self.assertAlmostEqual(A.counts(1e6, 2 * A.GATE_S), 204.8, places=9)

    def test_margin_improves_with_a_longer_gate_in_the_quantization_limited_regime(self):
        # A synthetic table whose oscillators are slow enough that quantization, not MC, sets the
        # margin: doubling the gate then doubles the margin. One test that fails if gate_s is ignored.
        slow = {o: c for o, c in COEF_WELL.items()}
        tab = synth(lambda o, p, v, t: linear(slow)(o, p, v, t) - 18.0 + math.log(2e3))
        m_def, _ = A.margin(tab, 1, 1, None)
        m_same, _ = A.margin(tab, 1, 1, None, gate_s=A.GATE_S)
        m_long, _ = A.margin(tab, 1, 1, None, gate_s=2 * A.GATE_S)
        self.assertEqual(m_def, m_same)                      # explicit default == no argument
        self.assertAlmostEqual(m_long / m_def, 2.0, places=9)  # quantization-limited: scales with gate

    def test_margin_accepts_a_per_oscillator_gate(self):
        # dict form: a longer gate on one oscillator only; oscillators absent keep the default.
        tab = synth(lambda o, p, v, t: linear(COEF_WELL)(o, p, v, t) - 18.0 + math.log(2e3))
        one, _ = A.margin(tab, 1, 1, None, gate_s={"osc_subth": 2 * A.GATE_S})
        none, _ = A.margin(tab, 1, 1, None)
        allosc, _ = A.margin(tab, 1, 1, None, gate_s=2 * A.GATE_S)
        self.assertGreater(one, none)       # one oscillator quieter than the default
        self.assertLess(one, allosc)        # but not as quiet as the whole bank at the long gate
        self.assertEqual(A._gate_of({"osc_subth": 1.0}, "osc_hd"), A.GATE_S)
        self.assertEqual(A._gate_of(None, "osc_hd"), A.GATE_S)
        self.assertEqual(A._gate_of(2.0, "osc_hd"), 2.0)

    def test_gate_descriptions_render_the_gate_in_use(self):
        # the default strings are byte-identical to the pre-parameter report text, which
        # records/2026-11-05-mc-margin.md quotes verbatim
        self.assertEqual(A.gate_desc(), "2^10 ref cycles @10 MHz")
        self.assertEqual(A.gate_desc(A.GATE_S), "2^10 ref cycles @10 MHz")
        self.assertEqual(A.gate_phrase(), "the default gate (2^10 @ 10 MHz)")
        self.assertEqual(A.gate_desc(2 ** 14 / A.REF_HZ), "2^14 ref cycles @10 MHz")
        self.assertEqual(A.gate_phrase(2 ** 14 / A.REF_HZ), "the 1.638 ms gate (2^14 @ 10 MHz)")
        self.assertEqual(A.gate_desc(1500 / A.REF_HZ), "1500 ref cycles @10 MHz")  # not a power of two
        self.assertEqual(A.fmt_time(102.4e-6), "102.4 us")

    def test_report_at_the_default_gate_is_byte_identical_to_the_implicit_default(self):
        # AC: the default behaviour does not move. The committed record quotes this output.
        freq = {"rows": [{"osc": o, "process": p, "vdd": v, "temp_c": t,
                          "f_hz": math.exp(linear(COEF_WELL)(o, p, v, t)) * 1e-9}
                         for o in A.OSCS for p in A.PROCESS for v in A.VDD for t in A.TEMP]}
        a, b = io.StringIO(), io.StringIO()
        A.report(freq, None, out=a)
        A.report(freq, None, out=b, gate_s=A.GATE_S)
        self.assertEqual(a.getvalue(), b.getvalue())
        self.assertIn("the default gate (2^10 @ 10 MHz)", a.getvalue())
        self.assertNotIn("# GATE:", a.getvalue())
        # a longer gate names itself and does not claim to be the default
        c = io.StringIO()
        A.report(freq, None, out=c, gate_s=2 ** 14 / A.REF_HZ)
        self.assertIn("# GATE: 2^14 ref cycles @10 MHz", c.getvalue())
        self.assertNotIn("the default gate", c.getvalue())

    def test_counter_limit_is_set_by_the_fastest_cell(self):
        # largest k with f*2^k/f_ref <= 2^24-1; one fast cell binds the whole oscillator
        rows = [{"osc": "osc_hd", "process": "tt", "vdd": 1.8, "temp_c": 27, "f_hz": 1e9},
                {"osc": "osc_hd", "process": "ff", "vdd": 1.8, "temp_c": 27, "f_hz": 1e6},
                {"osc": "osc_subth", "process": "tt", "vdd": 1.8, "temp_c": 27, "f_hz": 1e6},
                {"osc": "osc_wire", "process": "tt", "vdd": 1.8, "temp_c": 27, "f_hz": None}]
        tab = A.table(rows)
        k = A.counter_limit(tab, "osc_hd")
        self.assertEqual(k, int(math.floor(math.log2(A.COUNTER_MAX * A.REF_HZ / 1e9))))
        self.assertLessEqual(A.counts(1e9, 2 ** k / A.REF_HZ), A.COUNTER_MAX)
        self.assertGreater(A.counts(1e9, 2 ** (k + 1) / A.REF_HZ), A.COUNTER_MAX)
        self.assertEqual(A.counter_limit(tab, "osc_subth"), k + 10)   # 1000x slower -> ~9.97 more bits
        self.assertIsNone(A.counter_limit(tab, "osc_wire"))           # no usable cell

    def test_gate_sweep_rows_track_the_gate(self):
        freq = {"rows": [{"osc": o, "process": p, "vdd": v, "temp_c": t,
                          "f_hz": math.exp(linear(COEF_WELL)(o, p, v, t)) * 1e-9}
                         for o in A.OSCS for p in A.PROCESS for v in A.VDD for t in A.TEMP]}
        mc = {"samples": {"%s|%s|%.2f|%d" % (o, p, 1.8, 27): [1e6 * (1 + 0.001 * i) for i in range(5)]
                          for o in A.OSCS for p in A.PROCESS}}
        out = io.StringIO()
        rows = A.gate_sweep(freq, mc, 1.8, 27, osc="osc_subth", kmin=10, kmax=12, out=out)
        self.assertEqual([r["k"] for r in rows], [10, 11, 12])
        self.assertAlmostEqual(rows[0]["gate_s"], A.GATE_S, places=15)
        # counts double per k, sigma_quant halves
        for p in A.PROCESS:
            self.assertAlmostEqual(rows[1]["counts"][p] / rows[0]["counts"][p], 2.0, places=9)
        self.assertAlmostEqual(rows[1]["sigma_quant"] / rows[0]["sigma_quant"], 0.5, places=9)
        self.assertIn("SIMULATED", out.getvalue())
        self.assertIn("ref cycles", out.getvalue())

    def test_gate_sweep_quant_only_drops_the_mc_term(self):
        freq = {"rows": [{"osc": o, "process": p, "vdd": v, "temp_c": t,
                          "f_hz": math.exp(linear(COEF_WELL)(o, p, v, t)) * 1e-9}
                         for o in A.OSCS for p in A.PROCESS for v in A.VDD for t in A.TEMP]}
        mc = {"samples": {"%s|%s|%.2f|%d" % (o, p, 1.8, 27): [1e6 * (1 + 0.05 * i) for i in range(5)]
                          for o in A.OSCS for p in A.PROCESS}}
        with_mc = A.gate_sweep(freq, mc, 1.8, 27, kmin=10, kmax=10, out=io.StringIO())
        no_mc = A.gate_sweep(freq, mc, 1.8, 27, kmin=10, kmax=10, quant_only=True, out=io.StringIO())
        self.assertGreater(no_mc[0]["margin_uniform"][0], with_mc[0]["margin_uniform"][0])
        self.assertAlmostEqual(no_mc[0]["margin_uniform"][0],
                               A.margin(A.table(freq["rows"]), A.VDD.index(1.8), A.TEMP.index(27),
                                        None, False, gate_s=A.GATE_S)[0],
                               places=12)


if __name__ == "__main__":
    unittest.main()
