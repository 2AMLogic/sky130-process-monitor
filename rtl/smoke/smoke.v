// PLACEHOLDER - toolchain smoke only. NOT part of the process-monitor design.
// A 4-bit free-running counter used to prove cocotb + Icarus + Yosys run.
module smoke (
    input  wire       clk,
    input  wire       rst_n,
    output reg  [3:0] count
);
    always @(posedge clk or negedge rst_n)
        if (!rst_n) count <= 4'd0;
        else        count <= count + 4'd1;
endmodule
