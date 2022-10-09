import time
import random
import math
import serial
import sys
import ctypes
import copy
import config
import neopixel

pixels = neopixel.NeoPixel(config.pixel_pin, config.num_pixels, brightness=0.2, auto_write=False, pixel_order=config.ORDER)

def setStartingSnowflakes(snowflakes):
    for x in range(snowflakes):
        pixels[random.randint(0, config.num_pixels-1)] = (255, 255, 255)
    pixels.show()

def moveSnowflakes(trailDecay):
    for i in range(config.num_pixels):
        faded = getFadedToBlack(i, trailDecay)
        pixels[i] = faded

        column = getColumn(i)
        if i - 1 > 0:
            pixels[i-1] = faded

def fallingSnowflakes(trailDecay):
    setStartingSnowflakes(2)
    reverseOddColumns()
    moveSnowflakes(trailDecay)
    reverseOddColumns()
    pixels.show()


def getFadedToBlack(ledNo, fadeValue):
    oldColor = pixels[ledNo]
    r = oldColor[0]
    g = oldColor[1]
    b = oldColor[2]

    if (r<=10):
        r = 0
    else:
        r = r - ( r * fadeValue / 256 )

    if (g<=10):
        g = 0
    else:
        g = g - ( g * fadeValue / 256 )

    if (b<=10):
        b = 0
    else:
        b = b - ( b * fadeValue / 256 )

    return ( int(r), int(g), int(b) )

def reverseOddColumns():
    tempPixels = copy.deepcopy(pixels)

    for index, pixel in enumerate(pixels):
        column = getColumn(index)
        if index < config.num_pixels and column % 2 == 1:
            newIndex = (column - 1) * config.pixelsInRow + (column * config.pixelsInRow - index) - 1
            if newIndex < config.num_pixels:
                pixels[index] = tempPixels[newIndex]



def getColumn(position):
    return math.floor(position / config.pixelsInRow) + 1

try:
    pixels.fill((0, 0, 0))
    pixels.show()
    setStartingSnowflakes(10)

    while True:
        fallingSnowflakes(70)

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
