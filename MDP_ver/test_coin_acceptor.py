import random
import cocotb
from cocotb.triggers import RisingEdge, Timer

CLK_PERIOD = 10  # Clock period in ns

@cocotb.test()
async def simple_coin_acceptor_test(dut):
    """Test XOR output when both a_en and b_en are high in the same cycle"""

    # Clock initialization
    dut.clk.setimmediatevalue(0)

    async def clock_gen():
        while True:
            await Timer(CLK_PERIOD // 2, units='ns')
            dut.clk.value = not dut.clk.value

    cocotb.start_soon(clock_gen())

    # Initial reset
    dut.rst_n.value = 0
    dut.adata.value = 0
    dut.a_en.value = 0
    dut.bdata.value = 0
    dut.b_en.value = 0
    dut.y_rdy.value = 1  # Always ready to consume output

    await Timer(200, units='ns')
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    for i in range(20):
        # Random input values
        a = random.randint(0, 255)
        b = random.randint(0, 255)

        # Apply inputs and assert enable signals simultaneously
        dut.adata.value = a
        dut.bdata.value = b
        dut.a_en.value = 1
        dut.b_en.value = 1

        await RisingEdge(dut.clk)

        dut.a_en.value = 0
        dut.b_en.value = 0

        # Wait for y_en to be asserted
        for _ in range(10):
            await RisingEdge(dut.clk)
            if dut.y_en.value:
                break
        else:
            assert False, f"No output seen after 10 cycles for inputs a={a:02x}, b={b:02x}"

        # Check result
        y = dut.ydata.value.integer
        expected = a ^ b
        assert y == expected, f"Output {y:02x} != Expected {expected:02x} (a={a:02x}, b={b:02x})"

        # Wait until y_en deasserts before next transaction
        while dut.y_en.value:
            await RisingEdge(dut.clk)

