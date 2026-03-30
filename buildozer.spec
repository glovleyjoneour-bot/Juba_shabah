[app]
title = Juba Al Shabah
package.name = juba_shabah
package.domain = org.juba
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات الأساسية مع الترتيب الصحيح
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,stepic,plyer

orientation = portrait
fullscreen = 0

# الصلاحيات (أهم جزء لتطبيقك)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b

# اسم الأيقونة المربعة اللي رفعتها
icon.filename = icon.png

# تنظيف التنبيهات
p4a.branch = master
