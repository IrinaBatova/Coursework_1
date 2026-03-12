import pytest
import unittest
from pathlib import Path
import pandas as pd
from src.data_import import read_excel_file
from src.reports import spending_by_category


# Тестирование функции spending_by_category

file_path_ = str(Path(__file__).parent.parent / "data")
data = read_excel_file(path_to_file=f"{file_path_}/operations.xlsx")

df_data = pd.DataFrame(data)

# Проверяется, что функция корректно работает
def test_spending_by_category() -> None:
    assert spending_by_category(df_data, 'Супермаркеты') == None
    assert spending_by_category(df_data, 'Супермаркеты', "05.12.2026") == None

    # Ожидается 172 строки и 15 столбцов
    assert spending_by_category(df_data, 'Супермаркеты', "05.12.2021").shape == (172, 15)

    # Проверка, что 'Сумма операции' имеет тип числа с плавающей точкой
    assert spending_by_category(df_data, 'Супермаркеты', "05.12.2021")['Сумма операции'].dtype == 'float'

# Проверяется, что функция корректно выбрасывает исключения
def test_spending_by_category_raises_error():
    with pytest.raises(Exception) as exc_info:
        spending_by_category('25')
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == "spending_by_category() missing 1 required positional argument: 'category'"




if __name__ == "__main__":
    unittest.main()

