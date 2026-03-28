from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout

class JubaShabahApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        screen = MDScreen()
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.msg = MDTextField(hint_text="Juba Al Shabah - اكتب هنا", mode="rectangle")
        btn = MDRaisedButton(text="🔒 تشفير الآن", size_hint=(1, None))
        layout.add_widget(self.msg)
        layout.add_widget(btn)
        screen.add_widget(layout)
        return screen

if __name__ == "__main__":
    JubaShabahApp().run()
