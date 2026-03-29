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

# طلب الصلاحيات للأندرويد
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

class SteganoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.label = MDLabel(
            text="Juba Stegano - تشفير الصور",
            halign="center",
            font_style="H4"
        )
        
        self.input_text = MDTextField(
            hint_text="اكتب السر هنا...",
            mode="rectangle"
        )

        self.img_path = MDTextField(
            hint_text="اسم الصورة (مثلاً: input.png)",
            mode="rectangle"
        )

        btn_encode = MDRaisedButton(
            text="إخفاء النص في الصورة",
            pos_hint={"center_x": .5},
            on_release=self.encode_data
        )

        btn_decode = MDRaisedButton(
            text="استخراج النص من الصورة",
            pos_hint={"center_x": .5},
            on_release=self.decode_data
        )

        self.result_label = MDLabel(text="", halign="center", theme_text_color="Hint")

        layout.add_widget(self.label)
        layout.add_widget(self.input_text)
        layout.add_widget(self.img_path)
        layout.add_widget(btn_encode)
        layout.add_widget(btn_decode)
        layout.add_widget(self.result_label)
        self.add_widget(layout)

    def encode_data(self, instance):
        try:
            path = self.img_path.text
            if not os.path.exists(path):
                self.result_label.text = "الصورة غير موجودة!"
                return
            
            img = Image.open(path)
            message = self.input_text.text.encode('utf-8')
            new_img = stepic.encode(img, message)
            new_img.save("secret_juba.png", "PNG")
            self.result_label.text = "تم الحفظ باسم: secret_juba.png"
        except Exception as e:
            self.result_label.text = f"خطأ: {str(e)}"

    def decode_data(self, instance):
        try:
            path = self.img_path.text
            img = Image.open(path)
            decoded_message = stepic.decode(img)
            self.result_label.text = f"السر المستخرج: {decoded_message}"
        except Exception as e:
            self.result_label.text = "فشل الاستخراج أو لا يوجد سر"

class JubaApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        return SteganoScreen()

if __name__ == "__main__":
    JubaApp().run()
    
