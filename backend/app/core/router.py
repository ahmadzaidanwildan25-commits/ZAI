from app.core.intent import IntentEngine
from app.tools.apps import open_application


class ToolRouter:

    def __init__(self):

        self.intent_engine = IntentEngine()


    # ========================================================
    # ROUTE
    # ========================================================

    def route(self, text: str):

        intent = self.intent_engine.analyze(text)


        # ====================================================
        # APPLICATION
        # ====================================================

        if (
            intent.name == "application"
            and intent.action == "open"
        ):

            result = open_application(
                intent.target
            )

            return {
                "intent": intent.name,
                "confidence": intent.confidence,
                "action": intent.action,
                "target": intent.target,
                "executed": True,
                "success": result["success"],
                "reply": result["message"],
            }


        # ====================================================
        # SYSTEM
        # ====================================================

        if (
            intent.name == "system"
            and intent.action == "power"
        ):

            return {
                "intent": intent.name,
                "confidence": intent.confidence,
                "action": intent.action,
                "target": intent.target,
                "executed": False,
                "success": False,
                "reply": (
                    "Perintah sistem terdeteksi, "
                    "tetapi eksekusi sistem belum "
                    "diaktifkan."
                ),
            }


        # ====================================================
        # OTHER
        # ====================================================

        return {
            "intent": intent.name,
            "confidence": intent.confidence,
            "action": intent.action,
            "target": intent.target,
            "executed": False,
            "success": False,
            "reply": None,
        }