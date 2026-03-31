from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.utils import platform
from kivy.clock import Clock
import os

class GhostFinalUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_path = None
        self.temp_file = None
        
        # الواجهة الرئيسية (نفس تصميمك v5 بالضبط)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # الرأس
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.12))
        logo_path = "icon.png"
        if os.path.exists(logo_path):
            header.add_widget(KivyImage(source=logo_path, size_hint=(0.25, 1)))
        header.add_widget(MDLabel(text="GHOST PRO v5", font_style="H5", bold=True))
        main_layout.add_widget(header)

        # العرض
        self.img_preview = KivyImage(source='', size_hint=(1, 0.45))
        main_layout.add_widget(self.img_preview)

        # الإدخال
        self.msg_field = MDTextField(hint_text="Enter Message", mode="rectangle", size_hint=(1, None))
        main_layout.add_widget(self.msg_field)

        # الأزرار
        btns_row = BoxLayout(spacing=10, size_hint=(1, 0.1))
        btns_row.add_widget(MDFillRoundFlatIconButton(icon="image-plus", text="SELECT", on_release=self.open_gallery))
        btns_row.add_widget(MDFillRoundFlatIconButton(icon="lock", text="HIDE", on_release=self.process_hide))
        btns_row.add_widget(MDFillRoundFlatIconButton(icon="eye", text="EXTRACT", on_release=self.process_extract))
        main_layout.add_widget(btns_row)

        self.btn_download = MDRaisedButton(text="SAVE TO GALLERY", size_hint=(1, None), disabled=True, on_release=self.save_to_downloads)
        main_layout.add_widget(self.btn_download)

        self.status_label = MDLabel(text="Status: Ready", halign="center")
        main_layout.add_widget(self.status_label)
        self.add_widget(main_layout)

    def open_gallery(self, *args):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.on_selection)

    def on_selection(self, selection):
        if selection:
            self.selected_path = selection[0]
            self.img_preview.source = self.selected_path
            self.status_label.text = "Image Loaded!"

    def process_hide(self, *args):
        try:
            from PIL import Image
            import stepic
            img = Image.open(self.selected_path)
            encoded = stepic.encode(img, self.msg_field.text.encode())
            self.temp_file = os.path.join(os.getcwd(), "output.png")
            encoded.save(self.temp_file, "PNG")
            self.img_preview.source = self.temp_file
            self.img_preview.reload()
            self.btn_download.disabled = False
            self.status_label.text = "Success! Message Hidden."
        except Exception as e:
            self.status_label.text = f"Error: {str(e)[:15]}"

    def process_extract(self, *args):
        try:
            from PIL import Image
            import stepic
            img = Image.open(self.selected_path)
            self.msg_field.text = stepic.decode(img)
            self.status_label.text = "Message Extracted!"
        except:
            self.status_label.text = "No hidden data."

    def save_to_downloads(self, *args):
        try:
            from PIL import Image
            target = "/sdcard/Download/Ghost_Result.png" if platform == 'android' else "Result.png"
            Image.open(self.temp_file).save(target)
            self.status_label.text = "Saved in Downloads!"
        except:
            self.status_label.text = "Save Failed!"

class GhostApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return GhostFinalUI()

if __name__ == "__main__":
    GhostApp().run()
    
