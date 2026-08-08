from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import re
from typing import Optional


# ============================================================
# ZAI MODULES
# ============================================================

from app.ai import ask_ai

from app.memory import (
    remember,
    recall,
    forget,
    clear_memory,
    all_memory,
    get_memory_summary,

    add_chat_message,
    get_chat_history,
    get_chat_history_text,
    chat_history_count,
    clear_chat_history,
)

from app.prompt import SYSTEM_PROMPT


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="ZAI AI",
    description="Personal AI Assistant ZAI",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class Chat(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Pesan pengguna"
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "assistant": "ZAI",
        "status": "ONLINE",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "assistant": "ZAI"
    }


# ============================================================
# HELPER MEMORY
# ============================================================

def get_memory_answer(
    key: str,
    template: str
):

    value = recall(key)

    if value:

        return {
            "reply": template.format(value)
        }

    return {
        "reply": (
            "Maaf, saya belum mengetahui "
            "informasi tersebut."
        )
    }


# ============================================================
# AUTO MEMORY
# ============================================================

def save_memory_from_text(
    text: str
) -> Optional[dict]:

    clean_text = text.strip()

    patterns = [

        (
            r"^nama saya\s+(.+?)\s*$",
            "nama",
            "Baik, saya akan mengingat nama Anda {}."
        ),

        (
            r"^nama ku\s+(.+?)\s*$",
            "nama",
            "Baik, saya akan mengingat nama Anda {}."
        ),

        (
            r"^namaku\s+(.+?)\s*$",
            "nama",
            "Baik, saya akan mengingat nama Anda {}."
        ),

        (
            r"^umur saya\s+(\d+)\s*$",
            "umur",
            "Baik, saya ingat umur Anda {} tahun."
        ),

        (
            r"^usia saya\s+(\d+)\s*$",
            "umur",
            "Baik, saya ingat usia Anda {} tahun."
        ),

        (
            r"^saya tinggal di\s+(.+?)\s*$",
            "alamat",
            "Baik, saya akan mengingat bahwa Anda tinggal di {}."
        ),

        (
            r"^alamat saya\s+(.+?)\s*$",
            "alamat",
            "Baik, saya akan mengingat alamat Anda di {}."
        ),

        (
            r"^hobi saya\s+(.+?)\s*$",
            "hobi",
            "Baik, saya akan mengingat hobi Anda yaitu {}."
        ),

        (
            r"^hobi ku\s+(.+?)\s*$",
            "hobi",
            "Baik, saya akan mengingat hobi Anda yaitu {}."
        ),

        (
            r"^warna favorit saya\s+(.+?)\s*$",
            "warna",
            "Baik, saya akan mengingat warna favorit Anda yaitu {}."
        ),

        (
            r"^warna favoritku\s+(.+?)\s*$",
            "warna",
            "Baik, saya akan mengingat warna favorit Anda yaitu {}."
        ),

        (
            r"^makanan favorit saya\s+(.+?)\s*$",
            "makanan",
            "Baik, saya akan mengingat makanan favorit Anda yaitu {}."
        ),

        (
            r"^makanan favoritku\s+(.+?)\s*$",
            "makanan",
            "Baik, saya akan mengingat makanan favorit Anda yaitu {}."
        ),
    ]

    lower = clean_text.lower()

    for pattern, key, reply in patterns:

        match = re.match(
            pattern,
            lower,
            re.IGNORECASE
        )

        if not match:
            continue

        value = match.group(1).strip()

        if not value:
            continue

        invalid_values = {
            "siapa",
            "apa",
            "berapa",
            "dimana",
            "di mana",
            "?"
        }

        if value.lower() in invalid_values:
            continue

        remember(
            key,
            value
        )

        return {
            "reply": reply.format(value)
        }

    return None


# ============================================================
# MEMORY SUMMARY
# ============================================================

def format_memory_summary() -> str:

    memory = get_memory_summary()

    if not memory:

        return (
            "Saat ini saya belum memiliki "
            "informasi pribadi yang tersimpan."
        )

    return (
        "Berikut informasi yang saya ingat:\n\n"
        f"{memory}"
    )


# ============================================================
# DETECT MEMORY SUMMARY QUESTION
# ============================================================

def is_memory_summary_question(
    text: str
) -> bool:

    lower = text.lower().strip()

    questions = [

        "apa yang kamu ingat tentang saya",
        "apa yang kamu ingat tentang aku",
        "apa saja yang kamu ingat tentang saya",
        "apa saja yang kamu ingat tentang aku",
        "kamu ingat apa tentang saya",
        "kamu ingat apa tentang aku",
        "apa yang anda ingat tentang saya",
        "apa saja yang anda ingat tentang saya",

        "tampilkan memory saya",
        "tampilkan memori saya",
        "lihat memory saya",
        "lihat memori saya",
        "memory saya apa",
        "memori saya apa",
    ]

    return lower in questions


