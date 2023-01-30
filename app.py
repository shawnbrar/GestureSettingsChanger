import cv2
import gestureSettingsChanger 


cap = cv2.VideoCapture(-1)
# gesture volume change - always to be declared outside the while loop
gestSettingsControl = gestureSettingsChanger.gestureSettingsChanger("./gesture_recognizer.task", 60) 

while True:
    success, img = cap.read()
    img = cv2.resize(img, (320, 240))
    # First recognize the gesture
    gestSettingsControl.gestureRecognize(img)
    # Second change the settings
    gestSettingsControl.changeSettings(img)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    # Press q to quit
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

