from chat_bot import parse_command, trim_history, format_weather
from weather_api import describe_weather_code

def run_test(name, condition):
    if condition:
        print("ПРОЙДЕН:", name)
        return 1
    print("НЕ ПРОЙДЕН:", name)
    return 0

passed = 0

passed += run_test(
    "команда с аргументом",
    parse_command("/weather Нижний Новгород")
    == ("/weather", "Нижний Новгород"),
)
passed += run_test(
    "команда без аргумента",
    parse_command("/weather") == ("/weather", ""),
)
passed += run_test(
    "обычный текст",
    parse_command("Расскажи о Казани")
    == ("", "Расскажи о Казани"),
)
passed += run_test(
    "ограничение истории",
    trim_history(list(range(14)), 10) == list(range(4, 14)),
)
passed += run_test(
    "известный код погоды",
    describe_weather_code(0) == "ясно",
)
passed += run_test(
    "неизвестный код погоды",
    describe_weather_code(999) == "неизвестное состояние",
)

weather = {
    "city": "Тестоград",
    "temperature": 7,
    "feels_like": 4,
    "precipitation": 0,
    "wind_speed": 12,
    "description": "ясно",
}
text = format_weather(weather)
passed += run_test(
    "форматирование погоды",
    all(value in text for value in ["Тестоград", "7", "4", "0", "12"]),
)

print(f"Итог: {passed} из 7 проверок пройдено")