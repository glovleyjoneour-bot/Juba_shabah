[app]

# (str) Title of your application
title = GHOST PRO v5

# (str) Package name
package.name = ghost_pro

# (str) Package domain
package.domain = org.juba

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (تأكد من وجود أيقونة باسم icon.png)
source.include_exts = py,png,jpg,kv,atlas

# (str) Version of your application
version = 0.1

# (list) Application requirements
# ملاحظة: تم إضافة pyjnius و android لتمكين نظام الأذونات من العمل
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,stepic,plyer,setuptools,android,pyjnius

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientations
orientation = portrait

# (list) Permissions
# الأذونات الكاملة للوصول للصور في الأنظمة القديمة والحديثة
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# (list) Android architectures
# هذا السطر هو المسؤول عن عمل التطبيق على شاومي وسامسونج (64-bit) بجانب Ateto
android.archs = arm64-v8a, armeabi-v7a

# (bool) allow backup
android.allow_backup = True

# (str) The format used to package the app
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

# (str) Path to build folder
build_dir = ./.buildozer

# (str) Path to bin folder
bin_dir = ./bin
