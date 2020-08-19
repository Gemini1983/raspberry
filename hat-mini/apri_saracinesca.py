#!/usr/bin/env python3

import sys
import time
import datetime


print ('*****************************')

nmb_saracinesca=sys.argv[1]
time_open=int(sys.argv[2])

import automationhat
time.sleep(0.1) # Short pause after ads1015 class creation recommended

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

import ST7735 as ST7735

print("Apertura saracinesca numero: "+sys.argv[1])
print("Minuti apertura : "+sys.argv[2])

def draw_states():
    image = Image.open("/home/pi/example/automation-hat/examples/hat-mini/images/clean.jpg")
    draw = ImageDraw.Draw(image)

    # use a truetype font
    font = ImageFont.truetype("Vera.ttf", 20)
    font2 = ImageFont.truetype("Vera.ttf", 10)

    text_apertura = 'VALVOLA N. : '+nmb_saracinesca
    text_apertura2 = 'MINUTI : '+sys.argv[2]

    # drawing text size 
    draw.text((5, 5), text_apertura, (255,255,255), font=font) 
    draw.text((5, 40), text_apertura2, (255,255,255), font=font) 
    disp.display(image)
    time.sleep(2)
    draw.text((5, 45), "prova", (255,255,255), font=font2) 
    disp.display(image)

def draw_states_clean():
    image = Image.open("/home/pi/example/automation-hat/examples/hat-mini/images/clean.jpg")
    disp.display(image)


# Create ST7735 LCD display class.
disp = ST7735.ST7735(
    port=0,
    cs=ST7735.BG_SPI_CS_FRONT,
    dc=9,
    backlight=25,
    rotation=270,
    spi_speed_hz=4000000
)

# Initialize display.
disp.begin()

on_colour = (99, 225, 162)
off_colour = (235, 102, 121)
bg_colour = (25, 16, 45)

# Values to keep everything aligned nicely.
on_x = 115
on_y = 35

off_x = 46
off_y = on_y

dia = 10

# MAIN
print("Apertura alle: ",datetime.datetime.now())

automationhat.output[int(nmb_saracinesca)-1].write(1)
draw_states()
time.sleep(time_open)
automationhat.output[0].write(0)
draw_states_clean()

print("Chiusura alle: ",datetime.datetime.now())

