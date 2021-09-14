`include "ksa4.v"
`timescale 1ps/100fs

module Testbench;
reg
	clk=0,A0=0,B0=0,A1=0,A2=0,A3=0,B1=0,B2=0,B3=0,CIN=0;
wire
	SUM0,SUM1,SUM2,SUM3;

KSA4 dut (A0,B0,SUM0,SUM1,SUM2,SUM3,COUT,A1,A2,A3,B1,B2,B3,CIN,clk);

localparam CLK_PERIOD = 40;
always #CLK_PERIOD clk=~clk;

initial begin
	$dumpfile("testbench.vcd");
	$dumpvars(0, dut);
end

initial begin
	#(CLK_PERIOD + 10);
	// A0 B0 A1 A2 A3 B1 B2 B3 CIN
	// 1 1 1 1 1 1 1 1 1
	A0=~A0;
	B0=~B0;
	A1=~A1;
	A2=~A2;
	A3=~A3;
	B1=~B1;
	B2=~B2;
	B3=~B3;
	CIN=~CIN;
	#(10*CLK_PERIOD);
	// 1 1 0 1 1 1 1 1 1
	A0=~A0;
	B0=~B0;
	A2=~A2;
	A3=~A3;
	B1=~B1;
	B2=~B2;
	B3=~B3;
	CIN=~CIN;
	#(10*CLK_PERIOD);
	// 1 1 1 1 1 1 0 1 1
	A0=~A0;
	B0=~B0;
	A1=~A1;
	A2=~A2;
	A3=~A3;
	B1=~B1;
	B3=~B3;
	CIN=~CIN;
	#(10*CLK_PERIOD);
end

initial begin
	#10000 $finish;
end

endmodule