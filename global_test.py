# =================================================================================================
#                                      Les imports
# =================================================================================================

import time
import board
import busio
import pygame
import serial
import RPi.GPIO as GPIO
import adafruit_tpa2016
import adafruit_fingerprint
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

# =================================================================================================
#                                      Les branchements
# =================================================================================================

LEFT_PIN = 21
MIDDLE_PIN = 20
RIGHT_PIN = 16
WIFI_PIN = 1

# =================================================================================================
#                                      Les boutons
# =================================================================================================

flag = False
waited_pin = -1

def button_callback(id) :
    global flag
    global waited_pin
    if flag and id == waited_pin :
        print("Bouton appuyé. pin :", id)
        flag = False
    return

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MIDDLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(WIFI_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(LEFT_PIN, GPIO.RISING, callback=button_callback)
GPIO.add_event_detect(MIDDLE_PIN, GPIO.RISING, callback=button_callback)
GPIO.add_event_detect(RIGHT_PIN, GPIO.RISING, callback=button_callback)
GPIO.add_event_detect(WIFI_PIN, GPIO.RISING, callback=button_callback)

# =================================================================================================
#                                      Les hauts parleurs
# =================================================================================================

i2c = busio.I2C(board.SCL, board.SDA)
tpa = adafruit_tpa2016.TPA2016(i2c)
tpa.fixed_gain = 0
pygame.mixer.init()
voice_channel = pygame.mixer.Channel(0)
voice_sound = pygame.mixer.Sound('sound.wav')

# =================================================================================================
#                                      Le scanneur d'empreinte
# =================================================================================================

uart = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
if finger.read_templates() != adafruit_fingerprint.OK :
	print("Erreur à la lecture des templates d'empreinte")

# =================================================================================================
#                                      Le détecteur NFC/RFID
# =================================================================================================

i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = DigitalInOut(board.D6)
req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)
pn532.SAM_configuration()

# =================================================================================================
#                                      Le script
# =================================================================================================

print("Bonjour et bienvenue dans le test Hardware de Br'Eye.")
print("Nous allons tester ensemble si les périphériques sont fonctionnels.")

flag = True
waited_pin = MIDDLE_PIN
print("Veuillez appuyer sur le bouton central.")
while flag :
    time.sleep(0.5)

flag = True
waited_pin = LEFT_PIN
print("Veuillez appuyer sur le bouton gauche.")
while flag :
    time.sleep(0.5)

flag = True
waited_pin = RIGHT_PIN
print("Veuillez appuyer sur le bouton droit.")
while flag :
    time.sleep(0.5)

flag = True
waited_pin = WIFI_PIN
print("Veuillez appuyer sur le bouton wi-fi (caché).")
while flag :
    time.sleep(0.5)

print("Bien, nous allons maintenant tester la détection des tag nfc.")
print("Présentez un jeton de votre choix.")

while True :
	uid = pn532.read_passive_target(timeout=0.5)
	if uid is None :
		pass
	else :
		print("Le jeton", pn532.ntag2xx_read_block(0), "a été détecté.")
		break

print("Bien, nous allons maintenant tester le détecteur d'empreinte.")
print("Il est censé s'illuminer si il s'agit du même modèle.")
print("Placez votre doigt dessus pour l'éteindre.")
while finger.get_image() != adafruit_fingerprint.OK :
	pass
if finger.image_2_tz(1) == adafruit_fingerprint.OK :
	print("Je confirme, ceci est un doigt.")

print("Enfin, nous allons tester la carte son.")
time.sleep(1)
voice_channel.play(voice_sound)
time.sleep(3)

print("Attention les oreilles, nous allons maintenant augmenter le volume.")
time.sleep(2)
tpa.fixed_gain = 3
voice_channel.play(voice_sound)
time.sleep(3)

print("C'est bon, nous avons testé tous les périphériques, cette machine est fonctionnelle.")
