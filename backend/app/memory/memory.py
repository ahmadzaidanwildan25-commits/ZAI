import json
import os

DATABASE = "database/memory.json"


def load_memory():
    if not os.path.exists(DATABASE):
        return {}

    with open(DATABASE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(data):
    with open(DATABASE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)


def recall(key):
    memory = load_memory()
    return memory.get(key)


def all_memory():
    return load_memory()