# stt.py
# Распознавание через системный Android SpeechRecognizer.

import time

ON_ANDROID = False
try:
    from jnius import autoclass
    ON_ANDROID = True
except ImportError:
    pass


class STT:
    def __init__(self):
        self._result = None
        self._ready = False

    def transcribe(self, pcm_bytes=None) -> str:
        if not ON_ANDROID:
            return "STT работает только на Android"
        return self._recognize_live()

    def _recognize_live(self) -> str:
        from jnius import autoclass, PythonJavaClass, java_method
        from kivy.clock import mainthread

        SpeechRecognizer = autoclass("android.speech.SpeechRecognizer")
        RecognizerIntent = autoclass("android.speech.RecognizerIntent")
        Intent = autoclass("android.content.Intent")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")

        activity = PythonActivity.mActivity
        recognizer = SpeechRecognizer.createSpeechRecognizer(activity)
        outer = self

        class Listener(PythonJavaClass):
            __javainterfaces__ = ["android/speech/RecognitionListener"]

            @java_method("(Landroid/os/Bundle;)V")
            def onResults(self, bundle):
                results = bundle.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                if results and results.size() > 0:
                    outer._result = results.get(0)
                outer._ready = True

            @java_method("(Landroid/os/Bundle;)V")
            def onPartialResults(self, b): pass
            @java_method("(Landroid/os/Bundle;)V")
            def onReadyForSpeech(self, b): pass
            @java_method("(Landroid/os/Bundle;)V")
            def onBeginningOfSpeech(self, b): pass
            @java_method("(F)V")
            def onRmsChanged(self, v): pass
            @java_method("(Landroid/os/Bundle;)V")
            def onBufferReceived(self, b): pass
            @java_method("(Landroid/os/Bundle;)V")
            def onEndOfSpeech(self, b): pass
            @java_method("(I)V")
            def onError(self, code):
                outer._result = None
                outer._ready = True
            @java_method("(Landroid/os/Bundle;)V")
            def onEvent(self, t, b): pass

        listener = Listener()
        recognizer.setRecognitionListener(listener)

        intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                        RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "ru-RU")
        intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)

        self._result = None
        self._ready = False

        @mainthread
        def _start():
            recognizer.startListening(intent)

        _start()

        for _ in range(150):
            if self._ready:
                break
            time.sleep(0.1)

        try:
            recognizer.stopListening()
            recognizer.destroy()
        except Exception:
            pass
        return (self._result or "").strip()
