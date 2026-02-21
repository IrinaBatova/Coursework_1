import logging
import math
import pandas as pd
import inspect
import time
from datetime import datetime
from pprint import pprint
from pathlib import Path
from src import external_api
from data_import import read_excel_file, read_json_file

log_path = Path(__file__).parent.parent / "logs" / "utils.log"

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def get_greeting(date_string: str) -> str:
    """
    Функция получения приветствия в зависимости от переданного времени в формате "???", где ??? —
    «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    :param date_string: принимает дату и время в виде строки - 2026-01-18 12:57:29
    :return: возвращает приветствие в виде строки
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        user_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S") # возвращает 2026-01-18 15:57:29.084879
        user_hour = user_datetime.hour
        intervals = [
            ((6, 12), "Доброе утро"),
            ((12, 18), "Добрый день"),
            ((18, 23), "Добрый вечер"),
            ((23, 6), "Доброй ночи")
        ]
        for i in intervals:
            if i[0][0] <= user_hour < i[0][1]:
                logger.info(f'Функция "{func_name}" возвратила приветствие: "{i[1]}"')
                return i[1]

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: {ex}')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение:{ex}')

def get_formatted_date(data: str) -> str:
    """
    Функция переформатирования даты
    :param data: принимает дату в виде строки - 2026-01-18 12:57:29
    :return: возвращает переформатированную дату - в виде строки формата "ДД.ММ.ГГГГ" ("11.03.2024").
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        formatted_date = data[8:10] + "." + data[5:7] + "." + data[:4]
        logger.info(f'Функция "{func_name}" возвратила отформатированную дату: "{formatted_date}"')
        return formatted_date


    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: {ex}')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение:{ex}')


def get_time_period(user_data: str): # -> list:
    """
    Функция получения периода с начала месяца по переданную дату
    :param user_data: принимает дату в виде строки - 2026-01-18 12:57:29
    :return: возвращает период в виде списка, например: ['01.01.2026', '18.01.2026']
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        data_user_format = get_formatted_date(user_data)
        start_period = "01" + data_user_format[2:]
        period_list = [start_period, data_user_format]
        logger.info(f'Функция "{func_name}" возвратила период в виде списка: "{period_list}"')
        return period_list

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: {ex}')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение:{ex}')


def transaction_amount(transaction: dict) -> float:
    """
    Функция, которая принимает на вход транзакцию в любой валюте и возвращает сумму транзакции в рублях
    :param transaction: принимает на вход словарь с данными о транзакции
    :return: возвращает сумму транзакции (ключ amount) в рублях, тип данных float
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        # operation_amount = transaction.get("operationAmount")
        # if operation_amount and operation_amount.get("currency") and operation_amount["currency"].get("code") == "RUB":
        if transaction["Валюта операции"] == "RUB":
            logger.info(f'Функция "{func_name}" получает сумму транзакции в рублях')
            amount_rub = float((transaction.get("Сумма операции"))) # получаем сумму в рублях

        else:
            logger.info(f'Функция "{func_name}" получает сумму транзакции не в рублях')
            amount_no_rub = str(transaction.get("Сумма операции с округлением"))  # получаем сумму не в рублях
            print(amount_no_rub)
            currency = transaction.get("Валюта операции")  # получаем тип валюты
            # Вызываем функцию конвертации валюты
            logger.info(f'Функция "{func_name}" конвертирует сумму транзакции в {currency} в рубли')
            amount_rub = external_api.currency_conversion(amount_no_rub, currency)

        logger.info(f'Функция "{func_name}" возвратила сумму транзакции {amount_rub} в рублях.')
        return amount_rub

    except KeyError as ex:
        logger.error(f'Запрошенный ключ не найден в словаре. В функции "{func_name}" произошла ошибка: {ex}')
        raise KeyError(f"Запрошенный ключ не найден в словаре. {ex}")

    except ValueError as ex:
        logger.error(f'Не удалось преобразовать сумму в число. В функции "{func_name}" произошла ошибка: {ex}')
        raise ValueError(f'Не удалось преобразовать сумму в число. В функции "{func_name}" произошла ошибка: {ex}')

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')


