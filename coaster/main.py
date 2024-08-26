from machine import Pin, I2C
import ssd1306
import ds18x20
import onewire
import time


TEMP_COOL = 50
TEMP_DRINKABLE = 70

pin_r = Pin(4, Pin.OUT)
pin_g = Pin(3, Pin.OUT)
pin_b = Pin(2, Pin.OUT)


i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


ow = onewire.OneWire(Pin(28))
sensor = ds18x20.DS18X20(ow)
roms = sensor.scan()

if not roms:
    raise RuntimeError("No DS18B20 sensor found")

def draw_cooled():
    oled.fill(0)
    oled.text('Temp: Cooled', 0, 0)
    oled.show()

def draw_drinkable():
    oled.fill(0)
    oled.text('Temp: Drinkable', 0, 0)
    oled.show()

def draw_too_hot():
    oled.fill(0)
    oled.text('Temp: Too Hot', 0, 0)
    oled.show()

while True:
    sensor.convert_temp()
    time.sleep(1)
    for rom in roms:
        temp = sensor.read_temp(rom)
        if temp is None:
            oled.fill(0)
            oled.text('Error reading temp', 0, 0)
            oled.show()
        else:
            oled.fill(0)
            oled.text('Temp: {:.2f}C'.format(temp), 0, 0)
            if temp < TEMP_COOL:
                draw_cooled()
                pin_b.value(200)
            elif TEMP_COOL <= temp <= TEMP_DRINKABLE:
                draw_drinkable()
                pin_g.value(100)
            else:
                draw_too_hot()
                pin_r.value(200)
        time.sleep(2)
