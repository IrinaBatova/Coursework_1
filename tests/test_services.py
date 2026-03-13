import unittest
from pathlib import Path

import pytest

from src.data_import import read_excel_file_columns
from src.services import investment_bank

# Тестирование функции investment_bank

file_path = str(Path(__file__).parent.parent / "data")
transactions = read_excel_file_columns(
    f"{file_path}/operations.xlsx", ["Дата операции", "Сумма операции", "Валюта операции", "Категория"]
)


# Проверяется, что функция корректно работает
def test_investment_bank() -> None:
    assert investment_bank("2021-12", transactions, 10) == 571.38
    assert investment_bank("2021-12", transactions, 50) == 3301.38
    assert investment_bank("2021-12", transactions, 100) == 7851.38


# Проверяется, что функция корректно выбрасывает исключения
def test_investment_bank_raises_error():
    with pytest.raises(Exception) as exc_info:
        investment_bank("25", transactions, 10)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value) == "Функция investment_bank возвратила ошибку общее исключение: time data '25' "
        "does not match format '%Y-%m'"
    )


if __name__ == "__main__":
    unittest.main()
