import requests

from app.config import (
    OLLAMA_URL,
    MODEL_NAME,
    TIMEOUT,
)


def ask_ai(prompt: str) -> str:

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "think": False,

                "options": {
                    "num_predict": 300,
                    "temperature": 0.7,
                },
            },
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "response",
            ""
        ).strip()

        if not answer:
            raise RuntimeError(
                "Ollama tidak mengembalikan response."
            )

        return answer

    except requests.exceptions.Timeout:

        raise RuntimeError(
            "Ollama timeout."
        )

    except requests.exceptions.ConnectionError:

        raise RuntimeError(
            "Tidak dapat terhubung ke Ollama."
        )

    except Exception as error:

        raise RuntimeError(
            f"Ollama error: {error}"
        )