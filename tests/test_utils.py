import unittest
from pathlib import Path
from unittest.mock import patch

import pytest

from src.data_import import read_excel_file
from src.utils import (
    get_card_numbers,
    get_currency_rates,
    get_data_card,
    get_formatted_date,
    get_greeting,
    get_stock_prices,
    get_time_period,
    get_top_transactions,
    transaction_amount,
)

# Тестирование функции get_greeting


# С применением параметризации
@pytest.mark.parametrize(
    "date_string, intervals",
    [
        ("2026-01-18 07:57:29", "Доброе утро"),
        ("2026-01-18 13:57:29", "Добрый день"),
        ("2026-01-18 19:57:29", "Добрый вечер"),
        ("2026-01-18 02:57:29", "Доброй ночи"),
    ],
)
def test_get_greeting(date_string: str, intervals: str) -> None:
    assert get_greeting(date_string) == intervals


# Проверяется, что функция корректно выбрасывает исключения
def test_get_greeting_raises_error():
    with pytest.raises(Exception) as exc_info:
        get_greeting(2)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value)
        == 'Функция "get_greeting" возвратила ошибку общее исключение:strptime() argument 1 must be str, not int'
    )


# Тестирование функции get_formatted_date


def test_get_formatted_date() -> None:
    assert get_formatted_date("2026-01-18 12:57:29") == "18.01.2026"


# Проверяется, что функция корректно выбрасывает исключения
def test_get_formatted_date_raises_error():
    with pytest.raises(Exception) as exc_info:
        get_formatted_date(2)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value)
        == 'Функция "get_formatted_date" возвратила ошибку общее исключение:' + "'int' object is not subscriptable"
    )


# Тестирование функции get_time_period


def test_get_time_period() -> None:
    assert get_time_period("2026-01-18 12:57:29") == ["01.01.2026", "18.01.2026"]


# Проверяется, что функция корректно выбрасывает исключения
def test_get_time_period_raises_value_error():
    with pytest.raises(Exception) as exc_info:
        get_formatted_date(2)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value)
        == 'Функция "get_formatted_date" возвратила ошибку общее исключение:' + "'int' object is not subscriptable"
    )


# Тестирование функции transaction_amount


# Проверяется, что функция корректно обрабатывает транзакцию с валютой в "RUB"
def test_transaction_amount_rub(transactions_utils_rub: dict) -> None:
    assert transaction_amount(transactions_utils_rub) == 149.0


# Проверяется, что функция корректно обрабатывает транзакцию с валютой в "CNY"
@patch("src.external_api.currency_conversion", return_value=75)
def test_transaction_amount_cny(transactions_utils_cny: dict) -> None:
    assert transaction_amount(transactions_utils_cny) == 75


# Проверяется, что функция корректно выбрасывает исключения
class TestTransactionAmount(unittest.TestCase):

    def test_key_error(self) -> None:
        transaction: dict = {"Сумма операции": 5}
        with self.assertRaises(KeyError):
            transaction_amount(transaction)

    # def test_value_error(self) -> None:
    #     transaction = {'Валюта операции': 50, 'Сумма операции': -32.0}
    #     with self.assertRaises(ValueError):
    #         transaction_amount(transaction)


def test_transaction_amount_raises_error():
    with pytest.raises(Exception) as exc_info:
        transaction = {"Валюта операции": "RUB", "Сумма операции": "-32.0"}
        transaction_amount(transaction)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value)
        == "Функция transaction_amount возвратила ошибку общее исключение: bad operand type for abs(): 'str'"
    )


file_path_ = str(Path(__file__).parent.parent / "data")
list_of_transactions_ = read_excel_file(
    path_to_file=f"{file_path_}/operations.xlsx", time_period=["01.10.2019", "01.10.2019"]
)
# def test_list_of_transactions_():
#     pprint(list_of_transactions_)

# Тестирование функции get_card_numbers


# Проверяется, что функция корректно обрабатывает список словарей с данными по транзакциям
def test_get_card_numbers() -> None:
    assert get_card_numbers(list_of_transactions_) == ["*4556", "*7197"]


