import logging
import calendar
import math
import os
from pathlib import Path
import inspect
from datetime import datetime, date
import pandas as pd
from pprint import pprint
from src.external_api import currency_conversion
from src.utils import get_time_period
from src.data_import import read_excel_file_columns
from typing import Any, List, Dict

log_path = Path(__file__).parent.parent / "logs" / "services.log"

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

file_path = str(Path(__file__).parent.parent / "data")

# def read_excel_file_columns(path_to_file: str, columns: list[str]) -> list:
#     """
#     Функция, которая принимает на вход путь до Excel-файла и список с названиями столбцов для выгрузки
#     из Excel-файла, а возвращает список словарей с данными из заданных столбцов о финансовых транзакциях.
#     Если файл пустой, не Excel-файл или не найден, функция возвращает пустой список.
#     :param path_to_file: Строка - путь до Excel-файла
#     :param columns: Список с названиями столбцов в виде строк
#     :return: список словарей с данными из заданных столбцов
#     """
#
#     # Получаем имя текущей функции
#     func_name = inspect.currentframe().f_code.co_name
#
#     logger.info(f'Начала выполняться функция "{func_name}"')
#
#     try:
#         _, file_extension = os.path.splitext(path_to_file)  # Получаем расширение файла
#
#         # Проверяем, является ли расширение - '.xlsx'
#         if file_extension == ".xlsx":
#             logger.info(f"Загружаются данные из Excel-файла {path_to_file} в объект DataFrame")
#             # Создаем DataFrame по имени столбцов из Excel-файла
#             df_columns = pd.read_excel(f'{file_path}/operations.xlsx', usecols=columns)
#             # pprint(df)
#
#             if df_columns.empty:
#                 logger.info(f"Файл {path_to_file} пустой, возвращен пустой список.")
#                 print(f"Файл {path_to_file} пустой, возвращен пустой список.")
#                 return []
#             else:
#                 if 'Дата операции' in df_columns:
#                     # Преобразуем в нужный формат "строка" столбец 'Дата операции'
#                     df_columns['Дата операции'] = pd.to_datetime(df_columns['Дата операции'],
#                                                                  format='%d.%m.%Y %H:%M:%S').dt.strftime('%Y-%m-%d')
#                     # print(df)
#
#                 # Преобразуем в список словарей
#                 list_of_dicts = df_columns.to_dict(orient='records')
#                 # pprint(list_of_dicts)
#
#                 logger.info(f'Функция "{func_name}" возвратила список словарей с данными из заданных столбцов')
#                 return list_of_dicts
#
#     except FileNotFoundError as ex:
#         logger.error(f"Файл {path_to_file} не найден. Произошла ошибка: {ex}")
#         print(f"Файл {path_to_file} не найден, возвращен пустой список")
#         return []
#
#     except Exception as ex:
#         logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: {ex}')
#         print(f'Функция "{func_name}" возвратила ошибку общее исключение:{ex}')
#         return []



# list_of_dicts = read_excel_file_columns(f"{file_path}/operations.xlsx", ['Дата операции', 'Сумма операции'])
# pprint(list_of_dicts)

# 1. Создаём DataFrame, выбирая из Excel-файла только столбцы с заданными именами
df_transactions = pd.read_excel(f'{file_path}/operations.xlsx', usecols=['Дата операции', 'Сумма операции', 'Валюта операции', 'Категория'])
# pprint(df_transactions)
# print(df_transactions['Дата операции'].dtype)

