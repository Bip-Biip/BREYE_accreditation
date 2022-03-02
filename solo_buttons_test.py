import time
import RPi.GPIO as GPIO

LEFT_PIN = 21
MIDDLE_PIN = 20
RIGHT_PIN = 16
WIFI_PIN = 1

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
