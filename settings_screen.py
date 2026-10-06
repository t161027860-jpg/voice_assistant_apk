# settings_screen.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp

import config
from bluetooth_helper import list_bluetooth_devices


class SettingsScreen(BoxLayout):
    def __init__(self, on_close, **kwargs):
        super().__init__(orientation="vertical", padding=dp(15), spacing=dp(10), **kwargs)
        self.on_close = on_close

        self.add_widget(Label(text="Настройки", font_size="22sp", size_hint=(1, 0.08)))

        scroll = ScrollView(size_hint=(1, 0.82))
        body = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=dp(5))
        body.bind(minimum_height=body.setter("height"))

        body.add_widget(Label(text="Ключ Groq", font_size="18sp",
                              size_hint=(1, None), height=dp(30)))
        body.add_widget(Label(
            text="Получи на console.groq.com/keys",
            font_size="12sp", size_hint=(1, None), height=dp(25)
        ))
        self.groq_input = TextInput(
            text=config.GROQ_API_KEY, multiline=False, password=True,
            size_hint=(1, None), height=dp(45)
        )
        body.add_widget(self.groq_input)

        body.add_widget(Label(text="Bluetooth-устройства", font_size="18sp",
                              size_hint=(1, None), height=dp(30)))

        self.bt_label = Label(
            text="Нажми «Обновить»",
            size_hint=(1, None), height=dp(120), font_size="13sp"
        )
        body.add_widget(self.bt_label)

        btn_bt = Button(text="Обновить BT", size_hint=(1, None), height=dp(45))
        btn_bt.bind(on_press=self.refresh_bt)
        body.add_widget(btn_bt)

        btn_open_bt = Button(text="Открыть настройки Bluetooth Android",
                             size_hint=(1, None), height=dp(45))
        btn_open_bt.bind(on_press=self.open_android_bt)
        body.add_widget(btn_open_bt)

        scroll.add_widget(body)
        self.add_widget(scroll)

        btns = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        save = Button(text="Сохранить")
        save.bind(on_press=self.save)
        btns.add_widget(save)

        close = Button(text="Закрыть")
        close.bind(on_press=lambda *_: self.on_close())
        btns.add_widget(close)
        self.add_widget(btns)

    def refresh_bt(self, *_):
        devices = list_bluetooth_devices()
        if not devices:
            self.bt_label.text = ("Нет сопряжённых устройств.\n"
                                  "Подключи наушники в настройках Android.")
            return
        self.bt_label.text = "\n".join(f"- {d['name']}" for d in devices)

    def open_android_bt(self, *_):
        try:
            from jnius import autoclass
            Intent = autoclass("android.content.Intent")
            Settings = autoclass("android.provider.Settings")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            intent = Intent(Settings.ACTION_BLUETOOTH_SETTINGS)
            PythonActivity.mActivity.startActivity(intent)
        except Exception as e:
            print(f"BT settings error: {e}")

    def save(self, *_):
        config.GROQ_API_KEY = self.groq_input.text.strip()
        _save_to_file()
        popup = Popup(title="OK", content=Label(text="Сохранено"),
                      size_hint=(0.7, 0.3))
        popup.open()
        Clock.schedule_once(lambda *_: popup.dismiss(), 1.2)


def _save_to_file():
    import json, os
    try:
        from android.storage import app_storage_path
        path = os.path.join(app_storage_path(), "user_config.json")
    except Exception:
        path = "user_config.json"
    with open(path, "w") as f:
        json.dump({"groq_api_key": config.GROQ_API_KEY}, f)
    print(f"Saved: {path}")


def load_user_config():
    import json, os
    try:
        from android.storage import app_storage_path
        path = os.path.join(app_storage_path(), "user_config.json")
    except Exception:
        path = "user_config.json"
    if not os.path.exists(path):
        return
    try:
        with open(path) as f:
            data = json.load(f)
        config.GROQ_API_KEY = data.get("groq_api_key", "")
    except Exception as e:
        print(f"load error: {e}")
