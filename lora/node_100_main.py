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


class LoRa:
    """property
        old_settings, node, seconds, send_to_who
    """
    
    def __init__(self):
        
        print("property setting...")
        
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
        
        print("tty setting...")
        
        # self.old_settings = termios.tcgetattr(sys.stdin)
        # tty.setcbreak(sys.stdin.fileno())

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

    def sendImage(self, image):
        
        print("Transmitting an Image start ...")
        
        if len(image) == 0:
            print("Image is None")
        
        imageBytes = cv2.imencode('.jpg', image)[1].tobytes()
        
        print(imageBytes)
                        
        print("Creating package is completed")
        
        self.node.addr_temp = self.node.addr
        self.node.set(self.node.freq, self.send_to_who, self.node.power, self.node.rssi)
        
        print("ready to send complete")
        
        # if len(package) > 230:
            
        while len(imageBytes) > 230:
            self.node.send(str(imageBytes[:230]))
            del imageBytes[:230]
        
        self.node.send(str(imageBytes))
        print("------------sending finish-----------")
        # time.sleep(0.2)
        self.node.set(self.node.freq, self.node.addr_temp, self.node.power, self.node.rssi)

        
    def transmitImage(self, image):
        if len(image) != 0:
            print("Image is here")
            self.sendImage(image)
        
    def sendTest(self, index):
        
        temp = {}
        
        start = time.time()
        
        temp['time'] = start
        temp['count'] = index
        
        print("Transmitting start...")
        
        package = json.dumps(temp)

        print("creating a package is completed")

        self.node.addr_temp = self.node.addr
        self.node.set(self.node.freq, self.send_to_who, self.node.power, self.node.rssi)
        
        print("ready to send complete")
        
        self.node.send(package)
        print("------------sending finish-----------")
        # time.sleep(0.2)
        self.node.set(self.node.freq, self.node.addr_temp, self.node.power, self.node.rssi)


# old_settings = termios.tcgetattr(sys.stdin)
# tty.setcbreak(sys.stdin.fileno())


# #
# #    Need to disable the serial login shell and have to enable serial interface 
# #    command `sudo raspi-config`
# #    More details: see https://github.com/MithunHub/LoRa/blob/main/Basic%20Instruction.md
# #
# #    When the LoRaHAT is attached to RPi, the M0 and M1 jumpers of HAT should be removed.
# #


# #    The following is to obtain the temprature of the RPi CPU 
# def get_cpu_temp():
#     tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
#     cpu_temp = tempFile.read()
#     tempFile.close()
#     return float(cpu_temp)/1000

# #   serial_num
# #       PiZero, Pi3B+, and Pi4B use "/dev/ttyS0"
# #
# #    Frequency is [850 to 930], or [410 to 493] MHz
# #
# #    address is 0 to 65535
# #        under the same frequence,if set 65535,the node can receive 
# #        messages from another node of address is 0 to 65534 and similarly,
# #        the address 0 to 65534 of node can receive messages while 
# #        the another note of address is 65535 sends.
# #        otherwise two node must be same the address and frequence
# #
# #    The tramsmit power is {10, 13, 17, and 22} dBm
# #
# #    RSSI (receive signal strength indicator) is {True or False}
# #        It will print the RSSI value when it receives each message
# #

# #node = sx126x.sx126x(serial_num = "/dev/ttyS0",freq=433,addr=30,power=22,rssi=False)
# node = sx126x.sx126x(serial_num = "/dev/ttyS0",freq=915,addr=100,power=22,rssi=True)

# # def send_deal():
# #     get_rec = ""
# #     print("")
# #     print("input a string such as \033[1;32m20,Hello World\033[0m,it will send `Hello World` to node of address 20 ",flush=True)
# #     print("please input and press Enter key:",end='',flush=True)

# #     while True:
# #         rec = sys.stdin.read(1)
# #         if rec != None:
# #             if rec == '\x0a': break
# #             get_rec += rec
# #             sys.stdout.write(rec)
# #             sys.stdout.flush()

# #     get_t = get_rec.split(",")
    
