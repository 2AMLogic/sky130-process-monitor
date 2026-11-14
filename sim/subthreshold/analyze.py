#!/usr/bin/env python3
"""Reduce the klt sim reports under runs/ into check tables (stdout) and, with --append,
dated SIMULATED records appended to measurements/subthreshold_records.jsonl (append-only).
Pure post-processing: runs no simulation."""
import datetime, glob, gzip, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PDK_JSON = os.path.join(REPO, "sim", "pdk.json")   # sim/pdk.json owns the open_pdks pin; do not restate it here
with open(PDK_JSON) as fh: OPEN_PDKS = json.load(fh)["open_pdks"]
def load(pat):
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, pat))):
        out.append((os.path.relpath(f, REPO), json.load(gzip.open(f))))
    return out
def val(c, n):
    for m in c["measurements"]:
        if m["name"] == n:
            return m.get("value")
PROC = ["tt", "ff", "ss", "sf", "fs"]; TS = [-40, 27, 125]

grid = load("runs/osc_grid.report.json.gz")[0]
longs = load("runs/long_shards/*.gz")
fasts = load("runs/fast_shards/*.gz")
mc = load("runs/mc_shards/*.gz")
mc125 = load("runs/mc125_fast_shards/*.gz")
mccold = load("runs/mc_cold_long_shards/*.gz")
ctl = load("runs/osc_mc_control0.report.json.gz")[0]
probe = load("runs/probe.report.json.gz")[0]
env = grid[1]["environment"]

def cid(c):
    p, v, t = c["corner_id"].split("/")[:3]
    return p, float(v[:-1]), int(t[:-1])

# --- 1. oscillator grid: 80 us window, then 400 us re-run of the cells that did not resolve
F = {}; WIN = {}
for c in grid[1]["corners"]:
    F[cid(c)] = val(c, "f_osc_hz"); WIN[cid(c)] = 80
for _, d in longs:
    for c in d["corners"]:
        k = cid(c)
        if F.get(k) is None and val(c, "f_osc_hz") is not None:
            F[k] = val(c, "f_osc_hz"); WIN[k] = 400
STEP = {k: "2n/80u" for k in F}
for _, d in longs:
    for c in d["corners"]:
        if WIN.get(cid(c)) == 400: STEP[cid(c)] = "5n/400u"
for _, d in fasts:       # fine-step re-run supersedes the 2 ns-step value (2 ns step under-resolves periods < ~100 ns)
    for c in d["corners"]:
        k = cid(c); F[k] = val(c, "f_osc_hz"); WIN[k] = 3; STEP[k] = "0.2n/3u"
unres = sorted(k for k, v in F.items() if v is None)
print("== grid: %d/45 cells resolved; unresolved (no 11 rising edges within 400 us, f < ~27.5 kHz or not oscillating):" % (45 - len(unres)))
for k in unres: print("   ", k)
print("== f_osc [kHz] (window us)")
for p in PROC:
    for v in (1.62, 1.8, 1.98):
        row = []
        for t in TS:
            f = F.get((p, v, t)); row.append("%9s(%s)" % (("%.1f" % (f / 1e3)) if f else "none", STEP[(p, v, t)]))
        print("  %s %.2fV  %s" % (p, v, "  ".join(row)))
# monotonic in T
print("== check 1: f_osc increasing with T at each (corner, V) [resolved pairs only]")
bad = []; nchk = 0
for p in PROC:
    for v in (1.62, 1.8, 1.98):
        s = [(t, F[(p, v, t)]) for t in TS if F.get((p, v, t))]
        for (t0, f0), (t1, f1) in zip(s, s[1:]):
            nchk += 1
            if f1 <= f0: bad.append((p, v, t0, t1, f0, f1))
print("   pairs checked %d, violations %d  -> %s" % (nchk, len(bad), "PASS" if not bad else "FAIL"), bad)
# T and V sensitivity summary (tt)
for v in (1.62, 1.8, 1.98):
    f27, f125 = F.get(("tt", v, 27)), F.get(("tt", v, 125))
    print("   tt %.2fV f(125)/f(27) = %.2f" % (v, f125 / f27))
print("   tt 27C f(1.98)/f(1.62) = %.2f" % (F[("tt", 1.98, 27)] / F[("tt", 1.62, 27)]))

# --- 2. device probe
P = {}
for c in probe[1]["corners"]:
    P[cid(c)[0::2]] = {m["name"]: m.get("value") for m in c["measurements"]}
