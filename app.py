import cv2
import gestureVolumeChanger


cap = cv2.VideoCapture(-1)
# gesture volume change - always to be declared outside the while loop
gestVolControl = gestureVolumeChanger.gestureVolumeChanger("./gesture_recognizer.task", 60) 

while True:
    success, img = cap.read()
    img = cv2.resize(img, (320, 240))
    # First recognize the gesture
    gestVolControl.gestureRecognize(img)
    # Second change the volume
    gestVolControl.changeVolume(img)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    # Press q to quit
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

