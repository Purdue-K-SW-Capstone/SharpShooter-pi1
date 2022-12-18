from lora.hslr import HSLR
import json

class LoRa:
    
    def __init__(self):
        
        self.SERIAL_NUMBER = "/dev/ttyS0"
        self.FREQUENCY = 915
        self.ADDRESS = 100
        self.POWER = 22
        self.RSSI = True
        
        self.SEND_TO_WHO = 21
        
        self.node = HSLR(serial_num=self.SERIAL_NUMBER, freq=self.FREQUENCY, addr=self.ADDRESS, power=self.POWER, rssi=self.RSSI)
        
    def sendImage(self, imageBytes, width, height):
        # imageBytes = bytearray()
        
        # for i in range(0, 2300):
        #     imageBytes += b'\x01'
                
        print(imageBytes)
        print("Image size : " + str(len(imageBytes)) + ", " + str(len(imageBytes)/1024) +"KB")
        print("width : " + str(width))
        print("height : " + str(height))
        
        # node setting
        self.node.addr_temp = self.node.ADDRESS
        self.node.set(self.node.FREQUENCY, self.SEND_TO_WHO, self.node.POWER, self.node.RSSI)
                
        # send the imageBytes
        self.node.transmitImage(imageBytes, width, height)
        
        self.node.set(self.node.FREQUENCY, self.node.addr_temp, self.node.POWER, self.node.RSSI)
    
    def sendCoordinate(self, coordinate):
        
        print("coordinate : " + str(coordinate))
        
        temp = {}
        
        if len(coordinate) != 0:
            temp['coordinate'] = coordinate
        
        payload = json.dumps(temp)

        # node setting
        self.node.addr_temp = self.node.ADDRESS
        self.node.set(self.node.FREQUENCY, self.SEND_TO_WHO, self.node.POWER, self.node.RSSI)
        
        # send the payload
        self.node.transmitCoordinate(payload)        

        self.node.set(self.node.FREQUENCY, self.node.addr_temp, self.node.POWER, self.node.RSSI)


    def getImage(self):
        
        while True:
            imageBytes = self.node.receiveImage()
            
            if imageBytes != None:
                break
        
        return imageBytes
    
    def getPacket(self):
        # can receive only
        # 1. {sound: True}
        # 2. {start: True}

        payload = self.node.receivePacket()
        
        if payload != None:
            # change byte to json
            result = json.loads(payload)
            
            return result
        
        return {}