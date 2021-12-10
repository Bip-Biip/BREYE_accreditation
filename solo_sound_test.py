import time
import board
import busio
import pygame
import adafruit_max9744

i2c = busio.I2C(board.SCL, board.SDA)
amp = adafruit_max9744.MAX9744(i2c)
amp.volume = 32
pygame.mixer.init()
voice_channel = pygame.mixer.Channel(0)
voice_sound = pygame.mixer.Sound('sound.wav')

print("Nous allons tester la carte son.")
time.sleep(1)
voice_channel.play(voice_sound)
time.sleep(3)

print("Attention les oreilles, nous allons maintenant augmenter le volume.")
time.sleep(2)
amp.volume = 50
voice_channel.play(voice_sound)
time.sleep(3)