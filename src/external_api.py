import json
import os
from pprint import pprint

import requests
from dotenv import load_dotenv


def currency_conversion(amount: str, currency: str) -> float:
    """
    Функция для конвертации валюты.
    - param amount: принимает сумму транзакции в виде строки;
    - param currency: принимает тип валюты транзакции в виде строки;
    - return: возвращает сумму транзакции в рублях.
    """

    load_dotenv()
    api_key = os.getenv("API_KEY_APILayer")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
    payload: dict = {}
    headers = {"apikey": f"{api_key}"}

    try:
        response = requests.request("GET", url=url, headers=headers, data=payload)
        result = response.json()  # извлекаем данные из ответа в формате JSON и преобразуем их в Python-словарь (dict)

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


def currency_rate (base: str, symbols: str) -> dict:
    """
    Функция для получения текущего курса валюты.
    - param base: принимает тип валюты в виде строки;
    - param symbols: список разделенных запятыми кодов валют в виде строки
    - return: возвращает курс, заданных валют в рублях в виде словаря, где
    ключ это тип валюты, а значение курс валюты в рублях.
    """

    load_dotenv()
    api_key = os.getenv("API_KEY_APILayer")

    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"

    payload: dict = {}
    headers = {"apikey": f"{api_key}"}

    try:
        response = requests.request("GET", url=url, headers=headers, data=payload)
        result = response.json()  # извлекаем данные из ответа в формате JSON и преобразуем их в Python-словарь (dict)

        if "rates" in result:
            return result["rates"]
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

    return {}

def stock_prices (symbols: str) -> dict:
    """
    Функция для получения стоимости акции.
    - param symbols: принимает тикер акции в виде строки;
    - return: возвращает стоимость акции в виде словаря.
    """

    load_dotenv()
    api_key = os.getenv("API_KEY_Alpha_Vantage")

    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbols}&apikey={api_key}'

    try:
        r = requests.get(url)
        data = r.json()

        return data

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


if __name__ == "__main__":

    # print(currency_conversion("8221.37", "USD"))
    # print(currency_rate("RUB", "USD,EUR,CNY"))
    # print(currency_rate("USD", "RUB"))
    pprint(stock_prices("AAPL"))



# Результат response.json() - {'success': True,
#                              'query': {'from': 'USD', 'to': 'RUB', 'amount': 8221.37},
#                              'info': {'timestamp': 1764936187, 'rate': 76.749016},
#                              'date': '2025-12-05',
#                              'result': 630982.057672}

# Если превышен лимит обращений к API, ответ # {"message":"You have exceeded your daily\/monthly API rate limit.
# Please review and upgrade your subscription plan at https:\/\/promptapi.com\/subscriptions to continue."}
