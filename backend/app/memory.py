import json
import os

MEMORY_FILE = "data/memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return {}


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def remember(key, value):
    data = load_memory()
    data[key] = value
    save_memory(data)


def recall(key):
    data = load_memory()
    return data.get(key)


def forget(key):
    data = load_memory()
    if key in data:
        del data[key]
        save_memory(data)


def clear_memory():
    save_memory({})


def all_memory():
    return load_memory()