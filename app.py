import cv2
import mediapipe as mp
import time
import pulsectl
import volcontrol_module


cap = cv2.VideoCapture(-1)
# gesture volume change - always to be declared outside the while loop
volcontrol = volcontrol_module.gestureVolumeChanger("./gesture_recognizer.task", 60) 

while True:
    success, img = cap.read()
    img = cv2.resize(img, (320, 240))
    volcontrol.gestureRecognize(img)
    volcontrol.changeVolume(img)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

