from pathlib import Path

RAW_DIR = Path("data/raw")

files = sorted(RAW_DIR.glob("*.md"))
print("Документов:", len(files))

passed = 0
for path in files:
    text = path.read_text(encoding="utf-8")
    words = len(text.split())
    has_source = "source_id:" in text
    size = path.stat().st_size
    status = words >= 120 and has_source and size > 0
    if status:
        passed += 1
    print(
        path.name,
        "| байт:", size,
        "| слов:", words,
        "| source_id:", has_source,
        "| статус:", "ПРОЙДЕН" if status else "НЕ ПРОЙДЕН",
    )

print(f"Итог: {passed} из {len(files)} документов прошли проверку")