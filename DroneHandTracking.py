import cv2
import mediapipe as mp
import time
#import HandTrackingModule as htm
import math
from cvzone.HandTrackingModule import HandDetector

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands = 2)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img) #draw #, flipType = FALSE if it's confusinf left/right
    #hands = detector.findHands(img, draw= False) #no draw
    #img = detector.findHands(img)
    # lmList = detector.findPosition(img)
    # if len(lmList) != 0:
    #     #print(lmList[4], lmList[8])
    #     hands1 = hands[0]
    #
    #     x1, y1 = lmList[4][1], lmList[4][2]
    #     x2, y2 = lmList[8][1], lmList[8][2]
    #     cx, cy = (x1+x2)//2, (y1+y2)//2
    #
    #     cv2.circle(img, (x1, y1), 13,  (255, 0 ,255), cv2.FILLED)
    #     cv2.circle(img, (x2, y2), 13, (255, 0, 255), cv2.FILLED)
    #     cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
    #     cv2.circle(img, (cx, cy), 13, (255, 0, 255), cv2.FILLED)
    #
    #     length = math.hypot(x2-x1, y2-y1)
    #     print(length)
    #
    #     if length < 50:
    #         cv2.circle(img, (cx, cy), 13, (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)