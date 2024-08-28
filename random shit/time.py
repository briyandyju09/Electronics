import time
import board
import busio
import adafruit_ssd1306
import adafruit_ds1307
import digitalio
from adafruit_circuitplayground import cp

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
rtc = adafruit_ds1307.DS1307(i2c)

buttons = {
    "set_hour": digitalio.DigitalInOut(board.D2),
    "set_minute": digitalio.DigitalInOut(board.D3),
    "set_second": digitalio.DigitalInOut(board.D4)
}

for button in buttons.values():
    button.switch_to_input(pull=digitalio.Pull.UP)

def display_time():
    now = rtc.datetime
    oled.fill(0)
    oled.text("Date: {}-{}-{}".format(now.tm_year, now.tm_mon, now.tm_mday), 0, 0, 1)
    oled.text("Time: {}:{}:{}".format(now.tm_hour, now.tm_min, now.tm_sec), 0, 20, 1)
    oled.show()

def set_time():
    now = rtc.datetime
    if not buttons["set_hour"].value:
        rtc.datetime = time.struct_time((
            now.tm_year, now.tm_mon, now.tm_mday,
            (now.tm_hour + 1) % 24, now.tm_min, now.tm_sec,
            now.tm_wday, now.tm_yday, now.tm_isdst
        ))
        time.sleep(0.2)
    elif not buttons["set_minute"].value:
        rtc.datetime = time.struct_time((
            now.tm_year, now.tm_mon, now.tm_mday,
            now.tm_hour, (now.tm_min + 1) % 60, now.tm_sec,
            now.tm_wday, now.tm_yday, now.tm_isdst
        ))
        time.sleep(0.2)
    elif not buttons["set_second"].value:
        rtc.datetime = time.struct_time((
            now.tm_year, now.tm_mon, now.tm_mday,
            now.tm_hour, now.tm_min, (now.tm_sec + 1) % 60,
            now.tm_wday, now.tm_yday, now.tm_isdst
        ))
        time.sleep(0.2)

while True:
    set_time()
    display_time()
    time.sleep(1)
