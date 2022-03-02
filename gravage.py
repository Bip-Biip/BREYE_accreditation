# =================================================================================================
#                                      Imports
# =================================================================================================

import time
import board
import busio
import pygame
import RPi.GPIO as GPIO
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C


# =================================================================================================
#                                      Initialization
# =================================================================================================

i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = DigitalInOut(board.D6)
req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)
pn532.SAM_configuration()


# =================================================================================================
#                                      Buttons
# =================================================================================================

buttonflag = True

def button_callback(useless_id) :
	global buttonflag
	buttonflag = False
	return

LEFT_PIN = 21
MIDDLE_PIN = 20
RIGHT_PIN = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MIDDLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(LEFT_PIN, GPIO.RISING, callback=button_callback)
GPIO.add_event_detect(MIDDLE_PIN, GPIO.RISING, callback=button_callback)
GPIO.add_event_detect(RIGHT_PIN, GPIO.RISING, callback=button_callback)


# =================================================================================================
#                                      Letter's illustration
# =================================================================================================

def draw_letter(entier:int) :
	p1 = False
	p2 = False
	p3 = False
	# Le premier point
	if entier % 2 :
		p1 = True
	entier //= 2
	# Le deuxième point
	if entier % 2 :
		p2 = True
	entier //= 2
	# Le troisième point
	if entier % 2 :
		p3 = True
	entier //= 2
	# Le quatrième point
	if entier % 2 :
		if p1 :
			print("\t ### | ### ")
			print("\t ### | ### ")
		else :
			print("\t     | ### ")
			print("\t     | ### ")
	else :
		if p1 :
			print("\t ### |     ")
			print("\t ### |     ")
		else :
			print("\t     |     ")
			print("\t     |     ")
	print("\t-----|-----")
	entier //= 2
	# Le cinquième point
	if entier % 2 :
		if p2 :
			print("\t ### | ### ")
			print("\t ### | ### ")
		else :
			print("\t     | ### ")
			print("\t     | ### ")
	else :
		if p2 :
			print("\t ### |     ")
			print("\t ### |     ")
		else :
			print("\t     |     ")
			print("\t     |     ")
	print("\t-----|-----")
	entier //= 2
	# Le sixième point
	if entier % 2 :
		if p3 :
			print("\t ### | ### ")
			print("\t ### | ### ")
		else :
			print("\t     | ### ")
			print("\t     | ### ")
	else :
		if p3 :
			print("\t ### |     ")
			print("\t ### |     ")
		else :
			print("\t     |     ")
			print("\t     |     ")
	return


# =================================================================================================
#                                      Engraving function
# =================================================================================================

BLOCK = 4
pygame.mixer.init()
validate = pygame.mixer.Sound('lil_sound.wav')

def engraving(entier:int) :

	draw_letter(entier)
	print("Vous avez choisi de graver la lettre ci-dessus")
	print("Appuyez sur n'importe quel bouton pour interrompre")

	global buttonflag
	buttonflag = True
	previous_uid = None
	while buttonflag :
		uid = pn532.read_passive_target(timeout=0.5)
		if uid is None :
			pass
		elif uid == previous_uid :
			pass
		else :
			previous_uid = uid
			lock_bytes = bin(pn532.ntag2xx_read_block(2)[2])
			n = len(lock_bytes)
			if n-2 > BLOCK and lock_bytes[n-1-BLOCK] == '1' :
				print("	/!\ Opération abandonnée /!\ ")
				print("Ce jeton ne peut plus être inscrit, il est en lecture seule")
			else :
				validate.play()
				data = bytes([entier, 0, 0, 0])
				pn532.ntag2xx_write_block(BLOCK, data)
				pn532.power_down()


# =================================================================================================
#                                      Reception
# =================================================================================================

def askUser() :
	code = 0
	print("Décrivez la lettre que vous voulez graver ou entrez q pour quitter.")
	print(f"A titre d'exemple, pour graver la lettre {chr(10279)} il faut entrer xxxoox")
	value = input("Votre entrée : ")
	if value == 'q' :
		return 0
	elif len(value) != 6 :
		return -1
	else :
		for i in range(6) :
			if value[i] == 'x' :
				code += 2**i
			elif value[i] != 'o' :
				return -2
		return code


# =================================================================================================
#                                      Script
# =================================================================================================

flag = True
while flag :
	a = askUser()
	if a < 0 :
		print("Entrée invalide, destruction dans 3", end=' ')
		time.sleep(1)
		print("2", end=' ')
		time.sleep(1)
		print("1")
		time.sleep(1)
		flag = False
	elif a > 0 :
		engraving(a)
	else :
		flag = False

GPIO.cleanup()

