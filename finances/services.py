from datetime import datetime, timedelta

import requests
from django.conf import settings

BASE_URL = 'https://openexchangerates.org/api'

_cached_rates = {
    'rates': None,
    'ts': None,
}


def get_latest_rates():
    """
    Получает словарь курсов валют от Open Exchange Rates.
    Пример структуры:
    {
        "USD": 1,
        "EUR": 0.94,
        "UAH": 40.1,
        ...
    }

    Мы будем использовать это так:
    1 USD = rates['UAH']
    1 USD = rates['EUR']
    и т.д.
    """

    now = datetime.utcnow()

    # если уже есть кеш и он свежий (<30 мин) — используем его
    if (
        _cached_rates['rates'] is not None and
        _cached_rates['ts'] is not None and
        now - _cached_rates['ts'] < timedelta(minutes=30)
    ):
        return _cached_rates['rates']

    app_id = settings.OPENEX_APP_ID
    if not app_id:
        raise RuntimeError('OPENEXCHANGERATES_APP_ID is not set in .env')

    # Запрос к API
    resp = requests.get(
        f'{BASE_URL}/latest.json',
        params={'app_id': app_id}
    )
    resp.raise_for_status()

    data = resp.json()
    rates = data['rates']  # 1 USD = rates['XXX']

    # сохраняем в кеш
    _cached_rates['rates'] = rates
    _cached_rates['ts'] = now

    return rates


def convert_to_uah(amount, currency):
    """
    Конвертирует сумму 'amount' из currency (UAH / USD / EUR)
    в гривны (UAH) и возвращает float с округлением.
    """
    rates = get_latest_rates()

    # Если уже гривны — возвращаем как есть.
    if currency == 'UAH':
        return float(amount)

    # Логика:
    # rates['UAH'] = сколько гривен за 1 USD
    # rates['EUR'] = сколько евро за 1 USD? Нет.
    # Важно: OpenExchangeRates даёт курс в виде:
    # 1 USD = rates['UAH']
    # 1 USD = rates['EUR']
    #
    # Значит:
    #   1 currency = (1 currency / rates[currency]) USD
    #               = (amount / rates[currency]) USD
    #
    # Потом USD -> UAH:
    #   UAH = USD * rates['UAH']

    if currency not in rates:
        raise ValueError(f"Currency {currency} is not in rates")

    amount = float(amount)

    # конвертируем нашу валюту -> USD
    usd_value = amount / float(rates[currency])

    # потом USD -> UAH
    uah_value = usd_value * float(rates['UAH'])

    # округляем до 2 знаков
    return round(uah_value, 2)
