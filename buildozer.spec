[app]
title = GHOST PRO v5
package.name = ghost_pro
package.domain = org.juba
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات الإجبارية لمنع الكراش
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,stepic,plyer,setuptools,android

# الأذونات المطلوبة لتشغيل كود الـ Permission أعلاه
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.private_storage = True
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
