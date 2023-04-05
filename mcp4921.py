
class Mcp4921:

    def __init__(self, spi, cs, latch):

        self.spi = spi
        self.latch = latch
        self.cs = cs

    def set_dac(self, value):

        # b15 (write operation) b14 (buffered) b13 (Gain = 1) b12 (active mode operation)
        value = (1<<14) | (1<<13) | (1<<12) | value;
        value = value.to_bytes(2, 'big')

        self.latch.value(True)
        self.cs.value(False)

        self.spi.write(value)

        self.latch.value(False)
        self.cs.value(True)

