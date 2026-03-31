[app]
title = GHOST PRO v5
package.name = ghost_pro
package.domain = org.juba
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
# السطر المنقذ:
version = 0.1

# المتطلبات الصارمة:
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,stepic,plyer,setuptools,android

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
