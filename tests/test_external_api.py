import os
import unittest
from typing import Any
from unittest.mock import patch

from dotenv import load_dotenv

from src.external_api import currency_conversion, currency_rate, stock_prices

# Тестирование функции currency_conversion

load_dotenv()
api_key_1 = os.getenv("API_KEY_APILayer")
api_key_2 = os.getenv("API_KEY_Alpha_Vantage")


# patch — это специальный декоратор, который позволяет нам заменить реальный объект или функцию
# на заглушку во время выполнения теста.
@patch("requests.request")
def test_currency_conversion_1(mock_request: Any) -> None:

    # Настраиваем возвращаемое значение макета
    mock_request.return_value.json.return_value = {"result": 630982.057672}
    result = currency_conversion("8221.37", "USD")

    # Проверяем, что функция вернула ожидаемый результат
    assert result == 630982.057672, "Конвертация валюты не прошла как ожидалось"

    # Проверяем, что функция requests.request была вызвана только один раз и с определенными аргументами
    mock_request.assert_called_once_with(
        "GET",
        url="https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=8221.37",
        headers={"apikey": f"{api_key_1}"},
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
            headers={"apikey": f"{api_key_1}"},
            data={},
        )

# Тестирование функции currency_conversion currency_rate

@patch("requests.request")
def test_currency_rate(mock_request: Any) -> None:

    # Настраиваем возвращаемое значение макета
    # mock_request.return_value.json.return_value = {'base': 'USD',
    #                                                'date': '2026-02-19',
    #                                                'rates': {'RUB': 76.748081},
    #                                                'success': True,
    #                                                'timestamp': 1771524487}
    mock_request.return_value.json.return_value = {'rates': {'RUB': 76.748081}}

    # Вызываем тестируемую функцию currency_rate
    result = currency_rate("USD", "RUB")

    # Проверяем, что функция вернула ожидаемый результат
    assert result == {'RUB': 76.748081}, "Курс валюты не прошел как ожидалось"

    # Проверяем, что функция requests.request была вызвана только один раз и с определенными аргументами
    mock_request.assert_called_once_with(
        "GET",
        url="https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD",
        headers={"apikey": f"{api_key_1}"},
        data={},
    )

# Тестирование функции currency_conversion stock_prices

def test_stock_prices() -> None:
    with patch("requests.get") as mock_get:

        # Настраиваем возвращаемое значение макета
        mock_get.return_value.json.return_value = {'Global Quote': {'01. symbol': 'AAPL',
                                                                        '02. open': '258.9700',
                                                                        '03. high': '264.7500',
                                                                        '04. low': '258.1600',
                                                                        '05. price': '264.5800',
                                                                        '06. volume': '42070499',
                                                                        '07. latest trading day': '2026-02-20',
                                                                        '08. previous close': '260.5800',
                                                                        '09. change': '4.0000',
                                                                        '10. change percent': '1.5350%'}
                                                       }

        # Вызываем тестируемую функцию stock_prices
        result = stock_prices("AAPL")

        # Проверяем, что функция вернула ожидаемый результат
        assert result == {'Global Quote': {'01. symbol': 'AAPL',
                                           '02. open': '258.9700',
                                           '03. high': '264.7500',
                                           '04. low': '258.1600',
                                           '05. price': '264.5800',
                                           '06. volume': '42070499',
                                           '07. latest trading day': '2026-02-20',
                                           '08. previous close': '260.5800',
                                           '09. change': '4.0000',
                                           '10. change percent': '1.5350%'}
                          }

        # Проверяем, что функция requests.get была вызвана только один раз и с определенными аргументами
        mock_get.assert_called_once_with(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={api_key_2}')


if __name__ == "__main__":
    unittest.main()