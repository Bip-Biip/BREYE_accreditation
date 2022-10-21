import time
import board
import busio
import pygame
import adafruit_tpa2016

i2c = busio.I2C(board.SCL, board.SDA)
tpa = adafruit_tpa2016.TPA2016(i2c)
tpa.fixed_gain = 0
growing = True

pygame.mixer.init()
voice_channel = pygame.mixer.Channel(0)
voice_sound = pygame.mixer.Sound('music.mp3')
voice_channel.play(voice_sound)

for i in range(30):
    print(tpa.fixed_gain)
    if growing:
        if tpa.fixed_gain < 30:
            tpa.fixed_gain += 1
        else:
            growing = False
            tpa.fixed_gain -= 1
    else:
        if tpa.fixed_gain > 0:
            tpa.fixed_gain -= 1
        else:
            growing = True
            tpa.fixed_gain += 1
    time.sleep(5)
