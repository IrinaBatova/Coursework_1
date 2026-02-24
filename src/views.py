import logging
import inspect
from pprint import pprint
from datetime import datetime
from typing import Any, Dict
from pathlib import Path
from src.data_import import read_excel_file
from src.utils import get_greeting, get_time_period, get_cards, get_top_transactions, get_currency_rates, get_stock_prices

log_path = Path(__file__).parent.parent / "logs" / "views.log"

logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


file_path = str(Path(__file__).parent.parent / "data")

def main_page(data_user: str = None) -> Dict[str, Any]:
    """
    Функция для страницы «Главная» принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS,
    если дата пользователем не задана, то по умолчанию текущая дата и время.
    Функция для страницы «Главная» возвращает корректный JSON-ответ согласно ТЗ
    :param data_user: строка с датой и временем в формате YYYY-MM-DD HH:MM:SS, по умолчанию текущая дата
    :return: JSON-ответ
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        if data_user is None:
            data_user = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(data_user)

        # Период с начала месяца по заданную пользователем дату
        period = get_time_period(data_user)

        # Список транзакций за заданный период формата ["01.05.2020", "20.05.2020"]
        list_of_transactions = read_excel_file(path_to_file=f"{file_path}/operations.xlsx", time_period=period)

        # Проверяем пустой ли список
        if not list_of_transactions:
            logger.info(f'Функция "{func_name}" возвратила пустой JSON-ответ, нет транзакций за заданный период')
            print(f'Функция "{func_name}" возвратила пустой JSON-ответ, нет транзакций за заданный период')
            return {}

        else:
            # Приветствие
            greeting = get_greeting(data_user)

            # По каждой карте (последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые 100 рублей):
            cards = get_cards(list_of_transactions)

            # Топ-5 транзакций по сумме платежа
            top_transactions = get_top_transactions(list_of_transactions)

            # Курс валют
            currency_rates = get_currency_rates("RUB")

            # Стоимость акций из S&P500
            stock_prices = get_stock_prices()

            logger.info(f'Функция "{func_name}" возвратила JSON-ответ')

            return {
                "greeting": greeting,
                "cards": cards,
                "top_transactions": top_transactions,
                "currency_rates": currency_rates,
                "stock_prices": stock_prices
            }

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: {ex}')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение:{ex}')


if __name__ == "__main__":
    pprint(main_page("2021-12-31 13:57:29"))
    # pprint(main_page())
    # {
    #     "greeting": "Добрый день",
    #     "cards": [
    #         {
    #             "last_digits": "5814",
    #             "total_spent": 1262.00,
    #             "cashback": 12.62
    #         },
    #         {
    #             "last_digits": "7512",
    #             "total_spent": 7.94,
    #             "cashback": 0.08
    #         }
    #     ],
    #     "top_transactions": [
    #         {
    #             "date": "21.12.2021",
    #             "amount": 1198.23,
    #             "category": "Переводы",
    #             "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    #         },
    #         {
    #             "date": "20.12.2021",
    #             "amount": 829.00,
    #             "category": "Супермаркеты",
    #             "description": "Лента"
    #         },
    #         {
    #             "date": "20.12.2021",
    #             "amount": 421.00,
    #             "category": "Различные товары",
    #             "description": "Ozon.ru"
    #         },
    #         {
    #             "date": "16.12.2021",
    #             "amount": -14216.42,
    #             "category": "ЖКХ",
    #             "description": "ЖКУ Квартира"
    #         },
    #         {
    #             "date": "16.12.2021",
    #             "amount": 453.00,
    #             "category": "Бонусы",
    #             "description": "Кешбэк за обычные покупки"
    #         }
    #     ],
    #     "currency_rates": [
    #         {
    #             "currency": "USD",
    #             "rate": 73.21
    #         },
    #         {
    #             "currency": "EUR",
    #             "rate": 87.08
    #         }
    #     ],
    #     "stock_prices": [
    #         {
    #             "stock": "AAPL",
    #             "price": 150.12
    #         },
    #         {
    #             "stock": "AMZN",
    #             "price": 3173.18
    #         },
    #         {
    #             "stock": "GOOGL",
    #             "price": 2742.39
    #         },
    #         {
    #             "stock": "MSFT",
    #             "price": 296.71
    #         },
    #         {
    #             "stock": "TSLA",
    #             "price": 1007.08
    #         }
    #     ]
    # }