"""Placeholder cocotb smoke test for rtl/smoke/smoke.v (toolchain bring-up only)."""
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

# SMOKE_BREAK=1 inverts the expectation: the negative control (must fail).
OFFSET = 1 if os.environ.get("SMOKE_BREAK") == "1" else 0


@cocotb.test()
async def counts_up(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst_n.value = 0
    await Timer(25, unit="ns")
    dut.rst_n.value = 1
    for expected in range(1, 20):
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")
        assert dut.count.value.to_unsigned() == (expected + OFFSET) % 16, expected
