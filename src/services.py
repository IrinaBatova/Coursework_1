import calendar
import inspect
import logging
import math
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import Any, Dict, List

import pandas as pd

from src.data_import import read_excel_file_columns
from src.external_api import currency_conversion

log_path = Path(__file__).parent.parent / "logs" / "services.log"

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Настройка библиотеки pandas: чтобы при отображении объекта DataFrame показывались
# все столбцы без сокращений (многоточия)
# pd.set_option('display.max_columns', None)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Функция возвращает сумму, которую удалось бы отложить в «Инвесткопилку».
    :param month: Месяц, для которого рассчитывается отложенная сумма (строка в формате 'YYYY-MM').
    :param transactions: Список словарей, содержащий информацию о транзакциях
      (Дата операции — дата, когда произошла транзакция (строка в формате 'YYYY-MM-DD');
       Сумма операции — сумма транзакции в оригинальной валюте (число)).
    :param limit: Предел, до которого нужно округлять суммы операций (целое число)
    :return: Возвращает сумму инвесткопилки, тип данных float
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        # Создаем дату первого дня месяца в виде объекта datetime.date (только дата, без времени)
        first_day_month_dt = datetime.strptime(month, "%Y-%m").date()
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
        # print(f'Тип переменной last_day_month_dt: {type(last_day_month_dt)}')

        # Преобразуем список словарей в объект DataFrame
        df_transactions = pd.DataFrame(transactions)
        # print(df_transactions)

        # Преобразуем столбец 'Дата операции' из типа str в тип datetime64
        df_transactions["Дата операции"] = pd.to_datetime(df_transactions["Дата операции"], format="%Y-%m-%d")
        # print(df_transactions['Дата операции'][0])
        # print(df_transactions['Дата операции'].dtype)

        # Локализация (метод .dt.tz_localize('UTC') добавляет временную зону UTC) и
        # конвертация (метод .dt.tz_convert('Europe/Moscow') преобразует времена из
        # UTC в московское время) временной зоны
        s_local = df_transactions["Дата операции"].dt.tz_localize("UTC").dt.tz_convert("Europe/Moscow")
        # pprint(s_local[0])
        # print(f'Тип переменной s_local: {type(s_local[0])}')

        # Создаём маску (или фильтр) для данных. Используется метод between(), чтобы выбрать даты,
        # которые находятся в диапазоне между first_day_month_dt и last_day_month_dt, включительно
        # (inclusive="both"). Возвращает логическую маску (массив True/False)
        mask = s_local.dt.date.between(first_day_month_dt, last_day_month_dt, inclusive="both")

        # Создаём новый DataFrame df_transactions_filtered, состоящий только из строк df_transactions,
        # даты которых находятся в указанном диапазоне
        df_transactions_filtered = df_transactions[mask]
        # pprint(df_transactions_filtered)
        # print(df_transactions_filtered['Дата операции'].dtype)

        list_of_categories = ["Другое", "Переводы", "Наличные", "Финансы", "ЖКХ", "НКО"]

        # Создаём новый DataFrame, состоящий из строк, где значение 'Сумма операции' < 0, а
        # значение 'Категория' не совпадает со значениями в списке list_of_categories
        df_result = df_transactions_filtered[
            (df_transactions_filtered["Сумма операции"] < 0)
            & (~df_transactions_filtered["Категория"].isin(list_of_categories))
        ]
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

        # Считаем "Инвесткопилку"
        investment_piggy_bank = 0

        for transaction in list_result:

            if transaction["Валюта операции"] == "RUB":

                amount_rub = math.fabs(transaction["Сумма операции"])
                step = limit
                res = math.ceil(amount_rub / step) * step
                investment_piggy_bank += res - amount_rub

            else:
                amount_no_rub = str(math.fabs(transaction.get("Сумма операции")))  # получаем сумму не в рублях
                # print(amount_no_rub)
                currency = transaction.get("Валюта операции")  # получаем тип валюты

                # Вызываем функцию конвертации валюты
                logger.info(f'Функция "{func_name}" конвертирует сумму транзакции в {currency} в рубли')
                amount_rub = currency_conversion(amount_no_rub, currency)

                step = limit
                res = math.ceil(amount_rub / step) * step
                investment_piggy_bank += res - amount_rub

        logger.info(f'Функция "{func_name}" возвратила сумму, которую удалось бы отложить в «Инвесткопилку»')
        return round(investment_piggy_bank, 2)

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')
        # print(f'Функция {func_name} возвратила ошибку общее исключение: {ex}')
        raise Exception(f"Функция {func_name} возвратила ошибку общее исключение: {ex}")


if __name__ == "__main__":

    file_path = str(Path(__file__).parent.parent / "data")

    # pprint(read_excel_file_columns(f"{file_path}/operations.xlsx", ['Дата операции',
    # 'Сумма операции', 'Валюта операции', 'Категория']))

    transactions = read_excel_file_columns(
        f"{file_path}/operations.xlsx", ["Дата операции", "Сумма операции", "Валюта операции", "Категория"]
    )

    # pprint(transactions)
    pprint(investment_bank("2021-12", transactions, 10))
