import time
import board
import busio
import pygame
import adafruit_tpa2016

i2c = busio.I2C(board.SCL, board.SDA)
tpa = adafruit_tpa2016.TPA2016(i2c)
tpa.fixed_gain = -28

pygame.mixer.init()
pygame.mixer.set_num_channels(60)
voice_sound = pygame.mixer.Sound('music.wav')

for i in range(60):
    print(i+1)
    voice_channel = pygame.mixer.Channel(i)
    voice_channel.play(voice_sound)
    time.sleep(1)
