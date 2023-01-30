# Gesture Settings Changer

A python module to change the volume of a computer using gestures. The module uses `opencv` to get the live video stream, the `mediapipe` library to recognize the gestures and then the `pulsectl` library to change the volume/brightness of the computer.	

## Getting Started
Below is an example of how use can use the module. First we import the `cv2` and `gestureSettingsChanger` modules

    import cv2
    import gestureSettingsChanger

Then we get the video live stream from the webcam. In my computer it was with `-1`, so I've specified as following:
  
    cap = cv2.VideoCapture(-1)

Then we initialize the `gestureSettingsChanger` object from the `gestureSettingsChanger` module as follows:

    # gesture settingse changer - always to be declared outside the while loop
    gestSettingsControl = gestureSettingsChanger.gestureSettingsChanger("./gesture_recognizer.task", 60) 

Then we specify our main while loop which will first read the live video  stream, secondly recognize the gesture and then change the volume/brightness according to it.

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

This example has been provided in the `app.py` file.

To run the `app.py` file, you can use the following command

    python app.py

or 

    python3 app.py

## Gestures

Right hand should be used to control the volume and the left hand should be used to control the brightness. A close fist with fingers in the front is recognized as a stop gesture. If you do this with either hand, then, the volume/brightness will not change. 

To change the volume/brightness bring together your index and thumb finger or move them apart.

## Supported hardware
This program is tested on a Ubuntu 22.04. It may work on other linux distribution. Development for Windows and Mac will take time.

##  Further Development

There are still features which are to be added. Such as:-

1. Smoother volume and brightness changes
2. Addition of volume and brightness bar
3. Better FPS
4. Add windows and mac support
