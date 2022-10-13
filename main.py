from picam.load_cam import Cam
from lora.node_100_main import LoRa
import time

def main():
    
    print("open the cam")
    cam = Cam()
    
    # This LoRa can transmit 240bytes per packet. (maybe)
    print("open the LoRa")
    lora = LoRa()
    
    while True:
        #when sound sensor detect the gun sound
        print("ready to capture")
        
        pre = time.time()
        cam.capture()
        print("------------capture-----------")
        coordinates = cam.processing()
        print("----------get coordinates---------")
        
        lora.transmit(coordinates)
        aft = time.time()
        
        print(str(aft - pre) + " : seconds")
        print("Complete")
        
        time.sleep(10)
    
    
if __name__ == "__main__":
    main()



