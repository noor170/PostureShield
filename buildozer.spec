[app]
title = Posture Shield
package.name = postureshield
package.domain = org.ai
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,tflite
version = 1.0

# Android builds must use python-for-android recipes where available.
# `opencv` has a recipe; `opencv-python-headless` and `mediapipe` do not.
requirements = python3, kivy, numpy, opencv, libffi

log_level = 2

orientation = portrait

# ক্যামেরা এবং স্টোরেজ ব্যবহারের জন্য পারমিশন
permissions = CAMERA, INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Android specific (আপডেট করা হয়েছে)
# গুগল প্লে স্টোরের ২০২৬ সালের নিয়ম অনুযায়ী Target API Level কমপক্ষে ৩৪ হতে হবে
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.accept_sdk_license = True

# আর্কিটেকচার (আধুনিক ফোনের জন্য arm64-v8a মাস্ট)
android.archs = arm64-v8a, armeabi-v7a

# ক্যামেরা ব্যবহারের জন্য হার্ডওয়্যার ফিচার ঘোষণা
android.features = android.hardware.camera, android.hardware.camera.autofocus

# লজিস্টিক সেটিংস
android.allow_backup = True
