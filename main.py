import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from gtts import gTTS

class TextToSpeechApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # عنوان التطبيق
        self.label = Label(text="تحويل النص إلى صوت عربي", font_size=24, size_hint_y=0.1)
        self.layout.add_widget(self.label)
        
        # خانة إدخال النص
        self.text_input = TextInput(
            hint_text="اكتب النص العربي هنا...", 
            font_size=20, 
            multiline=True,
            halign='right'
        )
        self.layout.add_widget(self.text_input)
        
        # زر التشغيل
        self.play_button = Button(
            text="نطق النص", 
            font_size=22, 
            background_color=(0, 0.6, 0.8, 1),
            size_hint_y=0.15
        )
        self.play_button.bind(on_press=self.speak_text)
        self.layout.add_widget(self.play_button)
        
        return self.layout

    def speak_text(self, instance):
        text = self.text_input.text.strip()
        if text:
            try:
                # إنشاء الملف الصوتي باستخدام gTTS
                tts = gTTS(text=text, lang='ar')
                filename = "speech.mp3"
                
                # التأكد من حذف أي ملف قديم بنفس الاسم لمنع التداخل
                if os.path.exists(filename):
                    os.remove(filename)
                    
                tts.save(filename)
                
                # تشغيل الصوت عبر مكتبة Kivy الأساسية
                sound = SoundLoader.load(filename)
                if sound:
                    sound.play()
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    TextToSpeechApp().run()
