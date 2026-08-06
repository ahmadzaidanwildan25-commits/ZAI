import requests
from app.config import *

def ask_ai(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model":MODEL_NAME,
            "prompt":prompt,
            "stream":False,
            "think":False
        },
        timeout=TIMEOUT
    )

    response.raise_for_status()

    return response.json()["response"]
