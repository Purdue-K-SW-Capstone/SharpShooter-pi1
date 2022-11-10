#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
#    this is an UART-LoRa device and thers is an firmware on Module
#    users can transfer or receive the data directly by UART and dont
#    need to set parameters like coderate,spread factor,etc.
#    |============================================ |
#    |   It does not suport LoRaWAN protocol !!!   |
#    | ============================================|
#   
#    This script is mainly for Raspberry Pi 3B+, 4B, and Zero series
#    Since PC/Laptop does not have GPIO to control HAT, it should be configured by
#    GUI and while setting the jumpers, 
#    Please refer to another script pc_main.py
#

import sys
from . import sx126x
import threading
import time
import select
import termios
import tty
from threading import Timer
import cv2

import json
import struct

# from picam.load_cam import Cam

class LoRa:
    """property
        old_settings, node, seconds, send_to_who
    """
    
    def __init__(self, cam):
        
        print("property setting...")

        self.cam = cam
        
        #The following should be 238 bytes in total.
        #packet_size, timebytes
        self.packet_size = 234
        self.timebytes = 4
        
        self.serial_num = "/dev/ttyS0"
        self.freq = 915
        # self.freq = 433
        # send to who
        self.addr = 100
        self.power = 22
        self.rssi = True
        
        # it will send every seconds(default is 10) seconds 
        # send_to_who is the address of other node ( defult is 21)
        self.send_to_who = 21
        self.seconds = 5

        print("node setting...")
        self.node = sx126x.sx126x(serial_num = self.serial_num, freq=self.freq, addr=self.addr, power=self.power, rssi=self.rssi)
    
    def send_deal(self, coordinates):
        
        print("Transmitting start...")
        
        if not coordinates:
            print("coordinates is None")
        print(coordinates)

        package = json.dumps(coordinates)  # json을 문자열로 변환

        print("creating a package is completed")

        self.node.addr_temp = self.node.addr
        self.node.set(self.node.freq, self.send_to_who, self.node.power, self.node.rssi)
        
        print("ready to send complete")
        
        self.node.send(package)
        print("------------sending finish-----------")
        # time.sleep(0.2)
        self.node.set(self.node.freq, self.node.addr_temp, self.node.power, self.node.rssi)

    def transmit(self, coordinates):
        
        try:
            # time.sleep(1)
            
            if coordinates:        
                print("coordinates is here")            
                self.send_deal(coordinates)
                
            print("-----------Receiving----------")
            
            self.node.receive()
        
        except:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)


    # For sending Image
    # def sendImage(self, image):
        
    #     # package = []

    #     print("Transmitting an Image start ...")
        
    #     if len(image) == 0:
    #         print("Image is None")
        
    #     imageBytes = cv2.imencode('.jpg', image)[1].tobytes()
    #     # print(imageBytes)
        
    #     # print("Creating package is completed")
        
    #     self.node.addr_temp = self.node.addr
    #     self.node.set(self.node.freq, self.send_to_who, self.node.power, self.node.rssi)
        
    #     print("ready to send complete")

    #     print("image size : " + str(len(imageBytes)/1024) + "KB")
        
    #     for i in range(int(len(imageBytes)/230) + 1):

    #         package = []

    #         if i == int(len(imageBytes)/230):
    #             package.append(i)
    #             package.append(imageBytes[i*230:len(imageBytes)])

    #         package.append(i)

    #         package.append(imageBytes[i*230:(i+1)*230])

    #         # package = json.dumps(package)
    #         package.append("}")

    #         package = "".join(map(str, package))

    #         print(package)

    #         print(len(package))

    #         self.node.send(package)
    #         time.sleep(10)
    #         # self.node.send(str(imageBytes[i*230:(i+1)*230]))
            
    #     # while len(imageBytes) > 230:
    #     #     self.node.send(str(imageBytes[:230]))
    #     #     del imageBytes[:230]
        
    #     # self.node.send(str(imageBytes))
    #     print("------------sending finish-----------")
    #     # time.sleep(0.2)
    #     self.node.set(self.node.freq, self.node.addr_temp, self.node.power, self.node.rssi)

    def sendImageTest(self, image):
        
        print("Transmitting an Image start ...")
        
        if len(image) == 0:
            print("Image is None")
        
        imageBytes = cv2.imencode('.jpg', image)[1].tobytes()
        
        self.node.addr_temp = self.node.addr
        self.node.set(self.node.freq, self.send_to_who, self.node.power, self.node.rssi)
        
        print("ready to send complete")

        print("image size : " + str(len(imageBytes)/1024) + "KB")

        for i in range(int(len(imageBytes)/self.packet_size) + 1):

            print(time.time())
            curTime = round(time.time() - 1640000000, 3)
            print(curTime)
            
            # > is bigEndian
            packet = struct.pack(">f", curTime)  #4bytes

            c = struct.unpack(">f", packet)
            print(c)

            if i != int(len(imageBytes)/self.packet_size):

                print(imageBytes[i*self.packet_size:(i+1)*self.packet_size])
                print(len(imageBytes[i*self.packet_size:(i+1)*self.packet_size]))
        
                packet = packet + imageBytes[i*self.packet_size:(i+1)*self.packet_size]
        
                self.node.sendBytes(packet)
                print(i)
                time.sleep(1)
            else:
                print(imageBytes[i*self.packet_size:-1])
                print(len(imageBytes[i*self.packet_size:-1]))

                self.node.sendBytes(imageBytes[i*self.packet_size:-1])
                print(i)

        print("------------sending finish-----------")
        # time.sleep(0.2)
        self.node.set(self.node.freq, self.node.addr_temp, self.node.power, self.node.rssi)

        
        
    def transmitImage(self, image):
        if len(image) != 0:
            print("Image is here")
            # self.sendImage(image)
            self.sendImageTest(image)
    
    # # This is for test
    # def sendCoordinate(self, index, coordinate):
        
    #     temp = {}
        
    #     start = time.time()
        
    #     temp['time'] = start
    #     temp['count'] = index
    #     temp['coordinate'] = coordinate
        
    #     print("Transmitting start...")
        
    #     package = json.dumps(temp)

    #     print("creating a package is completed")

    #     self.node.addr_temp = self.node.addr
    #     self.node.set(self.node.freq, self.send_to_who, self.node.power, self.node.rssi)
        
    #     print("ready to send complete")
        
    #     self.node.send(package)
    #     print("------------sending finish-----------")
    #     # time.sleep(0.2)
    #     self.node.set(self.node.freq, self.node.addr_temp, self.node.power, self.node.rssi)

    # def sendImage(self, image):
        
    #     print("Transmitting an Image start ...")
        
    #     imageBytes = cv2.imencode('.jpg', image)[1].tobytes()
        
    #     self.node.addr_temp = self.node.addr
    #     self.node.set(self.node.freq, self.send_to_who, self.node.power, self.node.rssi)
        
    #     print("ready to send complete")

    #     print("image size : " + str(len(imageBytes)/1024) + "KB")

    #     for i in range(int(len(imageBytes)/self.packet_size) + 1):

    #         print(time.time())
    #         curTime = round(time.time() - 1640000000, 3)
    #         print(curTime)
            
    #         # > is bigEndian
    #         packet = struct.pack(">f", curTime)  #4bytes

    #         c = struct.unpack(">f", packet)
    #         print(c)

    #         if i != int(len(imageBytes)/self.packet_size):

    #             print(imageBytes[i*self.packet_size:(i+1)*self.packet_size])
    #             print(len(imageBytes[i*self.packet_size:(i+1)*self.packet_size]))
        
    #             packet = packet + imageBytes[i*self.packet_size:(i+1)*self.packet_size]
        
    #             self.node.sendBytes(packet)
    #             print(i)
    #             time.sleep(1)
    #         else:
    #             print(imageBytes[i*self.packet_size:-1])
    #             print(len(imageBytes[i*self.packet_size:-1]))

    #             self.node.sendBytes(imageBytes[i*self.packet_size:-1])
    #             print(i)

    #     print("------------sending finish-----------")
    #     # time.sleep(0.2)
    #     self.node.set(self.node.freq, self.node.addr_temp, self.node.power, self.node.rssi)
        
    def sendCoordinate(self):
        
        # get coordinate from Cam        
        coordinate = self.cam.captureForCoordinate()
        
        temp = {}
        
        # start = time.time()
        
        # temp['time'] = start
        
        if len(coordinate) != 0:
            xyCoordinate = [coordinate['x'], coordinate['y']]
            temp['coordinate'] = xyCoordinate
            # temp['x'] = coordinate['x']
            # temp['y'] = coordinate['y']
        payload = json.dumps(temp)

        print(payload)
        self.node.addr_temp = self.node.addr
        self.node.set(self.node.freq, self.send_to_who, self.node.power, self.node.rssi)

        # send the payload
        self.node.transmitCoordinate(payload)        

        self.node.set(self.node.freq, self.node.addr_temp, self.node.power, self.node.rssi)

    def sendImage(self):
        
        # get imageBytes from Cam
        # imageBytes = self.cam.firstCapture()
        
        # for test
        # image = cv2.imread('./lora/test.jpg')
        # imageBytes = cv2.imencode('.jpg', image)[1].tobytes()
 
        imageBytes = self.cam.firstCapture()
    
        print("imageBytes")
        print(imageBytes)
        print(str(len(imageBytes)/1024) + "KB")
        print("------------------")
    
        self.node.addr_temp = self.node.addr
        self.node.set(self.node.freq, self.send_to_who, self.node.power, self.node.rssi)
       
        # send the imageBytes
        self.node.transmitImageBytes(imageBytes)
        
        self.node.set(self.node.freq, self.node.addr_temp, self.node.power, self.node.rssi)

    def getPacket(self):
        # can receive only
        # 1. sound value({sound: True})
        # 2. start button({start: True})
        
        # type: string(json)
        
        processed = self.node.receive()
        
        if processed != None:
            result = json.loads(processed)
            # print(result)
            
            return result
        
        return {}
