# wake_word.py
# Упрощённая версия: ждём нажатия кнопки в UI.

import time


class WakeWordDetector:
    def __init__(self, *args, **kwargs):
        self._triggered = False

    def trigger(self):
        self._triggered = True

    def wait_for_wake_word(self) -> bool:
        self._triggered = False
        while not self._triggered:
            time.sleep(0.1)
        return True
