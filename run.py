from clientWS import ClientWS
from threading import Thread
from RfidReader import NFC
from time import sleep
import RPi.GPIO as GPIO
import subprocess

sleep(5)

# subprocess.call(['python3','BLEConnect.py'])

LED_RED = 17
LED_GREEN = 22
GPIO.setup(LED_RED, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(LED_GREEN, GPIO.OUT, initial= GPIO.HIGH)

############################ websocket connect
print('connecting...')
client = ClientWS('ws://192.168.20.143:80')
# client = ClientWS('ws://192.168.71.143:80')
thread = Thread(target=client.start)
thread.start()

############################ RFID reader

nfc = NFC()
nfc.addBoard("reader1",5)
nfc.addBoard("reader2",6)

try:
    while True:
        print("Hold a tag near the reader")
        id, text = nfc.read("reader1")
        id2, text2 = nfc.read("reader2")
        print("ID: %s\nText: %s" % (id,text))
        print("ID: %s\nText: %s" % (id2,text2))
        if text != None or text2 != None:
            GPIO.output(LED_GREEN,GPIO.HIGH)
            GPIO.output(LED_RED,GPIO.LOW)
        else:
            GPIO.output(LED_RED,GPIO.HIGH)
            GPIO.output(LED_GREEN,GPIO.LOW)
        sleep(1)
except KeyboardInterrupt:
    nfc.cleanup()
    raise