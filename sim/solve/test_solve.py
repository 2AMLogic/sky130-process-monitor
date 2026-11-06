"""Deterministic negative controls for solve.py (synthetic data, no simulator).
Run: python3 -I sim/solve/test_solve.py"""
import math
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S  # noqa: E402
A = S.A

COEF = {"osc_hd": (0.30, -0.05, 0.10, 0.10), "osc_nmos": (0.20, -0.20, 0.30, 0.02),
        "osc_pmos": (0.25, -0.02, 0.02, 0.30), "osc_wire": (0.10, 0.10, 0.03, 0.03),
        "osc_subth": (0.60, 0.50, 0.12, 0.15)}


def model(o, p, v, t):
    cv, ct, cn, cp = COEF[o]
    pn, pp = A.PCOORD[p]
    return 18.0 + cv * (v - 1.8) / 0.18 + ct * (t - 27) / 82.5 + cn * pn + cp * pp


def synth(drop=()):
    rows = [{"osc": o, "process": p, "vdd": v, "temp_c": t,
             "f_hz": None if (o, p, v, t) in drop else math.exp(model(o, p, v, t))}
            for o in A.OSCS for p in A.PROCESS for v in A.VDD for t in A.TEMP]
    return A.table(rows)


def mc(sig):
    return {o: sig for o in A.OSCS}


class T(unittest.TestCase):
    def test_row1_complete_passes_missing_fails(self):
        self.assertEqual(S.row1(synth())["verdict_target"], "PASS")
        r = S.row1(synth(drop={("osc_wire", "ss", 1.62, -40)}))
        self.assertEqual(r["verdict_target"], "FAIL")
        self.assertEqual(len(r["target_bank_5"]["missing_cells"]), 1)
        self.assertEqual(r["verdict_fallback"], "PASS")  # wire is not in the fallback bank

    def test_row2_known_corner_recovered_and_perturbed_fails(self):
        good = S.row2(synth(), mc(1e-4), 200, 1)
        self.assertEqual(good["target_5_corner"]["verdict"], "PASS")
        bad = S.row2(synth(), mc(0.5), 200, 1)   # noise far above the corner spacing
        self.assertEqual(bad["target_5_corner"]["verdict"], "FAIL")

    def test_row3_recovers_known_voltage(self):
        r = S.row3(synth(), mc(1e-4), 100, 1)
        self.assertLess(r["worst_p99_abs_err_v"], 0.02)
        r = S.row3(synth(), mc(0.3), 100, 1)
        self.assertGreater(r["worst_p99_abs_err_v"], 0.05)

    def test_row4_recovers_known_temperature(self):
        r = S.row4(synth(), mc(1e-4), 100, 1)
        self.assertLess(r["worst_p99_abs_err_c"], 2.0)
        r = S.row4(synth(), mc(0.3), 100, 1)
        self.assertGreater(r["worst_p99_abs_err_c"], 10.0)

    def test_missing_cell_reduces_oscillator_set_not_imputed(self):
        r = S.row4(synth(drop={("osc_nmos", "tt", 1.8, -40)}), mc(1e-4), 50, 1)
        self.assertIn("osc_nmos", r["oscillators_excluded"])

    def test_grade_vs_bounds(self):
        self.assertEqual(S.grade_vs(0.015, "row3_V")["target"], "PASS")
        self.assertEqual(S.grade_vs(0.015, "row3_V")["stretch"], "FAIL")
        self.assertEqual(S.grade_vs(None, "row4_T")["target"], "NOT GRADED")


class TY(unittest.TestCase):
    """yield_samples.py: synthetic MC at the binding cells; no simulator."""

    @staticmethod
    def fake_mc(sig, seed=3):
        import random
        rng = random.Random(seed)
        tab = synth()
        smp = {}
        for (o, p, v, t), f in tab.items():
            smp["%s|%s|%.2f|%d" % (o, p, v, t)] = [f * math.exp(rng.gauss(0, sig)) for _ in range(20)]
        return tab, {"samples": smp}

    def test_low_noise_in_limits_and_defect_control_degrades(self):
        import yield_samples as Y
        tab, mc = self.fake_mc(1e-4)
        doc = Y.build(tab, mc, mc, 1, defect=0.5)
        by = {m["name"]: m for m in doc["measurements"]}
        self.assertEqual(len(by["row3_dV"]["samples"]), 20)
        self.assertTrue(all(abs(x) < 0.02 for x in by["row3_dV"]["samples"]))
        self.assertTrue(all(abs(x) < 5 for x in by["row4_dT"]["samples"]))
        self.assertTrue(all(x > 0 for x in by["row2_margin_tt"]["samples"]))
        # the seeded defect moves the row 3 estimate out of its limit
        self.assertTrue(any(abs(x) > 0.02 for x in by["row3_dV"]["negative_control"]["samples"]))

    def test_high_noise_fails_limits_and_missing_draw_is_null_not_imputed(self):
        import yield_samples as Y
        tab, mc = self.fake_mc(0.3)
        doc = Y.build(tab, mc, mc, 1)
        by = {m["name"]: m for m in doc["measurements"]}
        self.assertTrue(any(abs(x) > 0.02 for x in by["row3_dV"]["samples"]))
        mc["samples"]["osc_hd|tt|1.62|-40"][2] = None
        r3, _ = Y.row3_samples(tab, mc, 1)
        self.assertIsNone(r3[2])


if __name__ == "__main__":
    unittest.main()
