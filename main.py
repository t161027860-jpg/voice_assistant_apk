# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp

import config
from stt import STT
from llm import ask_llm
from tts_android import speak as tts_speak
from settings_screen import SettingsScreen, load_user_config

try:
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.RECORD_AUDIO,
        Permission.INTERNET,
        Permission.BLUETOOTH,
        Permission.BLUETOOTH_ADMIN,
    ])
except Exception:
    pass


class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(15), spacing=dp(10), **kwargs)

        self.status = Label(text="Готов", font_size="20sp", size_hint=(1, 0.1))
        self.add_widget(self.status)

        self.log_view = Label(
            text="", font_size="13sp", size_hint=(1, 0.65),
            halign="left", valign="top"
        )
        scroll = ScrollView(size_hint=(1, 0.65))
        scroll.add_widget(self.log_view)
        self.add_widget(scroll)

        btn_listen = Button(text="Слушаю", size_hint=(1, 0.12), font_size="20sp")
        btn_listen.bind(on_press=self.on_listen)
        self.add_widget(btn_listen)

        btn_settings = Button(text="Настройки", size_hint=(1, 0.08))
        btn_settings.bind(on_press=self.open_settings)
        self.add_widget(btn_settings)

        self._logs = []
        self.stt = STT()

    def log(self, msg):
        Clock.schedule_once(lambda *_: self._append_log(msg))

    def _append_log(self, msg):
        self._logs.append(msg)
        self._logs = self._logs[-15:]
        self.log_view.text = "\n".join(self._logs)

    def set_status(self, text):
        Clock.schedule_once(lambda *_: setattr(self.status, "text", text))

    def open_settings(self, *_):
        settings = SettingsScreen(on_close=self.close_settings)
        self.clear_widgets()
        self.add_widget(settings)

    def close_settings(self):
        self.clear_widgets()
        self.__init__()

    def on_listen(self, *_):
        import threading
        self.set_status("Слушаю...")
        self.log("Начало распознавания")
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        try:
            text = self.stt.transcribe()
            if not text:
                self.log("Не расслышал")
                self.set_status("Готов")
                return
            self.log(f"Ты: {text}")
            self.set_status("Думаю...")
            answer = ask_llm(text)
            self.log(f"Ответ: {answer}")
            self.set_status("Говорю")
            tts_speak(answer)
            self.set_status("Готов")
        except Exception as e:
            self.log(f"Ошибка: {e}")
            self.set_status("Ошибка")


class VoiceApp(App):
    def build(self):
        load_user_config()
        self.title = "Voice Assistant"
        return Root()


if __name__ == "__main__":
    VoiceApp().run()
