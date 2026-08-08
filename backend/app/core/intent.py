from dataclasses import dataclass
from typing import Optional


@dataclass
class Intent:

    name: str
    confidence: float
    target: Optional[str] = None
    action: Optional[str] = None


class IntentEngine:

    def analyze(self, text: str) -> Intent:

        text = text.lower().strip()

        # ====================================================
        # SYSTEM
        # ====================================================

        if any(
            word in text
            for word in [
                "shutdown",
                "matikan komputer",
                "matikan pc",
                "matikan laptop",
                "restart komputer",
                "restart pc",
                "restart laptop",
            ]
        ):

            return Intent(
                name="system",
                confidence=0.95,
                action="power",
            )

        # ====================================================
        # APPLICATION
        # ====================================================

        applications = {
            "chrome": [
                "buka chrome",
                "buka google chrome",
                "jalankan chrome",
            ],

            "vscode": [
                "buka vscode",
                "buka vs code",
                "buka visual studio code",
                "jalankan vscode",
            ],

            "spotify": [
                "buka spotify",
                "jalankan spotify",
            ],

            "notepad": [
                "buka notepad",
                "buka catatan",
                "jalankan notepad",
            ],

            "calculator": [
                "buka kalkulator",
                "buka calculator",
                "jalankan kalkulator",
            ],

            "explorer": [
                "buka file explorer",
                "buka explorer",
                "buka file manager",
            ],
        }

        for target, phrases in applications.items():

            if any(
                phrase in text
                for phrase in phrases
            ):

                return Intent(
                    name="application",
                    confidence=0.95,
                    action="open",
                    target=target,
                )

        # ====================================================
        # FILE
        # ====================================================

        if any(
            word in text
            for word in [
                "buat file",
                "hapus file",
                "cari file",
                "buka file",
                "buat folder",
                "hapus folder",
                "buat direktori",
                "hapus direktori",
            ]
        ):

            return Intent(
                name="file",
                confidence=0.90,
            )

        # ====================================================
        # BROWSER
        # ====================================================

        if any(
            word in text
            for word in [
                "cari di google",
                "cari di internet",
                "search",
                "cari informasi",
                "buka website",
            ]
        ):

            return Intent(
                name="browser",
                confidence=0.90,
            )

        # ====================================================
        # GENERAL AI
        # ====================================================

        return Intent(
            name="conversation",
            confidence=0.60,
        )