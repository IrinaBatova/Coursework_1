import logging
import inspect
import os
from pprint import pprint

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional
from dateutil.relativedelta import relativedelta
from src.data_import import read_excel_file

log_path = Path(__file__).parent.parent / "logs" / "reports.log"

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Настройка библиотеки pandas: чтобы при отображении объекта DataFrame показывались
# все столбцы без сокращений (многоточия)
pd.set_option('display.max_columns', None)

def spending_by_category(df_transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)
    :param df_transactions: DataFrame с транзакциями
    :param category: название категории
    :param date: опциональная дата в формате '01.01.2026'; если дата не передана, то берется текущая дата
    :return: DataFrame с тратами по заданной категории за последние три месяца (от переданной даты)
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    if date is None:
        date = datetime.now().strftime("%d.%m.%Y")

    # Преобразуем текущую дату из строки в объект datetime
    current_date = datetime.strptime(date, "%d.%m.%Y").date()

    # Вычитаем из текущей даты три месяца
    three_months_ago = current_date - relativedelta(months=3)

    # Преобразуем столбец 'Дата операции' из типа str в тип datetime64
    df_transactions['Дата операции'] = pd.to_datetime(df_transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    # print(df_transactions['Дата операции'][0])
    # print(df_transactions['Дата операции'].dtype)

    # Локализация (метод .dt.tz_localize('UTC') добавляет временную зону UTC) и
    # конвертация (метод .dt.tz_convert('Europe/Moscow') преобразует времена из UTC в московское время) временной зоны
    s_local = df_transactions['Дата операции'].dt.tz_localize('UTC').dt.tz_convert('Europe/Moscow')
    # pprint(s_local[0])
    # print(f'Тип переменной s_local: {type(s_local[0])}')

    # Создаём маску (или фильтр) для данных. Используется метод between(), чтобы выбрать даты, которые находятся в диапазоне
    # между three_months_ago и current_date, включительно (inclusive="both"). Возвращает логическую маску (массив True/False)
    mask = s_local.dt.date.between(three_months_ago, current_date, inclusive="both")

    # Создаём новый DataFrame df_transactions_filtered, состоящий только из строк df_transactions,
    # даты которых находятся в указанном диапазоне
    df_transactions_filtered = df_transactions[mask]
    # pprint(df_transactions_filtered)
    # print(df_transactions_filtered['Дата операции'].dtype)

    # Проверяем пустой ли DataFrame
    if not df_transactions_filtered.empty:

        # # Создаём новый DataFrame, состоящий из строк, где значение 'Сумма операции' < 0, а
        # # значение 'Категория' совпадает со значением заданной категории 'category'
        df_result = df_transactions_filtered[(df_transactions_filtered['Сумма операции'] < 0) & (df_transactions_filtered['Категория'] == category)]
        logger.info(f'Функция "{func_name}" возвратила DataFrame')
        return df_result

    else:
        logger.info(f'Функция "{func_name}" возвратила пустой DataFrame, нет транзакций за заданный период')
        print(f'Функция "{func_name}" возвратила пустой DataFrame, нет транзакций за заданный период')



def file_write_decorator(path_to_file=None):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            if path_to_file is None:

                # Определяем путь к папке и файлу
                folder_path = str(Path(__file__).parent.parent / "data")
                file_name = 'operations_write_1.xlsx'
                full_path = os.path.join(folder_path, file_name)

                # # Создаем папку, если она не существует
                # if not os.path.exists(folder_path):
                #     os.makedirs(folder_path)

                result = func(*args, **kwargs)

                # Записываем в Excel файл
                result.to_excel(full_path, index=False, engine='xlsxwriter', sheet_name='Отчет по операциям')

                return result
            else:
                result = func(*args, **kwargs)

                # Записываем в Excel файл
                result.to_excel(path_to_file, index=False, engine='xlsxwriter', sheet_name='Отчет по операциям')

                return result
        return wrapper
    return my_decorator



if __name__ == "__main__":

    file_path_ = str(Path(__file__).parent.parent / "data")
    data = read_excel_file(path_to_file=f"{file_path_}/operations.xlsx")

    df_data = pd.DataFrame(data)

    # pprint(df_data)
    # print(type(df_data))

    # Вызов БЕЗ декоратора
    # pprint(spending_by_category(df_data, 'Супермаркеты'))
    # pprint(spending_by_category(df_data, 'Супермаркеты', "05.12.2021"))
    # pprint(spending_by_category(df_data, 'Супермаркеты', "05.12.2026"))


    # Вызов с декоратором (применяем вручную)

    # # Шаг 1: Получаем декоратор с заданным параметром
    # # file_write_decorator = file_write_decorator()
    # file_write_decorator = file_write_decorator(path_to_file=f"{file_path_}/operations_write_2.xlsx")
    #
    # # Шаг 2: Применяем декоратор к функции
    # decorated_spending_by_category = file_write_decorator(spending_by_category)
    #
    # # Шаг 3: Вызываем декорированную функцию
    # decorated_spending_by_category(df_data, 'Супермаркеты', "05.12.2021")


    # Можно сделать в одну строку:
    spending_by_category = file_write_decorator()(spending_by_category)
    # spending_by_category = file_write_decorator(path_to_file=f"{file_path_}/operations_write_2.xlsx")(spending_by_category)
    spending_by_category(df_data, 'Супермаркеты', "05.12.2021")