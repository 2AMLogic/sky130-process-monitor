"""cocotb tests for rtl/readout (testbench name: verification/readout/test_readout.py, Icarus).

Oscillators are modelled as ideal clocks; the reference clock is 10 MHz. Every figure
printed here is RTL simulation (Icarus), not silicon.

Count tolerance: the gate window is 2^k reference cycles. The window crosses into the
oscillator domain through a 2-flop synchroniser at each end, so the oscillator sees the
window with an edge-phase uncertainty of up to +-1 osc edge per gate edge. Expected
count = f_osc * 2^k * T_ref, accepted within +-2 (two gate edges x +-1).

READOUT_BREAK=1 adds an offset to every expected count: the negative control (must fail).

Spec section 6 (conversion time): `conversion_time_surfaces` drives the five oscillators at
periods taken from the committed frequency surfaces (not stand-ins) at the nominal cell and
the slowest-osc_subth cell, reads the bank at three gate settings, and writes a committed
machine-readable record (verification/readout/conversion-time.json; the SDF-annotated leg
writes conversion-time-sdf.json) grading each full read against the spec bounds. Reads that
time out are recorded with the gate setting and the observed stimulus.
"""
import json
import math
import os

import cocotb
from cocotb.clock import Clock
from cocotb.simtime import convert, get_sim_time
from cocotb.triggers import RisingEdge, Timer, ValueChange

REF_PS = 100_000  # 10 MHz reference clock
TOL = 2
BREAK = 5 if os.environ.get("READOUT_BREAK") == "1" else 0

CTRL, STATUS, COUNT, CAL = 0x0, 0x1, 0x2, 0x8
BUSY, DONE, OVF = 1, 2, 4


def ctrl(sel, k, start=1):
    return (k << 4) | (sel << 1) | start


class Host:
    """Register-port host in the clk_ref domain. Each access costs one clk_ref cycle."""

    def __init__(self, dut):
        self.dut = dut
        self.cycles = 0
        cocotb.start_soon(self._count())

    async def _count(self):
        while True:
            await RisingEdge(self.dut.clk_ref)
            self.cycles += 1

    async def write(self, addr, data):
        d = self.dut
        d.we.value, d.addr.value, d.wdata.value = 1, addr, data
        await RisingEdge(d.clk_ref)
        await Timer(1, unit="ns")
        d.we.value = 0

    async def read(self, addr):
        d = self.dut
        d.addr.value = addr
        await RisingEdge(d.clk_ref)
        self.read_edge = get_sim_time()  # timestamp before the read-data settling delay
        await Timer(1, unit="ns")
        return d.rdata.value.to_unsigned()

    async def read_one(self, sel, k, timeout=None):
        """Host-sequenced read of oscillator `sel`: start, poll STATUS.done, read COUNT[sel]."""
        await self.write(CTRL, ctrl(sel, k))
        for _ in range(timeout or (2 ** k + 200)):
            st = await self.read(STATUS)
            if st & DONE:
                break
        else:
            raise AssertionError(f"timeout waiting for done (sel={sel}, k={k})")
        return await self.read(COUNT + sel), st


async def setup(dut, osc_ps=None):
    """Start clocks (idle-low osc lines stay 0), reset, return a Host."""
    cocotb.start_soon(Clock(dut.clk_ref, REF_PS, unit="ps").start())
    dut.we.value, dut.addr.value, dut.wdata.value = 0, 0, 0
    dut.osc.value = 0
    dut.rst_n.value = 0
    for i, p in enumerate(osc_ps or []):
        if p:
            cocotb.start_soon(Clock(dut.osc[i], p, unit="ps").start())
    await Timer(3 * REF_PS + 7_000, unit="ps")
    dut.rst_n.value = 1
    await Timer(2 * REF_PS, unit="ps")
    return Host(dut)


def expected(period_ps, k):
    return (2 ** k) * REF_PS // period_ps


def check(got, exp, what):
    exp += BREAK
    assert abs(got - exp) <= TOL, f"{what}: count {got}, expected {exp} +-{TOL}"


@cocotb.test()
async def reset_values(dut):
    h = await setup(dut)
    assert await h.read(CTRL) == (10 << 4), "CTRL reset: k must be 10, sel 0"
    assert await h.read(STATUS) == 0
    for i in range(5):
        assert await h.read(COUNT + i) == 0, f"COUNT[{i}] reset"
        assert await h.read(CAL + i) == 0, f"CAL[{i}] reset"
    assert (dut.busy.value, dut.done.value, dut.overflow.value) == (0, 0, 0)


