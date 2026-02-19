import os
from typing import Any
from unittest.mock import patch

from dotenv import load_dotenv

from src.external_api import currency_conversion

# Тестирование функции currency_conversion

load_dotenv()
api_key = os.getenv("API_KEY_APILayer")



@patch("requests.request")
def test_currency_conversion_1(mock_request: Any) -> None:
    mock_request.return_value.json.return_value = {"result": 630982.057672}  # Настраиваем возвращаемое значение макета
    result = currency_conversion("8221.37", "USD")
    # Проверяем, что функция вернула ожидаемый результат
    assert result == 630982.057672, "Конвертация валюты не прошла как ожидалось"

    # Проверяем, что функция requests.request была вызвана только один раз и с определенными аргументами
    mock_request.assert_called_once_with(
        "GET",
        url="https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=8221.37",
        headers={"apikey": f"{api_key}"},
        data={},
    )


def test_currency_conversion_2() -> None:
    with patch("requests.request") as mock_request:
        # Настраиваем возвращаемое значение макета
        mock_request.return_value.json.return_value = {"result": 630982.057672}
        result = currency_conversion("8221.37", "USD")
        # Проверяем, что функция вернула ожидаемый результат
        assert result == 630982.057672, "Конвертация валюты не прошла как ожидалось"

        # Проверяем, что функция requests.request была вызвана только один раз и с определенными аргументами
        mock_request.assert_called_once_with(
            "GET",
            url="https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=8221.37",
            headers={"apikey": f"{api_key}"},
            data={},
        )
