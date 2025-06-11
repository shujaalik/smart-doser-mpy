from machine import Pin, Timer
import ubluetooth
from time import sleep_ms

class BLE():
    def __init__(self, name, callback):
        # Create internal objects for the onboard LED
        # blinking when no BLE device is connected
        # stable ON when connected
        self.callback = callback
        self.name = name
        self.ble = ubluetooth.BLE()
        self.connect()
        
    def connect(self):
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()
    
    def connected(self):
        print("BLE connected")
    
    def disconnect(self):
        print("BLE disconnected")
        self.ble.active(False)

    def ble_irq(self, event, data):
        if event == 1:
            self.connected()

        elif event == 2:
            self.advertiser()
        
        elif event == 3:         
            buffer = self.ble.gatts_read(self.rx)
            ble_msg = buffer.decode('UTF-8')
            self.callback(ble_msg)
            
    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        print("Send: ", data)
        if type(data).__name__ == "list":
            self.ble.gatts_notify(0, self.tx, "START")
            sleep_ms(100)
            for item in data:
                self.ble.gatts_notify(0, self.tx, str(item))
                sleep_ms(100)
            self.ble.gatts_notify(0, self.tx, "END")
        elif type(data).__name__ == "str":
            self.ble.gatts_notify(0, self.tx, data)

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(f"Bluetooth on by name: {self.name}")