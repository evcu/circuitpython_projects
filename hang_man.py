from adafruit_circuitplayground.express import cpx
import time
import board
import neopixel
from random import randint
pixel_pin = board.A1
num_pixels = 40
bness = [0.3,0.5]
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=bness[0], auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

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


def fill_beat(wait, head_on):
    c_switch = cpx.switch
    while True:
        if cpx.switch != c_switch:
            c_switch = cpx.switch
            cpx.pixels.fill(0)
            pixels.fill(0)
            pixels.brightness = (bness[0])
            pixels.show()
            cpx.pixels.brightness = bness[0]
            break
        if cpx.button_b:
            wait += 1
            while cpx.button_b:
                time.sleep(0.1)
        elif cpx.button_a:
            wait -= 1
            wait = max(0.5, wait)
            while cpx.button_a:
                time.sleep(0.1)
        color = wheel(randint(0,255))
        for i in range(8):
            pixels[15-i] = color
            pixels[16+i] = color
            pixels.show()
        for i in range(8):
            pixels[39-i] = color
            pixels[24+i] = color
            pixels[7-i] = color
            pixels.show()
        if head_on:
            for i in range(5):
                cpx.pixels[4-i] = color
                cpx.pixels[5+i] = color
        speed = 10.0
        for _ in range(randint(0,3)):
            for i in range(0,speed):
                cb = float(i)/speed*bness[1]
                pixels.brightness=(cb)
                pixels.show()
                if head_on: cpx.pixels.brightness=cb
                time.sleep(0.01)
        time.sleep(0.5)
        if head_on:
            for i in range(5):
                cpx.pixels[9-i] = 0
                cpx.pixels[0+i] = 0
        for i in range(8):
            pixels[32+i] = 0
            pixels[31-i] = 0
            pixels[i] = 0
            pixels.show()
        for i in range(8):
            pixels[23-i] = 0
            pixels[8+i] = 0
            pixels.show()
        time.sleep(wait)

B_DEC = 0.1
def traversing_balls(n_balls,wait):
    c_switch = cpx.switch
    start=time.monotonic()
    cpx.pixels.brightness = 0
    cpx.pixels[3:7]=[RED]*4
    cpx.pixels[0:10:9]=[RED]*2
    b_inc = 0
    c_b = 1
    locs = [randint(0,num_pixels-1) for _ in range(n_balls)]
    direction = [randint(0,1)*2-1 for _ in range(n_balls)]
    t = 0
    is_left = True
    c_time = time.monotonic()
    while True:
        if cpx.switch != c_switch:
           c_switch = cpx.switch
           for i in range(n_balls):
               pixels[locs[i]] = (0,0,0)
           break
        if cpx.button_b and n_balls<num_pixels:
            n_balls +=1
            locs.append(randint(0,num_pixels-1))
            direction.append(randint(0,1)*2-1)
            while cpx.button_b:
                time.sleep(0.1)
        elif cpx.button_a and n_balls>1:
            n_balls -=1
            pixels[locs[i]] = (0,0,0)
            del locs[-1]
            del direction[-1]
            while cpx.button_a:
                time.sleep(0.1)
        for i in range(n_balls):
            pixels[locs[i]] = (0,0,0)
            c_clr = wheel((t//5+i*255//n_balls)& 255)
            if locs[i] == 24:
                locs[i] = 16
                direction[i] = 1
            if locs[i] == 39:
                locs[i] = 15
                direction[i] = -1
            elif locs[i] == 23 and direction[i] ==1:
                locs[i] = 7
                direction[i]=-1
            elif locs[i] == 16:
                locs[i] = 17
                direction[i]=1
            elif locs[i] == 15:
                locs[i] = 14
                direction[i]=-1
            elif locs[i] == 7 and direction[i]==1:
                if is_left:
                   locs[i] = 23
                   direction[i] = -1
                   is_left = False
                else:
                    is_left = True
                    locs[i] = 8
            elif locs[i] == 0 and direction[i]==-1:
                locs[i] = 32 if is_left else 31
                direction[i] = 1 if is_left else -1
                is_left = not is_left
                cpx.pixels[3:7] = [c_clr]*4
                cpx.pixels.brightness = bness[0]
                b_inc = -B_DEC
            else:
                locs[i] = (locs[i] + direction[i]) % num_pixels
            pixels[locs[i]] = c_clr
            t+=1
        #cpx.pixels.fill(head_color)
        if cpx.pixels.brightness + b_inc<0:
            cpx.pixels.brightness = 0
            b_inc = 0
        else:
            cpx.pixels.brightness += b_inc

        pixels.show()
        time.sleep(wait)
        c_time = time.monotonic()

while True:
    # if cpx.button_b:
    #     cpx.red_led = True
    # else:
    #     cpx.red_led = False
    #     pixels.fill(RED)
    fill_beat(2,False)
    traversing_balls(2,0.01)
    fill_beat(5,True)
    # color_chase(RED, 0)  # Increase the number to slow down the color chase
    # color_chase(YELLOW, 0)
    # color_chase(GREEN, 0)
    # color_chase(CYAN, 0)
    # color_chase(BLUE, 0)
    # color_chase(PURPLE, 0)
    #
    # rainbow_cycle(0)
