from pathlib import Path
import pandas as pd
from src import views, reports, services
from pprint import pprint

# Модуль views.py
data_user = "2020-06-28 13:30:35"
pprint(views.main_page(data_user))


# Модуль services.py
file_path_ = str(Path(__file__).parent / "data")
transactions = services.read_excel_file_columns(f"{file_path_}/operations.xlsx", ['Дата операции', 'Сумма операции', 'Валюта операции', 'Категория'])

pprint(services.investment_bank('2021-12', transactions, 10))


# Модуль reports.py

data = reports.read_excel_file(path_to_file=f"{file_path_}/operations.xlsx")
df_data = pd.DataFrame(data)

# Вызов с декоратором (применяем вручную)
spending_by_category = reports.file_write_decorator()(reports.spending_by_category)
spending_by_category(df_data, 'Супермаркеты', "05.12.2021")







# if __name__ == "__main__":
#     data_user = "2020-06-28 13:30:35"