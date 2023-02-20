import time
import numpy as np
from time import sleep
from djitellopy import tello
import cv2
import HandTrackingModule as htm
import mediapipe as mp
import math

me = tello.Tello()
me.connect()
print(me.get_battery())


# me.takeoff()
# me.move_up(130)
# time.sleep(2.2)
me.streamon()

#faceTracking:
w, h = 360, 240
# cap = cv2.VideoCapture(0)
fbRange = [7000, 8000] # forward and backword range
pid = [0.4, 0.4, 0] #change these values if i can't find good results
pError = 0

#handTracking:
pTime = 0
cTime = 0
detector = htm.handDetector(detectionCon=0.7)

def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #for converting to grayscale
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8) # change those values for better results

    myFaceListC = []
    myFaceListArea = []

    if faces is None:
        return img, [[0, 0], 0]
    else:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cx = x + w//2
            cy = y + h//2
            area = w * h
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED )
            myFaceListC.append([cx, cy])
            myFaceListArea.append(area)

        if len(myFaceListArea) > 0:
            i = myFaceListArea.index(max(myFaceListArea))
            return img, [myFaceListC[i], myFaceListArea[i]]
        else:
            return img, [[0, 0], 0]

def trackFace(info, w, pid, pError):

    area = info[1]
    x,y = info[0]
    fb = 0

    error = x - w//2
    speed = pid[0] * error + pid [1]*(error-pError) # speed is yaw
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange [1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20
    if x == 0:
        speed = 0
        error = 0

    #print(speed, fb)
    print(area)
    me.send_rc_control(0, fb, 0, speed) # speed is yaw
    return error


while True:
    #faceTracking:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)

    #handTracking:
    #success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 5,  (255, 0 ,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        print(length)

        if length < 40:
            cv2.circle(img, (cx, cy), 6, (0, 255, 0), cv2.FILLED)
            me.flip_back()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        print("Q was clicked")
        break
