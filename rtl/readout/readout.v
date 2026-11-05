// Readout: gated oscillator counter + register file for the process monitor.
// Implements spec/target-spec.md §5 (Readout) and the cycle count of §6.
//
// Interface: plain synchronous register port in the reference-clock domain
// (no bus protocol; spec §5 declares no consumer). `clk_ref` is an INPUT: there
// is no on-die reference clock. `osc[4:0]` are the five oscillator outputs.
//
// Register map (addr is word-addressed, 4 bits; wdata/rdata 24 bits):
//   addr  name       access  content
//   0x0   CTRL       RW      [0]   start  write 1 to begin a read; self-clearing,
//                                         reads 0; ignored while busy or if sel > 4
//                            [3:1] sel    oscillator select, binary 0..4. Values 5..7
//                                         are not started (start is a no-op).
//                                         Only latched at an accepted start.
//                            [8:4] k      gate exponent: window = 2^k clk_ref cycles,
//                                         supported 0..31, reset default 10
//                            [23:9] reserved, read 0
//   0x1   STATUS     RO      [0] busy      accepted start .. count latched
//                            [1] done      set at latch, cleared by next accepted start
//                            [2] overflow  count saturated at 2^24-1 in the last window;
//                                          cleared by next accepted start
//   0x2..0x6  COUNT[0..4]  RO  24-bit count per oscillator, latched at gate end.
//                              Holds its value (saturated if overflowed) until that
//                              oscillator is read again.
//   0x8..0xC  CAL[0..4]    RW  24-bit calibration word per oscillator, plain storage
//                              (unused inside the block). Other addresses read 0.
// Writes to RO registers are ignored. All registers reset to 0 except CTRL.k = 10.
//
// Difference from the spec §5 table: that table is a planning figure (name/access
// only); this file fixes the addresses and bit fields. No spec/ edit is needed.
//
// Timing: start is accepted on the clk_ref edge that samples we/addr/wdata
// (busy=1 and the gate opens after that edge). The gate is open for exactly 2^k
// clk_ref cycles; done follows after the oscillator-domain handshake (see
// readout_counter.v for the crossing and its +-1 count gate-edge uncertainty).
//
// Assumption: `sel` is latched at start, so the oscillator clock mux
// (osc[sel_q]) only changes while not busy.
`default_nettype none
module readout (
    input  wire        clk_ref,
    input  wire        rst_n,
    input  wire        we,
    input  wire [3:0]  addr,
    input  wire [23:0] wdata,
    output reg  [23:0] rdata,
    input  wire [4:0]  osc,
    output wire        busy,
    output wire        done,
    output wire        overflow
);
    // ---- reference-clock domain: control, gate, registers ----
    reg [2:0]  sel_q;
    reg [4:0]  k_q;
    reg        busy_r, done_r, ovf_r;
    reg        gate_en;
    reg [31:0] gate_cnt;
    reg [23:0] count_r [0:4];
    reg [23:0] cal_r   [0:4];
    reg [2:0]  ctrl_sel;   // CTRL as last written (sel readback)
    reg [4:0]  ctrl_k;

    wire [2:0]  cnt_idx  = addr[2:0] - 3'd2;   // valid for addr 0x2..0x6
    wire [2:0]  cal_idx  = addr[2:0];          // valid for addr 0x8..0xC (low bits 0..4)
    wire        wr_ctrl  = we && (addr == 4'h0);
    wire        start_ok = wr_ctrl && wdata[0] && !busy_r && (wdata[3:1] <= 3'd4);
    wire [31:0] gate_last = (32'd1 << k_q) - 32'd1;

    // oscillator domain
    wire        osc_sel_clk = (sel_q == 3'd0) ? osc[0] :
                              (sel_q == 3'd1) ? osc[1] :
                              (sel_q == 3'd2) ? osc[2] :
                              (sel_q == 3'd3) ? osc[3] :
                              (sel_q == 3'd4) ? osc[4] : 1'b0;
    wire [23:0] cnt_o;
    wire        ovf_o, tog_o;

    readout_counter u_cnt (
        .osc_clk (osc_sel_clk), .rst_n (rst_n), .gate_en (gate_en),
        .count (cnt_o), .ovf (ovf_o), .done_tog (tog_o)
    );

    // osc -> ref: 2-flop synchroniser on the done toggle, third flop for edge detect
    reg tog_s1, tog_s2, tog_s3;
    wire latch = tog_s2 ^ tog_s3;

    integer i;
    always @(posedge clk_ref or negedge rst_n) begin
        if (!rst_n) begin
            sel_q <= 3'd0; k_q <= 5'd10; ctrl_sel <= 3'd0; ctrl_k <= 5'd10;
            busy_r <= 1'b0; done_r <= 1'b0; ovf_r <= 1'b0;
            gate_en <= 1'b0; gate_cnt <= 32'd0;
            tog_s1 <= 1'b0; tog_s2 <= 1'b0; tog_s3 <= 1'b0;
            for (i = 0; i < 5; i = i + 1) begin
                count_r[i] <= 24'd0;
                cal_r[i]   <= 24'd0;
            end
        end else begin
            tog_s1 <= tog_o; tog_s2 <= tog_s1; tog_s3 <= tog_s2;

            if (wr_ctrl) begin
                ctrl_sel <= wdata[3:1];
                ctrl_k   <= wdata[8:4];
            end
            if (we && addr >= 4'h8 && addr <= 4'hC)
                cal_r[cal_idx] <= wdata;

            if (start_ok) begin
                sel_q <= wdata[3:1]; k_q <= wdata[8:4];
                busy_r <= 1'b1; done_r <= 1'b0; ovf_r <= 1'b0;
                gate_en <= 1'b1; gate_cnt <= 32'd0;
            end else if (gate_en) begin
                gate_cnt <= gate_cnt + 32'd1;
                if (gate_cnt == gate_last) gate_en <= 1'b0;
            end

            if (busy_r && latch) begin
                count_r[sel_q] <= cnt_o;
                ovf_r  <= ovf_o;
                done_r <= 1'b1;
                busy_r <= 1'b0;
            end
        end
    end

    // ---- read mux ----
    always @* begin
        rdata = 24'd0;
        case (addr)
            4'h0: rdata = {15'd0, ctrl_k, ctrl_sel, 1'b0};
            4'h1: rdata = {21'd0, ovf_r, done_r, busy_r};
            4'h2, 4'h3, 4'h4, 4'h5, 4'h6: rdata = count_r[cnt_idx];
            4'h8, 4'h9, 4'hA, 4'hB, 4'hC: rdata = cal_r[cal_idx];
            default: rdata = 24'd0;
        endcase
    end

    assign busy     = busy_r;
    assign done     = done_r;
    assign overflow = ovf_r;

    wire _unused = &{1'b0, wdata[23:9]};
endmodule
`default_nettype wire
