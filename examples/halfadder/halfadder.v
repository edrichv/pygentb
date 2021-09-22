`include "modules/LSmitll_XORT_v2p1_selfcontained.v"
`include "modules/LSmitll_AND2T_v2p1_selfcontained.v"
`include "modules/LSmitll_SPLITT_v2p1_selfcontained.v"
`timescale 1ps/100fs
module HalfAdder(
    a,
    b,
    clk,
    s,
    cout
);

input 
    a, b, clk;
output 
    s, cout;

reg [12:0] net_r = 0;
wire[12:0] net_w;

assign net_w[0] = a;
assign net_w[3] = b;
assign net_w[8] = clk;
assign s = net_r[6];
assign cout = net_r[7];

always @(posedge net_w[0] or negedge net_w[0]) begin
    net_r[0] <= net_w[0];
end
always @(posedge net_w[1] or negedge net_w[1]) begin
    net_r[1] <= net_w[1];
end
always @(posedge net_w[2] or negedge net_w[2]) begin
    net_r[2] <= net_w[2];
end
always @(posedge net_w[3] or negedge net_w[3]) begin
    net_r[3] <= net_w[3];
end
always @(posedge net_w[4] or negedge net_w[4]) begin
    net_r[4] <= net_w[4];
end
always @(posedge net_w[5] or negedge net_w[5]) begin
    net_r[5] <= net_w[5];
end
always @(posedge net_w[6] or negedge net_w[6]) begin
    net_r[6] <= net_w[6];
end
always @(posedge net_w[7] or negedge net_w[7]) begin
    net_r[7] <= net_w[7];
end
always @(posedge net_w[8] or negedge net_w[8]) begin
    net_r[8] <= net_w[8];
end
always @(posedge net_w[9] or negedge net_w[9]) begin
    net_r[9] <= net_w[9];
end
always @(posedge net_w[10] or negedge net_w[10]) begin
    net_r[10] <= net_w[10];
end

LSmitll_SPLITT_v2p1_optimized split0 (net_r[0], net_w[1], net_w[2]);
LSmitll_SPLITT_v2p1_optimized split1 (net_r[3], net_w[4], net_w[5]);
LSmitll_SPLITT_v2p1_optimized split2 (net_r[8], net_w[9], net_w[10]);
LSmitll_XORT_v2p1_optimized xor0 (net_r[2], net_r[5], net_r[9], net_w[7]);
LSmitll_AND2T and0 (net_r[1], net_r[4], net_r[10], net_w[6]);

endmodule