import os
import subprocess
from typing import Optional


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APPLICATIONS = {
    "chrome": {
        "command": "chrome.exe",
        "display": "Google Chrome",
    },

    "vscode": {
        "command": "code",
        "display": "Visual Studio Code",
    },

    "visual studio code": {
        "command": "code",
        "display": "Visual Studio Code",
    },

    "spotify": {
        "command": "spotify.exe",
        "display": "Spotify",
    },

    "notepad": {
        "command": "notepad.exe",
        "display": "Notepad",
    },

    "calculator": {
        "command": "calc.exe",
        "display": "Calculator",
    },

    "calc": {
        "command": "calc.exe",
        "display": "Calculator",
    },

    "explorer": {
        "command": "explorer.exe",
        "display": "File Explorer",
    },

    "file explorer": {
        "command": "explorer.exe",
        "display": "File Explorer",
    },
}


# ============================================================
# NORMALIZE TARGET
# ============================================================

def normalize_target(target: Optional[str]) -> Optional[str]:

    if target is None:
        return None

    target = str(target).strip().lower()

    if not target:
        return None

    aliases = {
        "google chrome": "chrome",
        "chrome browser": "chrome",
        "vs code": "vscode",
        "visual studio": "vscode",
        "visual studio code": "vscode",
        "spotify music": "spotify",
        "kalkulator": "calculator",
        "calculator": "calculator",
        "file explorer": "explorer",
        "windows explorer": "explorer",
    }

    return aliases.get(target, target)


# ============================================================
# OPEN APPLICATION
# ============================================================

def open_application(target: Optional[str]) -> dict:

    target = normalize_target(target)

    if not target:

        return {
            "success": False,
            "message": "Saya belum mengetahui aplikasi yang ingin dibuka.",
        }

    application = APPLICATIONS.get(target)

    if not application:

        return {
            "success": False,
            "message": (
                f"Aplikasi '{target}' belum terdaftar "
                "di ZAI."
            ),
        }

    command = application["command"]
    display_name = application["display"]

    try:

        # ----------------------------------------------------
        # WINDOWS APPLICATION
        # ----------------------------------------------------

        if command.endswith(".exe"):

            subprocess.Popen(
                [command],
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        else:

            subprocess.Popen(
                [command],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        return {
            "success": True,
            "message": f"Membuka {display_name}.",
        }

    except FileNotFoundError:

        return {
            "success": False,
            "message": (
                f"{display_name} tidak ditemukan "
                "di komputer."
            ),
        }

    except Exception as error:

        print(
            f"[OPEN APPLICATION ERROR] {error}"
        )

        return {
            "success": False,
            "message": (
                f"Gagal membuka {display_name}."
            ),
        }


# ============================================================
# CHECK APPLICATION
# ============================================================

def application_exists(target: Optional[str]) -> bool:

    target = normalize_target(target)

    if not target:
        return False

    application = APPLICATIONS.get(target)

    if not application:
        return False

    command = application["command"]

    try:

        if command.endswith(".exe"):

            result = subprocess.run(
                [
                    "where",
                    command,
                ],
                capture_output=True,
                text=True,
                shell=False,
            )

        else:

            result = subprocess.run(
                [
                    "where",
                    command,
                ],
                capture_output=True,
                text=True,
                shell=True,
            )

        return result.returncode == 0

    except Exception:

        return False


# ============================================================
# GET APPLICATION LIST
# ============================================================

def get_available_applications() -> list:

    applications = []

    seen = set()

    for key, value in APPLICATIONS.items():

        display = value["display"]

        if display in seen:
            continue

        seen.add(display)

        applications.append(
            {
                "name": key,
                "display": display,
                "command": value["command"],
            }
        )

    return applications