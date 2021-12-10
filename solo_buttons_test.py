import time
import RPi.GPIO as GPIO

LEFT_PIN = 21
MIDDLE_PIN = 20
RIGHT_PIN = 16


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
