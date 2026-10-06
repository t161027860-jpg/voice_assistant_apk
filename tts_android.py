# tts_android.py
import time
import config

_tts_engine = None
_ready = False


def _init_android_tts():
    global _tts_engine, _ready
    if _tts_engine is not None:
        return
    try:
        from jnius import autoclass, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread

        TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
        Locale = autoclass("java.util.Locale")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")

        class _Listener(PythonJavaClass):
            __javainterfaces__ = ["android/speech/tts/TextToSpeech$OnInitListener"]

            @java_method("(I)V")
            def onInit(self, status):
                global _ready
                _ready = status == 0

        listener = _Listener()
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def create_engine():
            global _tts_engine
            _tts_engine = TextToSpeech(activity, listener)
            _tts_engine.setLanguage(Locale("ru", "RU"))

        create_engine()
    except Exception as e:
        print(f"TTS init error: {e}")


def speak(text: str):
    if not text:
        return
    try:
        _init_android_tts()
        for _ in range(30):
            if _ready:
                break
            time.sleep(0.1)
        if not _ready:
            print("TTS не готов")
            return
        from jnius import autoclass
        from android.runnable import run_on_ui_thread
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        QUEUE_FLUSH = 0

        @run_on_ui_thread
        def _say():
            _tts_engine.speak(text, QUEUE_FLUSH, None, "asst_utt")

        _say()
        time.sleep(min(1 + len(text) * 0.06, 15))
    except Exception as e:
        print(f"TTS error: {e}")
