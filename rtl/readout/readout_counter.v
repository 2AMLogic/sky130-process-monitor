// Oscillator-domain half of the readout: a 24-bit saturating counter clocked by
// the selected oscillator, gated by a window that is synchronised in from the
// reference-clock domain.
//
// Clock-domain crossing (oscillator <-> reference clock):
//   ref -> osc : gate_en is a level, passed through a 2-flop synchroniser clocked
//                by osc_clk. Counting runs while the synchronised gate is high.
//                The window seen by the oscillator is therefore the reference
//                window delayed by 2 osc edges at both ends; the number of osc
//                edges inside it differs from f_osc * 2^k / f_ref by up to +-1
//                (synchroniser phase at each gate edge, i.e. +-1 count of gate-edge
//                uncertainty) and the model accepts +-2 to cover both edges.
//   osc -> ref : when the gate closes the counter is frozen and `done_tog`
//                toggles (one osc edge after the synchronised gate falls). The
//                reference domain 2-flop-synchronises done_tog and only then reads
//                `count`/`ovf`, which have been stable for >= 3 reference cycles.
//                Multi-bit data is never sampled while it can change.
//
// Assumptions: `osc_clk` must be glitch-free while busy: the oscillator select is
// only changed (by the parent) while not busy, so the clock mux never switches
// with a window open. The oscillator must toggle after the gate closes for the
// done toggle to be produced; a stopped oscillator leaves the read busy.
`default_nettype none
module readout_counter (
    input  wire        osc_clk,   // selected oscillator
    input  wire        rst_n,     // asynchronous, active low
    input  wire        gate_en,   // reference-domain gate level (asynchronous to osc_clk)
    output reg  [23:0] count,     // held while the gate is closed
    output reg         ovf,       // counter saturated during the last window
    output reg         done_tog   // toggles once per completed window
);
    localparam [23:0] MAX = 24'hFF_FFFF;

    reg gate_s1, gate_s2;
    reg running;

    always @(posedge osc_clk or negedge rst_n) begin
        if (!rst_n) begin
            gate_s1  <= 1'b0;
            gate_s2  <= 1'b0;
            running  <= 1'b0;
            count    <= 24'd0;
            ovf      <= 1'b0;
            done_tog <= 1'b0;
        end else begin
            gate_s1 <= gate_en;
            gate_s2 <= gate_s1;
            if (gate_s2) begin
                running <= 1'b1;
                if (!running) begin
                    // First oscillator edge inside the window: restart the count.
                    count <= 24'd1;
                    ovf   <= 1'b0;
                end else if (count == MAX) begin
                    ovf   <= 1'b1;          // saturate: stick at 2^24 - 1
                end else begin
                    count <= count + 24'd1;
                end
            end else if (running) begin
                running  <= 1'b0;
                done_tog <= ~done_tog;
            end
        end
    end
endmodule
`default_nettype wire
