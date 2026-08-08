import json
import os
from typing import Any


# ============================================================
# ZAI MEMORY SYSTEM
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
CHAT_HISTORY_FILE = os.path.join(DATA_DIR, "chat_history.json")


# ============================================================
# INITIALIZE DATA DIRECTORY
# ============================================================

os.makedirs(DATA_DIR, exist_ok=True)


# ============================================================
# GENERIC JSON HELPERS
# ============================================================

def _load_json(file_path: str, default: Any):
    """
    Membaca file JSON dengan aman.
    Jika file belum ada atau rusak, kembalikan default.
    """

    if not os.path.exists(file_path):
        return default

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return default


def _save_json(file_path: str, data: Any):
    """
    Menyimpan data JSON dengan aman.
    """

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    temp_file = file_path + ".tmp"

    try:
        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        os.replace(temp_file, file_path)

    except OSError:

        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass

        raise


# ============================================================
# LONG-TERM MEMORY
# ============================================================

def load_memory() -> dict:
    """
    Mengambil seluruh memory pengguna.
    """

    data = _load_json(
        MEMORY_FILE,
        {}
    )

    if not isinstance(data, dict):
        return {}

    return data


def save_memory(data: dict):
    """
    Menyimpan seluruh memory pengguna.
    """

    if not isinstance(data, dict):
        data = {}

    _save_json(
        MEMORY_FILE,
        data
    )


def remember(key: str, value: str):
    """
    Menyimpan satu memory.
    """

    key = str(key).strip()
    value = str(value).strip()

    if not key or not value:
        return False

    data = load_memory()

    data[key] = value

    save_memory(data)

    return True


def recall(key: str):
    """
    Mengambil satu memory.
    """

    data = load_memory()

    return data.get(key)


def forget(key: str):
    """
    Menghapus satu memory.
    """

    data = load_memory()

    if key in data:

        del data[key]

        save_memory(data)

        return True

    return False


def clear_memory():
    """
    Menghapus seluruh long-term memory.
    """

    save_memory({})


def all_memory() -> dict:
    """
    Mengambil seluruh memory.
    """

    return load_memory()


def get_memory_summary() -> str:
    """
    Membuat ringkasan memory untuk diberikan kepada AI.
    """

    data = load_memory()

    if not data:
        return ""

    labels = {
        "nama": "Nama pengguna",
        "umur": "Umur pengguna",
        "alamat": "Alamat pengguna",
        "warna": "Warna favorit pengguna",
        "hobi": "Hobi pengguna",
        "makanan": "Makanan favorit pengguna",
    }

    lines = []

    for key, value in data.items():

        label = labels.get(
            key,
            key.replace("_", " ").title()
        )

        lines.append(
            f"- {label}: {value}"
        )

    return "\n".join(lines)


# ============================================================
# CHAT HISTORY
# ============================================================

def load_chat_history() -> list:
    """
    Mengambil seluruh chat history.
    """

    data = _load_json(
        CHAT_HISTORY_FILE,
        []
    )

    if not isinstance(data, list):
        return []

    return data


def save_chat_history(history: list):
    """
    Menyimpan chat history.
    """

    if not isinstance(history, list):
        history = []

    _save_json(
        CHAT_HISTORY_FILE,
        history
    )


def add_chat_message(
    role: str,
    content: str
):
    """
    Menambahkan satu pesan ke chat history.

    role:
    - user
    - assistant
    """

    role = str(role).strip().lower()
    content = str(content).strip()

    if role not in (
        "user",
        "assistant"
    ):
        return False

    if not content:
        return False

    history = load_chat_history()

    history.append({
        "role": role,
        "content": content
    })

    # ========================================================
    # BATASI HISTORY
    # ========================================================
    #
    # Kita simpan maksimal 20 pesan.
    # Jadi prompt tidak terus membesar.
    #

    history = history[-20:]

    save_chat_history(history)

    return True


def get_chat_history(
    limit: int = 10
) -> list:
    """
    Mengambil beberapa chat terakhir.
    """

    history = load_chat_history()

    if limit <= 0:
        return []

    return history[-limit:]


def get_chat_history_text(
    limit: int = 10,
    max_chars: int = 6000
) -> str:
    """
    Mengubah chat history menjadi teks
    yang siap dimasukkan ke prompt AI.

    max_chars digunakan agar prompt tidak
    menjadi terlalu besar.
    """

    history = get_chat_history(limit)

    if not history:
        return ""

    lines = []

    for message in history:

        role = message.get(
            "role",
            ""
        )

        content = message.get(
            "content",
            ""
        )

        if not content:
            continue

        if role == "user":
            speaker = "User"

        elif role == "assistant":
            speaker = "ZAI"

        else:
            speaker = role.title()

        lines.append(
            f"{speaker}: {content}"
        )

    text = "\n".join(lines)

    if len(text) > max_chars:
        text = text[-max_chars:]

    return text


def chat_history_count() -> int:
    """
    Menghitung jumlah pesan yang tersimpan.
    """

    return len(
        load_chat_history()
    )


def clear_chat_history():
    """
    Menghapus seluruh chat history.
    """

    save_chat_history([])


# ============================================================
# CLEAR EVERYTHING
# ============================================================

def clear_all_memory():
    """
    Menghapus long-term memory dan chat history.
    """

    clear_memory()
    clear_chat_history()