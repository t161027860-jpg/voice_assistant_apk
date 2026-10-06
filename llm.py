# llm.py
import requests
import config


def ask_llm(user_text: str) -> str:
    if not user_text.strip():
        return ""
    try:
        return _ask_groq(user_text)
    except requests.exceptions.ConnectionError:
        return "Нет интернета."
    except Exception as e:
        return f"Ошибка LLM: {e}"


def _ask_groq(user_text: str) -> str:
    if not config.GROQ_API_KEY:
        return "Ключ Groq не задан. Открой настройки приложения."

    headers = {
        "Authorization": f"Bearer {config.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.GROQ_MODEL,
        "messages": [
            {"role": "system", "content": config.SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
        "temperature": config.TEMPERATURE,
        "max_tokens": config.MAX_TOKENS,
    }
    r = requests.post(config.GROQ_URL, headers=headers, json=payload, timeout=45)
    if r.status_code != 200:
        return f"Groq вернул {r.status_code}"
    return r.json()["choices"][0]["message"]["content"].strip()
