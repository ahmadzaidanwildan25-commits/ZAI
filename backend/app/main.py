from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:8b"


class Chat(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "assistant": "ZAI",
        "status": "ONLINE"
    }


@app.post("/chat")
def chat(data: Chat):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": data.message,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        answer = response.json()["response"]

        return {
            "reply": answer
        }

    except Exception as e:
        return {
            "reply": f"Terjadi kesalahan: {str(e)}"
        }