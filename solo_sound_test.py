import time
import board
import busio
import pygame
import adafruit_tpa2016

i2c = busio.I2C(board.SCL, board.SDA)
tpa = adafruit_tpa2016.TPA2016(i2c)
tpa.fixed_gain = 0

pygame.mixer.init()
voice_channel = pygame.mixer.Channel(0)
voice_sound = pygame.mixer.Sound('sound.wav')

print("Nous allons tester la carte son.")
time.sleep(1)
voice_channel.play(voice_sound)
time.sleep(2)

print("Attention les oreilles, nous allons maintenant augmenter le volume.")
time.sleep(1)
tpa.fixed_gain = 3
voice_channel.play(voice_sound)
time.sleep(3)
