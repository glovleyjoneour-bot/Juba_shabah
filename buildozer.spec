[app]

# (str) عنوان التطبيق
title = GHOST PRO v5

# (str) اسم الحزمة (يجب أن يكون بحروف صغيرة بدون مسافات)
package.name = ghostpro

# (str) نطاق الحزمة (عادةً يكون عكس اسم موقعك أو اسمك)
package.domain = org.juba

# (str) مكان وجود كود المصدر
source.dir = .

# (list) امتدادات الملفات التي يجب تضمينها في الحزمة
source.include_exts = py,png,jpg,kv,atlas

# (str) إصدار التطبيق
version = 0.1

# (list) المتطلبات والمكتبات المطلوبة لعمل التطبيق
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,stepic,plyer,android

# (str) اسم أيقونة التطبيق
icon.filename = icon.png

# (str) اتجاه الشاشة (portrait = طولي)
orientation = portrait

# (list) الأذونات المطلوبة
# تم إزالة MANAGE_EXTERNAL_STORAGE لتجنب اعتبار التطبيق خطراً
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

# (int) إصدار أندرويد المستهدف
android.api = 33

# (int) الحد الأدنى لإصدار أندرويد المدعوم
android.minapi = 21

# (int) إصدار NDK (مكتبة التطوير الأصلية)
android.ndk = 25b

# (list) معماريات المعالج المدعومة (لدعم معظم الهواتف الحديثة)
android.archs = arm64-v8a, armeabi-v7a

# (bool) السماح بالنسخ الاحتياطي
android.allow_backup = True

# (str) صيغة الحزمة النهائية
android.release_artifact = apk
android.debug_artifact = apk


[buildozer]

# (int) مستوى السجل (0 = أخطاء فقط، 1 = معلومات، 2 = تصحيح الأخطاء)
log_level = 2

# (int) إظهار تحذير إذا تم تشغيل buildozer كـ root
warn_on_root = 1

# (str) مسار مجلد البناء
build_dir = ./.buildozer

# (str) مسار مجلد الملفات النهائية
bin_dir = ./bin
