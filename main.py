from iv_curve_tracer import IV_Curve_Tracer
from tmcs1108 import Tmcs1108
from pico_adc import Pico_ADC
from mcp4921 import Mcp4921
from wifi import setup_wifi_ap
from webapp import create_webapp

import os
from machine import Pin, SPI
import time

import json

with open('settings.json') as json_file:
    settings = json.load(json_file)

setup_wifi_ap(settings['wifi_ssid'], settings['wifi_password'])

try:
    os.mkdir('/data')
except:
    pass

try:
    with open('num.txt') as f:
        num = f.read()
except:
    with open('num.txt', 'w') as f:
        f.write(str(0))

btn = Pin(12, Pin.IN, Pin.PULL_UP)

led = Pin(25, Pin.OUT)

pv_voltage_sensor = Pico_ADC(26)

scale_factor = .2
voltage_offset_factor = 0.1
pv_adc = Pico_ADC(27)
pv_current_sensor = Tmcs1108(pv_adc, scale_factor, voltage_offset_factor)


dac_spi_clk_pin = Pin(2)
dac_spi_cs_pin = Pin(5, Pin.OUT)
dac_spi_data_pin = Pin(3)
dac_latch_pin = Pin(1, Pin.OUT)

dac_spi = SPI(0,
              baudrate=500_000,
              phase=0,
              polarity=0,
              bits=8,
              firstbit=SPI.MSB,
              sck=dac_spi_clk_pin,
              mosi=dac_spi_data_pin)
dac_cs = dac_spi_cs_pin
dac_latch = dac_latch_pin

dac = Mcp4921(dac_spi, dac_cs, dac_latch)

iv_curve_tracer = IV_Curve_Tracer(pv_voltage_sensor,
                                  pv_current_sensor,
                                  dac)

app = create_webapp(iv_curve_tracer)
app.run(port=80)
