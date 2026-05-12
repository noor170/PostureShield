from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import time

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import mediapipe as mp
except ImportError:
    mp = None

class PostureShieldApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical")
        self.status = Label(
            size_hint=(1, 0.15),
            text="Starting camera...",
        )
        self.img = Image(size_hint=(1, 0.85))
        root.add_widget(self.status)
        root.add_widget(self.img)

        self.capture = None
        if cv2 is not None:
            self.capture = cv2.VideoCapture(0)

        self.pose = None
        if cv2 is not None and mp is not None:
            self.mp_pose = mp.solutions.pose
            self.pose = self.mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )
            self.status.text = "Camera preview running"
        elif cv2 is not None:
            self.status.text = "Camera preview running. Posture detection unavailable."
        else:
            self.status.text = "Camera/OpenCV unavailable in this build."

        self.standard_y = None
        self.calibrated = False
        self.start_time = time.time()

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return root

    def update(self, dt):
        if self.capture is None:
            return

        ret, frame = self.capture.read()
        if not ret:
            self.status.text = "Unable to read from camera."
            return

        frame = cv2.flip(frame, 1)
        results = None
        if self.pose is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)

        current_time = time.time()

        if results and results.pose_landmarks:
            nose_y = results.pose_landmarks.landmark[0].y

            if not self.calibrated:
                if current_time - self.start_time > 3:
                    self.standard_y = nose_y
                    self.calibrated = True
            else:
                if nose_y > (self.standard_y + 0.05):
                    frame = cv2.GaussianBlur(frame, (99, 99), 0)
                    self.status.text = "Posture alert detected"
                else:
                    self.status.text = "Posture looks good"

        # Convert to Kivy Texture
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

if __name__ == '__main__':
    PostureShieldApp().run()
