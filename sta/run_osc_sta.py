#!/usr/bin/env python3
"""Corner-matched oscillator-clock STA for the readout counter (issue #89). SIMULATED / static timing only.

    python3 -I sta/run_osc_sta.py            # from the repo root; needs `uvx` and openroad on PATH

Periods come from the #29 frequency surfaces: the committed `sim/sensitivity/records/reports/grid_*.json.gz`
(klt sim envelopes) are re-read with sim/sensitivity/analyze.py `extract` (post-processing only, no simulation).
Writes 15 requests to sta/osc/ (3 liberty corners x 5 oscillators) and runs each with the pinned
`klayout-tools==0.9.1`, then writes the combined envelope sta/readout.osc-corner.sta.report.json.
Append-only: refuses to overwrite an existing report.

Why 15 single-corner requests: `constraints.clocks[].period_ns` is one value for every corner in a request, and
the oscillator period differs per corner. Why all five osc[] ports share one period inside a request: the
osc[i]-to-oscillator assignment is not recorded anywhere in rtl/ or spec/, and the counter is clocked by a mux
of all five, so "oscillator j drives whichever port is selected" is the mapping-independent statement.
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REPORTS = "sim/sensitivity/records/reports"
GRIDS = ["grid_osc_hd", "grid_osc_nmos", "grid_osc_pmos", "grid_osc_wire", "grid_osc_subth",
         "grid_osc_wire_sf_cold", "grid_osc_subth_sf_cold"]
OSCS = ["osc_hd", "osc_nmos", "osc_pmos", "osc_wire", "osc_subth"]
# liberty corner -> nearest #29 grid cell (process, vdd, temp_c). The liberty set has no 125 C / 1.62 / 1.98 V file.
CORNERS = {"ss_100C_1v60": ("ss", 1.62, 125), "tt_025C_1v80": ("tt", 1.80, 27), "ff_n40C_1v95": ("ff", 1.98, -40)}
IO_DELAY_NS = 10.0  # assumption: 10 % of the 100 ns clk_ref period, applied to every input / output port
OUT = "sta/readout.osc-corner.sta.report.json"
KLT = ["uvx", "--from", "klayout-tools==0.9.1", "klt"]


def freq_table():
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "freq.json")
        subprocess.run([sys.executable, "-I", "sim/sensitivity/analyze.py", "extract",
                        *[f"{REPORTS}/{g}.json.gz" for g in GRIDS], "-o", out], check=True, cwd=ROOT)
        return json.load(open(out))["rows"]


def main():
    os.chdir(ROOT)
    if os.path.exists(OUT):
        sys.exit(f"{OUT} exists; records are append-only - write a new file instead")
    rows = freq_table()
    results = []
    for corner, (proc, vdd, tc) in CORNERS.items():
        for osc in OSCS:
            cell = [r for r in rows if r["osc"] == osc and r["process"] == proc and abs(r["vdd"] - vdd) < 1e-9
                    and r["temp_c"] == tc and r["f_hz"]]
            if len(cell) != 1:
                sys.exit(f"expected exactly one oscillating grid cell for {osc} {proc} {vdd} {tc}, got {len(cell)}")
            f_hz = cell[0]["f_hz"]
            period = round(1e9 / f_hz, 4)
            clocks = [{"port": "clk_ref", "period_ns": 100.0}] + \
                     [{"port": f"osc[{i}]", "period_ns": period} for i in range(5)]
            req = {"schema": "klt.sta.request/1", "def": "../../layout/readout/out/readout.def",
                   "pdk": {"cell_library": "sky130_fd_sc_hd", "corners": [corner]},
                   "constraints": {"clocks": clocks, "clock_groups": [[c["port"]] for c in clocks],
                                   "input_delay_ns": IO_DELAY_NS, "output_delay_ns": IO_DELAY_NS}}
            path = f"sta/osc/{corner}.{osc}.sta.json"
            os.makedirs("sta/osc", exist_ok=True)
            json.dump(req, open(path, "w"), indent=2)
            open(path, "a").write("\n")
            p = subprocess.run(KLT + ["sta", "--format", "json", path], capture_output=True, text=True)
            if p.returncode != 0:
                sys.exit(f"klt sta failed for {path}:\n{p.stdout[-800:]}\n{p.stderr[-800:]}")
            env = json.loads(p.stdout)
            c = env["corners"][0]
            results.append({"corner": corner, "oscillator": osc, "request": path,
                            "grid_cell": {"process": proc, "vdd_V": vdd, "temp_C": tc},
                            "f_osc_hz": f_hz, "period_ns": period, "source_n_edges": cell[0]["n_edges"],
                            "setup_slack_ns": c["worst_slack_ns"], "hold_slack_ns": c["worst_hold_slack_ns"],
                            "fmax_mhz": c["fmax_mhz"], "timing_status": c["timing_status"],
                            "constraint_completeness": c["constraint_completeness"]["status"],
                            "setup_violation_count": c["setup_violation_count"],
                            "hold_violation_count": c["hold_violation_count"],
                            "worst_setup_path": c["worst_setup_path"], "worst_hold_path": c["worst_hold_path"]})
            print(corner, osc, period, c["worst_slack_ns"], c["worst_hold_slack_ns"], c["fmax_mhz"],
                  c["constraint_completeness"]["status"], flush=True)
    prov = env["provenance"]
    json.dump({"kind": "SIMULATED", "t1_item": 5, "domain": "digital", "analysis": "static timing (OpenSTA via klt sta)",
               "issue": 89, "io_delay_ns_assumed": IO_DELAY_NS, "clock_mode": env["clock_mode"],
               "geometry_source": env["geometry_source"], "engine": env["engine"], "engine_version": env["engine_version"],
               "klt_version": prov["klt_version"], "klt_git_commit": prov["klt_git_commit"],
               "pdk": prov["pdk"], "frequency_source": REPORTS, "results": results},
              open(OUT, "w"), indent=2)
    open(OUT, "a").write("\n")


main()
