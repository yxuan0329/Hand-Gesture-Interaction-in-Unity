# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 20:23:34 2022

@author: xuan
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

# parameter
WIDTH, HEIGHT = 640, 360 # 1280, 720

# remember to open your webcam from laptop
cap = cv2.VideoCapture(0) # device number = 0
cap.set(3, WIDTH) # width 
cap.set(4, HEIGHT) # height

# hand detect
detector = HandDetector(maxHands=1, detectionCon=0.8)

# communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    # get the frame from webcam
    success, img = cap.read()
    
    # hands
    hands, img = detector.findHands(img)
    
    data = []
    
    # landmark values - (x, y, z) * 21
    if hands:
        # get first hand detected
        hand = hands[0]
        
        #get the landmark list
        lmList = hand['lmList']
        print(lmList)
        for lm in lmList:
            data.extend([lm[0], HEIGHT - lm[1], lm[2]]) # reverse y-dir
        #print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    
