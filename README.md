# Gesture Volume Changer

A python module to change the volume of a computer using gestures. The module uses `opencv` to get the live video stream, the `mediapipe` library to recognize the gestures and then the `pulsectl` library to change the volume of the computer.	

## Getting Started
Below is an example of how use can use the module. First we import the `cv2` and `gestureVolumeChanger` modules

    import cv2
    import gestureVolumeChanger

Then we get the video live stream from the webcam. In my computer it was with `-1`, so I've specified as following:
  
    cap = cv2.VideoCapture(-1)

Then we initialize the `gestureVolumeChanger` object from the `gestureVolumeChanger` module as follows:

    # gesture volume change - always to be declared outside the while loop
    gestVolControl = gestureVolumeChanger.gestureVolumeChanger("./gesture_recognizer.task", 60)

Then we specify our main while loop which will first read the live video  stream, secondly recognize the gesture and then change the volume according to it.

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

This example has been provided in the `app.py` file.

To run the `app.py` file, you can use the following command

    python app.py

or 

    python3 app.py

## Gestures

A close fist with fingers in the front is recognized as a stop gesture. If you do this, then, the volume will not change. 

To change the volume bring together your index and thumb finger or move them apart.

##  Further Development

There are still features which are to be added. Such as:-

1. Smoother volume changes
2. Addition of volume bar
3. Better FPS
4. Add windows and mac support
