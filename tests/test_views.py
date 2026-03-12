import pytest
import unittest
from unittest.mock import patch, Mock
import json
from unittest import TestCase
from unittest.mock import patch, MagicMock
from src.views import main_page
from src.utils import get_greeting, get_time_period, get_data_card, get_top_transactions, get_currency_rates, get_stock_prices


# Тестирование функции main_page

@patch('src.views.get_greeting', return_value="Добрый вечер")
@patch('src.views.get_data_card', return_value=[{"last_digits": "5814", "total_spent": 1262.00, "cashback": 12.62},
                                                {"last_digits": "7512", "total_spent": 7.94, "cashback": 0.08}])
@patch('src.views.get_top_transactions', return_value=[
    {'amount': 22200.0, 'category': 'Зарплата', 'date': '01.10.2019',
     'description': 'Пополнение. ООО "ФОРТУНА". Зарплата'},
    {'amount': 2511.0, 'category': 'Переводы', 'date': '01.10.2019', 'description': 'Пополнение счета'},
    {'amount': -32.0, 'category': 'Фастфуд', 'date': '30.09.2019', 'description': 'Beijingshoudujichangca'},
    {'amount': 13.67, 'category': 'Переводы', 'date': '01.10.2019', 'description': 'Перевод между счетами'},
    {'amount': -93.0, 'category': 'Переводы', 'date': '01.10.2019', 'description': 'Алексей В.'}])
@patch('src.views.get_currency_rates',
       return_value=[{'currency': 'USD', 'rate': 79.52}, {'currency': 'EUR', 'rate': 79.52},
                     {'currency': 'CNY', 'rate': 79.52}])
@patch('src.views.get_stock_prices',
       return_value=[{'price': 260.83, 'stock': 'AAPL'}, {'price': 260.83, 'stock': 'AMZN'},
                     {'price': 260.83, 'stock': 'GOOGL'}, {'price': 260.83, 'stock': 'MSFT'},
                     {'price': 260.83, 'stock': 'TSLA'}])
def test_main_page(mock_get_stock_prices, mock_get_currency_rates, mock_get_top_transactions, mock_get_data_card,
                   mock_get_greeting):

    # Создаем объект Mock, который будет возвращать "Добрый вечер", когда мы его вызываем.
    mock_get_greeting.return_value = "Добрый вечер"

    # Создаем объект Mock, который будет возвращать список словарей, когда мы его вызываем.
    mock_get_data_card.return_value=[{"last_digits": "5814",
                                             "total_spent": 1262.00,
                                             "cashback": 12.62},
                                            {"last_digits": "7512",
                                             "total_spent": 7.94,
                                             "cashback": 0.08}
                                            ]

    # Создаем объект Mock, который будет возвращать список словарей, когда мы его вызываем.
    mock_get_top_transactions.return_value=[{'amount': 22200.0,
                                                    'category': 'Зарплата',
                                                    'date': '01.10.2019',
                                                    'description': 'Пополнение. ООО "ФОРТУНА". Зарплата'},
                                                   {'amount': 2511.0,
                                                    'category': 'Переводы',
                                                    'date': '01.10.2019',
                                                    'description': 'Пополнение счета'},
                                                   {'amount': -32.0,
                                                    'category': 'Фастфуд',
                                                    'date': '30.09.2019',
                                                    'description': 'Beijingshoudujichangca'},
                                                   {'amount': 13.67,
                                                    'category': 'Переводы',
                                                    'date': '01.10.2019',
                                                    'description': 'Перевод между счетами'},
                                                   {'amount': -93.0,
                                                    'category': 'Переводы',
                                                    'date': '01.10.2019',
                                                    'description': 'Алексей В.'}
                                                   ]

    # Создаем объект Mock, который будет возвращать список словарей, когда мы его вызываем.
    mock_get_currency_rates.return_value=[{'currency': 'USD', 'rate': 79.52},
                                                 {'currency': 'EUR', 'rate': 79.52},
                                                 {'currency': 'CNY', 'rate': 79.52}
                                                 ]

    # Создаем объект Mock, который будет возвращать "Добрый вечер", когда мы его вызываем.
    mock_get_stock_prices.return_value=[{'price': 260.83, 'stock': 'AAPL'},
                                               {'price': 260.83, 'stock': 'AMZN'},
                                               {'price': 260.83, 'stock': 'GOOGL'},
                                               {'price': 260.83, 'stock': 'MSFT'},
                                               {'price': 260.83, 'stock': 'TSLA'}]

    assert main_page("2018-01-01 07:57:29") == {
        'cards': [{'cashback': 12.62, 'last_digits': '5814', 'total_spent': 1262.0},
                  {'cashback': 0.08, 'last_digits': '7512', 'total_spent': 7.94}],
        'currency_rates': [{'currency': 'USD', 'rate': 79.52},
                           {'currency': 'EUR', 'rate': 79.52},
                           {'currency': 'CNY', 'rate': 79.52}],
        'greeting': 'Добрый вечер',
        'stock_prices': [{'price': 260.83, 'stock': 'AAPL'},
                         {'price': 260.83, 'stock': 'AMZN'},
                         {'price': 260.83, 'stock': 'GOOGL'},
                         {'price': 260.83, 'stock': 'MSFT'},
                         {'price': 260.83, 'stock': 'TSLA'}],
        'top_transactions': [{'amount': 22200.0,
                              'category': 'Зарплата',
                              'date': '01.10.2019',
                              'description': 'Пополнение. ООО "ФОРТУНА". Зарплата'},
                             {'amount': 2511.0,
                              'category': 'Переводы',
                              'date': '01.10.2019',
                              'description': 'Пополнение счета'},
                             {'amount': -32.0,
                              'category': 'Фастфуд',
                              'date': '30.09.2019',
                              'description': 'Beijingshoudujichangca'},
                             {'amount': 13.67,
                              'category': 'Переводы',
                              'date': '01.10.2019',
                              'description': 'Перевод между счетами'},
                             {'amount': -93.0,
                              'category': 'Переводы',
                              'date': '01.10.2019',
                              'description': 'Алексей В.'}]}

    # Проверяем, что каждый Mock объект был вызван хотя бы один раз
    mock_get_greeting.assert_called()
    mock_get_data_card.assert_called()
    mock_get_top_transactions.assert_called()
    mock_get_currency_rates.assert_called()
    mock_get_stock_prices.assert_called()



if __name__ == "__main__":
    unittest.main()
