from fastapi import FastAPI
from pydantic import BaseModel

from app.ai import ask_ai
from app.memory import remember, recall
from app.prompt import SYSTEM_PROMPT

app = FastAPI()


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

    text = data.message.strip()
    lower = text.lower()

    # ===========================
    # SIAPA NAMA SAYA
    # ===========================
    if (
        "siapa nama saya" in lower
        or "namaku siapa" in lower
        or "nama saya siapa" in lower
    ):

        nama = recall("nama")

        if nama:
            return {
                "reply": f"Nama Anda adalah {nama}."
            }

        return {
            "reply": "Maaf, saya belum mengetahui nama Anda."
        }

    # ===========================
    # MENYIMPAN NAMA
    # ===========================
    if lower.startswith("nama saya "):

        nama = text[10:].strip()

        # jangan simpan jika itu pertanyaan
        if nama.lower() in [
            "",
            "siapa",
            "?",
            "apa",
            "siapa?",
            "apa?"
        ]:
            pass
        else:
            remember("nama", nama)

            return {
                "reply": f"Baik, saya akan mengingat nama Anda {nama}."
            }

    # ===========================
    # PROMPT AI
    # ===========================
    nama = recall("nama")

    prompt = SYSTEM_PROMPT

    if nama:
        prompt += f"\n\nNama pengguna adalah {nama}."

    prompt += f"\n\nUser: {text}\nZAI:"

    jawaban = ask_ai(prompt)

    return {
        "reply": jawaban
    }