devs = sorted({n.split("_", 1)[1] for n in P[("tt", 27)] if n.startswith("s_")})
print("== device probe: |Vds|=0.9 V, Vdd=1.8 V; Id in A (abs), slope in mV/dec between |Vgs| 0.15 and 0.30 V")
def I(p, t, vg, d): return abs(P[(p, t)]["i%03d_%s" % (round(vg * 1000), d)])
osc_devs = ["n_w042", "n_w084", "p_w042", "p_w084", "l_w042"]
print("   (device, corner): Ioff(Vgs=0) @ -40/27/125 C ; S @ -40/27/125 C")
for d in osc_devs:
    for p in PROC:
        print("   %-7s %s Ioff %s  S %s" % (d, p,
              " ".join("%.3e" % I(p, t, 0.0, d) for t in TS),
              " ".join("%.1f" % P[(p, t)]["s_" + d] for t in TS)))
print("== check 2: Ioff and Id(0.30V) increasing with T (all devices, corners)")
bad = []; n = 0
for d in devs:
    for p in PROC:
        for vg in (0.0, 0.30):
            xs = [I(p, t, vg, d) for t in TS]; n += 1
            if not (xs[0] < xs[1] < xs[2]): bad.append((d, p, vg, xs))
print("   series checked %d, violations %d -> %s" % (n, len(bad), "PASS" if not bad else "FAIL"), bad[:5])
print("== check 3: slope S (|Vgs| 0.15->0.30 V) rises with T; S(125)/S(-40) vs ideal T ratio %.2f (accept 1.2..2.2). Series with Id(0.15 V) < 1.1e-13 A (10x the ~1.09e-14 A flat floor seen in the probe) at any T excluded (floor)" % (398.15 / 233.15))
bad = []; n = 0; excl = []; ratios = {}
for d in osc_devs:
    for p in PROC:
        if min(I(p, t, 0.15, d) for t in TS) < 1.1e-13: excl.append((d, p)); continue
        s = [P[(p, t)]["s_" + d] for t in TS]; n += 1; r = s[2] / s[0]; ratios[(d, p)] = r
        if not (s[0] < s[1] < s[2] and 1.2 <= r <= 2.2): bad.append((d, p, [round(x, 1) for x in s], round(r, 2)))
print("   series %d, violations %d, excluded %d -> %s" % (n, len(bad), len(excl), "PASS" if not bad else "FAIL"))
for b in bad: print("     ", b)
print("   excluded:", excl)
print("   ratio range: %.2f..%.2f" % (min(ratios.values()), max(ratios.values())))
print("   S [mV/dec] at |Vgs| 0.05->0.15 (deep) -40/27/125 C, tt:", {d: [round(P[("tt", t)]["s05_" + d], 1) for t in TS] for d in osc_devs})
print("   S [mV/dec] at |Vgs| 0.15->0.30, tt:", {d: [round(P[("tt", t)]["s_" + d], 1) for t in TS] for d in osc_devs})
print("== check 4: W-bin continuity: Id/W step between adjacent probe widths (0.01 um apart) at tt, 27C; FAIL if > 25%")
clusters = {"0.42": ["042", "043", "044"], "0.84": ["082", "083", "084", "085", "086"]}
bad = []
for kind in "npl":
    for cl, ws in clusters.items():
        ws = [w for w in ws if "%s_w%s" % (kind, w) in devs]
        for vg in (0.0, 0.15, 0.30):
            for a, b in zip(ws, ws[1:]):
                ia = I("tt", 27, vg, "%s_w%s" % (kind, a)) / int(a); ib = I("tt", 27, vg, "%s_w%s" % (kind, b)) / int(b)
                step = abs(ib / ia - 1)
                if step > 0.25: bad.append((kind, cl, vg, a, b, round(step, 3)))
print("   violations %d -> %s" % (len(bad), "PASS" if not bad else "FAIL"), bad)
print("   Id/W ratio between the two clusters, Vgs=0, tt 27C (W 0.84-0.86 vs 0.42-0.44 at the same L):")
for kind in "npl":
    if "%s_w082" % kind in devs:
        r = (I("tt", 27, 0.0, "%s_w084" % kind) / 0.84) / (I("tt", 27, 0.0, "%s_w042" % kind) / 0.42)
        print("     %s: (Ioff/W)[0.84] / (Ioff/W)[0.42] = %.2f" % (kind, r))
# --- 4. oscillator vs device-implied
print("== check 5: oscillator f(T) vs header device Id(T). Header = pfet_lvt L=0.5 W=0.42, |Vsg| = Vdd*1500/1800 = 0.30 V at 1.8 V")
for p in PROC:
    fr = F.get((p, 1.8, 125)) / F.get((p, 1.8, 27)); ir = I(p, 125, 0.30, "l_w042") / I(p, 27, 0.30, "l_w042")
    print("   %s f(125)/f(27) = %.2f   Id_lvt(125)/Id_lvt(27) = %.2f   ratio of ratios %.2f" % (p, fr, ir, fr / ir))
