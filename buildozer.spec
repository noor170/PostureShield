[app]
title = Posture Shield
package.name = postureshield
package.domain = org.ai
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,tflite
version = 1.0

# Requirements (Crucial for Android)
requirements = python3,kivy,opencv-python,mediapipe,numpy

orientation = portrait
permissions = CAMERA, INTERNET

# Android specific
android.archs = arm64-v8a
android.allow_backup = True
android.api = 31
