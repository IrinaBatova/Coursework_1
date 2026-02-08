import json
import os

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
    api_key = os.getenv("API_KEY")

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



if __name__ == "__main__":

    print(currency_conversion("8221.37", "USD"))


# Результат response.json() - {'success': True,
#                              'query': {'from': 'USD', 'to': 'RUB', 'amount': 8221.37},
#                              'info': {'timestamp': 1764936187, 'rate': 76.749016},
#                              'date': '2025-12-05',
#                              'result': 630982.057672}

# Если превышен лимит обращений к API, ответ # {"message":"You have exceeded your daily\/monthly API rate limit.
# Please review and upgrade your subscription plan at https:\/\/promptapi.com\/subscriptions to continue."}