# Проверяется, что функция корректно выбрасывает исключения
def test_get_card_numbers_raises_error():
    with pytest.raises(Exception) as exc_info:
        get_card_numbers([25])
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value)
        == "Функция get_card_numbers возвратила ошибку общее исключение: 'int' object has no attribute 'get'"
    )


# Тестирование функции get_data_card


# Проверяется, что функция корректно обрабатывает список словарей с данными по транзакциям
@patch("src.external_api.currency_conversion", return_value=75)
def test_get_data_card(transactions_utils_cny: dict) -> None:
    assert transaction_amount(transactions_utils_cny) == 75
    assert get_data_card(list_of_transactions_) == [
        {"cashback": 0.42, "last_digits": "4556", "total_spent": 42.0},
        {"cashback": 0.75, "last_digits": "7197", "total_spent": 75},
    ]


# Проверяется, что функция корректно выбрасывает исключения
def test_get_data_card_raises_error():
    with pytest.raises(Exception) as exc_info:
        get_data_card([{30}])
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value) == "Функция get_data_card возвратила ошибку общее исключение: "
        "Функция get_card_numbers возвратила ошибку общее исключение:"
        " 'set' object has no attribute 'get'"
    )


# Тестирование функции get_top_transactions


# Проверяется, что функция корректно обрабатывает список словарей с данными по транзакциям
def test_get_top_transactions() -> None:
    assert get_top_transactions(list_of_transactions_) == [
        {
            "amount": 22200.0,
            "category": "Зарплата",
            "date": "01.10.2019",
            "description": 'Пополнение. ООО "ФОРТУНА". Зарплата',
        },
        {"amount": 2511.0, "category": "Переводы", "date": "01.10.2019", "description": "Пополнение счета"},
        {"amount": -32.0, "category": "Фастфуд", "date": "30.09.2019", "description": "Beijingshoudujichangca"},
        {"amount": 13.67, "category": "Переводы", "date": "01.10.2019", "description": "Перевод между счетами"},
        {"amount": -93.0, "category": "Переводы", "date": "01.10.2019", "description": "Алексей В."},
    ]


# Проверяется, что функция корректно выбрасывает исключения
def test_get_top_transactions_raises_error():
    with pytest.raises(Exception) as exc_info:
        get_top_transactions([25])
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == "Функция get_top_transactions возвратила ошибку общее исключение: 'Сумма платежа'"


# Тестирование функции get_currency_rates


# Проверяется, что функция корректно возвращает курс в заданной валюте
@patch("src.external_api.currency_rate", return_value={"RUB": 79.524991})
def test_get_currency_rates(x: str) -> None:
    assert get_currency_rates("RUB") == [
        {"currency": "USD", "rate": 79.52},
        {"currency": "EUR", "rate": 79.52},
        {"currency": "CNY", "rate": 79.52},
    ]


# Проверяется, что функция корректно выбрасывает исключения
def test_get_currency_rates_raises_error():
    with pytest.raises(Exception) as exc_info:
        get_currency_rates("25")
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == "Функция get_currency_rates возвратила ошибку общее исключение: '25'"


# Тестирование функции get_stock_prices


# Проверяется, что функция корректно возвращает курс в заданной валюте
@patch(
    "src.external_api.stock_prices",
    return_value={
        "Global Quote": {
            "01. symbol": "AAPL",
            "02. open": "257.6450",
            "03. high": "262.4800",
            "04. low": "256.9500",
            "05. price": "260.8300",
            "06. volume": "30590765",
            "07. latest trading day": "2026-03-10",
            "08. previous close": "259.8800",
            "09. change": "0.9500",
            "10. change percent": "0.3656%",
        }
    },
)
def test_get_stock_prices(x) -> None:
    assert get_stock_prices() == [
        {"price": 260.83, "stock": "AAPL"},
        {"price": 260.83, "stock": "AMZN"},
        {"price": 260.83, "stock": "GOOGL"},
        {"price": 260.83, "stock": "MSFT"},
        {"price": 260.83, "stock": "TSLA"},
    ]


# Проверяется, что функция корректно выбрасывает исключения
def test_get_stock_prices_raises_error():
    with pytest.raises(Exception) as exc_info:
        get_stock_prices("25")
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == "get_stock_prices() takes 0 positional arguments but 1 was given"


if __name__ == "__main__":
    unittest.main()
