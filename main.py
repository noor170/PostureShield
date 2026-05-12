from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import mediapipe as mp
import time
import numpy as np

class PostureShieldApp(App):
    def build(self):
        self.img = Image()
        self.capture = cv2.VideoCapture(0)
        
        # Mediapipe Setup
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        self.standard_y = None
        self.calibrated = False
        self.start_time = time.time()
        
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.img

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret: return

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        current_time = time.time()
        
        if results.pose_landmarks:
            nose_y = results.pose_landmarks.landmark[0].y
            
            if not self.calibrated:
                if current_time - self.start_time > 3:
                    self.standard_y = nose_y
                    self.calibrated = True
            else:
                if nose_y > (self.standard_y + 0.05):
                    frame = cv2.GaussianBlur(frame, (99, 99), 0)

        # Convert to Kivy Texture
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

if __name__ == '__main__':
    PostureShieldApp().run()
