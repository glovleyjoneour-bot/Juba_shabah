[app]
title = GHOST PRO v5
package.name = ghost_pro
package.domain = org.juba
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
# الإصدار ضروري جداً
version = 0.1

# المتطلبات البرمجية
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,stepic,plyer,setuptools,android

icon.filename = icon.png
orientation = portrait

# الأذونات الكاملة لتخطي قيود أندرويد 11+
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# السطر الذهبي: دعم Ateto + الأجهزة القوية الأخرى
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