# --- 5. Monte Carlo
print("== Monte Carlo (mc_mm_switch scale 1), tt 1.80 V")
import statistics as st
samples = {}
MCSTEP = {27: "2n/80u"}
for _, d in mc:
    for c in d["corners"]:
        if cid(c)[2] == 27: samples.setdefault(27, []).append(val(c, "f_osc_hz"))
for t, grp, lab in ((125, mc125, "0.2n/3u"), (-40, mccold, "5n/400u")):
    for _, d in grp:
        for c in d["corners"]:
            samples.setdefault(t, []).append(val(c, "f_osc_hz")); MCSTEP[t] = lab
for t in TS:
    if t not in samples: continue
    xs = [x for x in samples[t] if x]; n_all = len(samples[t])
    nom = F.get(("tt", 1.8, t))
    if len(xs) > 1:
        print("   %4dC [%s]: N=%d, oscillating %d, mean %.1f kHz, sigma %.1f kHz (%.1f%%), min %.1f max %.1f, nominal(no mismatch) %s kHz" % (
            t, MCSTEP.get(t), n_all, len(xs), st.mean(xs) / 1e3, st.stdev(xs) / 1e3, 100 * st.stdev(xs) / st.mean(xs), min(xs) / 1e3, max(xs) / 1e3, nom and "%.1f" % (nom / 1e3)))
    else:
        print("   %4dC: N=%d, oscillating %d" % (t, n_all, len(xs)))
cf = [val(c, "f_osc_hz") for c in ctl[1]["corners"]]
print("   control (mismatch_scale 0, N=5): %s -> %s" % (cf, "identical = PASS" if len(set(cf)) == 1 else "FAIL"))

if "--append" in sys.argv:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    base = {"date_utc": now, "kind": "SIMULATED", "ngspice": env.get("engine_version"),
            "models_lib_sha256": env.get("models_lib_sha256"), "open_pdks_pin": OPEN_PDKS,
            "netlist": "design/osc_bank/osc_subth.spice"}
    out = os.path.join(REPO, "measurements", "subthreshold_records.jsonl")
    with open(out, "a") as fo:
        for (p, v, t), f in sorted(F.items()):
            r = dict(base, record="osc_grid", corner=p, vdd_V=v, temp_C=t, f_osc_hz=f,
                     no_complete_measurement_in_window=(f is None), tran_step_window=STEP[(p, v, t)],
                     testbench="sim/subthreshold/osc_subth_tb.spice", request="sim/subthreshold/osc_grid.request.json",
                     report=grid[0])
            fo.write(json.dumps(r) + "\n")
        for (p, t), m in sorted(P.items()):
            r = dict(base, record="device_probe", corner=p, vdd_V=1.8, temp_C=t, vds_V=0.9, values=m,
                     testbench="sim/subthreshold/probe_tb.spice", request="sim/subthreshold/probe.request.json", report=probe[0])
            fo.write(json.dumps(r) + "\n")
        for t, xs in sorted(samples.items()):
            r = dict(base, record="mc_mismatch", corner="tt", vdd_V=1.8, temp_C=t, n=len(xs), f_osc_hz_samples=xs, tran_step_window=MCSTEP.get(t),
                     monte_carlo={"seed": 20261105, "vary": "mismatch", "mismatch_scale": 1},
                     testbench="sim/subthreshold/osc_subth_tb.spice", request="sim/subthreshold/osc_mc.request.json")
            fo.write(json.dumps(r) + "\n")
    print("appended records to", out)

# --- 6. issue #44 follow-ups: >= 2 ms cold-cell re-run, gmin/abstol probe sweep, 5 MHz step audit
cold = load("runs/osc_grid_cold_2ms.report.json.gz")[0]
edges = load("runs/osc_grid_cold_2ms_edges.report.json.gz")[0]
env2 = cold[1]["environment"]
E = {cid(c): {m["name"]: m.get("value") for m in c["measurements"]} for c in edges[1]["corners"]}
print("== cold-cell re-run (5n/2m; ngspice %s): f = 8/(t_b - t_a), rising edges 3 and 11 of v(out)=0.9 V" % env2.get("engine_version"))
COLD = {}
for c in cold[1]["corners"]:
    k = cid(c); m = {x["name"]: x.get("value") for x in c["measurements"]}; COLD[k] = m
    print("   %s %.2fV %4dC  t_a %s  t_b %s  f %s" % (k[0], k[1], k[2], m["t_a"], m["t_b"], m["f_osc_hz"] and "%.1f Hz" % m["f_osc_hz"]))
