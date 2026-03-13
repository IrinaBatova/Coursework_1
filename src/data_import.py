import inspect
import json
import logging
import os
from pathlib import Path

import pandas as pd

# Настройка библиотеки pandas: чтобы при отображении объекта DataFrame показывались
# все столбцы без сокращений (многоточия)
# pd.set_option('display.max_columns', None)

log_path = Path(__file__).parent.parent / "logs" / "data_import.log"

logger = logging.getLogger("data_import")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_excel_file_columns(path_to_file: str, columns: list[str]) -> list:
    """
    Функция, которая принимает на вход путь до Excel-файла и список с названиями столбцов для выгрузки
    из Excel-файла, а возвращает список словарей с данными из заданных столбцов о финансовых транзакциях.
    Если файл пустой, не Excel-файл или не найден, функция возвращает пустой список.
    :param path_to_file: Строка - путь до Excel-файла
    :param columns: Список с названиями столбцов в виде строк
    :return: список словарей с данными из заданных столбцов
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        _, file_extension = os.path.splitext(path_to_file)  # Получаем расширение файла

        # Проверяем, является ли расширение - '.xlsx'
        if file_extension == ".xlsx":
            logger.info(f"Загружаются данные из Excel-файла {path_to_file} в объект DataFrame")

            # Создаём DataFrame, выбирая из Excel-файла только столбцы с заданными именами
            df_columns = pd.read_excel(f"{path_to_file}", usecols=columns)

            if df_columns.empty:
                logger.info(f"Файл {path_to_file} пустой, возвращен пустой список.")
                print(f"Файл {path_to_file} пустой, возвращен пустой список.")
                return []
            else:
                if "Дата операции" in df_columns:
                    # Преобразуем в нужный формат "строка" столбец 'Дата операции'
                    df_columns["Дата операции"] = pd.to_datetime(
                        df_columns["Дата операции"], format="%d.%m.%Y %H:%M:%S"
                    ).dt.strftime("%Y-%m-%d")
                    # print(df)

                # Преобразуем в список словарей
                list_of_dicts = df_columns.to_dict(orient="records")
                # pprint(list_of_dicts)

                logger.info(f'Функция "{func_name}" возвратила список словарей с данными из заданных столбцов')
                return list_of_dicts
        else:
            return []

    except FileNotFoundError as ex:
        logger.error(f"Файл {path_to_file} не найден. Произошла ошибка: {ex}")
        print(f"Файл {path_to_file} не найден, возвращен пустой список")
        return []

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: {ex}')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение:{ex}')
        return []


def read_excel_file(path_to_file: str, time_period: list = None) -> list:
    """
    Функция, которая принимает на вход путь до Excel-файла и возвращает список словарей с данными о
    финансовых транзакциях за заданный временной период. Если временной период не задан, то возвращает
    список словарей с данными по всем финансовым транзакциям. Если файл пустой, не Excel-файл или не
    найден, функция возвращает пустой список.
    :param path_to_file: Строка - путь до Excel-файла
    :param time_period: принимает список в формате ['01.01.2026', '18.01.2026'] с временным периодом
     для отбора транзакций из Excel-файла,
    не является обязательным, по умолчанию значение None
    :return: список словарей
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        _, file_extension = os.path.splitext(path_to_file)  # Получаем расширение файла

        if file_extension == ".xlsx":  # Проверяем, является ли расширение - '.xlsx'
            logger.info(f"Загружаются данные из Excel-файла {path_to_file} в объект DataFrame")
            df_transactions = pd.read_excel(path_to_file)  # читаем Excel-файл и создаем DataFrame

            if df_transactions.empty:
                logger.info(f"Файл {path_to_file} пустой, возвращен пустой список.")
                print(f"Файл {path_to_file} пустой, возвращен пустой список.")
                return []
            else:
                if time_period is None:
                    # Трансформируем DataFrame в список словарей с ключами, соответствующими названиям столбцов
                    list_of_transactions = df_transactions.to_dict(orient="records")
                    logger.info(
                        f'Функция "{func_name}" возвратила список словарей с данными о всех финансовых транзакциях.'
                    )
                    return list_of_transactions  # [0:5]
                else:
                    # pprint(df_transactions[['Дата операции', 'Дата платежа']].head()) # выводим первые 5 строк

                    # Преобразование в тип datetime64
                    df_transactions["Дата платежа"] = pd.to_datetime(
                        df_transactions["Дата платежа"], format="%d.%m.%Y"
                    )
                    # print(df_transactions['Дата платежа'][0])
                    # print(df_transactions['Дата платежа'].dtype)

                    # Локализация (метод .dt.tz_localize('UTC') добавляет временную зону UTC) и
                    # конвертация (метод .dt.tz_convert('Europe/Moscow') преобразует времена
                    # из UTC в московское время) временной зоны
                    s_local = df_transactions["Дата платежа"].dt.tz_localize("UTC").dt.tz_convert("Europe/Moscow")
                    # pprint(s_local[0])

                    # После преобразования строки в объект datetime, метод .date() используется
                    # для извлечения только даты, без времени.
                    start = pd.to_datetime(time_period[0], format="%d.%m.%Y").date()
                    end = pd.to_datetime(time_period[1], format="%d.%m.%Y").date()
                    # print(f'Тип переменной start: {type(start)}')

                    # Создаём маску (или фильтр) для данных. Используется метод between(), чтобы выбрать даты,
                    # которые находятся в диапазоне между start и end, включительно (inclusive="both").
                    # Возвращает логическую маску (массив True/False)
                    mask = s_local.dt.date.between(start, end, inclusive="both")

                    # Создаём новый DataFrame df_filtered, состоящий только из строк df_transactions,
                    # даты которых находятся в указанном диапазоне
                    df_filtered = df_transactions[mask]
                    # pprint(df_filtered)
                    # print(df_filtered['Дата платежа'].dtype)

                    # Изменяем тип данных в столбце 'Дата платежа' на строку
                    df_filtered["Дата платежа"] = df_filtered["Дата платежа"].astype(str)
                    # print(df_filtered['Дата платежа'].dtype)

                    # Преобразуем DataFrame в список словарей
                    list_of_transactions = df_filtered.to_dict(orient="records")

                    logger.info(
                        f'Функция "{func_name}" возвратила список словарей с данными о'
                        f" финансовых транзакциях за период {time_period}."
                    )

                    return list_of_transactions

        else:
            logger.info(f"Файл {path_to_file} не Excel файл, возвращен пустой список.")
            print(f"Файл {path_to_file} не .xlsx файл, возвращен пустой список.")
            return []

    except FileNotFoundError as ex:
        logger.error(f"Файл {path_to_file} не найден. Произошла ошибка: {ex}")
        print(f"Файл {path_to_file} не найден, возвращен пустой список")
        return []

    except Exception as ex:
        logger.error(f"Это общее исключение.{ex}")
        print(f"Это общее исключение.{ex}")

    return []


