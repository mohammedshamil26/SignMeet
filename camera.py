# camera.py
import joblib
import cv2
import mediapipe as mp
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

model = joblib.load(os.path.join(BASE_DIR, "gesture_model.pkl"))
gesture_map = joblib.load(os.path.join(BASE_DIR, "gesture_map.pkl"))

# Get expected number of features
expected_features = model.n_features_in_

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)


class VideoCamera(object):
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

        with open(os.path.join(STATIC_DIR, "detect.txt"), "w", encoding="utf-8") as ff:
            ff.write("")

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract features
                landmark_list = []
                for lm in hand_landmarks.landmark:
                    landmark_list.extend([lm.x, lm.y, lm.z])
                
                # Predict only if feature size matches
                if len(landmark_list) == expected_features:
                    prediction = model.predict([landmark_list])[0]
                    gesture_name = gesture_map.get(prediction, "Unknown")

                    gn=""
                    with open(os.path.join(STATIC_DIR, "class2.txt"), encoding="utf-8") as ff:
                        cn=ff.read()
                    cna=cn.split("|")

                    with open(os.path.join(STATIC_DIR, "class1.txt"), encoding="utf-8") as ff:
                        hn=ff.read()
                    hna=hn.split("|")
                    u=0
                    for cna1 in cna:
                        if cna1==gesture_name:
                            if u < len(hna):
                                gn=hna[u]
                            break
                        u+=1
                    if gn=="":
                        s=1
                    else:
                        with open(os.path.join(STATIC_DIR, "detect.txt"), "w", encoding="utf-8") as ff:
                            ff.write(gn)
                        print(gn)

                        cv2.putText(frame, f"{gn}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    with open(os.path.join(STATIC_DIR, "detect.txt"), "w", encoding="utf-8") as ff:
                        ff.write("")
        else:
            with open(os.path.join(STATIC_DIR, "detect.txt"), "w", encoding="utf-8") as ff:
                ff.write("")

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            raise RuntimeError("Could not encode the webcam frame.")
        return jpeg.tobytes()
