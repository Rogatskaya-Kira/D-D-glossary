from pathlib import Path
import csv
import re

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
REPORT_FILE = Path("data/metadata/cleaning_results.csv")

NOISE_LINES = {
    "главная", "меню", "поделиться",
    "принять cookie", "наверх", "версия для печати",
}

def split_metadata(text):
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4
    if end == -1:
        return "", text
    return text[:end + 5], text[end + 5:]

def clean_body(body):
    body = body.replace("\u00a0", " ").replace("\t", " ")
    cleaned = []
    for line in body.splitlines():
        line = re.sub(r" {2,}", " ", line).strip()
        if line.casefold() in NOISE_LINES:
            continue
        cleaned.append(line)
    text = "\n".join(cleaned)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"

def word_count(text):
    return len(re.findall(r"\b[\w-]+\b", text, flags=re.UNICODE))

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
rows = []

for source in sorted(RAW_DIR.glob("*.md")):
    raw = source.read_text(encoding="utf-8").replace("\r\n", "\n")
    metadata, body = split_metadata(raw)
    cleaned_body = clean_body(body)
    result = metadata + cleaned_body
    target = PROCESSED_DIR / source.name
    target.write_text(result, encoding="utf-8")

    before = len(raw)
    after = len(result)
    retained = round(after / before * 100, 1) if before else 0
    words = word_count(cleaned_body)
    has_meta = "source_id:" in metadata and "title:" in metadata
    status = "ПРОЙДЕН" if retained >= 65 and words >= 80 and has_meta else "ПРОВЕРИТЬ"
    rows.append([source.name, before, after, retained, words, has_meta, status])
    print(source.name, retained, words, status)

with REPORT_FILE.open("w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow([
        "file_name", "chars_before", "chars_after",
        "retained_percent", "words_after", "metadata", "status"
    ])
    writer.writerows(rows)

print("Обработано документов:", len(rows))


Подчеркните в коде пути к raw, processed и журналу.
Найдите функцию, которая отделяет метаданные от основного текста.
Найдите четыре операции нормализации: неразрывные пробелы, табуляция, повторные пробелы и пустые строки.
Найдите условие присвоения статуса «ПРОЙДЕН».
В отчёте одним предложением опишите назначение каждой функции.Подчеркните в коде пути к raw, processed и журналу.
Найдите функцию, которая отделяет метаданные от основного текста.
Найдите четыре операции нормализации: неразрывные пробелы, табуляция, повторные пробелы и пустые строки.
Найдите условие присвоения статуса «ПРОЙДЕН».
В отчёте одним предложением опишите назначение каждой функции.