# 2. Преобразование в тип datetime64 данные в столбце 'Дата операции'
df_transactions['Дата операции'] = pd.to_datetime(df_transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
# print(df_transactions['Дата операции'][0])
# print(df_transactions['Дата операции'].dtype)

# 3. Преобразование в нужный формат строки
df_transactions['Дата операции'] = pd.to_datetime(df_transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S').dt.strftime('%Y-%m-%d')
# print(df_transactions)
# print(df_transactions['Дата операции'].dtype)

 # 4. Преобразование в список словарей
list_of_dicts = df_transactions.to_dict(orient='records')
# pprint(list_of_dicts)



def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Функция возвращает сумму, которую удалось бы отложить в «Инвесткопилку».
    :param month: Месяц, для которого рассчитывается отложенная сумма (строка в формате 'YYYY-MM').
    :param transactions: Список словарей, содержащий информацию о транзакциях
      (Дата операции — дата, когда произошла транзакция (строка в формате 'YYYY-MM-DD');
       Сумма операции — сумма транзакции в оригинальной валюте (число)).
    :param limit: Предел, до которого нужно округлять суммы операций (целое число)
    :return:
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        # 1. Первое

        # Создаем дату первого дня месяца в виде объекта datetime.date (только дата, без времени)
        first_day_month_dt = datetime.strptime(month, '%Y-%m').date()
        # print(first_day_month_dt)
        # print(f'Тип переменной first_day_month_dt: {type(first_day_month_dt)}')

        # Получаем год и месяц
        year = first_day_month_dt.year
        month = first_day_month_dt.month

        # monthrange возвращает кортеж из двух элементов (1: день недели 1-го числа, 2:количество дней в месяце)
        # Получаем количество дней в месяце
        days_in_month = calendar.monthrange(year, month)[1]
        # print(days_in_month)

        # Создаем дату последнего дня месяца в виде объекта datetime.date (только дата, без времени)
        last_day_month_dt = datetime(year, month, days_in_month).date()
        # print(last_day_month_dt)
        # print(f'Тип переменной last_day_month_dt: {type(last_day_month_dt)}')

        # 2. Второе

        # Преобразуем список словарей в объект DataFrame
        df_transactions = pd.DataFrame(transactions)
        # print(df_transactions)
        # print(df_transactions['Дата операции'].dtype)

        # Преобразуем столбец 'Дата операции' из типа str в тип datetime64
        df_transactions['Дата операции'] = pd.to_datetime(df_transactions['Дата операции'], format='%Y-%m-%d')
        # print(df_transactions['Дата операции'][0])
        # print(df_transactions['Дата операции'].dtype)

        # Локализация (метод .dt.tz_localize('UTC') добавляет временную зону UTC) и
        # конвертация (метод .dt.tz_convert('Europe/Moscow') преобразует времена из UTC в московское время) временной зоны
        s_local = df_transactions['Дата операции'].dt.tz_localize('UTC').dt.tz_convert('Europe/Moscow')
        # pprint(s_local[0])
        # print(f'Тип переменной s_local: {type(s_local[0])}')

        # Создаём маску (или фильтр) для данных. Используется метод between(), чтобы выбрать даты, которые находятся в диапазоне
        # между first_day_month_dt и last_day_month_dt, включительно (inclusive="both"). Возвращает логическую маску (массив True/False)
        mask = s_local.dt.date.between(first_day_month_dt, last_day_month_dt, inclusive="both")

        # Создаём новый DataFrame df_transactions_filtered, состоящий только из строк df_transactions,
        # даты которых находятся в указанном диапазоне
        df_transactions_filtered = df_transactions[mask]
        # pprint(df_transactions_filtered)
        # print(df_transactions_filtered['Дата операции'].dtype)

        list_of_categories = ['Другое', 'Переводы', 'Наличные', 'Финансы', 'ЖКХ', 'НКО']

        # Создаём новый DataFrame, состоящий из строк, где значение 'Сумма операции' < 0, а
        # значение 'Категория' не совпадает со значениями в списке list_of_categories
        df_result = df_transactions_filtered[(df_transactions_filtered['Сумма операции'] < 0) & (~df_transactions_filtered['Категория'].isin(list_of_categories))]
        # print(df_result)

        # # Преобразуем DataFrame в список словарей
        list_result = df_result.to_dict(orient="records")
        # pprint(list_result)

        # list_result_ = [{'Валюта операции': 'RUB',
        #                       'Дата операции': Timestamp('2018-05-24 00:00:00'),
        #                       'Категория': 'Супермаркеты',
        #                       'Сумма операции': -445.39},
        #                      {'Валюта операции': 'TRY',
        #                       'Дата операции': Timestamp('2018-05-23 00:00:00'),
        #                       'Категория': 'Отели',
        #                       'Сумма операции': -10.0}]

        # 3. Считаем "Инвесткопилку"
        investment_piggy_bank = 0

        for transaction in list_result:

            if transaction["Валюта операции"] == "RUB":

                amount_rub = math.fabs(transaction['Сумма операции'])
                step = limit
                res = math.ceil(amount_rub / step) * step
                investment_piggy_bank += (res - amount_rub)

            else:
                amount_no_rub = str(math.fabs(transaction.get('Сумма операции')))  # получаем сумму не в рублях
                # print(amount_no_rub)
                currency = transaction.get('Валюта операции')  # получаем тип валюты

                # Вызываем функцию конвертации валюты
                logger.info(f'Функция "{func_name}" конвертирует сумму транзакции в {currency} в рубли')
                amount_rub = currency_conversion(amount_no_rub, currency)

                step = limit
                res = math.ceil(amount_rub / step) * step
                investment_piggy_bank += (res - amount_rub)

        return investment_piggy_bank

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: {ex}')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение:{ex}')



if __name__ == "__main__":

    # transactions = read_excel_file_columns(f"{file_path}/operations.xlsx", ['Дата операции', 'Сумма операции'])

    transactions = list_of_dicts
    #
    pprint(investment_bank('2018-05', transactions, 10))

    # pprint(read_excel_file_columns(f"{file_path}/operations.xlsx", ['Дата операции', 'Сумма операции']))
