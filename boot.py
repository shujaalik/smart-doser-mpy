from doser import Doser
from bt import BLE
from constants import DEVICE_NAME

doser = Doser()

def callback(cmd):
    print("Got Message: ", cmd)

bt = BLE(DEVICE_NAME, callback)