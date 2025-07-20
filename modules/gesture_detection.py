import cv2
import mediapipe as mp
from mediapipe.tasks import python
import time
import numpy as np
import os

class GestureRecognizer:
    def __init__(self):
        """
        Initializes the gesture recognizer with hardcoded configuration.
        """
        self.num_hands = 1

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(current_dir, "gesture_recognizer.task")

        self.min_detection_confidence = 0.65
        self.min_tracking_confidence = 0.65

        # Mediapipe Gesture Recognizer setup
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = GestureRecognizerOptions(
            base_options=python.BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.IMAGE,
            num_hands=self.num_hands
        )
        self.recognizer = GestureRecognizer.create_from_options(options)

        # MediaPipe Hands setup (optional drawing)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.num_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )

        # State buffer
        self.prev_gestures = []
        self.stable_gesture = None
        self.buffer_size = 4  # Number of consecutive detections for stability

    def get_gesture(self, image):
        """
        Detects and returns the gesture name from a given full image.
        """
        gesture_name = "None"
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                recognition_result = self.recognizer.recognize(mp_image)
                gesture_name = self.handle_gesture_result(recognition_result)
        return gesture_name

    def handle_gesture_result(self, result):
        """
        Extracts the first recognized gesture name from the result.
        """
        if result and any(result.gestures):
            for single_hand_gesture_data in result.gestures:
                return single_hand_gesture_data[0].category_name
        return "None"

    def get_stable_gesture(self, current_gesture):
        """
        Returns a stable gesture only if same gesture is repeated buffer_size times.
        """
        if current_gesture == "None":
            self.prev_gestures.clear()
            self.stable_gesture = None
            return None

        self.prev_gestures.append(current_gesture)
        if len(self.prev_gestures) > self.buffer_size:
            self.prev_gestures.pop(0)

        if len(self.prev_gestures) == self.buffer_size and all(g == self.prev_gestures[0] for g in self.prev_gestures):
            if self.stable_gesture != self.prev_gestures[0]:
                self.stable_gesture = self.prev_gestures[0]
                return self.stable_gesture

        return None


if __name__ == "__main__":
    recognizer = GestureRecognizer()
    img_path = "/home/hitech/music_website/modules/thumbup.jpeg"
    img = cv2.imread(img_path)
    gesture = recognizer.get_gesture(img)
    print(gesture)
        
    
    

    
    


