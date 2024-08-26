import random
from machine import Pin, I2C
import ssd1306
from nec import NEC_8
from utime import sleep

i2c = I2C(0, scl=Pin(21), sda=Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

pin_r = Pin(3, Pin.OUT)
pin_g = Pin(2, Pin.OUT)
pin_b = Pin(1, Pin.OUT)

pin_r.value(1)
pin_g.value(1)
pin_b.value(1)


ir_pin = Pin(6, Pin.IN)
ir_codes = {}

def set_rgb_color(color):
    pin_r.value(1 if color[0] == 0 else 0)  # Red
    pin_g.value(1 if color[1] == 0 else 0)  # Green
    pin_b.value(1 if color[2] == 0 else 0)  # Blue

def random_color():
    return [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]

def on_ir_receive(ir_code, addr, ext):
    if ir_code in ir_codes:
        color = ir_codes[ir_code]
    else:
        color = random_color()
        ir_codes[ir_code] = color

    oled.fill(0)
    oled.text("IR Code: {}".format(hex(ir_code)), 0, 0)
    oled.text("Address: {}".format(hex(addr)), 0, 10)
    oled.text("Color: {}".format(color), 0, 20)
    oled.show()
    set_rgb_color(color)

ir = NEC_8(ir_pin, on_ir_receive)

while True:
    sleep(1)
