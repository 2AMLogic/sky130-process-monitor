# rtl

Synthesizable Verilog. `rtl/smoke/` is a toolchain placeholder, not part of the design.

## readout/

Digital readout partition (spec §5, §6): a 24-bit saturating gated counter on one of five oscillator inputs, plus
the register file. `readout.v` is the top (registers, gate, reference-domain side of the crossing);
`readout_counter.v` is the oscillator-domain counter. `clk_ref` is an input (no on-die reference clock). The
register port is plain synchronous (`we`, `addr`, `wdata`, `rdata`); no bus protocol.

Register map (word addresses; same table is in the header of `readout/readout.v`):

| Addr | Name | Access | Content |
|---|---|---|---|
| 0x0 | `CTRL` | RW | `[0]` start (write 1, self-clearing, reads 0; ignored while busy or if sel > 4); `[3:1]` sel (binary 0..4; 5..7 do not start); `[8:4]` k (window = 2^k `clk_ref` cycles, 0..31, reset 10); rest reserved |
| 0x1 | `STATUS` | RO | `[0]` busy, `[1]` done, `[2]` overflow (count saturated; cleared by the next accepted start) |
| 0x2..0x6 | `COUNT[0..4]` | RO | 24-bit count, latched at gate end; saturates at 2^24 − 1 |
| 0x8..0xC | `CAL[0..4]` | RW | 24-bit calibration word, plain storage |

Difference from the spec §5 table: that table lists names and access only (a planning figure); addresses and bit
fields are fixed here. `spec/` is not edited.

Crossing: the gate is synchronised into the selected-oscillator domain (2 flops), the count is frozen when it
closes, and a toggle plus 2-flop synchroniser carries completion back before `COUNT` is latched. The gate edge
costs up to ±1 count per end. `sel` is latched at start, so the oscillator clock mux only changes while idle.
Details in `readout/readout_counter.v`.

**Minimum k.** Choose `k` so the gate window covers at least one oscillator period:
`2^k / f_ref >= 1 / f_osc`, i.e. `k >= ceil(log2(f_ref / f_osc))`. With a shorter window the read hangs
(`busy` never clears; only `rst_n` recovers) whenever no oscillator edge lands inside the window, which depends on
gate/oscillator phase. One edge in the window is enough to complete. Simulated (Icarus, RTL only, no corner):
`verification/readout/test_readout.py::k0_phase_sweep`. This applies only when the oscillator is slower than
`clk_ref` or `k` is very small; it is separate from the stopped-oscillator behaviour.

Testbench: `make -C verification/readout` (see `verification/README.md`).

## Synthesized netlist (T1 item 1)

`synth/readout/` holds the `klt synthesize` request (`request.json`, top `readout`, `sky130_fd_sc_hd`, `tt_025C_1v80`
liberty from the pinned sky130A), the gate-level netlist `readout.gl.v` (consumed by P&R and LVS), and the report
`readout.synth.json`. Regenerate after any RTL change, then re-attest (`attest/item1_digital.json`):

    export PDK=sky130A PDK_ROOT=<pinned PDK root>
    klt synthesize synth/readout/request.json --verify-equivalence --equiv-engine yosys-sequential \
        --format json > synth/readout/readout.synth.json
    cp synth/readout/.klt/synthesize/run-*/readout_synth.v synth/readout/readout.gl.v   # then rm -r synth/readout/.klt
    klt synthesize synth/readout/request.json --check synth/readout/readout.synth.json --netlist synth/readout/readout.gl.v

The report carries the yosys-sequential equivalence verdict (RTL vs netlist). Synthesis reports no timing.
