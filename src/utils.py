from datetime import datetime
from pprint import pprint


def get_time_for_greeting(date_string: str) -> str:
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




if __name__ == "__main__":
    data_user = "2026-01-18 12:57:29"
    pprint(get_time_for_greeting(data_user))



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