import os
import typing
import screen_brightness_control as sbc
import cv2
import mediapipe as mp
import pulsectl
import numpy as np

class gestureSettingsChanger:
    '''
    A class to change computer brightness and volume using gestures. To be always initialized outside the while loop.
    ...

    Attributes:
        gesture_recognizer_task_path : str
            path to the trained model
        threshold : int
            threshold for increasing a setting or decreassing a setting

    Methods
        gestureRecognize(img: np.ndarray)
            recognize the gesture in the image
        changeSettings(img: np.ndarray)
            increase or decrease the brightness/volume given an image
    '''

    def __init__(self, gesture_recognizer_task_path: str, threshold: int = 60) -> None:
        '''
        Initializes class attributes
        
        Args:
            gesture_recognizer_task_path : str
                path to the trained model bundled
            threshold : int
                threshold for increasing a setting or decreasing a setting

        Returns:
            None
        '''
        self.gesture_recognizer_task_path = gesture_recognizer_task_path
        self.threshold = threshold
        self.gestureResult = ''
        self.options = mp.tasks.vision.GestureRecognizerOptions(
                base_options=mp.tasks.BaseOptions(model_asset_path=self.gesture_recognizer_task_path),
                running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
                min_hand_detection_confidence = 0.3,
                result_callback=self._print_result
                )
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands = 2)
        self.mpDraw = mp.solutions.drawing_utils
        self.pulse = pulsectl.Pulse('volume_changer')
        self.sink = self.pulse.sink_list()[0]

    def _print_result(self, result: mp.tasks.vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        for gesture in result.gestures:
            self.gestureResult = [category.category_name for category in gesture][0]
        #print(self.gestureResult)

    def gestureRecognize(self, img: np.ndarray) -> None:
        '''
        Recognize the gesture in the image

        Args:
            img : np.ndarray
                an image
        
        Returns:
            None

        '''
        mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = img)
        with mp.tasks.vision.GestureRecognizer.create_from_options(self.options) as recognizer:
            recognizer.recognize_async(mp_image, 10)

    def changeSettings(self, img: np.ndarray) -> None:
        '''
        Change the brightness and volume levels

        Args:
            img : np.ndarray
                an image

        Returns:
            None
        '''
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if self.gestureResult != 'Closed_Fist':
            results = self.hands.process(imgRGB)
            # Right hand is detected as left
            if results.multi_handedness is not None and results.multi_handedness[0].classification[0].label == 'Left':
                self._rightHandVolChanger(results, img)
            # Left Hand is detected as right
            elif results.multi_handedness is not None and results.multi_handedness[0].classification[0].label == 'Right':
                self._leftHandBrightnessChanger(results, img)

    def _findDistance(self, results, img: np.ndarray) -> typing.Tuple[float, int, int]:
        thumb = results.multi_hand_landmarks[0].landmark[4]
        index = results.multi_hand_landmarks[0].landmark[8]
        thumb = {'x': round(thumb.x * img.shape[1]), 'y': round(thumb.y * img.shape[0])}
        index = {'x': round(index.x * img.shape[1]), 'y': round(index.y * img.shape[0])}
        distance = ((thumb['x'] - index['x']) ** 2 + (thumb['y'] - index['y']) ** 2) ** 0.5
        text_x, text_y = int((thumb['x'] + index['x'])/2), int((thumb['y'] + index['y'])/2)
        return distance, text_x, text_y

    def _rightHandVolChanger(self, results, img: np.ndarray) -> None:
        distance, text_x, text_y = self._findDistance(results, img)
        volume_change = 0.02 if distance > self.threshold else -0.02
        if self.pulse.volume_get_all_chans(self.sink) > 1:
            self.pulse.volume_set_all_chans(self.sink, 1)
        else:
            self.pulse.volume_change_all_chans(self.sink, volume_change)
        cv2.putText(img, str(int(round(self.pulse.volume_get_all_chans(self.sink), 2) * 100)), (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
        self.mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], self.mpHands.HAND_CONNECTIONS)

    def _leftHandBrightnessChanger(self, results, img: np.ndarray) -> None:
        distance, text_x, text_y = self._findDistance(results, img)
        current_brightness = sbc.get_brightness()[0]
        set_brightness_value = current_brightness + 5 if distance > self.threshold else current_brightness - 5
        if set_brightness_value > 100:
            os.system('gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 ' + str(100) + '>"')
        else:
            os.system('gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 '+ str(set_brightness_value) + '>"')
        cv2.putText(img, str(current_brightness), (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
        self.mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], self.mpHands.HAND_CONNECTIONS)