def get_card_numbers(list_of_transactions: list) -> list:
    """
    Функция получения номеров карт из заданного списка транзакций
    :param list_of_transactions: список словарей с данными по транзакциям
    :return: список, содержащий номера карт, встречающиеся в заданном списке транзакций
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        set_card_number = set()

        # Отбираем встречающиеся номера карт из списка транзакций в отдельное множество
        for i in list_of_transactions:
            n = i.get('Номер карты')
            set_card_number.add(n)

        # Удаляем объекты NaN из множества и форматируем множество в список
        list_card_numbers = list({x for x in set_card_number if not isinstance(x, float) or not math.isnan(x)})
        # print(list_card_numbers)
        logger.info(f'Функция "{func_name}" возвратила список, содержащий номера карт: "{list_card_numbers}"')
        return list_card_numbers

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')


def get_cards(list_of_transactions: list) -> list:
    """
    Функция получения обобщенных данных по картам из заданного списка транзакций
    :param list_of_transactions: список словарей с данными по транзакциям
    :return: список словарей с обобщенными данными по картам (последние четыре цифры
    номера карты, расходы по карте, кэшбэк)
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        # Отбираем встречающиеся номера карт из списка транзакций в отдельный список
        list_card_numbers = get_card_numbers(list_of_transactions)

        # Создаем словарь для хранения транзакций по номерам карт (ключ: номер карты,
        # значение ключа: пока пустой список под транзакции)
        transactions_by_card = {card: [] for card in list_card_numbers}
        # print(transactions_by_card)

        # Заполняем словарь
        for transaction in list_of_transactions:
            card_number = transaction['Номер карты']
            if card_number in transactions_by_card:
                transactions_by_card[card_number].append(transaction)
        # pprint(transactions_by_card)

        # Создаем пустой список для итоговых данных
        result_list = []

        for card_number in transactions_by_card:

            total_spent = 0

            # Суммируем все отрицательные суммы транзакций (расходы)
            for transaction in transactions_by_card[card_number]:
                amount = transaction.get('Сумма платежа')
                if amount < 0:
                    total_spent += amount

            # Извлекаем последние четыре цифры номера карты
            last_digits = str(card_number)[-4:]

            # Рассчитываем кэшбэк, предположим, что это 1% от потраченной суммы
            cashback = round((abs(total_spent) / 100), 2)

            # Создаем словарь для текущей карты и добавляем его в список
            result_list.append({
                "last_digits": last_digits,
                "total_spent": round(abs(total_spent), 2),
                "cashback": cashback
            })

        logger.info(f'Функция "{func_name}" возвратила список словарей с обобщенными данными по картам: "{result_list}"')

        return result_list

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')

# "cards": [
#     {
#       "last_digits": "5814",
#       "total_spent": 1262.00,
#       "cashback": 12.62
#     },
#     {
#       "last_digits": "7512",
#       "total_spent": 7.94,
#       "cashback": 0.08
#     }
#   ],

def get_top_transactions(list_of_transactions: list) -> list:
    """
    Функция получения пяти топ транзакций по картам из заданного списка транзакций
    :param list_of_transactions: список словарей с данными по транзакциям
    :return: список словарей с данными по отобранным пяти топ транзакциям
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        # Создаем DataFrame из списка транзакций
        transactions_df = pd.DataFrame(list_of_transactions)

        # Сортируем по колонке 'Сумма платежа' в убывающем порядке
        # sorted_df = transactions_df.sort_values(by='Сумма операции', key=abs, ascending=False)
        sorted_df = transactions_df.sort_values(by='Сумма платежа', key=abs, ascending=False)
        # pprint(sorted_df)

        # Получаем первые 5 строк
        top_5_df = sorted_df.head(5)
        # print(type(top_5_df))
        # print(top_5_df)

        # Преобразуем DataFrame top_5_df в список словарей
        top_5_list = top_5_df.to_dict('records')
        # pprint(top_5_list)

        # Создаем пустой список для итоговых данных
        result_list = []

        for el in top_5_list:

            # Отбираем нужные данные
            date_time = datetime.strptime(el.get('Дата операции'), "%d.%m.%Y %H:%M:%S")
            date = date_time.strftime('%d.%m.%Y')

            # amount = float(el.get('Сумма операции'))
            amount = float(el.get('Сумма платежа'))
            category = el.get('Категория')
            description = el.get('Описание')

            # Создаем словарь для текущей top-транзакции и добавляем его в список итоговых данных
            result_list.append({
                "date": date,
                "amount": amount,
                "category": category,
                "description": description
            })

        logger.info(
            f'Функция "{func_name}" возвратила список словарей с данными по отобранным пяти топ транзакциям: "{result_list}"')

        return result_list

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')

# "top_transactions": [
#     {
#       "date": "21.12.2021",
#       "amount": 1198.23,
#       "category": "Переводы",
#       "description": "Перевод Кредитная карта. ТП 10.2 RUR"
#     },
#     {
#       "date": "16.12.2021",
#       "amount": 453.00,
#       "category": "Бонусы",
#       "description": "Кешбэк за обычные покупки"
#     }
#   ]

def get_currency_rates(currency_type: str) -> list:
    """
    Функция возвращает курс в заданной валюте на список валют, заданный в файле
    user_settings.json в папке data
    :param currency_type: тип валюты в виде строки
    :return: курс в заданной валюте в виде списка
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:

        file_path = str(Path(__file__).parent.parent / "data")

        # Считываем данные из файла user_settings.json в папке data
        user_settings_currency = read_json_file(path_to_file=f"{file_path}/user_settings.json")
        # {'user_currencies': ['USD', 'EUR', 'CNY'], 'user_stocks': ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']}

        user_currencies = user_settings_currency['user_currencies']

        # {'RUB': 76.901329} возвращает функция external_api.currency_rate

        # Создаем пустой список для итоговых данных
        result_list = []

        for el in user_currencies:
            currency = el
            # Получаем курс в рублях по каждой валюте
            currency_rates_dist = external_api.currency_rate(el, currency_type)
            rate = round(currency_rates_dist[currency_type], 2)

            # Создаем словарь для текущих курсов валют и добавляем его в список итоговых данных
            result_list.append({
                "currency": currency,
                "rate": rate
            })

        logger.info(
            f'Функция "{func_name}" возвратила курс в заданной валюте в виде списка: "{result_list}"')

        return result_list

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')

