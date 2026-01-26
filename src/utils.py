from datetime import datetime
from pprint import pprint


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


if __name__ == "__main__":
    data_user = "2026-03-18 12:57:29"
    # print(get_date(data_user))
    print(get_time_period(data_user))
    pprint(get_greeting(data_user))



# def get_time_for_greeting(date_string): #=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
#     user_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S") # возвращает 2026-01-18 15:57:29.084879
#     user_hour = user_datetime.hour
#     if 6 <= user_hour < 12:
#         return "Доброе утро"
#     elif 12 <= user_hour <= 18:
#         return "Добрый день"
#     elif 18 <= user_hour <= 23:
#         return "Добрый вечер"
#     else:
#         return "Доброй ночи"