vk = ("sf", 1.8, 27); prev = F[vk]; new = COLD[vk]["f_osc_hz"]
print("   validation sf 1.80 V/27 C: 5n/400u (first run, ngspice 46) %.1f Hz vs 5n/2m (ngspice 47) %.1f Hz -> %.2f %% apart (tolerance 1 %%)" % (prev, new, 100 * abs(new / prev - 1)))
print("== cold cells without f_osc in 2 ms: first rising edges and output swing (window 100 us..2 ms)")
for k, m in sorted(E.items()):
    per = (m["t_e2"] - m["t_e1"]) if m["t_e1"] and m["t_e2"] else None
    print("   %s %.2fV %4dC  edge1 %s  edge2 %s  spacing-based f ~ %s  v(out) %.3g..%.3g V" % (
        k[0], k[1], k[2], m["t_e1"], m["t_e2"], per and "%.0f Hz" % (1 / per), m["v_min"], m["v_max"]))
print("== leakage-floor probe: Id at Vgs=0 [A], |Vds| 0.9 V, per solver setting")
SWEEP = (("gmin1e-17", "probe_gmin1e-17"), ("gmin1e-18", "probe_gmin1e-18"), ("gmin1e-15_abstol1e-18", "probe_gmin1e-15_abstol1e-18"))
PV = {"gmin1e-15": P}
for tag, fn in SWEEP:
    r = load("runs/%s.report.json.gz" % fn)[0]
    PV[tag] = {cid(c)[0::2]: {m["name"]: m.get("value") for m in c["measurements"]} for c in r[1]["corners"]}
for key in (("ss", -40), ("sf", -40), ("tt", 27)):
    for d in ("n_w042", "p_w042", "l_w042"):
        print("   %s %4dC %-6s %s" % (key[0], key[1], d, "  ".join("%s: %.4e" % (g, abs(PV[g][key]["i000_" + d])) for g in PV)))
fl = [abs(PV["gmin1e-18"][k]["i000_" + d]) for k in PV["gmin1e-18"] for d in devs if k[1] == -40 and k[0] in ("ss", "sf", "fs")]
print("   cold-corner Vgs=0 floor at gmin 1e-18: min %.4e max %.4e (gmin 1e-15: ~1.09e-14); gmin*Vds at 1e-15 = %.2e" % (min(fl), max(fl), 1e-15 * 0.9))
print("   header pfet_lvt Id(|Vsg| 0.30 V, tt 27 C) per setting: %s" % "  ".join("%s: %.5e" % (g, abs(PV[g][("tt", 27)]["i300_l_w042"])) for g in PV))
print("== 5 MHz audit: first-grid cells still at 2n step with f > 4.9 MHz:",
      [(k, round(v / 1e3, 1)) for k, v in sorted(F.items()) if v and v > 4.9e6 and STEP[k] == "2n/80u"])

if "--append-44" in sys.argv:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    base = {"date_utc": now, "kind": "SIMULATED", "ngspice": env2.get("engine_version"),
            "models_lib_sha256": env2.get("models_lib_sha256"), "open_pdks_pin": OPEN_PDKS,
            "netlist": "design/osc_bank/osc_subth.spice", "testbench": "sim/subthreshold/osc_subth_tb.spice"}
    out = os.path.join(REPO, "measurements", "subthreshold_records.jsonl")
    with open(out, "a") as fo:
        for (p, v, t), m in sorted(COLD.items()):
            r = dict(base, record="osc_grid_cold_2ms", corner=p, vdd_V=v, temp_C=t, f_osc_hz=m["f_osc_hz"], t_a_s=m["t_a"], t_b_s=m["t_b"],
                     no_complete_measurement_in_window=(m["f_osc_hz"] is None), tran_step_window="5n/2m",
                     request="sim/subthreshold/osc_grid_cold_2ms.request.json", report=cold[0])
            fo.write(json.dumps(r) + "\n")
        for (p, v, t), m in sorted(E.items()):
            r = dict(base, record="osc_cold_edges", corner=p, vdd_V=v, temp_C=t, values=m, tran_step_window="5n/2m",
                     request="sim/subthreshold/osc_grid_cold_2ms_edges.request.json", report=edges[0])
            fo.write(json.dumps(r) + "\n")
        for tag, fn in SWEEP:
            for (p, t), m in sorted(PV[tag].items()):
                r = dict(base, record="device_probe_solver_sweep", corner=p, vdd_V=1.8, temp_C=t, vds_V=0.9, solver=tag, values=m,
                         testbench="sim/subthreshold/probe_tb.spice", request="sim/subthreshold/%s.request.json" % fn,
                         report="sim/subthreshold/runs/%s.report.json.gz" % fn)
                fo.write(json.dumps(r) + "\n")
        print("appended issue-44 records to", out)