# "currency_rates": [
#     {
#         "currency": "USD",
#         "rate": 73.21
#     },
#     {
#         "currency": "EUR",
#         "rate": 87.08
#     }
# ]

def get_stock_prices() -> list:
    """
    Функция возвращает стоимость акций компаний, тикеры которых
    заданы в файле user_settings.json в папке data
    :param : без входных параметров
    :return: стоимость акций в виде списка
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:

        file_path = str(Path(__file__).parent.parent / "data")

        # Считываем данные из файла user_settings.json в папке data
        user_settings_currency = read_json_file(path_to_file=f"{file_path}/user_settings.json")
        # {'user_currencies': ['USD', 'EUR', 'CNY'], 'user_stocks': ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']}

        # Получаем список тикеров компаний из данных считанных из файла user_settings.json
        user_currencies = user_settings_currency['user_stocks']

        # Создаем пустой список для итоговых данных
        result_list = []

        for el in user_currencies:

            stock = el

            # Получаем стоимость акций, тикеры которых заданы в файле user_settings.json в папке data
            stock_prices_dist = external_api.stock_prices(el)
            # pprint(stock_prices_dist)

            if 'Global Quote' in stock_prices_dist:
                price_str = stock_prices_dist['Global Quote']['05. price']
                # pprint(price_str)
                price = round(float(price_str), 2)

                # Создаем словарь для стоимости акций компаний и добавляем его в список итоговых данных
                result_list.append({
                    "stock": stock,
                    "price": price
                })

            else:
                print(stock_prices_dist)
                return []

        logger.info(
            f'Функция "{func_name}" возвратила стоимость акций в виде списка: "{result_list}"')

        return result_list

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение: "{ex}"')

# Возвращает функция get_stock_prices (значение result_list), использовать для тестов:
# [{'price': 264.58, 'stock': 'AAPL'},
#  {'price': 210.11, 'stock': 'AMZN'},
#  {'price': 314.98, 'stock': 'GOOGL'},
#  {'price': 397.23, 'stock': 'MSFT'},
#  {'price': 411.82, 'stock': 'TSLA'}]


if __name__ == "__main__":
    data_user = "2026-03-18 12:57:29"
    # print(get_time_period(data_user))
    pprint(get_greeting(data_user))
    # file_path_ = str(Path(__file__).parent.parent / "data")
    # pprint(read_excel_file(path_to_file=f"{file_path_}/operations.xlsx", time_period=['01.12.2021', '31.12.2021']))
    #
    # list_of_transactions_ = read_excel_file(path_to_file=f"{file_path_}/operations.xlsx", time_period=['01.12.2021', '31.12.2021'])
    # pprint(get_card_numbers(list_of_transactions_))
    # pprint(get_cards(list_of_transactions_))
    # pprint(get_top_transactions(list_of_transactions_))
    #
    # pprint(get_currency_rates("RUB"))
    # pprint(get_stock_prices())

    # Данные для вызова функции transaction_amount()
    transactions_utils_rub = {
        'MCC': 5331.0,
        'Бонусы (включая кэшбэк)': 2,
        'Валюта операции': 'RUB',
        'Валюта платежа': 'RUB',
        'Дата операции': '23.09.2019 15:33:40',
        'Дата платежа': '2019-09-25',
        'Категория': 'Различные товары',
        'Кэшбэк': 0,
        'Номер карты': '*7197',
        'Округление на инвесткопилку': 0,
        'Описание': 'Улыбка радуги',
        'Статус': 'OK',
        'Сумма операции': -149.0,
        'Сумма операции с округлением': 149.0,
        'Сумма платежа': -149.0
    }

    transactions_utils_cny = {
        'MCC': 5813.0,
        'Бонусы (включая кэшбэк)': 0,
        'Валюта операции': 'CNY',
        'Валюта платежа': 'CNY',
        'Дата операции': '24.09.2019 19:15:33',
        'Дата платежа': '2019-09-25',
        'Категория': 'Рестораны',
        'Кэшбэк': 0,
        'Номер карты': '*4556',
        'Округление на инвесткопилку': 0,
        'Описание': 'Shang Hai Xing Ba Ke K',
        'Статус': 'OK',
        'Сумма операции': -32.0,
        'Сумма операции с округлением': 32.0,
        'Сумма платежа': -32.0
    }

    # print(transaction_amount(transactions_utils_rub))
    # print(transaction_amount(transactions_utils_cny))

    # Ответ
    # {'Global Quote': {
    #     '01. symbol': 'AAPL',
    #     '02. open': '263.6000',
    #     '03. high': '266.8200',
    #     '04. low': '262.4500',
    #     '05. price': '264.3500',
    #     '06. volume': '34203337',
    #     '07. latest trading day': '2026-02-18',
    #     '08. previous close': '263.8800',
    #     '09. change': '0.4700',
    #     '10. change percent': '0.1781%'}}
