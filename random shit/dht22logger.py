import time
import board
import adafruit_dht
import adafruit_ssd1306
import digitalio
import storage
import adafruit_sdcard
import busio
import microcontroller
import os


dht_device = adafruit_dht.DHT22(board.D5)


i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D10)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")


logfile_path = "/sd/data_log.txt"


def log_data(temp, hum):
    with open(logfile_path, "a") as logfile:
        timestamp = time.localtime()
        log_entry = f"{timestamp.tm_year}-{timestamp.tm_mon:02}-{timestamp.tm_mday:02} " \
                    f"{timestamp.tm_hour:02}:{timestamp.tm_min:02}:{timestamp.tm_sec:02}," \
                    f"Temp: {temp:.1f}C, Humidity: {hum:.1f}%\n"
        logfile.write(log_entry)


while True:
    try:

        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        
        log_data(temperature_c, humidity)
        
        oled.fill(0)
        oled.text("Temp: {:.1f}C".format(temperature_c), 0, 0, 1)
        oled.text("Humidity: {:.1f}%".format(humidity), 0, 20, 1)
        oled.text("Logging to SD", 0, 40, 1)
        oled.show()

    except RuntimeError as e:
        print("Reading from DHT22 failed, retrying...:", e)


    time.sleep(10)
