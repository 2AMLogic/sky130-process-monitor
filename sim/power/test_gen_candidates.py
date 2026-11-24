#!/usr/bin/env python3
"""Unit tests for the issue #280 iteration bench (no simulator). Run: python3 -I sim/power/test_gen_candidates.py

Two subjects, both load-bearing for the record:
  1. The variant generator is faithful: the base lever of every family regenerates the committed
     design netlist device-for-device (canonical compare), and each lever changes exactly the
     devices it names (capacitor value, resistor length, one FET geometry axis, or the stage count).
  2. The analysis splits power the way the record claims: the explicit-capacitor term is
     N*C*VDD*dV*f, the DC term is the committed idle current, and the residual is what remains;
     gradability of a gap cell follows analyze_power.MIN_EDGES (the #8 rule), never a local number.
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_candidates as G  # noqa: E402
import analyze_iteration as I  # noqa: E402

DESIGN = os.path.join(HERE, "..", "..", "design", "osc_bank")


def canon_family(fam, tag):
    return G.canonical_devices("\n".join(G.make_variant(fam, tag)))


def caps(entries):
    return [e for e in entries if e[0] == "c"]


def resistors(entries):
    return [e for e in entries if e[0] == "r"]


def fets(entries):
    return [e for e in entries if e[0] == "x"]


class Parity(unittest.TestCase):
    def test_base_reproduces_every_design_netlist(self):
        G.assert_parity()  # raises AssertionError naming the family on any drift

    def test_levers_keep_the_device_kinds(self):
        for fam, spec in G.CANDIDATES.items():
            base = canon_family(fam, "base")
            base_kinds = {e[0] for e in base}
            for tag, lever in spec["levers"].items():
                if tag == "base":
                    continue
                var = canon_family(fam, tag)
                self.assertEqual({e[0] for e in var}, base_kinds, "%s_%s" % (fam, tag))
                if "n" not in lever:
                    self.assertEqual(len(base), len(var), "%s_%s changed the device count" % (fam, tag))


class Levers(unittest.TestCase):
    def test_wire_cap_lever_changes_only_cap_values(self):
        base, var = canon_family("wire", "base"), canon_family("wire", "c050")
        self.assertEqual(len(base), len(var))
        self.assertTrue(all("50f" in e[1] for e in caps(var)))
        self.assertTrue(all("100f" in e[1] for e in caps(base)))
        self.assertEqual([r for r in resistors(var)], [r for r in resistors(base)])
        self.assertEqual(sorted(fets(var)), sorted(fets(base)))

    def test_wire_stage_count_lever_changes_stage_count(self):
        base, var = canon_family("wire", "base"), canon_family("wire", "n021")
        # 10 stages gone: 10 x (1 pfet + 1 nfet + 1 R + 1 C)
        self.assertEqual(len(base) - len(var), 40)
        # one lever at a time: the only device not present in the base is the new last-stage
        # R (the removed stages shifted which stage terminates on `out`)
        extra = set(var) - set(base)
        self.assertEqual(len(extra), 1)
        self.assertEqual(list(extra)[0][0], "r")
        self.assertTrue(list(extra)[0][1][-1].endswith("res_generic_m1"))

    def test_nmos_length_lever_changes_only_nfet_geometry(self):
        base, var = canon_family("nmos", "base"), canon_family("nmos", "l20")
        self.assertEqual(len(base), len(var))
        changed = [e for e in var if e not in base]
        # exactly the 30 inverter pull-down nfets moved L=0.5 -> 2.0 (the enable NAND keeps its size)
        self.assertEqual(len(changed), 30)
        self.assertTrue(all(e[1][-1].endswith("nfet_01v8") and dict(e[2])["l"] == 2.0 for e in changed))


class Requests(unittest.TestCase):
    def test_probe_targets_the_binding_cell(self):
        for name, req in G.all_requests().items():
            if not name.startswith("probe_"):
                continue
            osc = name[len("probe_"):-len(".json")]
            p, v, t = G.BINDING[osc]
            self.assertEqual(req["corners"]["units"],
                             [{"process": p, "temperature_c": t, "supply_v": {"vdd": v}}], osc)

    def test_gap_windows_average_over_the_settled_half(self):
        import re
        for name, req in G.gap_requests().items():
            meas = req["measurements"][0]["spice"]
            frm = re.search(r"from=(\S+)", meas).group(1)
            to = re.search(r"to=(\S+)", meas).group(1)
            self.assertEqual(G._half(to), frm, name)
            self.assertEqual(len(req["corners"]["units"]), 1, name)

    def test_candgrid_covers_the_box(self):
        grids = G.grid_requests(["wire_r004w02", "hd_n061"])
        for req in grids.values():
            self.assertEqual(req["corners"]["process"], G.PROCESS)
            self.assertEqual(len(req["corners"]["supply_v"]["vdd"]) * len(req["corners"]["temperature_c"])
                             * len(G.PROCESS), 45)

    def test_probe_deck_is_committed_body_plus_one_options_line(self):
        with open(os.path.join(HERE, "tb", "active_osc_wire.spice")) as f:
            base_lines = f.read().splitlines()
        with open(os.path.join(HERE, "..", "sensitivity", "osc", "tb_osc_wire_probe.spice")) as f:
            sens_probe = f.read().splitlines()
        opt = next(l for l in sens_probe if l.startswith(".options"))
        text = G.probe_deck_text()
        with open(os.path.join(HERE, "tb", "active_osc_wire_probe.spice")) as f:
            self.assertEqual(text, f.read())
        lines = text.splitlines()
        base_non_comment = [l for l in base_lines if not l.startswith("*")]
        probe_non_comment = [l for l in lines if not l.startswith("*")]
        self.assertEqual(len(probe_non_comment), len(base_non_comment) + 1)
        idx = probe_non_comment.index(".options rshunt=1e12")
        self.assertEqual(probe_non_comment[idx - 1], opt)
        self.assertEqual(probe_non_comment[:idx - 1] + probe_non_comment[idx:], base_non_comment)


def probe_report(osc="osc_wire", e_j=2.0e-9, win_s=1.25e-6, i_a=-1.0e-3, n_edges=100,
                 period_ns=9.03, vdd=1.98, proc="ff", t_c=-40):
    times = [(k + 1) * period_ns * 1e-9 for k in range(n_edges)]
    return {"netlist": {"path": "sim/power/tb/active_%s.spice" % osc},
            "corners": [{"process": proc, "supply_v": {"vdd": vdd}, "temperature_c": t_c, "status": "pass",
                         "measurements": [
                             {"name": "e_vdd", "value": e_j, "status": "pass",
                              "energy": {"net": e_j, "from": win_s, "to": 2 * win_s}},
                             {"name": "i_avg", "value": i_a, "status": "pass"},
                             {"name": "t_rise", "value": n_edges, "status": "pass",
                              "crossings": {"times": times}},
                             {"name": "t_s1", "value": n_edges, "status": "pass",
                              "crossings": {"times": [x + 60e-12 for x in times]}},
                             {"name": "t_n1", "value": n_edges, "status": "pass",
                              "crossings": {"times": [x + 69e-12 for x in times]}},
                             {"name": "vhi_n1", "value": 1.99, "status": "pass"},
                             {"name": "vlo_n1", "value": 0.0, "status": "pass"},
                             {"name": "vhi_s1", "value": 1.99, "status": "pass"},
                             {"name": "vlo_s1", "value": 0.0, "status": "pass"}]}],
            "environment": {}}


class AnalyzeDecompose(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.d.name, "probe_osc_wire.json")
        with open(self.path, "w") as f:
            json.dump(probe_report(), f)
        self.idle = os.path.join(self.d.name, "idle.json")
        with open(self.idle, "w") as f:
            json.dump({"rows": [{"kind": "idle", "osc": "osc_wire", "process": "ff", "vdd": 1.98,
                                 "temp_c": -40, "i_a": 5e-9, "unit_status": "pass"}]}, f)

    def tearDown(self):
        self.d.cleanup()

    def test_terms_add_up_and_residual_is_explicit(self):
        r = I.decompose([self.path], self.idle)["probes"][0]
        self.assertAlmostEqual(r["P_supply_uW"], 2.0e-9 / 1.25e-6 * 1e6)  # 1600 uW
        self.assertAlmostEqual(r["P_dc_idle_uW"], 1.98 * 5e-9 * 1e6)      # ~0.01 uW
        f = I.freq_from_crossings([(k + 1) * 9.03e-9 for k in range(100)])
        self.assertAlmostEqual(r["P_explicit_uW"], 31 * 100e-15 * 1.98 * 1.99 * f * 1e6)
        self.assertAlmostEqual(r["P_supply_uW"] - r["P_explicit_uW"] - r["P_dc_idle_uW"],
                               r["P_residual_uW"])
        # measured RC fraction: 69-60 = 9 ps over the period/(2*31)
        self.assertAlmostEqual(r["rc_delay_s"], 9e-12)

    def test_binding_drift_is_refused(self):
        bad = os.path.join(self.d.name, "bad.json")
        with open(bad, "w") as f:
            json.dump({"rows": [{"kind": "active", "osc": "osc_wire", "process": "tt", "vdd": 1.8,
                                 "temp_c": 27, "i_a": 1e-4}]}, f)
        with self.assertRaises(SystemExit):
            I.binding(bad)


class AnalyzeGaps(unittest.TestCase):
    def _gap(self, n_edges, i_a=1e-7):
        times = [(k + 1) * 1e-3 for k in range(n_edges)]
        return {"netlist": {"path": "sim/power/tb/active_osc_subth.spice"},
                "corners": [{"process": "sf", "supply_v": {"vdd": 1.62}, "temperature_c": -40,
                             "status": "pass",
                             "measurements": [{"name": "i_avg", "value": i_a, "status": "pass"},
                                              {"name": "t_rise", "value": n_edges, "status": "pass",
                                               "crossings": {"times": times}}]}],
                "environment": {}}

    def test_gradability_is_the_8_rule(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "g.json")
            for n, gradable in ((I.MIN_EDGES - 1, False), (I.MIN_EDGES, True), (0, False)):
                with open(p, "w") as f:
                    json.dump(self._gap(n), f)
                rows = I.gaps([p])["gaps"]
                self.assertEqual(rows[0]["gradable"], gradable, "n=%d" % n)
                self.assertEqual(rows[0]["n_edges"], n)


# Pinned (explicit, no glob): open PRs add reports to these directories, so a glob would drift.
REC = os.path.join(HERE, "records")
RPT = os.path.join(REC, "reports")
SENS_RPT = os.path.join(HERE, "..", "sensitivity", "records", "reports")
IDLE_TABLE = os.path.join(REC, "2026-11-05-power-table-complete.json")
PROBES = ["probe_osc_wire", "probe_osc_nmos", "probe_osc_pmos", "probe_osc_hd"]
CANDS = ["cand_hd_n021", "cand_hd_n061", "cand_nmos_l10", "cand_nmos_l20", "cand_nmos_l30",
         "cand_nmos_n021", "cand_nmos_wp015", "cand_pmos_l10", "cand_pmos_l20", "cand_pmos_n021",
         "cand_pmos_wn015", "cand_wire_c025", "cand_wire_c050", "cand_wire_n021", "cand_wire_n061",
         "cand_wire_r002", "cand_wire_r002w02", "cand_wire_r004", "cand_wire_r004w02",
         "cand_wire_r005", "cand_wire_w02", "cand_wire_w04"]
GAPS = ["gap_osc_subth_sf_1.62V_-40C", "gap_osc_subth_sf_1.80V_-40C", "gap_osc_subth_sf_1.98V_-40C",
        "gap_osc_subth_ss_1.62V_-40C", "gap_osc_subth_ss_1.80V_-40C",
        "gap_osc_wire_sf_1.62V_-40C_relaxed"]
# order matters: grid_osc_hd_5p is attributed to osc_hd by _osc_of and must come after grid_osc_hd
BASELINE = ["grid_osc_hd", "grid_osc_nmos", "grid_osc_pmos", "grid_osc_subth", "grid_osc_wire",
            "grid_osc_hd_5p"]


def rpt(name):
    return os.path.join(RPT, name + ".json.gz")


def rec(name):
    with open(os.path.join(REC, name)) as f:
        return json.load(f)


class ReproduceCommittedRecords(unittest.TestCase):
    """The committed 2026-11-21 records regenerate from the committed .json.gz raw reports."""

    def test_binding(self):
        got = I.binding(IDLE_TABLE)
        want = rec("2026-11-21-binding.json")
        self.assertEqual(json.loads(json.dumps(got)), want)

    def test_decompose(self):
        got = I.decompose([rpt(n) for n in PROBES], IDLE_TABLE)
        self.assertEqual(json.loads(json.dumps(got)), rec("2026-11-21-decompose.json"))

    def test_screens(self):
        got = I.screens([rpt(n) for n in CANDS])
        self.assertEqual(json.loads(json.dumps(got)), rec("2026-11-21-screens.json"))

    def test_gaps_retained_rows(self):
        got = I.gaps([rpt(n) for n in GAPS])
        want = [g for g in rec("2026-11-21-gaps.json")["gaps"] if g.get("report_retained", True)]
        self.assertEqual(len(want), 6)
        self.assertEqual(json.loads(json.dumps(got["gaps"])), want)

    def test_candgrid(self):
        base = [os.path.join(SENS_RPT, n + ".json.gz") for n in BASELINE]
        for name in ("hd_n061", "nmos_l30", "pmos_l10", "wire_r004w02"):
            got = I.candgrid(rpt("candgrid_" + name), base)
            self.assertEqual(json.loads(json.dumps(got)),
                             rec("2026-11-21-candgrid-%s.json" % name), name)


class IdentityFromNetlistMetadata(unittest.TestCase):
    """Oscillator/candidate identity comes from netlist.path, never from the report's filename."""

    def test_screens_and_decompose_ignore_outer_filename(self):
        import gzip
        import shutil
        with tempfile.TemporaryDirectory() as d:
            c = os.path.join(d, "anything.json.gz")
            shutil.copy(rpt("cand_wire_r004w02"), c)
            self.assertEqual(I.screens([c])["screens"][0]["candidate"], "wire_r004w02")
            pr = os.path.join(d, "renamed.json.gz")
            shutil.copy(rpt("probe_osc_wire"), pr)
            self.assertEqual(I.decompose([pr], IDLE_TABLE)["probes"][0]["osc"], "osc_wire")
            with gzip.open(c, "rt") as f:
                rep = json.load(f)
            self.assertEqual(I._cand_of(rep), "wire_r004w02")

    def test_cand_of_rejects_non_candidate_netlist(self):
        with self.assertRaises(ValueError):
            I._cand_of({"netlist": {"path": "sim/power/tb/active_osc_wire.spice"}})

    def test_skip_edges_is_the_shared_constant(self):
        self.assertIs(I.SKIP_EDGES, I._SENS.SKIP_EDGES)
        self.assertIs(I._load, I._SENS._load)


if __name__ == "__main__":
    unittest.main()
