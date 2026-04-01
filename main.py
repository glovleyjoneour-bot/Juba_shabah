from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.utils import platform
from kivy.clock import Clock
import os

# وظيفة طلب الأذونات الرسمية لأجهزة 2099
def ask_permissions():
    if platform == 'android':
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE
            ])
        except Exception as e:
            print(f"PERMISSION_GATE_ERROR: {e}")

class GhostProUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_path = None
        
        # الواجهة الأصلية v5 كما في صورك
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Header (Logo + Title)
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        # تأكد من وجود ملف icon.png في المشروع
        header.add_widget(KivyImage(source='icon.png', size_hint=(0.3, 1)))
        header.add_widget(MDLabel(text="GHOST PRO v5", font_style="H4", bold=True, halign="center"))
        layout.add_widget(header)

        # Preview
        self.img_preview = KivyImage(source='', size_hint=(1, 0.5))
        layout.add_widget(self.img_preview)

        # Input
        self.msg_input = MDTextField(
            hint_text="Enter Secret Message", 
            mode="rectangle", 
            size_hint=(1, None), 
            height="50dp"
        )
        layout.add_widget(self.msg_input)

        # Buttons
        btns = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        btns.add_widget(MDFillRoundFlatIconButton(icon="image-plus", text="SELECT", on_release=self.open_gallery))
        btns.add_widget(MDFillRoundFlatIconButton(icon="lock", text="HIDE", on_release=self.hide_message))
        btns.add_widget(MDFillRoundFlatIconButton(icon="eye", text="EXTRACT", on_release=self.extract_message))
        layout.add_widget(btns)

        self.status = MDLabel(text="Status: Secured", halign="center", theme_text_color="Hint")
        layout.add_widget(self.status)
        self.add_widget(layout)

    def open_gallery(self, *args):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.on_selection)
        except: self.status.text = "Gallery Error"

    def on_selection(self, selection):
        if selection:
            self.selected_path = selection[0]
            self.img_preview.source = self.selected_path
            self.status.text = "Image Loaded"

    def hide_message(self, *args):
        if not self.selected_path:
            self.status.text = "Select Image First!"
            return
        try:
            from PIL import Image
            import stepic
            img = Image.open(self.selected_path)
            new_img = stepic.encode(img, self.msg_input.text.encode('utf-8'))
            
            # المسار الآمن للحفظ في أندرويد
            if platform == 'android':
                path = "/sdcard/Download/ghost_hidden.png"
            else:
                path = "ghost_hidden.png"
                
            new_img.save(path, "PNG")
            self.status.text = "Saved in Downloads"
        except Exception as e:
            self.status.text = f"Error: {str(e)[:15]}"

    def extract_message(self, *args):
        if not self.selected_path: return
        try:
            from PIL import Image
            import stepic
            img = Image.open(self.selected_path)
            decoded = stepic.decode(img)
            self.msg_input.text = decoded if isinstance(decoded, str) else decoded.decode('utf-8')
            self.status.text = "Extracted"
        except:
            self.status.text = "No message found"

class GhostApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return GhostProUI()

    # طلب الإذن فور تشغيل التطبيق لضمان عدم الكراش
    def on_start(self):
        Clock.schedule_once(lambda dt: ask_permissions(), 1)

if __name__ == "__main__":
    GhostApp().run()
    
