import requests
from datetime import datetime
from time import mktime

from django.core.management.base import BaseCommand

from common.models import CurrencyStamp


CURRENCIES = {'USD': {'iso': 840},
              'EUR': {'iso': 978}
              }
CODES = {c.get('iso'): k for k, c in CURRENCIES.items()}

ADDRESS = {
    'nbu': 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json',
    'mono': 'https://api.monobank.ua/bank/currency'
}


class Command(BaseCommand):

    def do(self, **kwargs):
        CurrencyStamp.objects.create(**kwargs)

    def handle(self, **options):
        params = {'content-type': 'application/json'}
        nbu_raw = requests.get(ADDRESS['nbu'], params=params).json()
        params['X-Time'] = str(int(mktime(datetime.now().timetuple())))
        mono_raw = requests.get(ADDRESS['mono'], params=params).json()

        for cur in nbu_raw:
            currency = cur.get('cc', '')
            if currency in CURRENCIES.keys():
                self.do(bank='nbu',
                        currency=currency,
                        exchangerate=cur.get('rate'))

        for cur in mono_raw:
            isocode = cur.get('currencyCodeA', None)
            if all([isocode in CODES.keys(),
                    cur.get('currencyCodeB', None) == 980]):
                self.do(bank='mono',
                        currency=CODES.get(isocode, None),
                        exchangerate=cur.get('rateBuy', None))
