import os
import shutil
import subprocess
from typing import Optional


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(
        r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
    ),
]


def find_chrome() -> Optional[str]:
    """
    Mencari Google Chrome pada lokasi umum Windows.
    """

    # Cek lokasi yang diketahui
    for path in CHROME_PATHS:
        if os.path.isfile(path):
            return path

    # Cek PATH Windows
    chrome_from_path = shutil.which("chrome.exe")

    if chrome_from_path:
        return chrome_from_path

    return None


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
# RESOLVE APPLICATION COMMAND
# ============================================================

def resolve_command(target: str) -> Optional[str]:

    if target == "chrome":
        return find_chrome()

    application = APPLICATIONS.get(target)

    if not application:
        return None

    command = application["command"]

    # Untuk executable Windows, cek PATH terlebih dahulu.
    if command.endswith(".exe"):
        resolved = shutil.which(command)

        if resolved:
            return resolved

    # Untuk command seperti "code", cek PATH.
    resolved = shutil.which(command)

    if resolved:
        return resolved

    # Tetap kembalikan command agar subprocess dapat mencoba
    # command tersebut jika Windows bisa menemukannya.
    return command


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

    display_name = application["display"]
    command = resolve_command(target)

    if not command:
        return {
            "success": False,
            "message": (
                f"{display_name} tidak ditemukan "
                "di komputer."
            ),
        }

    try:

        # ----------------------------------------------------
        # WINDOWS APPLICATION
        # ----------------------------------------------------

        subprocess.Popen(
            [command],
            shell=False,
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

    command = resolve_command(target)

    if not command:
        return False

    # Jika command sudah berupa path absolut
    if os.path.isabs(command):
        return os.path.isfile(command)

    try:

        result = subprocess.run(
            ["where", command],
            capture_output=True,
            text=True,
            shell=False,
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