# ============================================================
# MEMORY QUERY
# ============================================================

def handle_memory_query(
    text: str
) -> Optional[dict]:

    lower = text.lower().strip()

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    if is_memory_summary_question(text):

        return {
            "reply": format_memory_summary()
        }

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    if (
        "siapa nama saya" in lower
        or "nama saya siapa" in lower
        or "namaku siapa" in lower
        or "nama saya apa" in lower
    ):

        return get_memory_answer(
            "nama",
            "Nama Anda adalah {}."
        )

    # --------------------------------------------------------
    # AGE
    # --------------------------------------------------------

    if (
        "umur saya berapa" in lower
        or "berapa umur saya" in lower
        or "usia saya berapa" in lower
        or "berapa usia saya" in lower
    ):

        return get_memory_answer(
            "umur",
            "Umur Anda {} tahun."
        )

    # --------------------------------------------------------
    # ADDRESS
    # --------------------------------------------------------

    if (
        "alamat saya dimana" in lower
        or "alamat saya di mana" in lower
        or "saya tinggal dimana" in lower
        or "saya tinggal di mana" in lower
    ):

        return get_memory_answer(
            "alamat",
            "Anda tinggal di {}."
        )

    # --------------------------------------------------------
    # HOBBY
    # --------------------------------------------------------

    if (
        "apa hobi saya" in lower
        or "hobi saya apa" in lower
        or "hobi saya apa ya" in lower
    ):

        return get_memory_answer(
            "hobi",
            "Hobi Anda adalah {}."
        )

    # --------------------------------------------------------
    # COLOR
    # --------------------------------------------------------

    if (
        "warna favorit saya apa" in lower
        or "warna favorit saya" in lower
        or "warna saya apa" in lower
    ):

        return get_memory_answer(
            "warna",
            "Warna favorit Anda adalah {}."
        )

    # --------------------------------------------------------
    # FOOD
    # --------------------------------------------------------

    if (
        "makanan favorit saya apa" in lower
        or "makanan favorit saya" in lower
        or "makanan saya apa" in lower
    ):

        return get_memory_answer(
            "makanan",
            "Makanan favorit Anda adalah {}."
        )

    return None


# ============================================================
# MEMORY COMMANDS
# ============================================================

def handle_memory_commands(
    text: str
) -> Optional[dict]:

    lower = text.lower().strip()

    # --------------------------------------------------------
    # FORGET NAME
    # --------------------------------------------------------

    if (
        "lupakan nama saya" in lower
        or "hapus nama saya" in lower
    ):

        if forget("nama"):

            return {
                "reply": (
                    "Baik. Saya sudah "
                    "menghapus nama Anda dari memory."
                )
            }

        return {
            "reply": (
                "Nama Anda belum tersimpan "
                "di memory."
            )
        }

    # --------------------------------------------------------
    # FORGET AGE
    # --------------------------------------------------------

    if (
        "lupakan umur saya" in lower
        or "hapus umur saya" in lower
    ):

        if forget("umur"):

            return {
                "reply": (
                    "Baik. Saya sudah "
                    "menghapus umur Anda dari memory."
                )
            }

        return {
            "reply": (
                "Umur Anda belum tersimpan "
                "di memory."
            )
        }

    # --------------------------------------------------------
    # FORGET ADDRESS
    # --------------------------------------------------------

    if (
        "lupakan alamat saya" in lower
        or "hapus alamat saya" in lower
    ):

        if forget("alamat"):

            return {
                "reply": (
                    "Baik. Saya sudah "
                    "menghapus alamat Anda dari memory."
                )
            }

        return {
            "reply": (
                "Alamat Anda belum tersimpan "
                "di memory."
            )
        }

    # --------------------------------------------------------
    # CLEAR PROFILE MEMORY
    # --------------------------------------------------------

    if (
        lower == "hapus semua memory"
        or lower == "hapus semua memori"
        or lower == "reset memory"
        or lower == "reset memori"
    ):

        clear_memory()

        return {
            "reply": (
                "Baik. Seluruh memory profil "
                "Anda sudah dihapus."
            )
        }

    # --------------------------------------------------------
    # CLEAR CHAT HISTORY
    # --------------------------------------------------------

    if (
        lower == "hapus riwayat chat"
        or lower == "hapus chat history"
        or lower == "reset chat history"
        or lower == "hapus percakapan"
    ):

        clear_chat_history()

        return {
            "reply": (
                "Baik. Seluruh riwayat percakapan "
                "sudah dihapus."
            )
        }

    return None


