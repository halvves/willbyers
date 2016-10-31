import sys
import os
import time

# LED LIBRARY
from neopixel import *

# TWITTER LIBRARY
from twython import Twython,TwythonStreamer

# LED STRIP CONFIG:
LED_COUNT      = 26      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# SETUP TWITTER ACCESS
CONSUMER_KEY = {{FILL IN YOUR CONSUMER KEY}}
CONSUMER_SECRET = {{FILL IN YOUR CONSUMER SECRET}}
ACCESS_KEY = {{FILL IN YOUR ACCESS TOKEN}}
ACCESS_SECRET = {{FILL IN YOUR ACCESS TOKEN SECRET}}

# TWITTER SEARCH/FILTER TERMS
TERMS = '@upsidedownwill'

# MAP LETTER ARRAY
ALPHA = [
    'Z','Y','X','W','V','U','T','S','R',
    'I','J','K','L','M','N','O','P','Q',
    'H','G','F','E','D','C','B','A'
]

# CURRENTLY ALL THREE COLORS ARE WARM WHITE
# TO SHINE THROUGH OUR CERAMIC BULBS (YAY AUTHENTICITY)
# BUT I LEFT IT AS AN ARRAY FROM TESTING SO YOU CAN RGB IT UP:
# [Color(255,0,0),Color(0,255,0),Color(0,0,255)]
# AND THERE IS ALREADY A LITTLE MODULUS 3 THERE TO SHOW THE DIFF COLORS
COLORS = [Color(255,200,200),Color(255,200,200),Color(255,200,200)]

C_OFF = Color(0,0,0)
C_WHITE = Color(255,200,200)

# LIGHT EM ALL UP
def chaser(strip):
        for i in range(strip.numPixels(), -1, -1):
                strip.setPixelColor(i, C_WHITE)
                strip.show()
                time.sleep(0.03)

# DISPLAY TEXT ON LIGHTS
def textLights(strip, string, wait_ms=1000):
        chaser(strip)
        time.sleep(wait_ms/1000.0)
        # Clear LEDs
        for i in range(strip.numPixels()):
                strip.setPixelColor(i,C_OFF)
                strip.show()
        time.sleep(wait_ms/1000.0)
        # Play through letters
        for i in string:
                if i == ' ':
                        time.sleep(wait_ms/2000.0)
                elif i.upper() in ALPHA:
                        lightIndex = ALPHA.index(i.upper())
                        strip.setPixelColor(lightIndex,COLORS[lightIndex%3])
                        strip.show()
                        time.sleep(wait_ms/1000.0)
                        strip.setPixelColor(lightIndex,C_OFF)
                        strip.show()
                        time.sleep(wait_ms/10000.0)

# HANDLE THE STREEEEEEEEEEAM
class MyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        txt = data['text']
                        if txt.startswith(TERMS):
                                txt = txt[16:]
                                print '///A MESSAGE FROM THE UPSIDE DOWN'
                                print txt.encode('utf-8')
                                print '------------------'
                                textLights(strip, txt.encode('utf-8'))
                        else:
                                print '///WAS NOT A DIRECT REPLY'
                                print txt.encode('utf-8')
                                print '------------------'

        def on_error(self, err, data):
                print err, data

# MAIN FUNCTION
if __name__ == '__main__':
        # INIT LEDS
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        strip.begin()

        print ('Should I Stay Or Should I Go Now')

        # BEGIN TWITTER STREAM
        stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
        stream.statuses.filter(track=TERMS)
