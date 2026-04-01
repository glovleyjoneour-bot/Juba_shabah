[app]

# (str) Title of your application
title = GHOST PRO v5

# (str) Package name
package.name = ghost_pro

# (str) Package domain
package.domain = org.juba

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Version of your application
version = 0.1

# (list) Application requirements
# تمت إضافة android و pyjnius لضمان عمل نظام الأذونات بدون كراش
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,stepic,plyer,setuptools,android,pyjnius

# (str) Custom source folders for requirements
# (list) Permissions
# أذونات الوصول الكامل للذاكرة لتجنب قيود أندرويد الحديث
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# (list) Android architectures
# دعم الـ 64 بت (arm64-v8a) هو السر لعمله على شاومي وسامسونج
android.archs = arm64-v8a, armeabi-v7a

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (bool) Window management - if True, the window will be resizable
android.allow_backup = True

# (str) The format used to package the app
android.release_artifact = apk
android.debug_artifact = apk

# (list) List of service to declare
# android.services = 

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1

# (str) Path to build folder
# build_dir = ./.buildozer

# (str) Path to bin folder
# bin_dir = ./bin