# ============================================================
# BUILD AI PROMPT
# ============================================================

def build_ai_prompt(
    user_message: str
) -> str:

    prompt = SYSTEM_PROMPT

    # --------------------------------------------------------
    # PROFILE MEMORY
    # --------------------------------------------------------

    memory_summary = get_memory_summary()

    if not memory_summary:

        memory_summary = (
            "Belum ada informasi pribadi "
            "yang tersimpan."
        )

    prompt += (
        "\n\n===== MEMORY PENGGUNA =====\n"
        f"{memory_summary}"
    )

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    history = get_chat_history_text(
        limit=20
    )

    if not history:

        history = (
            "Belum ada riwayat percakapan."
        )

    prompt += (
        "\n\n===== RIWAYAT PERCAKAPAN =====\n"
        f"{history}"
    )

    # --------------------------------------------------------
    # CURRENT MESSAGE
    # --------------------------------------------------------

    prompt += (
        "\n\n===== PESAN TERBARU =====\n"
        f"User: {user_message}\n"
        "ZAI:"
    )

    return prompt


# ============================================================
# CHAT
# ============================================================

@app.post("/chat")
def chat(data: Chat):

    text = data.message.strip()

    if not text:

        raise HTTPException(
            status_code=400,
            detail="Pesan tidak boleh kosong."
        )

    # --------------------------------------------------------
    # MEMORY AUTO SAVE
    # --------------------------------------------------------

    memory_result = save_memory_from_text(
        text
    )

    if memory_result:

        add_chat_message(
            "user",
            text
        )

        add_chat_message(
            "assistant",
            memory_result["reply"]
        )

        return memory_result

    # --------------------------------------------------------
    # MEMORY QUERY
    # --------------------------------------------------------

    memory_query_result = handle_memory_query(
        text
    )

    if memory_query_result:

        add_chat_message(
            "user",
            text
        )

        add_chat_message(
            "assistant",
            memory_query_result["reply"]
        )

        return memory_query_result

    # --------------------------------------------------------
    # MEMORY COMMAND
    # --------------------------------------------------------

    command_result = handle_memory_commands(
        text
    )

    if command_result:

        add_chat_message(
            "user",
            text
        )

        add_chat_message(
            "assistant",
            command_result["reply"]
        )

        return command_result

    # --------------------------------------------------------
    # BUILD AI PROMPT
    # --------------------------------------------------------

    prompt = build_ai_prompt(
        text
    )

    # --------------------------------------------------------
    # CALL AI
    # --------------------------------------------------------

    try:

        jawaban = ask_ai(
            prompt
        )

    except Exception as error:

        print(
            f"[ZAI AI ERROR] {error}"
        )

        return {
            "reply": (
                "Maaf, terjadi masalah saat "
                "menghubungkan ke AI."
            )
        }

    if not jawaban:

        jawaban = (
            "Maaf, saya belum mendapatkan "
            "jawaban dari AI."
        )

    # --------------------------------------------------------
    # SAVE CHAT HISTORY
    # --------------------------------------------------------

    add_chat_message(
        "user",
        text
    )

    add_chat_message(
        "assistant",
        jawaban
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "reply": jawaban
    }


# ============================================================
# GET MEMORY
# ============================================================

@app.get("/memory")
def get_memory():

    return {
        "memory": all_memory()
    }


# ============================================================
# GET MEMORY SUMMARY
# ============================================================

@app.get("/memory/summary")
def memory_summary():

    return {
        "memory": get_memory_summary()
    }


# ============================================================
# GET CHAT HISTORY
# ============================================================

@app.get("/history")
def history(
    limit: int = 50
):

    if limit < 1:
        limit = 1

    if limit > 200:
        limit = 200

    return {
        "count": chat_history_count(),
        "messages": get_chat_history(limit)
    }


# ============================================================
# CLEAR MEMORY
# ============================================================

@app.delete("/memory")
def delete_memory():

    clear_memory()

    return {
        "success": True,
        "message": (
            "Seluruh memory profil "
            "telah dihapus."
        )
    }


# ============================================================
# CLEAR CHAT HISTORY
# ============================================================

@app.delete("/history")
def delete_history():

    clear_chat_history()

    return {
        "success": True,
        "message": (
            "Seluruh riwayat percakapan "
            "sudah dihapus."
        )
    }


# ============================================================
# STATUS
# ============================================================

@app.get("/status")
def status():

    return {
        "assistant": "ZAI",
        "status": "ONLINE",
        "memory_items": len(
            all_memory()
        ),
        "chat_messages": chat_history_count()
    }