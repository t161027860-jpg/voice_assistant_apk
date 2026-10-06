# config.py
import os

# ---------- Wake word ----------
WAKE_PHRASE = ["слушай", "запиши"]
WAKE_ALTERNATIVES = [
    ["слушай", "запиши"],
    ["слушай", "запись"],
]

# ---------- Аудио ----------
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 4000
SILENCE_THRESHOLD = 500
SILENCE_DURATION = 2.0
MAX_RECORD_SECONDS = 30

# ---------- Vosk ----------
VOSK_MODEL_PATH = "vosk-model-small-ru-0.22"

# ---------- LLM ----------
LLM_BACKEND = "groq"
GROQ_API_KEY = ""
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = (
    "Ты — голосовой ассистент. Отвечай кратко (1–3 предложения), "
    "на русском языке, дружелюбно. Без markdown и списков."
)
MAX_TOKENS = 200
TEMPERATURE = 0.7

# ---------- TTS ----------
TTS_BACKEND = "android"
EDGE_VOICE = "ru-RU-DmitryNeural"

# ---------- Настройки пользователя ----------
PREFERRED_MIC_ID = None
PREFERRED_OUTPUT_ID = None
