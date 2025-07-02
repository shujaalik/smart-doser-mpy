import network
from constants import DEVICE_NAME, SSID, PASS
from umqttsimple import MQTTClient
import ubinascii
import machine
from time import sleep
import gc
import _thread
from actor import act
gc.collect()

station = network.WLAN(network.STA_IF)
station.active(True)
station.config(dhcp_hostname=str(DEVICE_NAME))

mqtt_server = 'broker.hivemq.com'
client_id = ubinascii.hexlify(machine.unique_id())
scan_topic_sub = "client_to_doser/broadcast"
scan_topic_pub = "doser_to_client/broadcast"
topic_sub = "client_to_doser/"+client_id.decode()
topic_pub = "doser_to_client/"+client_id.decode()

class Wifi:
    def __init__(self):
        self.client = None
        self.mqtt_connected = False
        _thread.start_new_thread(self.run, ())
    
    def run(self):
        while True:
            if self.mqtt_connected == False:
                if not station.isconnected():
                    if not self.connect():
                        continue
                else:
                    try:
                        self.connect_mqtt()
                    except OSError as e:
                        print("error connecting MQTT: ", e)
                        gc.collect()
                        self.client = None
                        self.mqtt_connected = False
                        sleep(1)
            else:
                try:
                    self.client.check_msg()
                except OSError as e:
                    print("error checking MQTT: ", e)
                    gc.collect()
                    self.client = None
                    self.mqtt_connected = False
                    sleep(1)
    
    def broadcast_publish(self, msg):
        self.client.publish(scan_topic_pub, msg)
    
    def publish_direct(self, msg):
        self.client.publish(topic_pub, msg)
    
    def connect(self):
        try:
            print("Connecting to wifi...")
            station.active(False)
            sleep(0.1)
            station.active(True)
            station.connect(SSID, PASS)
            count = 0
            while not station.isconnected():
                count += 1
                sleep(0.1)
                if count > 70:
                    return False
            print("connected with Local IP: ", station.ifconfig()[0])
            return True
        except BaseException as e:
            print("error connecting to wifi: \n", e)
            return False
    
    def sub_cb(self, topic, msg):
        try:
            print((topic, msg))
            cmd = msg
            print("Got MQTT Message: ", cmd)
            act(cmd, self.publish_direct if topic.decode() == topic_sub else self.broadcast_publish)
        except Exception as e:
            print("Error in Message: ", e)
        
    def connect_mqtt(self):
        print("Connecting to mqtt...")
        client = MQTTClient(client_id, mqtt_server)
        client.set_callback(self.sub_cb)
        client.connect()
        client.subscribe(topic_sub)
        client.subscribe(scan_topic_sub)
        print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
        self.client = client
        self.mqtt_connected = True

