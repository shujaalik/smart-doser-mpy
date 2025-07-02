from bt import BLE
from wifi import Wifi
from constants import DEVICE_NAME
from actor import act

prev_message = None
def ble_handler(cmd):
    global prev_message
    if cmd[-1] == "&":
        if prev_message is None:
            prev_message = cmd.replace("&", "")
        else:
            prev_message = prev_message + cmd.replace("&", "")
        return
    elif prev_message is not None:
        prev_message = prev_message + cmd.replace("&", "")
        cmd = prev_message
        prev_message = None
    print(cmd)
    act(cmd, bt.send)

bt = BLE(DEVICE_NAME, ble_handler)
wifi = Wifi()