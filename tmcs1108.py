class Tmcs1108:

    def __init__(self, adc, scale_factor, voltage_offset_factor):

        self.adc = adc
        self.scale_factor = 1.0 / scale_factor
        self.voltage_offset_factor = voltage_offset_factor


    def get_current(self):

        result  = (self.adc.get_voltage() - (self.adc.get_vref() * self.voltage_offset_factor))
        result *= self.scale_factor

        if result < 0.0:
            result = 0.0

        return result