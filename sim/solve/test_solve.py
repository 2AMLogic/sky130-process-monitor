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

    # ---- issue #288: cell eligibility is the analyzer's per-cell sigma, not a raw slot count.
    def _keep_two(self, mc, key):
        """Leave a cell its first two draws and null the rest: 20 slots, 2 usable (#288 repro)."""
        mc["samples"][key] = mc["samples"][key][:2] + [None] * 18

    def test_two_usable_draws_exclude_the_cell_not_the_row(self):
        # 20 slots with only 2 usable draws passed the raw slot-count check, then
        # crashed the weight arithmetic with a TypeError (squaring/dividing by a
        # missing sigma). Such a cell simply has no per-cell estimate, so the
        # oscillator drops out of that row's set and the row still builds.
        import yield_samples as Y
        tab, mc = self.fake_mc(1e-4)
        self._keep_two(mc, "osc_nmos|tt|1.62|-40")
        r3, o3 = Y.row3_samples(tab, mc, 1)
        self.assertIsNotNone(r3)
        self.assertNotIn("osc_nmos", o3)
        self._keep_two(mc, "osc_nmos|ff|1.62|27")
        r4, o4 = Y.row4_samples(tab, mc, mc, 1)
        self.assertIsNotNone(r4)
        self.assertNotIn("osc_nmos", o4)
        tab2, mc2 = self.fake_mc(1e-4)
        self._keep_two(mc2, "osc_nmos|ff|1.80|27")   # the row 4 calibration cell
        r4c, o4c = Y.row4_samples(tab2, mc2, mc2, 1)
        self.assertIsNotNone(r4c)
        self.assertNotIn("osc_nmos", o4c)
        for p in A.PROCESS:
            self._keep_two(mc, "osc_nmos|%s|1.98|27" % p)
        r2, o2 = Y.row2_samples(tab, mc, 1)
        self.assertIsNotNone(r2)
        self.assertNotIn("osc_nmos", o2)

    def test_build_survives_the_baseline_having_only_two_usable_draws(self):
        # The exact #288 report: osc_hd keeps 2 of 20 draws and rows 2, 3 and 4
        # all raised TypeError. The build must now complete: rows 3/4 drop
        # osc_hd, and row 2, whose baseline is gone, reports no measurement.
        import yield_samples as Y
        tab, mc = self.fake_mc(1e-4)
        for key in ("osc_hd|tt|1.98|27", "osc_hd|tt|1.62|-40", "osc_hd|ff|1.80|27"):
            self._keep_two(mc, key)
        doc = Y.build(tab, mc, mc, 1, defect=0.5)
        self.assertEqual([m["name"] for m in doc["measurements"]], ["row3_dV", "row4_dT"])
        for m in doc["measurements"]:
            with self.subTest(row=m["spec_row"]):
                self.assertEqual(len(m["samples"]), 20)
                self.assertNotIn(None, m["samples"])
                self.assertNotIn("negative_control", m)
        remaining = [o for o in A.OSCS if o != "osc_hd"]
        self.assertEqual(doc["cells"]["row3"]["oscillators"], remaining)
        self.assertEqual(doc["cells"]["row4"]["oscillators"], remaining)
        self.assertEqual(doc["cells"]["row2"]["oscillators"], [])

    def test_row2_controls_require_the_configured_defect_oscillator(self):
        from unittest.mock import patch
        import yield_samples as Y
        tab, mc = self.fake_mc(1e-4)
        self._keep_two(mc, "osc_nmos|tt|1.98|27")
        with patch.object(Y, "DEFECT_OSC", "osc_nmos"):
            doc = Y.build(tab, mc, mc, 1)
        margins = [m for m in doc["measurements"] if m["spec_row"] == "2"]
        self.assertEqual([m["name"] for m in margins], ["row2_margin_%s" % p for p in A.PROCESS])
        for m in margins:
            self.assertNotIn("negative_control", m)
        for m in doc["measurements"]:
            if m["spec_row"] in ("3", "4"):
                self.assertIn("osc_nmos", m["negative_control"]["description"])

    def test_one_eligible_oscillator_leaves_every_row_unused(self):
        import yield_samples as Y
        tab, mc = self.fake_mc(1e-4)
        for o in A.OSCS:
            if o != A.BASELINE:
                for cell in ("tt|1.98|27", "tt|1.62|-40", "ff|1.80|27"):
                    self._keep_two(mc, "%s|%s" % (o, cell))
        doc = Y.build(tab, mc, mc, 1)
        self.assertEqual(doc["measurements"], [])
        for row in ("row2", "row3", "row4"):
            with self.subTest(row=row):
                self.assertEqual(doc["cells"][row]["oscillators"], [])

    def test_zero_spread_cell_with_three_draws_is_eligible(self):
        # A zero mismatch sigma is a real estimate, not a missing one: the cell
        # stays weightable, and its 17 missing draws stay null at their indices.
        import yield_samples as Y
        tab, mc = self.fake_mc(1e-4)
        key = "osc_nmos|tt|1.62|-40"
        mc["samples"][key] = [mc["samples"][key][0]] * 3 + [None] * 17
        r3, o3 = Y.row3_samples(tab, mc, 1)
        self.assertIn("osc_nmos", o3)
        self.assertEqual(len(r3), 20)
        self.assertTrue(all(r3[k] is not None for k in range(3)))
        self.assertTrue(all(r3[k] is None for k in range(3, 20)))

    def test_missing_draw_in_eligible_cell_stays_null_rows_2_and_4(self):
        # Draw indices are preserved: a null draw among otherwise usable ones
        # yields a null sample at that index (measurement or calibration side),
        # never an imputed reading. Row 3 is covered above; rows 2 and 4 here.
        import yield_samples as Y
        tab, mc = self.fake_mc(1e-4)
        mc["samples"]["osc_nmos|ff|1.62|27"][2] = None      # row 4 measurement draw
        r4, _ = Y.row4_samples(tab, mc, mc, 1)
        self.assertIsNone(r4[2])
        mc["samples"]["osc_nmos|ff|1.80|27"][5] = None      # row 4 calibration draw
        r4, _ = Y.row4_samples(tab, mc, mc, 1)
        self.assertIsNone(r4[5])
        for p in A.PROCESS:
            mc["samples"]["osc_nmos|%s|1.98|27" % p][7] = None   # one row 2 draw
        r2, _ = Y.row2_samples(tab, mc, 1)
        for p in A.PROCESS:
            self.assertIsNone(r2[p][7])

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

    # ---- issue #317 (spec/decisions/0005): the row-4 seeded defect is injected on the measurement
    # draw only; the calibration read stays nominal (post-calibration drift). Before 0005 the same
    # defect was passed to both draws() calls, so it subtracted out exactly in d = rd - cal and the
    # control certified noise reshuffling, not estimator sensitivity. Every assertion below that goes
    # through row4_samples failed on that code: the list was the nominal all-zero one at every defect.
    # The calibrated() loop is the issue's measurement method (both RNG streams held fixed); it spells
    # the injection out itself, so it documents the sensitivity and row4_samples carries the regression.
    def test_row4_negative_control_moves_with_the_defect(self):
        import random
        import yield_samples as Y
        tab, mc = self.fake_mc(1e-4)
        p0, v0, t0 = Y.CELLS["row4"]
        oscs = list(A.OSCS)
        mod = {o: [S.tmodel_delta(tab, o, v0, tt) for tt in S.TGRID] for o in oscs}

        def calibrated(defect):
            # row4_samples' grading loop with both RNG streams held fixed (identically seeded per
            # arm, the issue's measurement method): the deltas differ only through the defect.
            ds, sg, _ = Y.draws(tab, mc, oscs, p0, v0, t0, random.Random("y4ctl"), defect)
            cs, scal, ncal = Y.draws(tab, mc, oscs, p0, 1.8, 27, random.Random("y4calctl"), 0.0)
            sd = {o: math.sqrt(sg[o] ** 2 + scal[o] ** 2) for o in oscs}
            out = []
            for k, rd in enumerate(ds):
                cal = cs[k % ncal] if ncal else None
                if rd is None or cal is None:
                    out.append(None)
                    continue
                d = {o: rd[o] - cal[o] for o in oscs}
                out.append(round(S.TGRID[S.solve_t(d, mod, sd, oscs, S.TGRID)] - t0, 4))
            return out

        nom, ctl, gross = calibrated(0.0), calibrated(Y.DEFECT), calibrated(0.5)
        self.assertNotEqual(nom, ctl)
        shift = [abs(c - n) for n, c in zip(nom, ctl)]
        self.assertTrue(all(x >= 0.5 for x in shift), shift)   # every draw moves >= one TGRID step
        self.assertTrue(all(abs(x) > 5 for x in gross))        # a gross defect fails the +-5 C limit
        fn_nom, _ = Y.row4_samples(tab, mc, mc, 1)             # and through row4_samples itself
        fn_ctl, _ = Y.row4_samples(tab, mc, mc, 1, Y.DEFECT)
        fn_gross, _ = Y.row4_samples(tab, mc, mc, 1, 0.5)
        self.assertNotEqual(fn_nom, fn_ctl)
        self.assertTrue(all(x is not None and abs(x) >= 0.5 for x in
                            (c - n for n, c in zip(fn_nom, fn_ctl))), (fn_nom, fn_ctl))
        self.assertTrue(all(x is not None and abs(x) > 5 for x in fn_gross), fn_gross)


if __name__ == "__main__":
    unittest.main()
