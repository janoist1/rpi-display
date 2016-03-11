#!/usr/bin/env python

import time
import netifaces as net
import psutil

# import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

interfaces = ['wlan0', 'wlan1', 'eth0']

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)


# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)


def is_interface_up(interface):
    if interface not in net.interfaces():
        return False
    addr = net.ifaddresses(interface)
    return net.AF_INET in addr


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font.
font = ImageFont.load_default()
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# some padding
padding = 2

while True:
    cursor = [0, 0]
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # CPU
    text = "CPU " + str(psutil.cpu_percent(interval=1)) + "%"
    draw.text(tuple(cursor), text, font=font, fill=255)
    cursor[1] += font.getsize(text)[1]

    # MEM
    text = "SMEM " + str(psutil.swap_memory().percent) + "%" \
           + " VMEM " + str(psutil.virtual_memory().percent) + "%"
    draw.text(tuple(cursor), text, font=font, fill=255)
    cursor[1] += font.getsize(text)[1]

    # NET
    for interface in interfaces:
        if is_interface_up(interface):
            ip = net.ifaddresses(interface)[net.AF_INET][0]['addr']
            text = interface + " " + ip
        else:
            text = interface + " down"

        draw.text(tuple(cursor), text, font=font, fill=255)
        cursor[1] += font.getsize(text)[1]

    # Display image.
    disp.image(image)
    disp.display()

    time.sleep(1)
