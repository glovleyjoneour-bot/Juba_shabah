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

# وظيفة طلب الأذونات - حجر الزاوية لمنع الكراش
def request_android_permissions():
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.MANAGE_EXTERNAL_STORAGE
        ])

class GhostFinalUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_path = None
        self.temp_file = "output_ghost.png"
        
        # طلب الأذونات بعد ثانية من فتح الواجهة
        Clock.schedule_once(lambda dt: request_android_permissions(), 1)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Header v5
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.12))
        header.add_widget(MDLabel(text="GHOST PRO v5", font_style="H5", bold=True))
        layout.add_widget(header)

        # Image Preview
        self.img_preview = KivyImage(source='', size_hint=(1, 0.45))
        layout.add_widget(self.img_preview)

        # Input Field
        self.msg_field = MDTextField(hint_text="Enter Message", mode="rectangle", size_hint=(1, None))
        layout.add_widget(self.msg_field)

        # Action Buttons
        btns = BoxLayout(spacing=10, size_hint=(1, 0.1))
        btns.add_widget(MDFillRoundFlatIconButton(icon="image-plus", text="SELECT", on_release=self.select_image))
        btns.add_widget(MDFillRoundFlatIconButton(icon="lock", text="HIDE", on_release=self.hide_data))
        btns.add_widget(MDFillRoundFlatIconButton(icon="eye", text="EXTRACT", on_release=self.extract_data))
        layout.add_widget(btns)

        self.status = MDLabel(text="Status: Secured", halign="center")
        layout.add_widget(self.status)
        self.add_widget(layout)

    def select_image(self, *args):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.on_selection)
        except Exception as e:
            self.status.text = "Gallery Error"

    def on_selection(self, selection):
        if selection:
            self.selected_path = selection[0]
            self.img_preview.source = self.selected_path
            self.status.text = "Image Selected"

    def hide_data(self, *args):
        if not self.selected_path:
            self.status.text = "Select Image First!"
            return
        try:
            from PIL import Image
            import stepic
            img = Image.open(self.selected_path)
            encoded = stepic.encode(img, self.msg_field.text.encode('utf-8'))
            encoded.save(self.temp_file, "PNG")
            self.status.text = "Encoded & Ready"
        except Exception as e:
            self.status.text = f"Hide Error: {str(e)[:10]}"

    def extract_data(self, *args):
        if not self.selected_path: return
        try:
            from PIL import Image
            import stepic
            img = Image.open(self.selected_path)
            decoded = stepic.decode(img)
            self.msg_field.text = decoded if isinstance(decoded, str) else decoded.decode('utf-8')
            self.status.text = "Extracted"
        except:
            self.status.text = "No Data Found"

class GhostApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return GhostFinalUI()

if __name__ == "__main__":
    GhostApp().run()
    
