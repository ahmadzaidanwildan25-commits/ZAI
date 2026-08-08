import os
import subprocess


def open_application(target: str):
    target = (target or "").lower().strip()

    applications = {
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
        "vscode": [
            r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        ],
        "spotify": [
            r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
        ],
    }

    if target not in applications:
        return {
            "success": False,
            "message": f"Aplikasi '{target}' belum didukung."
        }

    for path in applications[target]:
        path = os.path.expandvars(path)

        if os.path.exists(path):
            try:
                subprocess.Popen([path])

                return {
                    "success": True,
                    "message": f"Membuka {target}."
                }

            except Exception as error:
                return {
                    "success": False,
                    "message": f"Gagal membuka {target}: {error}"
                }

    # Fallback menggunakan Windows Start
    try:
        subprocess.Popen(
            ["cmd", "/c", "start", "", target],
            shell=False
        )

        return {
            "success": True,
            "message": f"Membuka {target}."
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Aplikasi '{target}' tidak ditemukan: {error}"
        }
