# camera.py
import cv2
import mediapipe as mp
import csv
import os

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "static", "hand_gesture_data")
os.makedirs(DATA_DIR, exist_ok=True)

class VideoCamera1(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            self.video.release()
            raise RuntimeError("Could not open the webcam.")
    
    def __del__(self):
        if hasattr(self, "video"):
            self.video.release()
        
    
    def get_frame(self):
        ret, frame = self.video.read()
        if not ret or frame is None:
            raise RuntimeError("Could not read a frame from the webcam.")

        frame = cv2.flip(frame, 1)

        with open(os.path.join(BASE_DIR, "static", "label.txt"), encoding="utf-8") as ff:
            glabel=ff.read()

        with open(os.path.join(BASE_DIR, "static", "label1.txt"), encoding="utf-8") as ff:
            gfile=ff.read()
      
        GESTURE_LABEL = glabel  # Change for different gestures
        if not gfile:
            raise RuntimeError("No gesture sample file is selected.")
        FILE_NAME = os.path.join(DATA_DIR, f"{gfile}")


        with open(FILE_NAME, mode="a", newline="") as f:
            writer = csv.writer(f)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Extract hand landmark data
                    landmark_list = []
                    for lm in hand_landmarks.landmark:
                        landmark_list.extend([lm.x, lm.y, lm.z])

                    # Save to CSV
                    writer.writerow(landmark_list)

            cv2.putText(frame, f"Recording: {GESTURE_LABEL}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            
        
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            raise RuntimeError("Could not encode the webcam frame.")
        return jpeg.tobytes()
