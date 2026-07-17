import os
import threading
from kivy.app import App
from kivy.uix.boxplot import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from gtts import gTTS
import speech_recognition as sr
import requests

class GeminiVoiceApp(App):
    def build(self):
        # إعداد واجهة التطبيق بشكل مشابه لنسختك المستقرة
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.label = Label(
            text="Gemini Infinite Voice\nاضغط على الزر وتحدث مباشرة", 
            font_size=22, 
            halign='center',
            size_hint_y=0.3
        )
        self.layout.add_widget(self.label)
        
        # زر التحدث والاستماع
        self.listen_button = Button(
            text="تحدث الآن 🎤",
            font_size=24,
            background_color=(0, 0.5, 0.8, 1),
            size_hint_y=0.2
        )
        self.listen_button.bind(on_press=self.start_voice_process)
        self.layout.add_widget(self.listen_button)
        
        # مفتاح الـ API الخاص بك
        self.api_key = "AQ.Ab8RN6KU5M-0Gv_QiNcmstQTNoLeVyDg11bqRGDpObYNLc24qw"
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        
        return self.layout

    def start_voice_process(self, instance):
        # تشغيل العملية في الخلفية لمنع تعليق واجهة التطبيق (Kivy Lag)
        threading.Thread(target=self.process_voice).start()

    def process_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.update_label("جاري الاستماع... 🎧")
            try:
                # ضبط الحساسية وسحب الصوت
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5)
                self.update_label("جاري معالجة الصوت... 🔄")
                
                # تحويل الصوت إلى نص عبر جوجل
                user_text = recognizer.recognize_google(audio, language='ar-EG')
                self.update_label(f"سؤالك: {user_text}")
                
                # إرسال النص إلى Gemini
                ai_response = self.ask_gemini(user_text)
                self.update_label(f"Gemini: {ai_response}")
                
                # نطق الإجابة
                self.speak_text(ai_response)
                
            except sr.UnknownValueError:
                self.update_label("لم أسمعك جيداً، اضغط وتحدث مجدداً.")
            except Exception as e:
                self.update_label(f"خطأ: {str(e)}")

    def ask_gemini(self, prompt):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        try:
            response = requests.post(self.gemini_url, json=payload, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "عذراً، فشلت في الاتصال بالذكاء الاصطناعي."
        except:
            return "مشكلة في شبكة الإنترنت."

    def speak_text(self, text):
        try:
            filename = "response.mp3"
            tts = gTTS(text=text, lang='ar')
            
            if os.path.exists(filename):
                os.remove(filename)
                
            tts.save(filename)
            sound = SoundLoader.load(filename)
            if sound:
                sound.play()
        except Exception as e:
            print(f"Error in TTS: {e}")

    def update_label(self, text):
        # تحديث النص على الشاشة بشكل آمن
        self.label.text = text

if __name__ == '__main__':
    GeminiVoiceApp().run()
