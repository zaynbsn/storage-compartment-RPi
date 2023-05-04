import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
from time import sleep

class NFC():
    def __init__(self, bus=0, device=0, spd=1000000):
        self.reader = SimpleMFRC522()
        self.close()
        self.boards = {}
        
        self.bus = bus
        self.device = device
        self.spd = spd

    def config(self):
        GPIO.setmode(GPIO.BCM)

    def cleanup(self):
        GPIO.cleanup()

    def reinit(self):
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        self.reader.READER.MFRC522_Init()

    def close(self):
        self.reader.READER.spi.close()

    def addBoard(self, rid, pin):
        self.boards[rid] = pin

    def selectBoard(self, rid):
        if not rid in self.boards:
            # print("readerid " + rid + " not found")
            return False

        for loop_id in self.boards:
            GPIO.setup(self.boards[loop_id], GPIO.OUT)
            GPIO.output(self.boards[loop_id], loop_id == rid)
        return True

    def read(self, rid):
        if not self.selectBoard(rid):
            return None

        self.reinit()
        cid, val = self.reader.read_no_block()
        self.close()

        return cid, val

    def write(self, rid, value):
        if not self.selectBoard(rid):
            return False

        self.reinit()
        self.reader.write_no_block(value)
        self.close()
        return True

GPIO.setmode(GPIO.BCM)


############################# USE
# nfc = NFC()
# nfc.addBoard("reader1",5)
# nfc.addBoard("reader2",6)

# try:
#     while True:
#         print("Hold a tag near the reader")
#         id, text = nfc.read("reader1")
#         id2, text2 = nfc.read("reader2")
#         print("ID: %s\nText: %s" % (id,text))
#         print("ID: %s\nText: %s" % (id2,text2))
#         sleep(1)
# except KeyboardInterrupt:
#     # GPIO.cleanup()
#     raise   