@cocotb.test()
async def count_correctness(dut):
    """Several (f_osc, k) pairs incl. an oscillator slower than clk_ref (333 ns) and k = 0."""
    periods = [40_000, 10_000, 137_000, 333_334, 4_000]
    h = await setup(dut, periods)
    cases = [(0, 10), (1, 10), (2, 8), (3, 10), (4, 6), (1, 0), (0, 1)]
    for sel, k in cases:
        cnt, st = await h.read_one(sel, k)
        check(cnt, expected(periods[sel], k), f"f_osc={1e6 / periods[sel]:.3f} MHz, k={k}")
        assert not st & OVF
        dut._log.info(
            f"count ok: osc[{sel}] f_osc={1e6 / periods[sel]:.3f} MHz k={k} count={cnt} "
            f"(ideal {expected(periods[sel], k)})"
        )


@cocotb.test()
async def select_switching(dut):
    """All five inputs selected in turn; each COUNT[i] independent, repeat in reverse order."""
    periods = [40_000, 25_000, 20_000, 12_500, 8_000]
    h = await setup(dut, periods)
    k = 8
    got = {}
    for i in list(range(5)) + [4, 3, 2, 1, 0]:
        got[i], _ = await h.read_one(i, k)
        check(got[i], expected(periods[i], k), f"osc[{i}]")
    for i in range(5):
        assert await h.read(COUNT + i) == got[i], f"COUNT[{i}] changed by a later read"
    assert len({got[i] for i in range(5)}) == 5, "counts must be distinct per oscillator"


@cocotb.test()
async def busy_done_sequencing(dut):
    h = await setup(dut, [40_000, 20_000, 0, 0, 0])
    k = 6  # 64 ref cycles
    await h.write(CTRL, ctrl(0, k))
    assert await h.read(STATUS) == BUSY, "busy set, done clear right after start"
    assert dut.busy.value == 1 and dut.done.value == 0
    # start while busy (different oscillator) is ignored
    await h.write(CTRL, ctrl(1, k))
    polls = 0
    while not (await h.read(STATUS)) & DONE:
        polls += 1
        assert polls < 400, "done never set"
    assert await h.read(STATUS) == DONE, "busy clear, done set, no overflow"
    c0 = await h.read(COUNT + 0)
    check(c0, expected(40_000, k), "osc[0] after ignored start")
    assert await h.read(COUNT + 1) == 0, "start during busy must not read osc[1]"
    # done is cleared by the next accepted start
    await h.write(CTRL, ctrl(1, k))
    assert await h.read(STATUS) == BUSY
    while not (await h.read(STATUS)) & DONE:
        pass
    check(await h.read(COUNT + 1), expected(20_000, k), "osc[1]")
    assert await h.read(COUNT + 0) == c0, "COUNT[0] must be held"
    # sel out of range: not started
    for bad in (5, 6, 7):
        await h.write(CTRL, ctrl(bad, 4))
        assert (await h.read(STATUS)) & BUSY == 0, f"sel={bad} must not start"
    # start bit self-clears / reads 0
    assert (await h.read(CTRL)) & 1 == 0


@cocotb.test()
async def cal_readback(dut):
    h = await setup(dut)
    vals = [0xA5A5A5, 0x000001, 0xFFFFFF, 0x123456, 0x800000]
    for i, v in enumerate(vals):
        await h.write(CAL + i, v)
    for i, v in enumerate(vals):
        assert await h.read(CAL + i) == v, f"CAL[{i}]"
    # writes to RO registers are ignored
    await h.write(STATUS, 0xFFFFFF)
    await h.write(COUNT, 0xFFFFFF)
    assert await h.read(STATUS) == 0 and await h.read(COUNT) == 0
    # CTRL fields read back (no start)
    await h.write(CTRL, ctrl(3, 17, start=0))
    assert await h.read(CTRL) == (17 << 4) | (3 << 1)
    assert await h.read(STATUS) == 0, "no start requested"


@cocotb.test()
async def reset_mid_gate(dut):
    h = await setup(dut, [40_000, 0, 0, 0, 0])
    await h.write(CTRL, ctrl(0, 10))
    await Timer(20 * REF_PS, unit="ps")
    assert dut.busy.value == 1
    dut.rst_n.value = 0
    await Timer(3 * REF_PS, unit="ps")
    dut.rst_n.value = 1
    await Timer(3 * REF_PS, unit="ps")
    assert await h.read(STATUS) == 0
    assert await h.read(CTRL) == (10 << 4), "k back to default"
    cnt, _ = await h.read_one(0, 6)
    check(cnt, expected(40_000, 6), "read after mid-gate reset")


