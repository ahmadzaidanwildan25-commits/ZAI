from app.core.router import ToolRouter


router = ToolRouter()


tests = [
    "buka chrome",
    "matikan komputer",
    "buat folder baru",
    "cari di google tentang AI",
    "siapa kamu?",
]


for text in tests:

    result = router.route(text)

    print()
    print("USER :", text)
    print("ZAI  :", result)