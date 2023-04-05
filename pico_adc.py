from machine import ADC

class Pico_ADC:

    def __init__(self, pin_number):

        self.adc = ADC(pin_number)

    def get_vref(self):

        return 3.3

    def get_voltage(self):

        result = self.adc.read_u16() / 65535 * self.get_vref()

        return result