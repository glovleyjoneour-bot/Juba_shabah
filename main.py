from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from PIL import Image
import stepic
import os

# إعداد الصلاحيات للأندرويد
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

class SteganoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # العنوان الرئيسي
        self.label = MDLabel(
            text="JUBA GHOST - SECURE",
            halign="center",
            font_style="H4",
            theme_text_color="Primary"
        )
        
        # حقل إدخال الرسالة السرية
        self.input_text = MDTextField(
            hint_text="Secret Message",
            helper_text="Text to hide inside the image",
            helper_text_mode="on_focus",
            mode="rectangle"
        )

        # حقل إدخال اسم الصورة (يجب أن تكون في مجلد الصور أو الداونلود)
        self.img_path = MDTextField(
            hint_text="Source Image Name (e.g. photo.png)",
            helper_text="Make sure image is in Download folder",
            helper_text_mode="on_focus",
            mode="rectangle"
        )

        # زر الإخفاء (الأول)
        btn_encode = MDRaisedButton(
            text="HIDE & SAVE TO DOWNLOADS",
            size_hint=(.9, None),
            pos_hint={"center_x": .5},
            on_release=self.encode_data
        )

        # زر الاستخراج (الثاني)
        btn_decode = MDRaisedButton(
            text="EXTRACT SECRET MESSAGE",
            size_hint=(.9, None),
            pos_hint={"center_x": .5},
            on_release=self.decode_data
        )

        # نص الحالة بالأسفل
        self.result_label = MDLabel(
            text="Status: Ready", 
            halign="center", 
            theme_text_color="Hint"
        )

        layout.add_widget(self.label)
        layout.add_widget(self.input_text)
        layout.add_widget(self.img_path)
        layout.add_widget(btn_encode)
        layout.add_widget(btn_decode)
        layout.add_widget(self.result_label)
        self.add_widget(layout)

    def get_download_path(self, filename):
        if platform == 'android':
            # المسار الرسمي لمجلد التحميلات في أجهزة شاومي وغيرها
            return os.path.join("/sdcard/Download", filename)
        return filename

    def encode_data(self, instance):
        try:
            # محاولة البحث عن الصورة في مجلد التحميلات أولاً
            source_file = self.get_download_path(self.img_path.text)
            
            if not os.path.exists(source_file):
                self.result_label.text = "Error: Source image not found in Downloads!"
                return
            
            img = Image.open(source_file)
            message = self.input_text.text.encode('utf-8')
            
            # عملية التشفير
            new_img = stepic.encode(img, message)
            
            # مسار الحفظ النهائي في مجلد Downloads
            output_path = self.get_download_path("secret_juba_ghost.png")
            new_img.save(output_path, "PNG")
            
            self.result_label.text = "Success! Saved in Download folder."
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"

    def decode_data(self, instance):
        try:
            source_file = self.get_download_path(self.img_path.text)
            if not os.path.exists(source_file):
                self.result_label.text = "Error: File not found in Downloads!"
                return

            img = Image.open(source_file)
            decoded_message = stepic.decode(img)
            
            if isinstance(decoded_message, bytes):
                decoded_message = decoded_message.decode('utf-8')
                
            self.result_label.text = f"Message: {decoded_message}"
        except Exception as e:
            self.result_label.text = "No secret message found!"

class JubaApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        return SteganoScreen()

if __name__ == "__main__":
    JubaApp().run()
    
