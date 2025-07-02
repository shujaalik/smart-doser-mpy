from doser import Doser
import json
import machine
import ubinascii

doser = Doser()
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = "client_to_doser/"+client_id.decode()

def act(cmd, callback):
    cmd = json.loads(cmd)
    print("Got Message: ", cmd)
    if cmd["action"] == "SCAN":
        callback(topic_sub)
    if cmd["action"] == "SYNC":
        callback("ACK")
    elif cmd["action"] == "INSERT_DOSE":
        callback("ACK")
        dose = float(cmd["data"])
        doser.insert_dose(dose)
    elif cmd["action"] == "ROTATE":
        callback("ACK")
        rotations = int(cmd["data"])
        doser.rotate(rotations)
    elif cmd["action"] == "STOP":
        callback("ACK")
        doser.stop()
    elif cmd["action"] == "RUN_PROGRAM":
        callback("ACK")
        doser.run_schedule(cmd["data"]["dose"], cmd["data"]["interval"], cmd["data"]["intervalValue"])