from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.window import Window
from PIL import Image
import stepic
import os

# تحديد مسار الحفظ الخاص بالتطبيق (لا يحتاج أذونات)
if platform == 'android':
    from android.storage import app_storage_path
    APP_FOLDER = app_storage_path()
else:
    APP_FOLDER = os.getcwd()

class GhostProUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_path = None
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 1. العنوان
        header = MDLabel(
            text="👻 GHOST PRO", 
            halign="center", 
            font_style="H4", 
            bold=True,
            theme_text_color="Custom",
            text_color=(0.2, 0.6, 1, 1),
            size_hint_y=None,
            height=60
        )
        layout.add_widget(header)

        # 2. منطقة عرض الصورة
        self.img_preview = KivyImage(source='', size_hint=(1, 0.5))
        layout.add_widget(self.img_preview)

        # 3. حقل النص السري
        self.msg_input = MDTextField(
            hint_text="Enter Secret Message...",
            mode="rectangle",
            size_hint=(1, None),
            height="50dp"
        )
        layout.add_widget(self.msg_input)

        # 4. الأزرار
        btns = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.15))
        
        btn_select = MDFillRoundFlatIconButton(
            icon="image-plus", 
            text="SELECT", 
            on_release=self.open_gallery
        )
        btn_hide = MDFillRoundFlatIconButton(
            icon="lock", 
            text="HIDE", 
            on_release=self.hide_message
        )
        btn_extract = MDFillRoundFlatIconButton(
            icon="eye", 
            text="EXTRACT", 
            on_release=self.extract_message
        )

        btns.add_widget(btn_select)
        btns.add_widget(btn_hide)
        btns.add_widget(btn_extract)
        layout.add_widget(btns)

        # 5. شريط الحالة
        self.status = MDLabel(
            text="Status: Ready", 
            halign="center", 
            theme_text_color="Hint",
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.status)
        
        self.add_widget(layout)

    def open_gallery(self, *args):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.on_selection, filters=[("Images", "*.png", "*.jpg", "*.jpeg")])
        except Exception as e:
            self.status.text = f"Gallery Error: {str(e)}"

    def on_selection(self, selection):
        if selection and len(selection) > 0:
            path = selection[0]
            # تنظيف المسار لأجهزة أندرويد
            if path.startswith('file://'):
                path = path[7:]
            
            # التحقق من وجود الملف
            if os.path.exists(path):
                self.selected_path = path
                self.img_preview.source = path
                self.img_preview.reload()
                self.status.text = "Image Selected"
            else:
                self.status.text = "File not found!"

    def hide_message(self, *args):
        if not self.selected_path:
            self.status.text = "Select an image first!"
            return
        
        if not self.msg_input.text:
            self.status.text = "Enter a message first!"
            return

        try:
            # فتح الصورة وتحويلها
            img = Image.open(self.selected_path).convert('RGB')
            message = self.msg_input.text.encode('utf-8')
            
            # تشفير الرسالة داخل الصورة
            new_img = stepic.encode(img, message)
            
            # حفظ الصورة في مجلد التطبيق الخاص (آمن ولا يحتاج أذونات)
            save_name = "ghost_hidden.png"
            save_path = os.path.join(APP_FOLDER, save_name)
            
            new_img.save(save_path, "PNG")
            
            self.status.text = f"Saved to: {save_name}"
            self.show_popup("Success", f"Image saved inside app folder.\nPath: {save_path}")
            
        except Exception as e:
            self.status.text = f"Error: {str(e)}"
            print(f"Error: {e}")

    def extract_message(self, *args):
        if not self.selected_path:
            self.status.text = "Select an image first!"
            return
        
        try:
            img = Image.open(self.selected_path).convert('RGB')
            decoded = stepic.decode(img)
            
            if isinstance(decoded, bytes):
                msg = decoded.decode('utf-8')
            else:
                msg = str(decoded)
                
            self.msg_input.text = msg
            self.status.text = "Extracted Successfully!"
            
        except Exception as e:
            self.status.text = "No hidden message found."
            print(f"Extract Error: {e}")

    def show_popup(self, title, text):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

class GhostApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return GhostProUI()

    def on_start(self):
        # لا نحتاج لطلب أذونات التخزين لأننا نحفظ في مجلد التطبيق
        pass

if __name__ == "__main__":
    GhostApp().run()
