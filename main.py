from picam.load_cam import Cam
from lora.lora import LoRa

def main():
    
    # open the camera
    cam = Cam()
    print("Cam is opened")
    
    # open the LoRa
    lora = LoRa()
    print("LoRa is opened")
    
    while True:
        
        value = lora.getPacket()
    
        if value.get("sound") == 1:

            coordinate = cam.captureForCoordinate()
            
            lora.sendCoordinate(coordinate)
            print("-----coordinate is sent-----")
        
        if value.get("start") == 1:
            # get first picture
            imageBytes, width, height = cam.firstCapture()

            lora.sendImage(imageBytes, width, height)

            print("-----target's image is sent-----")

def test():
    # open the camera
    cam = Cam()
    print("Cam is opened")
    
    imageBytes, width, height = cam.firstCapture()

    
    lora = LoRa()
    print("LoRa is opened")
    
    lora.sendImage(imageBytes, width, height)

    
if __name__ == "__main__":
    main()
    # test()