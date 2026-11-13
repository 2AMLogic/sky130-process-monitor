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


class TEST(unittest.TestCase):
    """The shared row 2/3/4 estimators themselves (synthetic data, no simulator)."""

    def test_solve_v_recovers_the_true_voltage_and_corner(self):
        tab = synth()
        oscs, t, p0, v0 = list(A.OSCS), 27, "sf", 1.80
        models = {(o, p): S.vmodel(tab, o, p, t, None, S.VGRID) for o in oscs for p in A.PROCESS}
        meas = {o: math.log(tab[(o, p0, v0, t)]) for o in oscs}
        _, v, p = S.solve_v(meas, models, {o: 1.0 for o in oscs}, oscs, S.VGRID)
        self.assertAlmostEqual(v, v0, places=6)
        self.assertEqual(p, p0)

    def test_solve_t_recovers_the_true_temperature(self):
        tab = synth()
        oscs, v0, t0 = list(A.OSCS), 1.80, -40
        mod = {o: [S.tmodel_delta(tab, o, v0, tt) for tt in S.TGRID] for o in oscs}
        d = {o: math.log(tab[(o, "tt", v0, t0)]) - math.log(tab[(o, "tt", 1.8, 27)]) for o in oscs}
        self.assertAlmostEqual(S.TGRID[S.solve_t(d, mod, {o: 1.0 for o in oscs}, oscs, S.TGRID)], t0, places=6)

    def test_classify_is_the_argmin_of_distances(self):
        cen = {"a": [0.0, 0.0], "b": [1.0, 0.0], "c": [0.0, 1.0]}
        x, w = [0.9, 0.1], [1.0, 1.0]
        d = S.distances(cen, x, w)
        self.assertEqual(sorted(d), ["a", "b", "c"])
        self.assertEqual(S.classify(cen, x, w), min(d, key=d.get))
        self.assertEqual(S.classify(cen, x, w), "b")


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

    # ---- issue #136: the yield samples ARE the graded estimators, not a re-typed copy.
    # Both tests re-derive every sample by calling the shared estimator over the shared grid, so a
    # divergent search, residual or grid in either file breaks them. SIGMA is deliberately well above
    # the 1e-4 "clean" case: at 1e-4 every draw collapses onto one grid point and the comparison
    # passes for any grid at least as fine as solve.VGRID, which would make the guard vacuous. Each
    # test therefore also asserts the samples actually spread over several grid points.
    SIGMA = 0.02

    def test_row3_samples_use_the_graded_estimator_and_grid(self):
        import random
        import yield_samples as Y
        tab, mc = self.fake_mc(self.SIGMA)
        got, oscs = Y.row3_samples(tab, mc, 1)
        p0, v0, t0 = Y.CELLS["row3"]
        full = {(o, p): S.vmodel(tab, o, p, t0, None, S.VGRID) for o in oscs for p in A.PROCESS}
        ds, sg, _ = Y.draws(tab, mc, oscs, p0, v0, t0, random.Random("%s|y3|%s" % (1, 0.0)), 0.0)
        want = [None if rd is None else round(S.solve_v(rd, full, sg, oscs, S.VGRID)[1] - v0, 6) for rd in ds]
        self.assertGreater(len(set(got)), 3, "noise too low to distinguish grids; raise SIGMA")
        self.assertEqual(got, want)

    def test_row4_samples_use_the_graded_estimator_and_grid(self):
        import random
        import yield_samples as Y
        tab, mc = self.fake_mc(self.SIGMA)
        got, oscs = Y.row4_samples(tab, mc, mc, 1)
        p0, v0, t0 = Y.CELLS["row4"]
        mod = {o: [S.tmodel_delta(tab, o, v0, tt) for tt in S.TGRID] for o in oscs}
        ds, sg, _ = Y.draws(tab, mc, oscs, p0, v0, t0, random.Random("%s|y4|%s" % (1, 0.0)), 0.0)
        cs, scal, ncal = Y.draws(tab, mc, oscs, p0, 1.8, 27, random.Random("%s|y4cal|%s" % (1, 0.0)), 0.0)
        sd = {o: math.sqrt(sg[o] ** 2 + scal[o] ** 2) for o in oscs}
        want = []
        for k, rd in enumerate(ds):
            cal = cs[k % ncal] if ncal else None
            if rd is None or cal is None:
                want.append(None)
                continue
            d = {o: rd[o] - cal[o] for o in oscs}
            want.append(round(S.TGRID[S.solve_t(d, mod, sd, oscs, S.TGRID)] - t0, 4))
        self.assertGreater(len(set(got)), 3, "noise too low to distinguish grids; raise SIGMA")
        self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