@cocotb.test()
async def saturation_overflow(dut):
    """Counter sticks at 2^24-1 and sets overflow; overflow cleared by the next start.

    Reaching 2^24 organically takes ~16.8M oscillator cycles (minutes of Icarus wall time), so the
    counter is back-door preloaded to 2^24-16 once the gate is open (hierarchical deposit on
    u_cnt.count); the remaining ~10k oscillator edges of the window must saturate it.
    """
    h = await setup(dut, [10_000, 40_000, 0, 0, 0])
    await h.write(CTRL, ctrl(0, 10))
    for _ in range(4):
        await RisingEdge(dut.clk_ref)
    assert dut.u_cnt.running.value == 1, "gate must be open before the preload"
    dut.u_cnt.count.value = 0xFFFFF0
    for _ in range(2 ** 10 + 200):
        st = await h.read(STATUS)
        if st & DONE:
            break
    else:
        raise AssertionError("timeout waiting for done")
    cnt = await h.read(COUNT + 0)
    assert cnt == 0xFFFFFF, f"saturated count {cnt:#x}"
    assert st & OVF, "overflow must be set"
    assert dut.overflow.value == 1
    cnt1, st1 = await h.read_one(1, 6)
    check(cnt1, expected(40_000, 6), "osc[1] after overflow")
    assert not st1 & OVF, "overflow cleared by the next start"
    assert await h.read(COUNT + 0) == 0xFFFFFF, "saturated COUNT[0] kept"
    dut._log.info("saturation ok: count=0xFFFFFF overflow set then cleared (RTL sim, Icarus, preloaded counter)")


@cocotb.test()
async def full_read_cycle_count(dut):
    """Five oscillators at 10 MHz reference, k = 10: clk_ref cycles first start .. fifth done."""
    periods = [40_000, 25_000, 20_000, 12_500, 8_000]
    h = await setup(dut, periods)
    k = 10
    start = h.cycles
    gates = []
    for i in range(5):
        c0 = h.cycles
        cnt, _ = await h.read_one(i, k)
        check(cnt, expected(periods[i], k), f"osc[{i}]")
        gates.append(h.cycles - c0)
    total = h.cycles - start
    gate_cycles = 5 * 2 ** k
    overhead = total - gate_cycles
    dut._log.info(
        f"SIMULATED (RTL simulation, Icarus, test_readout.py::full_read_cycle_count; 10 MHz clk_ref, k={k}): "
        f"full five-oscillator read = {total} clk_ref cycles = {total * REF_PS / 1e9:.4f} ms; "
        f"gate-only = {gate_cycles} cycles = {gate_cycles * REF_PS / 1e9:.4f} ms (spec §6 planning figure 0.512 ms); "
        f"handshake + host-access overhead = {overhead} cycles ({overhead / 5:.1f} per oscillator); "
        f"per-oscillator {gates}"
    )
    assert total >= gate_cycles
    assert total < 1.2 * gate_cycles, "overhead unexpectedly large"


