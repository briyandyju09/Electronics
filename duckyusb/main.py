import time
import usb_hid
from keyboard import Keyboard
from keyboard_layout_us import KeyboardLayoutUS
import adafruit_ducky

led = Pin(5, Pin.OUT)

time.sleep(1)
led.toggle()
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

duck = adafruit_ducky.Ducky("duckyscript.txt", keyboard, keyboard_layout)

result = True
while result is not False:
    result = duck.loop()

if result = True:
      led.toggle()
