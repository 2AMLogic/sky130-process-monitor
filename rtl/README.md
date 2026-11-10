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

Testbench: `make -C verification/readout` (see `verification/README.md`).
