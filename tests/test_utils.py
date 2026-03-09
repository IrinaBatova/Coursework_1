import pytest
import unittest
import re
from unittest.mock import patch, mock_open
from src.utils import get_greeting, get_formatted_date, get_time_period, transaction_amount
from src.external_api import currency_conversion


# Тестирование функции get_greeting

# С применением параметризации
@pytest.mark.parametrize(
    "date_string, intervals", [("2026-01-18 07:57:29", "Доброе утро"), ("2026-01-18 13:57:29", "Добрый день"),
                               ("2026-01-18 19:57:29", "Добрый вечер"), ("2026-01-18 02:57:29", "Доброй ночи")]
)
def test_get_greeting(date_string: str, intervals: str) -> None:
    assert get_greeting(date_string) == intervals

# Проверяется, что функция корректно выбрасывает исключения
def test_get_greeting_raises_error():
    with pytest.raises(Exception) as exc_info:
        get_greeting(2)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == 'Функция "get_greeting" возвратила ошибку общее исключение:strptime() argument 1 must be str, not int'


# Тестирование функции get_formatted_date

def test_get_formatted_date() -> None:
    assert get_formatted_date("2026-01-18 12:57:29") == "18.01.2026"

# Проверяется, что функция корректно выбрасывает исключения
def test_get_formatted_date_raises_error():
    with pytest.raises(Exception) as exc_info:
        get_formatted_date(2)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == 'Функция "get_formatted_date" возвратила ошибку общее исключение:'+"'int' object is not subscriptable"


# Тестирование функции get_time_period

def test_get_time_period() -> None:
    assert get_time_period("2026-01-18 12:57:29") == ['01.01.2026', '18.01.2026']

# Проверяется, что функция корректно выбрасывает исключения
def test_get_time_period_raises_value_error():
    with pytest.raises(Exception) as exc_info:
        get_formatted_date(2)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == 'Функция "get_formatted_date" возвратила ошибку общее исключение:'+"'int' object is not subscriptable"


# Тестирование функции transaction_amount

# Проверяется, что функция корректно обрабатывает транзакцию с валютой в "RUB"
def test_transaction_amount_rub(transactions_utils_rub: dict) -> None:
    assert transaction_amount(transactions_utils_rub) == 149.0


# Проверяется, что функция корректно обрабатывает транзакцию с валютой в "CNY"
@patch("src.external_api.currency_conversion", return_value=75)
def test_transaction_amount_cny(transactions_utils_cny: dict) -> None:
    assert currency_conversion('32.0', 'CNY') == 75
    assert transaction_amount(transactions_utils_cny) == 75


# Проверяется, что функция корректно выбрасывает исключения
class TestTransactionAmount(unittest.TestCase):

    def test_key_error(self) -> None:
        transaction: dict = {'Сумма операции': 5}
        with self.assertRaises(KeyError):
            transaction_amount(transaction)

    def test_value_error(self) -> None:
        transaction = {'Валюта операции': 5, 'Сумма операции': '5'}
        with self.assertRaises(ValueError):
            transaction_amount(transaction)

if __name__ == "__main__":
    unittest.main()