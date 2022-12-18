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
        # get Packet for image capture and coordinate calculation
        value = lora.getPacket()
    
        # if sound is detected
        if value.get("sound") == 1:
            
            # get coordinate
            coordinate = cam.captureForCoordinate()
            
            # send coordinate to pi2
            lora.sendCoordinate(coordinate)
            print("-----coordinate is sent-----")
        
        # if user clicks start button on web
        if value.get("start") == 1:
            
            # get first picture
            imageBytes, width, height = cam.firstCapture()

            # send first image of target to pi2 using LoRa
            lora.sendImage(imageBytes, width, height)

            print("-----target's image is sent-----")
    
if __name__ == "__main__":
    main()
