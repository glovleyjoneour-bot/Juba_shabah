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

# --- نظام طلب الأذونات للأندرويد ---
def ask_permissions(*args):
    if platform == 'android':
        try:
            from android.permissions import request_permissions, Permission
            # نطلب كل صلاحيات الذاكرة المتاحة لتجنب الكراش
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE
            ])
        except Exception as e:
            print(f"Permission Error: {e}")

class GhostFinalUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_path = None
        self.temp_file = None
        
        # تشغيل طلب الأذونات بعد ثانية من فتح التطبيق (تكتيك لتجاوز الفحص الأولي)
        Clock.schedule_once(ask_permissions, 1)
        
        # الواجهة الرئيسية (ترتيب عمودي) كما في الصور
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

        # 3. حقل النص (الإدخال والاستخراج)
        self.msg_field = MDTextField(
            hint_text="Enter Secret Message or Extract from Image",
            mode="rectangle",
            icon_right="email-lock",
            size_hint=(1, None)
        )
        main_layout.add_widget(self.msg_field)

        # 4. صف الأزرار الرئيسي (SELECT - HIDE - EXTRACT)
        btns_row = BoxLayout(spacing=10, size_hint=(1, 0.1))
        
        btn_select = MDFillRoundFlatIconButton(
            icon="image-plus", text="SELECT", 
            on_release=self.open_gallery
        )
        btn_hide = MDFillRoundFlatIconButton(
            icon="lock", text="HIDE", 
            on_release=self.process_hide
        )
        btn_extract = MDFillRoundFlatIconButton(
            icon="eye-check", text="EXTRACT",
            md_bg_color=(0, 0.5, 0.2, 1), # لون أخضر مميز كما في الصورة
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
            text="Status: System Ready", 
            halign="center", 
            theme_text_color="Secondary"
        )
        main_layout.add_widget(self.status_label)

        self.add_widget(main_layout)

    # --- الدوال البرمجية مع الاستدعاء الذكي (Lazy Imports) لمنع الكراش ---
    def open_gallery(self, *args):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.on_selection)
        except:
            self.status_label.text = "Error opening gallery"

    def on_selection(self, selection):
        if selection:
            self.selected_path = selection[0]
            self.img_preview.source = self.selected_path
            self.status_label.text = "Image Selected!"

    def process_hide(self, *args):
        from PIL import Image as PilImage
        import stepic # استدعاء داخلي لتجنب ثقل الإقلاع
        
        if not self.selected_path or not self.msg_field.text:
            self.status_label.text = "Missing Image or Message!"
            return
        try:
            img = PilImage.open(self.selected_path)
            # تشفير النص داخل الصورة
            encoded_data = stepic.encode(img, self.msg_field.text.encode('utf-8'))
            self.temp_file = os.path.join(os.getcwd(), "temp_ghost.png")
            encoded_data.save(self.temp_file, "PNG")
            
            # تحديث العرض
            self.img_preview.source = self.temp_file
            self.img_preview.reload()
            self.btn_download.disabled = False
            self.status_label.text = "Message Hidden! Ready to Save."
        except Exception as e:
            self.status_label.text = f"Error: {str(e)[:20]}"

    def process_extract(self, *args):
        from PIL import Image as PilImage
        import stepic
        
        if not self.selected_path:
            self.status_label.text = "Select an image first!"
            return
        try:
            img = PilImage.open(self.selected_path)
            decoded_msg = stepic.decode(img)
            if isinstance(decoded_msg, bytes):
                decoded_msg = decoded_msg.decode('utf-8')
            self.msg_field.text = decoded_msg
            self.status_label.text = "Message Extracted Successfully!"
        except:
            self.status_label.text = "No hidden message found."

    def save_to_downloads(self, *args):
        from PIL import Image as PilImage
        try:
            # تحديد مسار التحميل في أندرويد
            target = "/sdcard/Download/Ghost_Secret_Image.png" if platform == 'android' else "Ghost_Secret_Image.png"
            output_img = PilImage.open(self.temp_file)
            output_img.save(target, "PNG")
            self.status_label.text = "Saved to Downloads folder!"
        except:
            self.status_label.text = "Permission Denied! Check Settings."

class GhostApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return GhostFinalUI()

if __name__ == "__main__":
    GhostApp().run()
    