def read_json_file(path_to_file: str) -> dict:
    """
    Функция, которая принимает на вход путь до JSON-файла и возвращает
    список словарей с данными о финансовых транзакциях. Если файл
    пустой, содержит не список или не найден, функция возвращает пустой список.
    :param path_to_file: Путь до JSON-файла
    :return: словарь
    """
    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        with open(path_to_file, encoding="utf-8") as f:  # Открываем файл и читаем строки
            logger.info(f"Открываем файл {path_to_file} и читаем строки")
            first_char = f.read(1)
            if not first_char:
                logger.info(f"Файл {path_to_file} пустой, возвращен пустой список.")
                print(f"Файл {path_to_file} пустой")
                return {}
            f.seek(0)  # перемещаем указатель чтения/записи в начало файла
            user_settings_currency = json.load(f)
            if type(user_settings_currency) is dict:
                logger.info(f'Функция "{func_name}" возвратила словарь с данными о финансовых транзакциях.')
                return user_settings_currency
            else:
                logger.info(
                    f'Файл {path_to_file} не содержит словарь, функция "{func_name}" возвратила пустой словарь.'
                )
                print(f'Файл {path_to_file} не содержит словарь, функция "{func_name}" возвратила пустой словарь.')
                return {}

    except FileNotFoundError as ex:
        logger.error(f"Файл {path_to_file} не найден. Произошла ошибка: {ex}")
        print(f"Файл {path_to_file} не найден")
        return {}

    except json.JSONDecodeError as ex:
        logger.error(f"Ошибка декодирования JSON-файла {path_to_file} : {ex}")
        print(f"Ошибка декодирования JSON-файла {path_to_file} : {ex}")

    except Exception as ex:
        logger.error(f"Это общее исключение.{ex}")
        print(f"Это общее исключение.{ex}")

    return {}


if __name__ == "__main__":
    file_path = str(Path(__file__).parent.parent / "data")
    # print(read_excel_file(path_to_file=f"{file_path}/operations.xlsx"))
    # pprint(read_excel_file(path_to_file=f"{file_path}/operations.xlsx"))
    # pprint(read_excel_file(path_to_file=f"{file_path}/operations.xlsx", time_period=['25.09.2019', '25.09.2019']))
    # print(read_json_file(path_to_file=f"{file_path}/user_settings.json"))
    # pprint(read_excel_file_columns(path_to_file=f"{file_path}/operations.xlsx",
    # columns=['Дата операции', 'Сумма операции']))
    # pprint(read_excel_file_columns(f"{file_path}/operations.xlsx",
    # ['Дата операции', 'Сумма операции', 'Валюта операции']))
    # pprint(read_excel_file_columns(f"{file_path}/operations.xlsx", ['Сумма операции', 'Валюта операции']))

# s = df_transactions['Дата платежа'] # — это Pandas Series с временными метками (datetime-like)
# print(getattr(s.dt, "tz", None))  # если tz-aware — покажет таймзону                    #
# print(s.loc[130])  # проблемная строка
# Отбор строк в диапазоне дат
# start_date = pd.to_datetime(time_period[0], format='%d.%m.%Y').date()  # начало диапазона
# end_date = pd.to_datetime(time_period[1], format='%d.%m.%Y').date() # конец диапазона
# Диапазон дат
# df_filtered_range = df_transactions.query('@start_date <= `Дата платежа` <= @end_date')

# if start_date == end_date:
#     df_filtered_range = df_transactions[(df_transactions['Дата платежа'] == start_date)]
# else:
#     df_filtered_range = df_transactions[(df_transactions['Дата платежа'] >=
#     start_date) & (df_transactions['Дата платежа'] <= end_date)]

# df_transactions.sort_values(by='Дата платежа', inplace=True)
# df = df_transactions.sort_values(by='Дата платежа', ascending=True)
# df_filtered = df_transactions['01.12.2021' <= df_transactions['Дата платежа'] >= '18.12.2021']

# pprint(df_filtered)
# filtered_df_transactions = df_transactions[df_transactions['Дата платежа'].isin(pd.to_datetime(time_period,
# format="%d.%m.%Y"))]
# filtered_df_transactions = df_transactions[df_transactions['Дата платежа'].between('01.12.2021', '31.12.2021')]
