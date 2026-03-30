from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.utils import platform
from PIL import Image as PilImage
import stepic
import os

class GhostUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # واجهة عمودية رئيسية
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=25)

        # --- القسم الأول: الشعار والعنوان (Header) ---
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        
        # اللوجو بالزاوية اليسرى العليا
        logo_path = "icon.png" # تأكد من وجود الملف في مجلد المشروع
        if os.path.exists(logo_path):
            self.logo = KivyImage(
                source=logo_path,
                size_hint=(0.3, 1),
                pos_hint={"center_y": .5}
            )
        else:
            self.logo = MDLabel(text="👻", halign="center", font_style="H3", size_hint=(0.3, 1))

        # عنوان التطبيق بجانب اللوجو
        self.title = MDLabel(
            text="GHOST\nSTEGANO",
            halign="left",
            font_style="H4",
            theme_text_color="Primary",
            size_hint=(0.7, 1),
            pos_hint={"center_y": .5}
        )

        header_layout.add_widget(self.logo)
        header_layout.add_widget(self.title)

        # --- القسم الثاني: إدخال البيانات (Input) ---
        input_layout = BoxLayout(orientation='vertical', spacing=15)
        
        # حقل الرسالة السرية (أكثر تفصيلاً)
        self.secret_msg = MDTextField(
            hint_text="Type your secure message...",
            helper_text="Use English characters only",
            helper_text_mode="on_focus",
            mode="rectangle",
            icon_right="key-variant",
            size_hint=(1, None)
        )

        # حقل اسم الصورة (الموجودة في الداونلود)
        self.image_name = MDTextField(
            hint_text="Source image name (e.g. icon.png)",
            helper_text="Make sure file is in Downloads folder",
            helper_text_mode="on_persistent",
            mode="rectangle",
            icon_right="folder-image",
            size_hint=(1, None)
        )

        input_layout.add_widget(self.secret_msg)
        input_layout.add_widget(self.image_name)

        # --- القسم الثالث: التحكم والحالة (Control) ---
        control_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, 0.4))

        # أزرار الإخفاء والاستخراج (بتفاصيل أكثر)
        btn_hide = MDRaisedButton(
            text="🔒 HIDE MESSAGE & SAVE",
            size_hint=(1, None),
            md_bg_color=(103/255, 58/255, 183/255, 1), # DeepPurple
            on_release=self.process_hide
        )

        btn_show = MDRaisedButton(
            text="🔓 EXTRACT MESSAGE",
            size_hint=(1, None),
            on_release=self.process_extract
        )

        # نص الحالة بالأسفل (مرتب)
        self.status = MDLabel(
            text="Status: GHOST ACTIVE",
            halign="center",
            theme_text_color="Secondary",
            size_hint=(1, None)
        )

        control_layout.add_widget(btn_hide)
        control_layout.add_widget(btn_show)
        control_layout.add_widget(self.status)

        # إضافة جميع الأقسام للواجهة الرئيسية
        main_layout.add_widget(header_layout)
        main_layout.add_widget(input_layout)
        main_layout.add_widget(control_layout)
        self.add_widget(main_layout)

    def get_path(self, filename):
        if platform == 'android':
            return f"/sdcard/Download/{filename}"
        return filename

    def process_hide(self, instance):
        try:
            in_file = self.get_path(self.image_name.text)
            if not os.path.exists(in_file):
                self.status.text = "Error: File not found in Downloads!"
                return
            
            img = PilImage.open(in_file)
            data = self.secret_msg.text.encode('utf-8')
            new_img = stepic.encode(img, data)
            
            out_file = self.get_path("ghost_output.png")
            new_img.save(out_file, "PNG")
            self.status.text = "Success! Saved as ghost_output.png"
        except Exception as e:
            self.status.text = "Error: Permission Denied"

    def process_extract(self, instance):
        try:
            in_file = self.get_path(self.image_name.text)
            img = PilImage.open(in_file)
            decoded = stepic.decode(img)
            if isinstance(decoded, bytes):
                decoded = decoded.decode('utf-8')
            self.status.text = f"Msg: {decoded}"
        except:
            self.status.text = "No hidden data found"

class GhostApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return GhostUI()

if __name__ == "__main__":
    GhostApp().run()
    
