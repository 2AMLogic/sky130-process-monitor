"""cocotb tests for rtl/readout (testbench name: verification/readout/test_readout.py, Icarus).

Oscillators are modelled as ideal clocks; the reference clock is 10 MHz. Every figure
printed here is RTL simulation (Icarus), not silicon.

Count tolerance: the gate window is 2^k reference cycles. The window crosses into the
oscillator domain through a 2-flop synchroniser at each end, so the oscillator sees the
window with an edge-phase uncertainty of up to +-1 osc edge per gate edge. Expected
count = f_osc * 2^k * T_ref, accepted within +-2 (two gate edges x +-1).

READOUT_BREAK=1 adds an offset to every expected count: the negative control (must fail).
"""
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

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
