module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/coin_acceptor_rtl.fst");
    $dumpvars(0, coin_acceptor_rtl);
end
endmodule
