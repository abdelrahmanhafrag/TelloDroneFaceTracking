from djitellopy import tello

from time import sleep

me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()
# me.takeoff()

# if cv2.waitkey(1) & 0xFF == ord('q'):
#     me.land()
# sleep(20)
# me.land()

while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
