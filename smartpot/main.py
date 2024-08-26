from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf, sys
import utime
from dht import DHT22
from time import sleep

pix_res_x = 128
pix_res_y = 64
dht = DHT22(Pin(10)) 

def init_i2c(scl_pin, sda_pin):
    i2c_dev = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=200000)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]
    
    if not i2c_addr:
        print('No I2C Display Found')
        sys.exit()
    else:
        print("I2C Address      : {}".format(i2c_addr[0]))
        print("I2C Configuration: {}".format(i2c_dev))
    
    return i2c_dev

def display_text(oled, temp, hum):
    oled.fill(0) 
    
    if temp < 20:
        oled.text("Oh no! It's too", 0, 0)
        oled.text("cold for me!!", 0, 10)
    elif temp > 40:
        oled.text("Uh oh! It's too", 0, 0)
        oled.text("hot! I can't", 0, 10)
        oled.text("breathe!", 0, 20)
    else:
        oled.text("Temp: " + str(temp) + "C", 0, 0)
    

    if hum < 30:
        oled.text("I'm so thirsty!", 0, 40)
    elif hum > 70:
        oled.text("Too humid!", 0, 40)
    else:
        oled.text("Humidity: " + str(hum) + "%", 0, 40)
    
    oled.show()

def main():
    i2c_dev = init_i2c(scl_pin=27, sda_pin=26)
    oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)
    
    while True:
        dht.measure()
        temp = dht.temperature()
        hum = dht.humidity()
        
        display_text(oled, temp, hum)
        
        utime.sleep(2) 

if __name__ == '__main__':
    main()
