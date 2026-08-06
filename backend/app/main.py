from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:8b"


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
                "model": MODEL,
                "prompt": data.message,
                "stream": False,
                "think": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 256,
                    "keep_alive": "30m"
                }
            },
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return {
            "reply": result["response"]
        }

    except Exception as e:
        return {
            "reply": f"ERROR : {str(e)}"
        }