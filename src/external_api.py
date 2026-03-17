import json
import os
import time
from pprint import pprint
from typing import Any

import requests
from dotenv import load_dotenv


def currency_conversion(amount: str, currency: str) -> float:
    """
    Функция для конвертации валюты.
    - param amount: принимает сумму транзакции в виде строки;
    - param currency: принимает тип валюты транзакции в виде строки;
    - return: возвращает сумму транзакции в рублях.
    """

    # Читаем пары ключ-значение из .env файла и загружаем их в переменные окружения скрипта
    load_dotenv()

    # Безопасно получаем значение переменной окружения API_KEY_APILayer из файла .env
    api_key = os.getenv("API_KEY_APILayer")

    # Задаем адрес сайта, к которому хотим обратиться
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"

    payload: dict = {}
    headers = {"apikey": f"{api_key}"}

    try:
        # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
        response = requests.request("GET", url=url, headers=headers, data=payload)

        # Извлекаем данные из ответа в формате JSON и преобразуем их в Python-словарь (dict)
        result = response.json()
        # pprint(result)

        if "result" in result:
            return float(result["result"])
        else:
            print(result)

    except requests.exceptions.RequestException as e:
        print(f"Сообщение об ошибке: {e}")

    except json.JSONDecodeError as e:
        print("Ошибка декодирования. Invalid result.")
        print(f"Сообщение об ошибке: {e.msg}")
        print(f"Строка: {e.lineno}, колонка: {e.colno}")

    except TypeError:
        print("The object type is not serializable in JSON format.")

    except Exception as e:
        print(f"Ошибка {e}")

    return 0.0


def currency_rate(base: str, symbols: str) -> dict[Any, Any]:
    """
    Функция для получения текущего курса валюты.
    - param base: принимает тип валюты в виде строки;
    - param symbols: список разделенных запятыми кодов валют в виде строки
    - return: возвращает курс, заданных валют в рублях в виде словаря, где
    ключ это тип валюты, а значение курс валюты в рублях.
    """

    # Читаем пары ключ-значение из .env файла и загружаем их в переменные окружения скрипта
    load_dotenv()

    # Безопасно получаем значение переменной окружения API_KEY_APILayer из файла .env
    api_key = os.getenv("API_KEY_APILayer")

    # Задаем адрес сайта, к которому хотим обратиться
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"

    payload: dict = {}
    headers = {"apikey": f"{api_key}"}

    try:
        # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
        response = requests.request("GET", url=url, headers=headers, data=payload)

        # Извлекаем данные из ответа в формате JSON и преобразуем их в Python-словарь (dict)
        result = response.json()
        # pprint(result)

        if "rates" in result:
            return result["rates"]
        else:
            raise Exception(f"{result}")

    except requests.exceptions.RequestException as e:
        print(f"Сообщение об ошибке: {e}")

    except json.JSONDecodeError as e:
        print("Ошибка декодирования. Invalid result.")
        print(f"Сообщение об ошибке: {e.msg}")
        print(f"Строка: {e.lineno}, колонка: {e.colno}")

    except TypeError:
        print("The object type is not serializable in JSON format.")

    except Exception as e:
        print(f"Ошибка {e}")

    return {}


def stock_prices(symbols: str) -> dict:
    """
    Функция для получения стоимости акции.
    - param symbols: принимает тикер акции в виде строки;
    - return: возвращает стоимость акции в виде словаря.
    """

    # Читаем пары ключ-значение из .env файла и загружаем их в переменные окружения скрипта
    load_dotenv()

    # Безопасно получаем значение переменной окружения API_KEY_APILayer из файла .env
    api_key = os.getenv("API_KEY_Alpha_Vantage")

    # Задаем адрес сайта, к которому хотим обратиться
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbols}&apikey={api_key}"

    # Приостанавливаем выполнение текущего потока программы на 1,5 секунды для задержки запроса
    time.sleep(1.5)

    try:
        # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
        response = requests.get(url)

        # Извлекаем данные из ответа в формате JSON и преобразуем их в Python-словарь (dict)
        data = response.json()

        if "Global Quote" in data:
            return data
        else:
            print(f"Функция stock_prices превысила количество бесплатных запросов: {data}")

    except requests.exceptions.RequestException as e:
        print(f"Сообщение об ошибке: {e}")

    except json.JSONDecodeError as e:
        print("Ошибка декодирования. Invalid data.")
        print(f"Сообщение об ошибке: {e.msg}")
        print(f"Строка: {e.lineno}, колонка: {e.colno}")

    except TypeError:
        print("The object type is not serializable in JSON format.")

    except Exception as e:
        print(f"Ошибка {e}")

    return {}


if __name__ == "__main__":

    # pprint(currency_conversion("8221.37", "USD"))
    # pprint(currency_rate("RUB", "USD,EUR,CNY"))
    # pprint(currency_rate("USD", "RUB"))
    pprint(stock_prices("AAPL"))


# Результат response.json() - {'success': True,
#                              'query': {'from': 'USD', 'to': 'RUB', 'amount': 8221.37},
#                              'info': {'timestamp': 1764936187, 'rate': 76.749016},
#                              'date': '2025-12-05',
#                              'result': 630982.057672}

# Если превышен лимит обращений к API, ответ # {"message":"You have exceeded your daily\/monthly API rate limit.
# Please review and upgrade your subscription plan at https:\/\/promptapi.com\/subscriptions to continue."}

# Возвращает функция stock_prices("AAPL")
# {'Global Quote': {'01. symbol': 'AAPL',
#                   '02. open': '258.6600',
#                   '03. high': '258.9500',
#                   '04. low': '254.1800',
#                   '05. price': '255.7600',
#                   '06. volume': '40794020',
#                   '07. latest trading day': '2026-03-12',
#                   '08. previous close': '260.8100',
#                   '09. change': '-5.0500',
#                   '10. change percent': '-1.9363%'}}
