import os
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.exceptions import GigaChatException

load_dotenv()

SYSTEM_PROMPT = (
    "Ты — справочник по настольной ролевой игре Dungeons & Dragons 5e. "
    "Отвечай кратко и по делу: правила, характеристики монстров, "
    "параметры заклинаний, классы, расы. Если не уверен — скажи об этом."
)


def ask_guide(question):
    """Отправляет вопрос по D&D в GigaChat и возвращает ответ."""
    auth_key = os.getenv("GIGACHAT_AUTH_KEY")
    if not auth_key:
        raise ValueError("В файле .env не найден GIGACHAT_AUTH_KEY")

    with GigaChat(
        credentials=auth_key,
        scope="GIGACHAT_API_PERS",
        model="GigaChat-2-Pro",
        verify_ssl_certs=False,  # временно; лучше поставить сертификат Минцифры
    ) as giga:
        response = giga.chat({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            "temperature": 0.7,
        })

    return {
        "question": question,
        "answer": response.choices[0].message.content,
    }


if __name__ == "__main__":
    question = input("Какой у тебя вопрос? ")
    try:
        result = ask_guide(question)

        print("Вопрос:", result["question"])
        print("Ответ:", result["answer"])
    except GigaChatException as error:
        print("Ошибка запроса к GigaChat:", error)
    except (ValueError, KeyError) as error:
        print("Ошибка данных:", error)
def ask_gigachat_with_history(history, system_prompt):
    token = get_access_token()
    messages = [
        {"role": "system", "content": system_prompt}
    ] + history

    response = requests.post(
        "https://api.giga.chat/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "model": "GigaChat-2",
            "messages": messages,
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
