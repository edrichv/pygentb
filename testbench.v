`include "/home/edrich/github/pygentb/examples/ksa8/ksa8.v"
`timescale 1ps/100fs

module Testbench;
reg
	clk=0,a0=0,b0=0,a1=0,a2=0,a3=0,a4=0,a5=0,a6=0,a7=0,b1=0,b2=0,b3=0,b4=0,b5=0,b6=0,b7=0,cin=0;
wire
	sum0,sum1,sum2,sum3,sum4,sum5,sum6,sum7,cout;

KSA8 dut (
	.a0(a0),
	.b0(b0),
	.a1(a1),
	.a2(a2),
	.a3(a3),
	.a4(a4),
	.a5(a5),
	.a6(a6),
	.a7(a7),
	.b1(b1),
	.b2(b2),
	.b3(b3),
	.b4(b4),
	.b5(b5),
	.b6(b6),
	.b7(b7),
	.cin(cin),
	.clk(clk),
	.sum0(sum0),
	.sum1(sum1),
	.sum2(sum2),
	.sum3(sum3),
	.sum4(sum4),
	.sum5(sum5),
	.sum6(sum6),
	.sum7(sum7),
	.cout(cout)
);

localparam CLK_PERIOD = 100;
always #CLK_PERIOD clk=~clk;

initial begin
	$dumpfile("testbench.vcd");
	$dumpvars(0, dut);
end

initial begin
	#(CLK_PERIOD + 50);
	// a0 b0 a1 a2 a3 a4 a5 a6 a7 b1 b2 b3 b4 b5 b6 b7 cin
	// 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
	a0=~a0;
	b0=~b0;
	a1=~a1;
	a2=~a2;
	a3=~a3;
	a4=~a4;
	a5=~a5;
	a6=~a6;
	a7=~a7;
	b1=~b1;
	b2=~b2;
	b3=~b3;
	b4=~b4;
	b5=~b5;
	b6=~b6;
	b7=~b7;
	cin=~cin;
	#(50*CLK_PERIOD);
end

initial begin
	#20000 $finish;
end

endmodule