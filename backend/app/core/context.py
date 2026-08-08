from typing import List, Dict


class ContextEngine:

    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.history: List[Dict[str, str]] = []

    def add_user_message(self, message: str):
        self.history.append({
            "role": "user",
            "content": message,
        })

        self._limit_history()

    def add_assistant_message(self, message: str):
        self.history.append({
            "role": "assistant",
            "content": message,
        })

        self._limit_history()

    def get_history(self) -> List[Dict[str, str]]:
        return self.history.copy()

    def clear(self):
        self.history.clear()

    def _limit_history(self):
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]