async def _drive_osc(sig, period_ps, delay_ps):
    """Ideal osc: low for delay_ps, then 50% duty square wave (phase set by delay_ps)."""
    sig.value = 0
    await Timer(max(delay_ps, 1), unit="ps")
    while True:
        sig.value = 1
        await Timer(period_ps // 2, unit="ps")
        sig.value = 0
        await Timer(period_ps - period_ps // 2, unit="ps")


async def _phase_trial(dut, h, period_ps, phase_ps, k):
    """One read of osc[0] with the oscillator's first rising edge phase_ps after the CTRL write
    edge. Returns (busy_cleared, count). A hung read is recovered with an asynchronous reset."""
    dut.osc[0].value = 0
    # CTRL write is sampled on the next clk_ref edge; place the osc relative to that edge.
    d = dut
    d.we.value, d.addr.value, d.wdata.value = 1, CTRL, ctrl(0, k)
    await RisingEdge(d.clk_ref)
    drv = cocotb.start_soon(_drive_osc(dut.osc[0], period_ps, phase_ps))
    await Timer(1, unit="ns")
    d.we.value = 0
    cleared, cnt = False, None
    for _ in range(60):
        st = await h.read(STATUS)
        if st & DONE:
            cleared = True
            break
    if cleared:
        cnt = await h.read(COUNT + 0)
    drv.cancel()
    dut.osc[0].value = 0
    if not cleared:
        dut.rst_n.value = 0
        await Timer(3 * REF_PS, unit="ps")
        dut.rst_n.value = 1
        await Timer(3 * REF_PS, unit="ps")
    return cleared, cnt


@cocotb.test()
async def k0_phase_sweep(dut):
    """Phase sweep: gate start vs osc edge, k in {0, 1}, osc slower than clk_ref (1 us, 333 ns)
    and equal/faster. Reports, per phase, whether busy clears. RTL simulation, Icarus, no corner.

    Finding (issue #82): a read hangs (busy never clears, only rst_n recovers) iff NO osc rising
    edge lands inside the gate window. One edge is enough (gate_s1 -> gate_s2 -> running still
    completes after the gate drops), so it is not a two-edge condition. Window >= one osc period
    always completes. Hence the documented minimum k: 2^k * T_ref >= T_osc."""
    h = await setup(dut)
    for period_ps in (1_000_000, 333_334, 100_000, 40_000):
        for k in (0, 1, 2):
            step = max(period_ps // 25, 1_000)
            hung = []
            for phase in range(0, period_ps + step, step):
                ok, cnt = await _phase_trial(dut, h, period_ps, phase, k)
                if not ok:
                    hung.append(phase)
            window_ps = (2 ** k) * REF_PS
            if window_ps >= period_ps:
                assert not hung, (
                    f"window {window_ps} ps >= osc period {period_ps} ps (k={k}) must always "
                    f"complete, but busy never cleared at phases {hung}"
                )
            else:
                # Short window: a read hangs exactly when no osc edge lands inside it.
                assert hung, f"k={k}, osc period {period_ps} ps: expected phase-dependent hang"
                assert len(hung) < len(range(0, period_ps + step, step)), "some phases must complete"
            dut._log.info(
                f"SIMULATED (RTL, Icarus, test_readout.py::k0_phase_sweep): osc period {period_ps} ps, "
                f"k={k}: busy never cleared at {len(hung)} phases {hung}"
            )


# ----------------------------------------------------- spec section 6 conversion time (issue #281)
#
# Every period below is a committed surface value, extracted with
# sim/sensitivity/analyze.py `extract` over the nine reports in the order fixed by
# sim/sensitivity/records/2026-11-14-osc-subth-gate-sizing.md section 1 (later rows
# overwrite earlier ones, so the order decides the winner); the f_hz written here is the
# last-row-wins winner for that cell, and source_report names the report it came from.
# Nothing in this bench re-derives a frequency from crossings.

CONV_OSC_ORDER = ("osc_hd", "osc_nmos", "osc_pmos", "osc_wire", "osc_subth")
_R = "sim/sensitivity/records/reports"
_WIRE_PROBE_CAVEAT = (
    "osc_wire at this cell is MISSING in both committed grid reports (timestep_too_small "
    "under default solver options); the value is the relaxed-options debug probe "
    "(reltol=0.01 gmin=1e-10 method=gear), whose bias check measured up to +0.2 percent at "
    "three cells that did converge under default options and does not bound the bias at this "
    "cell (sim/sensitivity/records/2026-11-06-mc-offnominal-cold-margin.md section 1)."
)

CONV_CELLS = {
    "nominal": {
        "grid_cell": {"process": "tt", "vdd_V": 1.80, "temp_C": 27},
        "osc": {
            "osc_hd": {"f_hz": 641025642.5249137, "source_report": f"{_R}/grid_osc_hd.json.gz"},
            "osc_nmos": {"f_hz": 221971285.92119876, "source_report": f"{_R}/grid_osc_nmos.json.gz"},
            "osc_pmos": {"f_hz": 79365062.28017792, "source_report": f"{_R}/grid_osc_pmos.json.gz"},
            "osc_wire": {"f_hz": 75669245.54416709, "source_report": f"{_R}/grid_osc_wire.json.gz"},
            "osc_subth": {"f_hz": 2840955.9890419813, "source_report": f"{_R}/grid_osc_subth.json.gz"},
        },
    },
    # The cell with the slowest osc_subth on the committed surfaces (945.75 us period;
    # gate-sizing record section 5). osc_wire here is the relaxed-solver probe value.
    "sf_1v98_n40C": {
        "grid_cell": {"process": "sf", "vdd_V": 1.98, "temp_C": -40},
        "osc": {
            "osc_hd": {"f_hz": 687286213.5010563, "source_report": f"{_R}/grid_osc_hd.json.gz"},
            "osc_nmos": {"f_hz": 272349986.45454586, "source_report": f"{_R}/grid_osc_nmos.json.gz"},
            "osc_pmos": {"f_hz": 105125516.7644808, "source_report": f"{_R}/grid_osc_pmos.json.gz"},
            "osc_wire": {
                "f_hz": 84985845.34411676,
                "source_report": f"{_R}/probe_wire_sf_relaxed.json.gz",
                "caveat": _WIRE_PROBE_CAVEAT,
            },
            "osc_subth": {
                "f_hz": 1057.366320595822,
                "source_report": f"{_R}/grid_osc_subth_sf_cold.json.gz",
            },
        },
    },
}

# The three gate settings the gate-sizing record tabulates (sections 5-6): the spec
# section 5 default, k = 14 on the whole bank, and k = 14 on osc_subth only.
CONV_GATE_SETTINGS = (
    {"name": "spec_default_k10_all", "k": {o: 10 for o in CONV_OSC_ORDER}},
    {"name": "k14_all_five", "k": {o: 14 for o in CONV_OSC_ORDER}},
    {"name": "k14_osc_subth_only", "k": {**{o: 10 for o in CONV_OSC_ORDER}, "osc_subth": 14}},
)

SPEC6_BOUNDS_S = {"target": 1e-3, "fallback": 1e-2, "stretch": 1e-4}

_OSC_HD_TRUST = (
    "Independent STA limitation (sta/readout.osc-corner.sta.report.json): counter setup "
    "slack is -1.227 ns at tt_025C_1v80 and counter Fmax is below the osc_hd surface "
    "frequency in every reported liberty corner. Icarus drops the SDF TIMINGCHECK sections. "
    "The simulation does not establish the cause of the timeout."
)


def _conv_meta(cell):
    metas = []
    for name in CONV_OSC_ORDER:
        src = cell["osc"][name]
        m = dict(src)
        m["name"] = name
        m["period_ps"] = round(1e12 / src["f_hz"])
        metas.append(m)
    return metas


async def _conv_osc(sig, period_ps, first_rise, delay_ps):
    """50% duty oscillator at period_ps whose first rising edge is delay_ps after the
    coroutine starts; the time (simulator steps) of that first rise is recorded in first_rise[0]
    before it happens."""
    sig.value = 0
    await Timer(max(delay_ps, 1), unit="ps")
    first_rise[0] = get_sim_time()
    sig.value = 1
    await Timer(period_ps // 2, unit="ps")
    sig.value = 0
    await Timer(period_ps - period_ps // 2, unit="ps")
    while True:
        sig.value = 1
        await Timer(period_ps // 2, unit="ps")
        sig.value = 0
        await Timer(period_ps - period_ps // 2, unit="ps")


_PHASE_CONVENTION = (
    "the oscillator's first rising edge is half an oscillator period after the clk_ref edge "
    "that samples the CTRL start write -- a fixed, reproducible mid-phase. When the gate "
    "window is shorter than one oscillator period, completion is phase-dependent "
    "(test_readout.py::k0_phase_sweep: a read hangs iff no rising edge lands inside the "
    "window), so this convention is part of the recorded result."
)


def _ref_cycles(start_edge, end_edge):
    cycles, remainder = divmod(end_edge - start_edge, convert(REF_PS, "ps", to="step"))
    assert remainder == 0, "both timestamps must be sampled clk_ref edges"
    return cycles


async def _count_rises(signal, counts, name, high_value):
    while True:
        await ValueChange(signal)
        if signal.value == high_value:
            counts[name] += 1


async def _conv_read_one(dut, h, sel, k, meta, sdf_leg):
    """Return the read record, sampled CTRL edge and first STATUS edge showing DONE
    (None on timeout). Only relative times are written to the record."""
    d = dut
    period_ps = meta["period_ps"]
    bound = (2 ** k) + math.ceil(4.0 * period_ps / REF_PS) + 100
    d.we.value, d.addr.value, d.wdata.value = 1, CTRL, ctrl(sel, k)
    await RisingEdge(d.clk_ref)  # CTRL write sampled here
    write_edge = get_sim_time()
    rises = {}
    monitors = []
    if sdf_leg and meta["name"] == "osc_hd":
        routed = d.klt_sdf_dut
        # Icarus exposes change callbacks on the whole input vector. All unselected bits are low.
        for name, signal, high_value in (
            ("osc_input", d.osc, 1 << sel),
            ("osc_sel_clk", routed.osc_sel_clk, 1),
            ("tog_o", routed.tog_o, 1),
            ("done", d.done, 1),
        ):
            rises[name] = 0
            monitors.append(cocotb.start_soon(_count_rises(signal, rises, name, high_value)))
    first_rise = [None]
    drv = cocotb.start_soon(_conv_osc(d.osc[sel], period_ps, first_rise, period_ps // 2))
    await Timer(1, unit="ns")
    d.we.value = 0
    completed, st, polls = False, 0, 0
    done_at = None
    for _ in range(bound):
        st = await h.read(STATUS)
        polls += 1
        if st & DONE:
            completed = True
            done_at = h.read_edge
            break
    for monitor in monitors:
        monitor.cancel()
    res = {
        "sel": sel,
        "osc": meta["name"],
        "k": k,
        "gate_cycles": 2 ** k,
        "gate_ps": (2 ** k) * REF_PS,
        "f_hz_surface": meta["f_hz"],
        "period_ps": period_ps,
        "source_report": meta["source_report"],
        "phase_evidence": {
            "first_osc_edge_after_ctrl_write_ps": (
                convert(first_rise[0] - write_edge, "step", to="ps") if first_rise[0] is not None else None
            ),
            "gate_window_ps": (2 ** k) * REF_PS,
            "gate_window_over_osc_period": round(((2 ** k) * REF_PS) / period_ps, 6),
        },
        "completed": completed,
    }
    if "caveat" in meta:
        res["surface_caveat"] = meta["caveat"]
    if rises:
        res["rising_edges_through_last_status_poll"] = rises
    if completed:
        cycles = _ref_cycles(write_edge, done_at)
        assert cycles == polls, "one STATUS poll per clk_ref cycle after the CTRL write"
        res["cycles_write_to_done"] = cycles
        res["seconds_at_10MHz"] = cycles * REF_PS / 1e12
        res["status_polls"] = polls
        res["count_observed"] = await h.read(COUNT + sel)
        res["overflow"] = bool(st & OVF)
        assert res["cycles_write_to_done"] >= 2 ** k, "a completed read is never shorter than its gate"
    else:
        if sdf_leg:
            why = f"STATUS.done stayed clear through all {polls} polls at the driven {period_ps} ps period"
        elif (2 ** k) * REF_PS < period_ps:
            why = (
                f"gate window {2 ** k} clk_ref cycles ({(2 ** k) * REF_PS / 1e6} us) is shorter "
                f"than one oscillator period ({period_ps / 1e6} us), and no oscillator rising "
                "edge landed inside the window at the recorded phase (test_readout.py::"
                "k0_phase_sweep: busy never clears in that case)"
            )
        else:
            why = (
                f"the gate window spans {round(((2 ** k) * REF_PS) / period_ps, 3)} oscillator "
                "periods, so oscillator rising edges landed inside it and the read still did "
                "not complete"
            )
        res["did_not_complete"] = {
            "poll_bound_cycles": bound,
            "status_polls": polls,
            "recovered_by": "asynchronous rst_n pulse in the bench (the only recovery)",
            "why": why,
        }
    # Park the oscillator before the next selection: the clock mux may only switch while
    # not busy, and unselected osc inputs are ignored by the RTL.
    drv.cancel()
    d.osc[sel].value = 0
    if not completed:
        d.rst_n.value = 0
        await Timer(3 * REF_PS, unit="ps")
        d.rst_n.value = 1
        await Timer(3 * REF_PS, unit="ps")
    return res, write_edge, done_at


def _grade_spec6(seconds):
    b = {
        "target_lt_1ms": seconds < SPEC6_BOUNDS_S["target"],
        "fallback_lt_10ms": seconds < SPEC6_BOUNDS_S["fallback"],
        "stretch_lt_100us": seconds < SPEC6_BOUNDS_S["stretch"],
    }
    v = (
        f"full read {seconds * 1e3:.4f} ms at 10 MHz: target (<1 ms) "
        f"{'PASS' if b['target_lt_1ms'] else 'FAIL'}, fallback (<10 ms) "
        f"{'PASS' if b['fallback_lt_10ms'] else 'FAIL'}, stretch (<100 us) "
        f"{'PASS' if b['stretch_lt_100us'] else 'FAIL'}"
    )
    return b, v


async def _conv_full_read(dut, h, cell_label, cell, setting, sdf_leg):
    metas = _conv_meta(cell)
    per = []
    for sel, meta in enumerate(metas):
        r, write_edge, done_at = await _conv_read_one(dut, h, sel, setting["k"][meta["name"]], meta, sdf_leg)
        if sel == 0:
            first_write = write_edge
        if sdf_leg and meta["name"] == "osc_hd":
            r["gate_level_timing_trust"] = _OSC_HD_TRUST
        per.append(r)
    done = all(p["completed"] for p in per)
    full = {
        "cell": cell_label,
        "gate_setting": setting["name"],
        "k_per_osc": setting["k"],
        "oscillators": per,
        "full_read": {
            "definition": (
                "clk_ref rising edges from the edge that samples the first CTRL start write to "
                "the first STATUS poll edge showing done on the fifth oscillator. The interval "
                "includes the first four COUNT reads. with_count_reads_cycles ends at the "
                "fifth COUNT read edge."
            ),
            "completed": done,
            "gate_only_cycles": sum(p["gate_cycles"] for p in per),
        },
    }
    fr = full["full_read"]
    hung = [p["osc"] for p in per if not p["completed"]]
    if done:
        cycles = _ref_cycles(first_write, done_at)
        # Between successive conversions the host reads COUNT, then writes the next CTRL.
        assert cycles == sum(p["status_polls"] for p in per) + 2 * (len(per) - 1)
        fr["cycles"] = cycles
        fr["seconds_at_10MHz"] = cycles * REF_PS / 1e12
        fr["with_count_reads_cycles"] = _ref_cycles(first_write, h.read_edge)
        assert fr["with_count_reads_cycles"] == cycles + 1
        fr["overhead_cycles"] = cycles - fr["gate_only_cycles"]
        b, v = _grade_spec6(fr["seconds_at_10MHz"])
        fr["spec6_bounds"] = b
        fr["spec6_verdict"] = v
        assert cycles >= fr["gate_only_cycles"], "full read cannot beat its gate-only time"
    else:
        fr["did_not_complete"] = {
            "oscillators": hung,
            "spec6_verdict": (
                "did not complete: no full-read conversion time exists at this cell and gate "
                "setting, so no spec section 6 bound is graded for it"
            ),
        }
    return full


@cocotb.test()
async def conversion_time_surfaces(dut):
    """Spec section 6 conversion time: full five-oscillator reads at periods taken from the
    committed frequency surfaces (nominal cell and the slowest-osc_subth cell), three gate
    settings, graded against the spec bounds and written to a committed record by this bench.
    SIMULATED (RTL or SDF-annotated gate level, Icarus); nothing measured. Reads that do not
    complete are recorded as such. The SDF-annotated leg runs the nominal cell only (the SDF
    is the tt_025C_1v80 post-route session at typ)."""
    sdf_leg = not (hasattr(dut, "u_cnt") and hasattr(dut.u_cnt, "count"))
    cells = list(CONV_CELLS.items()) if not sdf_leg else [("nominal", CONV_CELLS["nominal"])]
    h = await setup(dut)  # reference clock + reset; oscillators start per read
    results = []
    for label, cell in cells:
        for setting in CONV_GATE_SETTINGS:
            full = await _conv_full_read(dut, h, label, cell, setting, sdf_leg)
            results.append(full)
            fr = full["full_read"]
            if fr["completed"]:
                dut._log.info(
                    f"SIMULATED (Icarus, test_readout.py::conversion_time_surfaces): {label} / "
                    f"{setting['name']}: {fr['spec6_verdict']}"
                )
            else:
                hung = ", ".join(fr["did_not_complete"]["oscillators"])
                dut._log.info(
                    f"SIMULATED (Icarus, test_readout.py::conversion_time_surfaces): {label} / "
                    f"{setting['name']}: did not complete ({hung}); no spec section 6 grade"
                )
    record = {
        "schema": "sky130-process-monitor.conversion-time/1",
        "kind": "SIMULATED",
        "description": (
            "Spec section 6 conversion time (full read of all five oscillators) at oscillator "
            "periods taken from the committed frequency surfaces, measured by the bench itself "
            "and graded against the spec bounds exactly as they come out. No spec bound is "
            "changed and no gate is picked by this record; reads that do not complete are "
            "recorded as such. Every oscillator period names its source surface report and grid "
            "cell. Count correctness is NOT graded here (other tests in this module do that); "
            "count_observed values are recorded unasserted."
        ),
        "bench": {
            "test": "verification/readout/test_readout.py::conversion_time_surfaces",
            "engine": "icarus via cocotb",
            "reference_clock_hz": 1e7,
            "read_sequence": (
                "five host-sequenced reads in the fixed order osc_hd, osc_nmos, osc_pmos, "
                "osc_wire, osc_subth (CTRL sel 0..4); each oscillator's driver runs only during "
                "its own read (unselected osc inputs are ignored by the RTL clock mux, which "
                "switches only while not busy)"
            ),
            "osc_assignment_note": (
                "osc[i] / CTRL sel i is this bench's convention; neither rtl/ nor spec/ fixes "
                "an osc[i]-to-oscillator assignment (sta/run_osc_sta.py records the same gap)"
            ),
            "phase_convention": _PHASE_CONVENTION,
        },
        "leg": {
            "id": "sdf-annotated-gate-level" if sdf_leg else "pre-layout-rtl",
            "sources": (
                "layout/readout/out/readout.v + sky130_fd_sc_hd verilog + "
                "layout/readout/out_sdf/readout_route.sdf at corner typ "
                "(verification/readout/request-sdf.json)"
            )
            if sdf_leg
            else "rtl/readout/readout.v + rtl/readout/readout_counter.v",
            "detected_by": (
                "dut.u_cnt hierarchy absent (flat routed netlist)"
                if sdf_leg
                else "dut.u_cnt hierarchy present (readout_counter instance)"
            ),
        },
        "spec_section_6_bounds_s": SPEC6_BOUNDS_S,
        "surface_extraction": (
            "f_hz values are the last-row-wins winners of sim/sensitivity/analyze.py extract "
            "over the nine reports in the order fixed by "
            "sim/sensitivity/records/2026-11-14-osc-subth-gate-sizing.md section 1"
        ),
        "cells": {
            label: {
                "grid_cell": cell["grid_cell"],
                "why": (
                    "nominal cell"
                    if label == "nominal"
                    else "the cell with the slowest osc_subth on the committed surfaces "
                    "(sim/sensitivity/records/2026-11-14-osc-subth-gate-sizing.md section 5)"
                ),
                "osc": {
                    name: {
                        "f_hz": src["f_hz"],
                        "period_ps": round(1e12 / src["f_hz"]),
                        "source_report": src["source_report"],
                        **({"caveat": src["caveat"]} if "caveat" in src else {}),
                    }
                    for name, src in cell["osc"].items()
                },
            }
            for label, cell in CONV_CELLS.items()
        },
        "gate_settings": [
            {
                "name": s["name"],
                "k_per_osc": s["k"],
                "why": (
                    "spec section 5 default gate (2^10 clk_ref cycles)"
                    if s["name"] == "spec_default_k10_all"
                    else "gate-sizing record section 5 k = 14, whole bank"
                    if s["name"] == "k14_all_five"
                    else "gate-sizing record section 5 k = 14 on osc_subth only, others default"
                ),
            }
            for s in CONV_GATE_SETTINGS
        ],
        "cells_run": [label for label, _ in cells],
        "results": results,
        "does_not_establish": [
            "nothing here is measured; every figure is Icarus simulation at the leg named above",
            "counter timing at osc_hd's surface frequency is a recorded spec section 5 FAIL "
            "(sta/readout.osc-corner.sta.report.json); this record measures conversion-time "
            "behaviour, not timing closure, and re-runs at the surface period rather than "
            "substituting a slower one",
            "count correctness is not graded by this bench (test_readout.py count tests grade it)",
            "the relaxed-solver osc_wire value at the sf cell carries the probe caveat recorded "
            "beside it and is not re-derived here",
        ],
    }
    if sdf_leg:
        record["leg"]["limits"] = [
            "typ corner only: the SDF is the tt_025C_1v80 post-route session, so only the "
            "nominal cell is run; the sf_1v98_n40C cell is a corner mismatch and is not",
            "partial annotation (Icarus drops SDF TIMINGCHECK and the zero-delay INTERCONNECT "
            "entries; see verification/README.md disclosed limits)",
            _OSC_HD_TRUST,
            "ideal oscillator inputs at nominal surface periods, down to 1.560 ns for osc_hd. "
            "Per-read edge counts show how many input edges reached osc_sel_clk and whether "
            "tog_o or done rose during the observation interval (verification/README.md limit 4).",
        ]
    out = "conversion-time-sdf.json" if sdf_leg else "conversion-time.json"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), out)
    with open(path, "w") as f:
        json.dump(record, f, indent=1)
        f.write("\n")
    assert os.path.getsize(path) > 0, "conversion-time record must not be empty"
    dut._log.info(f"wrote {out} ({len(results)} cell x gate-setting results)")
