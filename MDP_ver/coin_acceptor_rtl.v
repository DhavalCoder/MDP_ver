module coin_acceptor_rtl (
    input wire clk,
    input wire rst_n,
    input wire [7:0] adata,
    input wire a_en,
    output wire a_rdy,
    input wire [7:0] bdata,
    input wire b_en,
    output wire b_rdy,
    output reg  [7:0] ydata,
    output reg y_en,
    input wire y_rdy
);
    assign a_rdy = 1'b1;
    assign b_rdy = 1'b1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            y_en  <= 1'b0;
            ydata <= 8'h00;
        end else if (a_en && b_en && y_rdy) begin
            y_en  <= 1'b1;
            ydata <= adata ^ bdata;
        end else begin
            y_en  <= 1'b0;
        end
    end
endmodule
