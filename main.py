from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.utils import platform
from PIL import Image as PilImage
import stepic
import os

# مكتبة اختيار الملفات (تشتغل على الكمبيوتر والأندرويد)
from plyer import filechooser

class GhostV4(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_image_path = None
        self.output_image_path = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Header مع اللوجو
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        if os.path.exists("icon.png"):
            header.add_widget(KivyImage(source="icon.png", size_hint=(0.2, 1)))
        header.add_widget(MDLabel(text="GHOST PRO", font_style="H5", halign="left"))
        layout.add_widget(header)

        # عرض الصورة المختارة (لوحة المعاينة)
        self.preview_img = KivyImage(
            source='icon.png' if os.path.exists('icon.png') else '',
            size_hint=(1, 0.4),
            allow_stretch=True
        )
        layout.add_widget(self.preview_img)

        # حقل الرسالة
        self.secret_input = MDTextField(
            hint_text="Enter Secret Message",
            mode="rectangle",
            size_hint=(1, None)
        )
        layout.add_widget(self.secret_input)

        # أزرار التحكم
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        
        btn_select = MDFillRoundFlatIconButton(
            icon="image-plus",
            text="SELECT IMAGE",
            on_release=self.open_gallery
        )
        
        btn_process = MDFillRoundFlatIconButton(
            icon="lock-check",
            text="HIDE & PREVIEW",
            on_release=self.process_steganography
        )
        
        buttons_layout.add_widget(btn_select)
        buttons_layout.add_widget(btn_process)
        layout.add_widget(buttons_layout)

        # زر الحفظ النهائي (يظهر بعد المعالجة)
        self.btn_download = MDRaisedButton(
            text="DOWNLOAD TO GALLERY",
            size_hint=(1, None),
            disabled=True,
            on_release=self.save_to_gallery
        )
        layout.add_widget(self.btn_download)

        self.status = MDLabel(text="Select an image to start", halign="center", theme_text_color="Hint")
        layout.add_widget(self.status)

        self.add_widget(layout)

    def open_gallery(self, *args):
        filechooser.open_file(on_selection=self.on_file_selected)

    def on_file_selected(self, selection):
        if selection:
            self.selected_image_path = selection[0]
            self.preview_img.source = self.selected_image_path
            self.status.text = "Image Selected!"

    def process_steganography(self, instance):
        if not self.selected_image_path or not self.secret_input.text:
            self.status.text = "Please select image and type message!"
            return

        try:
            img = PilImage.open(self.selected_image_path)
            message = self.secret_input.text.encode('utf-8')
            new_img = stepic.encode(img, message)
            
            # حفظ مؤقت للعرض داخل التطبيق
            temp_path = os.path.join(os.getcwd(), "temp_preview.png")
            new_img.save(temp_path, "PNG")
            
            self.output_image_path = temp_path
            self.preview_img.source = temp_path
            self.preview_img.reload() # تحديث الصورة في الواجهة
            
            self.btn_download.disabled = False
            self.status.text = "Message Hidden! Tap Download below."
        except Exception as e:
            self.status.text = f"Error: {str(e)[:20]}"

    def save_to_gallery(self, instance):
        try:
            if platform == 'android':
                dest = "/sdcard/Download/Ghost_Secret.png"
            else:
                dest = "Ghost_Secret.png"
            
            img = PilImage.open(self.output_image_path)
            img.save(dest, "PNG")
            self.status.text = f"Saved in Downloads as Ghost_Secret"
        except:
            self.status.text = "Save Failed! Check Permissions."

class GhostApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return GhostV4()

if __name__ == "__main__":
    GhostApp().run()
            
