from picam.load_cam import Cam
from lora.node_100_main import LoRa
import time

# Sending coordinate code
# def main():
    
#     print("open the cam")
#     cam = Cam()
    
#     # This LoRa can transmit 240bytes per packet. (maybe)
#     print("open the LoRa")
#     lora = LoRa()
        
#     while True:
#         # #This code is for coordinates
        
#         #when sound sensor detect the gun sound
#         print("ready to capture")
        
#         cam.capture()
#         print("------------capture-----------")
#         coordinates = cam.processing()
#         print("----------get coordinates---------")
        
#         lora.transmit(coordinates)
        
#         print("Complete")
                
#         time.sleep(2)
        
        
# Sending Image code
def mainImage():       
     
    print("open the cam")
    cam = Cam()
    
    # This LoRa can transmit 240bytes per packet. (maybe)
    print("open the LoRa")
    lora = LoRa()
        
    #This code is for Transmitting Image
    
    print("ready to capture")
    
    # pre = time.time()
    print("------------capture-----------")
    cam.capture()
    print("----------get image---------")
    image = cam.getImage()
    
    lora.transmitImage(image)
    
    # aft = time.time()
    
    # print(str(aft - pre) + " : seconds")
    print("Complete")
    
    
    
def captureAndSendCoordinate():
    
    cam = Cam()
    print("-------cam is opened-------")

    INDEX = 1
    
    while True: 

        cam.capture()
        print("------------captured--------------")
        
        coordinate = cam.processing()
        print("-------coordinate is gotten--------")
        
        lora.sendCoordinate(INDEX, coordinate)
        INDEX+=1
        print("---------complete---------")
        time.sleep(3)

def processAndSendImage(lora):
    
    cam = Cam()
    print("-------cam is opened-------")
    
    print("------------capture-----------")
    cam.capture()
    print("----------get image---------")
    image = cam.getImage()
    
    if len(image) == 0:
        print("can't get an image")
        pass
    
    lora.sendImage(image)
    
    
    

if __name__ == "__main__":
    
    cam = Cam()
    
    # dependency injection
    lora = LoRa(cam)
    print("LoRa is opened")
    
    # for test
    # imageBytes = cam.firstCapture()
    # lora.sendImage()
    
    
    while True:
        # 방법 1. receive 로직에 총소리, tablet start버튼을 받는 로직을 둘 다 넣어 놓는다.
        # 방법 2. 그냥 main함수 while문에서 receiveSoundValue함수와 receiveStartBtn함수를 실시간으로 실행시킨다.
        # as I see, The way 1 is better than way 2
        
        # receiving the sound value(True or False) constantly

        value = lora.getPacket()
        
        if value.get("sound") == 1:
            print(value)
            lora.sendCoordinate()
            print("-----coordinate is sent-----")
        
        if value.get("start") == 1:
            print(value)
            lora.sendImage()
            print("-----target's image is sent-----") 

        # if it is a gun sound, we take a picture and send the coordinate to pi2.
        # if value == Gunsound:
        # captureAndSendCoordinate(lora)
            
        # if start button on tablet is clicked, we send a target image to pi2.
        # if value == StartBtn
        # processAndSendImage(lora)
