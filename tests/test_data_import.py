import unittest
from io import BytesIO
from unittest.mock import mock_open, patch

import pandas as pd

from src.data_import import read_excel_file, read_excel_file_columns, read_json_file

# Тестирование функции read_excel_file

# Создаем объект, список словарей
mock_data_list = [{"id": "650703", "state": "EXECUTED"}, {"id": "3598919", "state": "EXECUTED"}]

# Создаем объект DataFrame
mock_data_df = pd.DataFrame({"id": ["650703", "3598919"], "state": ["EXECUTED", "EXECUTED"]})
mock_data_empty = pd.DataFrame()  # Пустой DataFrame

# Используем BytesIO для создания буфера в памяти
excel_buffer = BytesIO()

# Записываем DataFrame в BytesIO как в Excel-файл
with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    mock_data_df.to_excel(writer, index=False)

# Получаем данные из BytesIO
excel_data = excel_buffer.getvalue()

# Создаем объекты, которые будет представлять замоканные версии функции open
mock_file = mock_open(read_data=excel_data)
mock_file_empty = mock_open(read_data="")


# Проверяем, что функция возвращает список словарей
@patch("builtins.open", mock_file)
def test_read_excel_file_() -> None:
    with patch("pandas.read_excel", return_value=mock_data_df):
        assert read_excel_file("./data/transactions_excel.xlsx") == mock_data_list


# Проверяем, что функция возвращает пустой список, если файл пуст
@patch("builtins.open", mock_file_empty)
def test_read_excel_file_1() -> None:
    with patch("pandas.read_excel", return_value=mock_data_empty):
        assert read_excel_file("./data/empty.xlsx") == []


# Проверяем, что функция возвращает пустой список, если тип файла не .xlsx
@patch("builtins.open", mock_file)
def test_read_excel_file_2() -> None:
    with patch("pandas.read_excel", return_value=mock_data_df):
        assert read_excel_file("./data/operations.json") == []


# Проверяем, что функция возвращает пустой список, если файл не найден
@patch("builtins.open", mock_file)
def test_read_excel_file_3() -> None:
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        assert read_excel_file("transactions_excel.xlsx") == []


# Тестирование функции read_excel_file_columns

# Создаем объект, список словарей
mock_data_list_ = [{"id": "650703", "state": "EXECUTED"}, {"id": "3598919", "state": "EXECUTED"}]

# Создаем объект DataFrame
mock_data_df = pd.DataFrame({"id": ["650703", "3598919"], "state": ["EXECUTED", "EXECUTED"]})
mock_data_empty_ = pd.DataFrame()  # Пустой DataFrame

# Используем BytesIO для создания буфера в памяти
excel_buffer = BytesIO()

# Записываем DataFrame в BytesIO как в Excel-файл
with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    mock_data_df.to_excel(writer, index=False)

# Получаем данные из BytesIO
excel_data = excel_buffer.getvalue()

# Создаем объекты, которые будет представлять замоканные версии функции open
mock_file = mock_open(read_data=excel_data)
mock_file_empty = mock_open(read_data="")


# Проверяем, что функция возвращает список словарей
@patch("builtins.open", mock_file)
def test_read_excel_file_columns_() -> None:
    with patch("pandas.read_excel", return_value=mock_data_df):
        assert (
            read_excel_file_columns(
                "./data/transactions_excel.xlsx", ["Дата операции", "Сумма операции", "Валюта операции"]
            )
            == mock_data_list_
        )


# Проверяем, что функция возвращает пустой список, если файл пуст
@patch("builtins.open", mock_file_empty)
def test_read_excel_file_columns_1() -> None:
    with patch("pandas.read_excel", return_value=mock_data_empty_):
        assert (
            read_excel_file_columns("./data/empty.xlsx", ["Дата операции", "Сумма операции", "Валюта операции"]) == []
        )


# Проверяем, что функция возвращает пустой список, если тип файла не .xlsx
@patch("builtins.open", mock_file)
def test_read_excel_file_columns_2() -> None:
    with patch("pandas.read_excel", return_value=mock_data_df):
        assert (
            read_excel_file_columns("./data/operations.json", ["Дата операции", "Сумма операции", "Валюта операции"])
            == None
        )


# Проверяем, что функция возвращает пустой список, если файл не найден
@patch("builtins.open", mock_file)
def test_read_excel_file_columns_3() -> None:
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        assert (
            read_excel_file_columns("transactions_excel.xlsx", ["Дата операции", "Сумма операции", "Валюта операции"])
            == []
        )


# Тестирование функции read_json_file

# Создаем объект, который будет представлять замоканную версию функции open
mock_file = mock_open(
    read_data='{"user_currencies": ["USD", "EUR", "CNY"],' ' "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}'
)


# Проверяется, что функция возвращает словарь
@patch("builtins.open", mock_file)
def test_read_json_file_() -> None:
    with patch(
        "json.load",
        return_value={
            "user_currencies": ["USD", "EUR", "CNY"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
        },
    ):
        assert read_json_file("./data/operations.json") == {
            "user_currencies": ["USD", "EUR", "CNY"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
        }


# Проверяется, что функция возвращает пустой словарь, если словарь в файле пуст
@patch("builtins.open", mock_file)
def test_read_json_file_1() -> None:
    with patch("json.load", return_value={}):
        assert read_json_file("./data/operations.json") == {}


# Проверяется, что функция возвращает пустой словарь, если файл содержит не словарь
@patch("builtins.open", mock_file)
def test_read_json_file_2() -> None:
    with patch("json.load", return_value=[{"id": 1, "amount": 100}]):
        assert read_json_file("./data/operations.json") == {}


# Проверяется, что функция возвращает пустой словарь, если файл не найден
@patch("builtins.open", mock_file)
def test_read_json_file_3() -> None:
    with patch("json.load", return_value=None):
        assert read_json_file("./data/operations.json") == {}


if __name__ == "__main__":
    unittest.main()
