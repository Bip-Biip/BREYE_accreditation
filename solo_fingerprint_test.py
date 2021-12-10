import serial
import adafruit_fingerprint

uart = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
if finger.read_templates() != adafruit_fingerprint.OK :
	print("Erreur à la lecture des templates d'empreinte")


print("Nous allons tester le détecteur d'empreinte.")
print("Il est censé s'illuminer si il s'agit du même modèle.")
print("Placez votre doigt dessus pour l'éteindre.")
while finger.get_image() != adafruit_fingerprint.OK :
	pass
if finger.image_2_tz(1) == adafruit_fingerprint.OK :
	print("Je confirme, ceci est un doigt.")
