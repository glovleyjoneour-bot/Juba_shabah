from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.utils import platform
from PIL import Image as PilImage
import stepic
import os
from plyer import filechooser

class GhostFinalUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_path = None
        
        # الواجهة الرئيسية (ترتيب عمودي)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 1. الرأس (الشعار والعنوان)
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.12))
        logo_path = "icon.png"
        if os.path.exists(logo_path):
            header.add_widget(KivyImage(source=logo_path, size_hint=(0.25, 1)))
        
        header.add_widget(MDLabel(
            text="GHOST PRO v5", 
            font_style="H5", 
            bold=True,
            halign="left"
        ))
        main_layout.add_widget(header)

        # 2. منطقة عرض الصورة (Preview)
        self.img_preview = KivyImage(
            source='', 
            size_hint=(1, 0.45), 
            allow_stretch=True,
            keep_ratio=True
        )
        main_layout.add_widget(self.img_preview)

        # 3. حقل النص (للإدخال أو لعرض الرسالة المكشوفة)
        self.msg_field = MDTextField(
            hint_text="Enter Secret Message or Extract from Image",
            mode="rectangle",
            icon_right="email-lock",
            size_hint=(1, None)
        )
        main_layout.add_widget(self.msg_field)

        # 4. صف الأزرار الرئيسي (3 أزرار متساوية)
        btns_row = BoxLayout(spacing=10, size_hint=(1, 0.1))
        
        btn_select = MDFillRoundFlatIconButton(
            icon="image-plus", text="SELECT", 
            on_release=self.open_gallery
        )
        btn_hide = MDFillRoundFlatIconButton(
            icon="lock", text="HIDE", 
            on_release=self.process_hide
        )
        # الزر الجديد اللي طلبته للكشف
        btn_extract = MDFillRoundFlatIconButton(
            icon="eye-check", text="EXTRACT",
            md_bg_color=(0, 0.5, 0.2, 1), # لون أخضر غامق للتمييز
            on_release=self.process_extract
        )
        
        btns_row.add_widget(btn_select)
        btns_row.add_widget(btn_hide)
        btns_row.add_widget(btn_extract)
        main_layout.add_widget(btns_row)

        # 5. زر الحفظ النهائي والحالة
        self.btn_download = MDRaisedButton(
            text="DOWNLOAD TO GALLERY",
            size_hint=(1, None),
            disabled=True,
            on_release=self.save_to_downloads
        )
        main_layout.add_widget(self.btn_download)

        self.status_label = MDLabel(
            text="Status: Ready", 
            halign="center", 
            theme_text_color="Secondary"
        )
        main_layout.add_widget(self.status_label)

        self.add_widget(main_layout)

    def open_gallery(self, *args):
        filechooser.open_file(on_selection=self.on_selection)

    def on_selection(self, selection):
        if selection:
            self.selected_path = selection[0]
            self.img_preview.source = self.selected_path
            self.status_label.text = "Image Selected!"

    def process_hide(self, *args):
        if not self.selected_path or not self.msg_field.text:
            self.status_label.text = "Select image and type message!"
            return
        try:
            img = PilImage.open(self.selected_path)
            # تشفير الرسالة
            encoded_data = stepic.encode(img, self.msg_field.text.encode('utf-8'))
            
            # حفظ مؤقت للمعالجة
            self.temp_file = os.path.join(os.getcwd(), "temp_output.png")
            encoded_data.save(self.temp_file, "PNG")
            
            self.img_preview.source = self.temp_file
            self.img_preview.reload()
            self.btn_download.disabled = False
            self.status_label.text = "Message Hidden! Tap Download."
        except Exception as e:
            self.status_label.text = f"Error: {str(e)[:20]}"

    def process_extract(self, *args):
        if not self.selected_path:
            self.status_label.text = "Select an image first!"
            return
        try:
            img = PilImage.open(self.selected_path)
            # فك تشفير الرسالة
            decoded_msg = stepic.decode(img)
            if isinstance(decoded_msg, bytes):
                decoded_msg = decoded_msg.decode('utf-8')
            
            self.msg_field.text = decoded_msg
            self.status_label.text = "Message Extracted Successfully!"
        except:
            self.status_label.text = "No hidden message found."

    def save_to_downloads(self, *args):
        try:
            target = "/sdcard/Download/Ghost_Secret_Image.png" if platform == 'android' else "Ghost_Secret_Image.png"
            output_img = PilImage.open(self.temp_file)
            output_img.save(target, "PNG")
            self.status_label.text = "Saved in Downloads folder!"
        except:
            self.status_label.text = "Permission Denied! Check Settings."

class GhostApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return GhostFinalUI()

if __name__ == "__main__":
    GhostApp().run()
    