# #     node.addr_temp = node.addr
# #     node.set(node.freq,int(get_t[0]),node.power,node.rssi)
# #     node.send(get_t[1])
# #     time.sleep(0.2)
# #     node.set(node.freq,node.addr_temp,node.power,node.rssi)

# #     print('\x1b[2A',end='\r')
# #     print(" "*100)
# #     print(" "*100)
# #     print(" "*100)
# #     print('\x1b[3A',end='\r')

# def send_deal():
#     get_rec = ""
#     # print("")
#     # print("input a coordinates such as \033[1;32m 30,200 \033[0m")
#     # print("please input and press Enter key:",end='',flush=True)
#     print("Transmitting start...")
    
#     global coordinates
#     print(type(coordinates))
#     if coordinates:
#         print("coordinates is None")
#     print("coordinates : " + coordinates)


#     # while True:
#     #     rec = sys.stdin.read(1)
#     #     if rec != None:
#     #         if rec == '\x0a': break
#     #         get_rec += rec
#     #         sys.stdout.write(rec)
#     #         sys.stdout.flush()
    
#     # get_t = get_rec.split(",")
#     # temp = {'x': get_t[0], 'y': get_t[1]}
#     package = json.dumps(coordinates)  # json을 문자열로 변환


#     node.addr_temp = node.addr
#     node.set(node.freq, 21, node.power, node.rssi)
#     node.send(package)
#     time.sleep(0.2)
#     node.set(node.freq, node.addr_temp, node.power, node.rssi)




# def send_cpu_continue(send_to_who,continue_or_not = True):
    
#     if continue_or_not:
#         global timer_task
#         global seconds
#         node.send_to = send_to_who
#         node.addr_temp = node.addr
#         node.set(node.freq,node.send_to,node.power,node.rssi)
#         node.send("CPU Temperature:"+str(get_cpu_temp())+" C")
#         time.sleep(0.2)
#         node.set(node.freq,node.addr_temp,node.power,node.rssi)
#         timer_task = Timer(seconds,send_cpu_continue,(send_to_who,))
#         timer_task.start()
#     else:
#         node.send_to = send_to_who
#         node.addr_temp = node.addr
#         node.set(node.freq,node.send_to,node.power,node.rssi)
#         node.send("CPU Temperature:"+str(get_cpu_temp())+" C")
#         time.sleep(0.2)
#         node.set(node.freq,node.addr_temp,node.power,node.rssi)
#         timer_task.cancel()
#         pass
    
# try:
#     time.sleep(1)
#     print("Press \033[1;32mEsc\033[0m to exit")
#     print("Press \033[1;32mi\033[0m   to send")
#     print("Press \033[1;32ms\033[0m   to send cpu temperature every 10 seconds")
    
#     # it will send every seconds(default is 10) seconds 
#     # send_to_who is the address of other node ( defult is 21)
#     send_to_who = 21 
#     seconds = 5
#     # timer_task = Timer(seconds,send_cpu_continue,(send_to_who,))
    
#     while True:

#         if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
#             c = sys.stdin.read(1)

#             # dectect key Esc
#             if c == '\x1b': break
#             # dectect key i
#             if c == '\x69':
#                 send_deal()
#             # dectect key s
#             if c == '\x73':
#                 print("Press \033[1;32mc\033[0m   to exit the send task")
#                 timer_task = Timer(seconds,send_cpu_continue,(send_to_who,))
#                 timer_task.start()
                
#                 while True:
#                     if sys.stdin.read(1) == '\x63':
#                         timer_task.cancel()
#                         print('\x1b[1A',end='\r')
#                         print(" "*100)
#                         print('\x1b[1A',end='\r')
#                         break

#             sys.stdout.flush()
            
            
#         node.receive()
        
#         # timer,send messages automatically
        
# except:
#     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
#     # print('\x1b[2A',end='\r')
#     # print(" "*100)
#     # print(" "*100)
#     # print('\x1b[2A',end='\r')

# termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
# # print('\x1b[2A',end='\r')
# # print(" "*100)
# # print(" "*100)
# # print('\x1b[2A',end='\r')
