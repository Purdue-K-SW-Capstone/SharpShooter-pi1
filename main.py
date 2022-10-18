from picam.load_cam import Cam
from lora.node_100_main import LoRa
import time

# Seding coordinate code
def main():
    
    print("open the cam")
    cam = Cam()
    
    # This LoRa can transmit 240bytes per packet. (maybe)
    print("open the LoRa")
    lora = LoRa()
        
    while True:
        # #This code is for coordinates
        
        #when sound sensor detect the gun sound
        print("ready to capture")
        
        cam.capture()
        print("------------capture-----------")
        coordinates = cam.processing()
        print("----------get coordinates---------")
        
        lora.transmit(coordinates)
        
        print("Complete")
                
        time.sleep(2)
        
        
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
    
    
    
#This code is for Test
def mainTest():
    
    print("open the LoRa")
    lora = LoRa()
    
    INDEX = 1
    
    while True: 
        lora.sendTest(INDEX)
        INDEX+=1
        print("---------complete---------")
        time.sleep(3)
            
    
    
if __name__ == "__main__":
    # main()
    mainImage()
    # mainTest()