
import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    auth_key = os.getenv("GIGACHAT_AUTH_KEY")
    if not auth_key:
        raise ValueError("В файле .env не найден GIGACHAT_AUTH_KEY")

    response = requests.post(
        "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        headers={
            "Authorization": f"Basic {auth_key}",
            "RqUID": str(uuid.uuid4()),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data={"scope": "GIGACHAT_API_PERS"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]

def ask_gigachat(question):
    token = get_access_token()
    response = requests.post(
        "https://api.giga.chat/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "model": "GigaChat-2",
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.3,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

if __name__ == "__main__":
    user_question = input("Введите вопрос: ")
    try:
        print(ask_gigachat(user_question))
    except requests.RequestException as error:
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