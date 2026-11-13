from gigachat_api import ask_gigachat_with_history
from prompt_templates import SYSTEM_PROMPT
from config import (
    PROJECT_NAME,
    SYSTEM_PROMPT,
    MAX_HISTORY_MESSAGES,
)

history = []

print("Глоссарий запущен.")
print("Спроси про расу, класс, правило или попроси помочь с персонажем.")
print("Для завершения введи /exit")

def parse_command(text):
    text = text.strip()
    if not text.startswith("/"):
        return "", text
    parts = text.split(maxsplit=1)
    command = parts[0].lower()
    argument = parts[1].strip() if len(parts) == 2 else ""
    return command, argument

def trim_history(messages, limit):
    return messages[-limit:]

# После добавления ответа:
history = trim_history(history, MAX_HISTORY_MESSAGES)

def show_history(messages):
    if not messages:
        print("История пуста.")
        return

    for number, message in enumerate(messages, start=1):
        role = "Вы" if message["role"] == "user" else "Бот"
        print(f"{number}. {role}: {message['content']}")
def save_history(messages):
    path = "report/day04_dialogue.txt"
    with open(path, "w", encoding="utf-8") as file:
        for number, message in enumerate(messages, start=1):
            role = "Вы" if message["role"] == "user" else "Бот"
            file.write(
                f"{number}. {role}: {message['content']}\n"
            )
    print("Диалог сохранён в", path)

while True:
    user_text = input("что хочешь узнать? ").strip()

    if user_text == "/exit":
        print("Диалог завершён.")
        break

    if not user_text:
        print("Введи непустое сообщение.")
        continue

    history.append({"role": "user", "content": user_text})

    try:
        answer = ask_gigachat_with_history(
            history, SYSTEM_PROMPT
        )
    except Exception as error:
        history.pop()
        print("Ошибка обращения к API: Сервис временно недоступен. Повторите позже")
        continue

    history.append({"role": "assistant", "content": answer})
    print("Глоссарий:", answer)
    if user_text == "/help":
        print("/help — показать команды")
        print("/history — показать историю")
        print("/clear — очистить историю")
        print("/exit — завершить работу")
        continue

    if user_text == "/history":
        show_history(history)
        continue

    if user_text == "/clear":
        history.clear()
        print("История очищена.")
        continue

    history.append({"role": "assistant", "content": answer})

    if len(history) > 10:
        history = history[-10:]



from config import (
    PROJECT_NAME,
    SYSTEM_PROMPT,
    MAX_HISTORY_MESSAGES,
)

print(PROJECT_NAME, "запущен.")