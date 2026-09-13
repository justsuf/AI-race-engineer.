import requests
from config import OLLAMA_HOST, OLLAMA_MODEL

SYSTEM_PROMPT = (
    "You are a concise, professional racing engineer speaking to your driver over the radio. "
    "Keep responses to one short sentence, radio-style. No filler, no greetings, just the message. "
    "Sound calm and precise, like a real motorsport engineer."
)

def get_engineer_response(situation: str) -> str:
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": situation},
                ],
                "stream": False,
            },
            timeout=10,
        )
        response.raise_for_status()
        content = response.json().get("message", {}).get("content")
        if not isinstance(content, str) or not content.strip():
            print("[Engineer] Ollama gaf geen bruikbare tekst terug.")
            return None
        return content.strip()
    except (requests.exceptions.RequestException, ValueError, TypeError, KeyError) as e:
        print(f"[Engineer] Kon Ollama niet bereiken: {e}")
        return None