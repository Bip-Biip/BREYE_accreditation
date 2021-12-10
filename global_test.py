# =================================================================================================
#                                      Les imports
# =================================================================================================

import time
import board
import busio
import pygame
import serial
import RPi.GPIO as GPIO
import adafruit_max9744
import adafruit_fingerprint
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

# =================================================================================================
#                                      Les branchements
# =================================================================================================

LEFT_PIN = 21
MIDDLE_PIN = 20
RIGHT_PIN = 16

# =================================================================================================
#                                      Les boutons
# =================================================================================================

BUTTON_LEFT = 0
BUTTON_MIDDLE = 1
BUTTON_RIGHT = 2
BUTTON_RELEASED = 0
BUTTON_PRESSED = 1
BUTTON_STAND_BY = 2

buttons_state = [BUTTON_RELEASED]*3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MIDDLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def setButtonState(button_id, button_state):

	last_state = buttons_state[button_id]

	if last_state == button_state:
		return False

	if last_state == BUTTON_STAND_BY and button_state == BUTTON_PRESSED:
		return False

	buttons_state[button_id] = button_state
	
	if last_state == BUTTON_STAND_BY and button_state == BUTTON_RELEASED:
		return False

	if button_state == BUTTON_RELEASED:
		if sum([1 if buttons_state[b] == BUTTON_PRESSED else 0 for b in range(3)]) == 2:
			for b in buttons_state :
				if buttons_state[b] == BUTTON_PRESSED:
					buttons_state[b] = BUTTON_STAND_BY
			print("C'est un triple appui.")
		elif sum([1 if buttons_state[b] == BUTTON_PRESSED else 0 for b in range(3)]) == 1:
			double_id = [button_id]
			for b in buttons_state :
				if buttons_state[b] == BUTTON_PRESSED:
					double_id.append(b)
					buttons_state[b] = BUTTON_STAND_BY
			print("C'est un double appui. [" + str(double_id[0]) + "] et [" + str(double_id[1]) + "]")
		else :
			if button_id == 0 :
				print("Bouton gauche. [0]")
			if button_id == 1 :
				print("Bouton milieu. [1]")
			if button_id == 2 :
				print("Bouton droit. [2]")

	return True

# =================================================================================================
#                                      Les hauts parleurs
# =================================================================================================

i2c = busio.I2C(board.SCL, board.SDA)
amp = adafruit_max9744.MAX9744(i2c)
amp.volume = 32
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
print("Vous disposez de 10 secondes pour tester les boutons.")
a = 0
while a < 2000 :
	# Left button
	if GPIO.input(LEFT_PIN) != GPIO.HIGH :
		x = setButtonState(BUTTON_LEFT, BUTTON_PRESSED)
	else :
		x = setButtonState(BUTTON_LEFT, BUTTON_RELEASED)
	# Middle button
	if GPIO.input(MIDDLE_PIN) != GPIO.HIGH :
		y = setButtonState(BUTTON_MIDDLE, BUTTON_PRESSED)
	else :
		y = setButtonState(BUTTON_MIDDLE, BUTTON_RELEASED)
	# Right button
	if GPIO.input(RIGHT_PIN) != GPIO.HIGH :
		z = setButtonState(BUTTON_RIGHT, BUTTON_PRESSED)
	else :
		z = setButtonState(BUTTON_RIGHT, BUTTON_RELEASED)
	# Little pause
	a += 1
	time.sleep(0.005)

print("Bien, nous allons maintenant tester la détection des tag nfc.")
print("Présentez un jeton de votre choix.")

while True :
	uid = pn532.read_passive_target(timeout=0.5)
	if uid is None :
		pass
	else :
		print("La tuile", pn532.ntag2xx_read_block(0), "a été détectée")
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
amp.volume = 50
voice_channel.play(voice_sound)
time.sleep(3)

print("Nous allons maintenant baisser le volume.")
time.sleep(2)
amp.volume = 14
voice_channel.play(voice_sound)
time.sleep(4)

print("C'est bon, nous avons testé tous les périphériques, cette machine est fonctionnelle.")
