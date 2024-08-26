import random
from machine import Pin, I2C
import ssd1306
from nec import NEC_8
from utime import sleep


i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


pin_r = Pin(25, Pin.OUT)
pin_g = Pin(32, Pin.OUT)
pin_b = Pin(26, Pin.OUT)


pin_r.value(0)
pin_g.value(0)
pin_b.value(0)


ir_pin = Pin(27, Pin.IN)


ir_codes = {}

def set_rgb_color(color):
    pin_r.value(1 if color[0] else 0)
    pin_g.value(1 if color[1] else 0)
    pin_b.value(1 if color[2] else 0)

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
