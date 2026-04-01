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

# وظيفة طلب الأذونات لضمان التوافق مع الأنظمة الحديثة
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
            print(f"Permission Error: {e}")

class GhostProUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_path = None
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Header (Logo + Title) كما في تصميمك
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        header.add_widget(KivyImage(source='icon.png', size_hint=(0.3, 1)))
        header.add_widget(MDLabel(text="GHOST PRO v5", font_style="H4", bold=True, halign="center"))
        layout.add_widget(header)

        # Preview - مربع عرض الصورة
        self.img_preview = KivyImage(source='', size_hint=(1, 0.5))
        layout.add_widget(self.img_preview)

        # Input - حقل الرسالة
        self.msg_input = MDTextField(
            hint_text="Enter Secret Message", 
            mode="rectangle", 
            size_hint=(1, None), 
            height="50dp"
        )
        layout.add_widget(self.msg_input)

        # Buttons - الأزرار الثلاثة
        btns = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        btns.add_widget(MDFillRoundFlatIconButton(icon="image-plus", text="SELECT", on_release=self.open_gallery))
        btns.add_widget(MDFillRoundFlatIconButton(icon="lock", text="HIDE", on_release=self.hide_message))
        btns.add_widget(MDFillRoundFlatIconButton(icon="eye", text="EXTRACT", on_release=self.extract_message))
        layout.add_widget(btns)

        # Status - حالة النظام
        self.status = MDLabel(text="Status: Ready", halign="center", theme_text_color="Hint")
        layout.add_widget(self.status)
        
        self.add_widget(layout)

    def open_gallery(self, *args):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.on_selection)
        except:
            self.status.text = "Gallery Error"

    def on_selection(self, selection):
        if selection and len(selection) > 0:
            path = selection[0]
            # تنظيف المسار للأندرويد (إزالة file:// إذا وجدت)
            if path.startswith('file://'):
                path = path[7:]
            
            self.selected_path = path
            # تحديث الواجهة فوراً
            Clock.schedule_once(lambda dt: self._refresh_image(path), 0)

    def _refresh_image(self, path):
        self.img_preview.source = path
        self.img_preview.reload() # إجبار التطبيق على عرض الصورة الجديدة
        self.status.text = "Image Selected Successfully"

    def hide_message(self, *args):
        if not self.selected_path:
            self.status.text = "Select an image first!"
            return
        try:
            from PIL import Image
            import stepic
            
            img = Image.open(self.selected_path)
            # تحويل التنسيق لضمان عمل الإخفاء على أي صورة
            img = img.convert('RGB') 
            
            message = self.msg_input.text.encode('utf-8')
            new_img = stepic.encode(img, message)
            
            # مسار الحفظ في التنزيلات
            if platform == 'android':
                path = "/sdcard/Download/ghost_hidden.png"
            else:
                path = "ghost_hidden.png"
                
            new_img.save(path, "PNG")
            self.status.text = "Success! Saved in Downloads"
        except Exception as e:
            self.status.text = f"Error: Process Failed"

    def extract_message(self, *args):
        if not self.selected_path: return
        try:
            from PIL import Image
            import stepic
            img = Image.open(self.selected_path)
            decoded = stepic.decode(img)
            self.msg_input.text = decoded if isinstance(decoded, str) else decoded.decode('utf-8')
            self.status.text = "Message Extracted"
        except:
            self.status.text = "No hidden message found"

class GhostApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return GhostProUI()

    def on_start(self):
        # طلب الأذونات بعد ثانية واحدة من تشغيل الواجهة
        Clock.schedule_once(lambda dt: ask_permissions(), 1)

if __name__ == "__main__":
    GhostApp().run()
    
