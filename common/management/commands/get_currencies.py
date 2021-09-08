import requests
from datetime import datetime
from time import mktime

from django.core.management.base import BaseCommand

from common.models import MonoCurrency, NbuCurrency


CURRENCIES = {'USD': {'iso': 840},
              'EUR': {'iso': 978}
              }
CODES = {c.get('iso'): k for k, c in CURRENCIES.items()}

ADDRESS = {
    'nbu': 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json',
    'mono': 'https://api.monobank.ua/bank/currency'
}


class Command(BaseCommand):

    def handle(self, **options):
        nbu_data, mono_data = {}, {}

        params = {'content-type': 'application/json'}
        nbu_raw = requests.get(ADDRESS['nbu'], params=params).json()
        params['X-Time'] = str(int(mktime(datetime.now().timetuple())))
        mono_raw = requests.get(ADDRESS['mono'], params=params).json()

        for cur in nbu_raw:
            currency = cur.get('cc')
            if currency in CURRENCIES.keys():
                nbu_data.update({currency: cur.get('rate')})

        for cur in mono_raw:
            isocode = cur.get('currencyCodeA', None)
            if all([isocode in CODES.keys(),
                    cur.get('currencyCodeB', None) == 980]):
                mono_data.update({CODES.get(isocode): cur.get('rateBuy')})

        NbuCurrency.objects.create(rate_usd=nbu_data.get('USD', 0),
                                   rate_eur=nbu_data.get('EUR', 0),
                                   )
        MonoCurrency.objects.create(rate_usd=mono_data.get('USD', 0),
                                    rate_eur=mono_data.get('EUR', 0),
                                    )
