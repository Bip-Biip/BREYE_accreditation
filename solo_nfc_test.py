import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = DigitalInOut(board.D6)
req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)
pn532.SAM_configuration()

print("Nous allons tester la détection des tag nfc.")
print("Présentez un jeton de votre choix.")

while True :
	uid = pn532.read_passive_target(timeout=0.5)
	if uid is None :
		pass
	else :
		print("Le jeton", pn532.ntag2xx_read_block(0), "a été détecté.")
		break
