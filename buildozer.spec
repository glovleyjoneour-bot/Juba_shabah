[app]

# (str) Title of your application
title = GHOST PRO v5

# (str) Package name
package.name = ghost_pro_juba

# (str) Package domain (needed for android packaging)
package.domain = org.juba.ghost

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# الترتيب هنا ضروري جداً لضمان استقرار المكتبات
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,stepic,plyer,setuptools,android

# (str) Custom source folders for requirements
# (list) Garden requirements
# (str) Presplash of the application
# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be monitor for touches
# (list) Permissions
# الأذونات الكاملة لتخطي قيود أندرويد 11 و 12 و 13 و 14
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API, should be as high as possible.
# API 33 هو الأكثر استقراراً حالياً لمتطلبات جوجل وأجهزة شاومي
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
# (str) Android SDK directory (if empty, it will be automatically downloaded)
# (str) ANT directory (if empty, it will be automatically downloaded)

# (list) Android architectures to build for
# دعم كل أنواع المعالجات (64 بت و 32 بت) لضمان التشغيل على كل الأجهزة
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (OS >= 6.0)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar)
android.debug_artifact = apk

# (list) Gradle dependencies
# android.gradle_dependencies = 

# (list) add java files
# android.add_src = 

# (list) Android AAR archives to add
# android.add_aars = 

# (list) Java classes to keep (for logcat)
# android.add_javaclasses = 

# (list) The Android libs to copy in the library/libs directory
# android.copy_libs = 

# (bool) If True, then skip trying to update the Android sdk
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# android.accept_sdk_license = True

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (str) Android additional libraries to copy into libs/armeabi
# android.add_libs_armeabi = libs/android-v7a/*.so
# android.add_libs_armeabi_v8a = libs/android-v8a/*.so

# (str) Android entry point, default is to use start.py
# android.entrypoint = 

# (list) Pattern to whitelist for the whole project
# android.whitelist = 

# (str) Path to a custom whitelist file
# android.whitelist_src = 

# (str) Path to a custom blacklist file
# android.blacklist_src = 

# (list) List of Java files to add to the android project
# android.add_src = 

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

