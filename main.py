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

class JubaGhostScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=20)

        # واجهة إنجليزية بالكامل لتجنب المربعات
        self.title = MDLabel(
            text="JUBA GHOST - DOWNLOADS",
            halign="center",
            font_style="H4",
            theme_text_color="Primary"
        )
        
        self.msg_input = MDTextField(
            hint_text="Secret Message",
            mode="rectangle"
        )

        self.img_input = MDTextField(
            hint_text="Source Image (e.g. icon.png)",
            helper_text="Put image in Download folder first",
            helper_text_mode="on_focus",
            mode="rectangle"
        )

        btn_hide = MDRaisedButton(
            text="HIDE & SAVE TO DOWNLOADS",
            size_hint=(.9, None),
            pos_hint={"center_x": .5},
            on_release=self.run_hide
        )

        btn_show = MDRaisedButton(
            text="EXTRACT FROM DOWNLOADS",
            size_hint=(.9, None),
            pos_hint={"center_x": .5},
            on_release=self.run_extract
        )

        self.status = MDLabel(text="Status: Ready", halign="center", theme_text_color="Hint")

        layout.add_widget(self.title)
        layout.add_widget(self.msg_input)
        layout.add_widget(self.img_input)
        layout.add_widget(btn_hide)
        layout.add_widget(btn_show)
        layout.add_widget(self.status)
        self.add_widget(layout)

    def get_download_path(self, filename):
        if platform == 'android':
            # هذا المسار يضمن الوصول لمجلد التحميلات العام في أندرويد 11+
            from android.storage import primary_external_storage_path
            return os.path.join(primary_external_storage_path(), "Download", filename)
        return filename

    def run_hide(self, instance):
        try:
            # يبحث عن الصورة الأصلية في الـ Download
            input_path = self.get_download_path(self.img_input.text)
            if not os.path.exists(input_path):
                self.status.text = "Error: Source not in Download folder"
                return
            
            img = Image.open(input_path)
            message = self.msg_input.text.encode('utf-8')
            new_img = stepic.encode(img, message)
            
            # يحفظ الصورة المشفرة في الـ Download
            output_path = self.get_download_path("ghost_output.png")
            new_img.save(output_path, "PNG")
            self.status.text = "Success! Saved in Download folder"
        except Exception as e:
            self.status.text = "Error: Check Permissions"

    def run_extract(self, instance):
        try:
            input_path = self.get_download_path(self.img_input.text)
            if not os.path.exists(input_path):
                self.status.text = "Error: Image not found"
                return
            img = Image.open(input_path)
            decoded = stepic.decode(img)
            if isinstance(decoded, bytes):
                decoded = decoded.decode('utf-8')
            self.status.text = f"MSG: {decoded}"
        except:
            self.status.text = "No hidden message found"

class JubaApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        return JubaGhostScreen()

if __name__ == "__main__":
    JubaApp().run()
    
