import time
from utils import val_or_max, val_or_min
from dsp import find_pmax_idx, get_oversample_region

class IV_Curve_Tracer:

    def __init__(self,
                 pv_voltage_sensor,
                 pv_current_sensor,
                 dac):

        self.pv_voltage_sensor = pv_voltage_sensor
        self.pv_current_sensor = pv_current_sensor
        self.dac = dac

    def _get_pv_voltage(self, scale_factor=11):

        result = self.pv_voltage_sensor.get_voltage() * scale_factor
        return result

    def _get_pv_current(self):

        result = self.pv_current_sensor.get_current()
        return result

    def _measure_one(self, dac_value, settle_time=0.001, cool_time=0.001, num_measurements=2):

        pv_voltage = 0.0
        pv_current = 0.0
        scale_factor = 1.0 / num_measurements

        self.dac.set_dac(dac_value)
        time.sleep(settle_time)

        for i in range(num_measurements):
            if i % 2 == 0:
                pv_voltage += self._get_pv_voltage() * scale_factor
                pv_current += self._get_pv_current() * scale_factor
            else:
                pv_current += self._get_pv_current() * scale_factor
                pv_voltage += self._get_pv_voltage() * scale_factor

        self.dac.set_dac(0)
        time.sleep(cool_time)

        #print(f'Measuring {dac_value} Current {pv_current} Voltage {pv_voltage}')

        return (pv_voltage, pv_current)

    def measure(self, start, end, step):

        for i in range(start, end, step):
            point = self._measure_one(i, num_measurements = 8)
            yield point

    def run(self):

        pmax_idx = find_pmax_idx(self.measure)
        print(f'Pmax idx {pmax_idx}')

        start_idx = val_or_min(pmax_idx - 200, 0)
        end_idx = val_or_max(pmax_idx + 50, 4095)

        points = [None] * 350
        i = 0
        for point in self.measure(start_idx, end_idx, 1):
            points[i] = point
            i += 1

        points[0:(i-1)].sort(key=lambda x: x[0])

        oversample_idx = get_oversample_region(points[0:(i-1)]) + start_idx
        oversample_start_idx = val_or_min(oversample_idx - 10, 0)
        oversample_end_idx = val_or_max(oversample_idx + 10, 4095)

        for _ in range(5):
            for point in self.measure(oversample_start_idx, oversample_end_idx, 1):
                points[i] = point
                i += 1
        print(i)
        points.sort(key=lambda x: x[0])

        return points

