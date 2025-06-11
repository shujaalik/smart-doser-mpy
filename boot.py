from doser import Doser
from bt import BLE
from constants import DEVICE_NAME
import json

doser = Doser()

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
    cmd = json.loads(cmd)
    print("Got Message: ", cmd)
    if cmd["action"] == "SYNC":
        bt.send("ACK")
    elif cmd["action"] == "INSERT_DOSE":
        bt.send("ACK")
        dose = float(cmd["data"])
        doser.insert_dose(dose)
    elif cmd["action"] == "ROTATE":
        bt.send("ACK")
        rotations = int(cmd["data"])
        doser.rotate(rotations)

bt = BLE(DEVICE_NAME, ble_handler)