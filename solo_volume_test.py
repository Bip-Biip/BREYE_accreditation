import time
import board
import busio
import pygame
import adafruit_tpa2016

i2c = busio.I2C(board.SCL, board.SDA)
tpa = adafruit_tpa2016.TPA2016(i2c)
tpa.fixed_gain = 6

pygame.mixer.init()
# voice_sound = pygame.mixer.Sound('music.wav')
# voice_sound = pygame.mixer.Sound('victoire.wav')
voice_sound = pygame.mixer.Sound('victoire_au.wav')
voice_channel = pygame.mixer.Channel(0)
voice_channel.play(voice_sound)
time.sleep(15)
