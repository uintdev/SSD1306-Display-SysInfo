# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

import os
import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

print('--- SSD1306 Display SysInfo ---\n\n')

msgFile = os.path.dirname(os.path.abspath(__file__)) + "/msg.txt"
print('Message file to check for: ' + msgFile + '\n\n')

# Create the I2C interface
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing
# Make sure to create image with mode '1' for 1-bit color
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes
# First define some constants to allow easy resizing of shapes
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font
font = ImageFont.load_default()

# Configure font
fontPath = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font = ImageFont.truetype(fontPath, 9)

# Center font
def center_text(img, font, text, color=(255, 255, 255)):
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font)
    position = ((width - text_width) / 2, (height - text_height) / 2)
    draw.text(position, text, color, font=font)
    return img

while True:
    # Draw a black filled box to clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Display message from file temporarily if exists
    if os.path.isfile(msgFile):
        # Get content
        with open(msgFile, "r") as file:
            content = file.readline().strip()
        
        # Set up font size
        contentLength = len(content)
        fontSize = 12
        if contentLength >= 20:
            fontSize = 10
        fontMsg = ImageFont.truetype(fontPath, fontSize)

        # Center text
        _, _, text_width, text_height = draw.textbbox((0, 0), content, font=fontMsg)
        position = ((128 - text_width) / 2, (32 - text_height) / 2)

        # Draw text
        draw.text(position, content, font=fontMsg, fill=255)
        disp.image(image)
        disp.show()
        
        # Delete message file
        os.remove(msgFile)

        # Delay next display update
        time.sleep(3)
        continue 

    # Monitoring information
    cmd = 'date +"%H:%M"'
    Time = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'cut -f 1 -d " " /proc/loadavg'
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s / %s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d / %d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Draw text
    draw.text(((x + width) - 30, top + 0), Time, font=font, fill=255)
    draw.text((x, top + 0), "IP: " + IP, font=font, fill=255)
    draw.text((x, top + 8), "CPU load: " + CPU, font=font, fill=255)
    draw.text((x, top + 16), MemUsage, font=font, fill=255)
    draw.text((x, top + 25), Disk, font=font, fill=255)

    # Display image
    disp.image(image)
    disp.show()

    # Delay next display update
    time.sleep(0.5)
