import logging
import math
from datetime import datetime
from pprint import pprint
from pathlib import Path
from src import external_api
from data_import import read_excel_file

log_path = Path(__file__).parent.parent / "logs" / "data_import.log"

logger = logging.getLogger("data_import")
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
                return i[1]

    except Exception as ex:
        print(f"Это общее исключение.{ex}")

def get_formatted_date(data: str) -> str:
    """
    Функция переформатирования даты
    :param data: принимает дату в виде строки - 2026-01-18 12:57:29
    :return: возвращает переформатированную дату - в виде строки формата "ДД.ММ.ГГГГ" ("11.03.2024").
    """
    try:
        formatted_date = data[8:10] + "." + data[5:7] + "." + data[:4]
        return formatted_date

    except Exception as ex:
        print(f"Это общее исключение.{ex}")


def get_time_period(user_data: str): # -> list:
    """
    Функция получения периода с начала месяца по переданную дату
    :param user_data: принимает дату в виде строки - 2026-01-18 12:57:29
    :return: возвращает период в виде списка, например: ['01.01.2026', '18.01.2026']
    """
    try:
        data_user_format = get_formatted_date(user_data)
        start_period = "01" + data_user_format[2:]
        period_list = [start_period, data_user_format]
        return period_list

    except Exception as ex:
        print(f"Это общее исключение.{ex}")

def transaction_amount(transaction: dict) -> float:
    """
    Функция, которая принимает на вход транзакцию и возвращает сумму транзакции в рублях
    :param transaction: принимает на вход словарь с данными о транзакции
    :return: возвращает сумму транзакции (ключ amount) в рублях, тип данных float
    """

    logger.info("Начала выполняться функция transaction_amount")
    try:
        # operation_amount = transaction.get("operationAmount")
        # if operation_amount and operation_amount.get("currency") and operation_amount["currency"].get("code") == "RUB":
        if transaction["Валюта операции"] == "RUB":
            logger.info("Получаем сумму транзакции в рублях")
            amount_rub = float((transaction.get("Сумма операции"))) # получаем сумму в рублях

        else:
            logger.info("Получаем сумму транзакции не в рублях")
            amount_no_rub = str(transaction.get("Сумма операции с округлением"))  # получаем сумму не в рублях
            print(amount_no_rub)
            currency = transaction.get("Валюта операции")  # получаем тип валюты
            # Вызываем функцию конвертации валюты
            logger.info(f"Конвертируем сумму транзакции в {currency} в рубли")
            amount_rub = external_api.currency_conversion(amount_no_rub, currency)

        logger.info(f"Функция transaction_amount возвратила сумму транзакции {amount_rub} в рублях.")
        return amount_rub

    except KeyError as ex:
        logger.error(f"Запрошенный ключ не найден в словаре. Произошла ошибка: {ex}")
        raise KeyError(f"Запрошенный ключ не найден в словаре. {ex}")

    except ValueError as ex:
        logger.error(f"Не удалось преобразовать сумму в число. Произошла ошибка: {ex}")
        raise ValueError(f"Не удалось преобразовать сумму в число. Произошла ошибка: {ex}")

    except Exception as ex:
        logger.error(f"Это общее исключение. Произошла ошибка: {ex}")
        raise Exception(f"Это общее исключение. Произошла ошибка: {ex}")


def get_cards(list_of_transactions: list) -> list:
    """
    Функция получения обобщенных данных по картам из заданного списка транзакций
    :param list_of_transactions: список словарей с данными по транзакциям
    :return: список словарей с обобщенными данными по картам (последние четыре цифры
    номера карты, расходы по карте, кэшбэк)
    """

    total_spent = 0
    set_card_number = set()

    # Отбираем встречающиеся номера карт из списка транзакций в отдельное множество
    for i in list_of_transactions:
        n = i.get('Номер карты')
        set_card_number.add(n)

    # Удаляем объекты NaN из множества и форматируем множество в список
    list_card_numbers = list({x for x in set_card_number if not isinstance(x, float) or not math.isnan(x)})
    # print(list_card_numbers)

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

    result_list = []  # Создаем пустой список для итоговых данных

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

    return result_list

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


if __name__ == "__main__":
    # data_user = "2026-03-18 12:57:29"
    # print(get_date(data_user))
    # print(get_time_period(data_user))
    # pprint(get_greeting(data_user))
    # pprint(get_cards())
    file_path = str(Path(__file__).parent.parent / "data")
    # pprint(read_excel_file(path_to_file=f"{file_path}/operations.xlsx", time_period=['01.12.2021', '31.12.2021']))

    list_of_transactions_ = read_excel_file(path_to_file=f"{file_path}/operations.xlsx", time_period=['01.12.2021', '31.12.2021'])
    pprint(get_cards(list_of_transactions_))

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
