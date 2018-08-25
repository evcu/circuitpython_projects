# CircuitPython demo - NeoPixel
import time
import board
import neopixel
from touchio import TouchIn
from digitalio import DigitalInOut, Direction
from random import randint
pixel_pin = board.A0
num_pixels = 40

pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=0.2, auto_write=False)
# Capacitive touch on A2
touch2 = TouchIn(board.A2)
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase_mid(color, wait):
    is_rand = color == -1
    while True:
        if is_rand:
            color = wheel(randint(0,255))
        pixels.fill(0)
        pixels.show()
        if touch2.value:
            cap_routine()
            return
        for i in range(num_pixels//2):
            pixels[num_pixels//2-i-1] = color
            pixels[num_pixels//2+i] = color
            time.sleep(wait)
            pixels.show()
        for i in range(num_pixels//2):
            pixels[i] = 0
            pixels[num_pixels-i-1] = 0
            time.sleep(wait)
            pixels.show()


def cap_routine():
    led.value = touch2.value
    while touch2.value:
        time.sleep(0.1)
    led.value = 0

def rainbow_cycle(wait,X):
    while True:
        for j in range(X):
            if touch2.value:
                cap_routine()
                return
            for i in range(num_pixels):
                rc_index = int(i*256/num_pixels + j*256/X)
                pixels[i] = wheel(rc_index & 255)
            pixels.show()
            time.sleep(wait)

while True:
    rainbow_cycle(0,32)
    rainbow_cycle(0,64)
    rainbow_cycle(0,128)
    color_chase_mid(-1,0)
    color_chase_mid(-1,0.02)
    color_chase_mid(-1,0.04)
    color_chase_mid(-1,0.06)
