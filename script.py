import logging
import argparse
import time
from typing import Dict, Tuple, List, Union

from tornado.httpclient import HTTPClient, HTTPError
from tornado.escape import json_decode
from tabulate import tabulate


TABULATE_HEADERS = ('Time', 'Buy', 'Sell',)


def setup_logger():
    log = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler()
    log.addHandler(stream_handler)


class TornadoHttpClientMixin:
    def __init__(self):
        self.http_client = HTTPClient()

    @property
    def url(self) -> str:
        raise NotImplementedError('Please specify `url`')

    def fetch_data(self) -> Dict[str, List]:
        try:
            response = self.http_client.fetch(self.url.format(time.time()))
        except HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            logging.getLogger(__name__).error('HTTPError: ' + str(e))
        except Exception as e:
            logging.getLogger(__name__).error('Error: ' + str(e))
        else:
            return json_decode(response.body)

    def close_http_client(self):
        self.http_client.close()


class CurrencyMixin:
    currency_name = None

    @property
    def available_currencies(self) -> Tuple[str]:
        raise NotImplementedError('Please specify `available_currencies` in proper order')


class RbcClient(TornadoHttpClientMixin, CurrencyMixin):
    url = 'https://www.rbc.ru/ajax/indicators?_={}'
    available_currencies = ('USD', 'EUR',)

    def get_currency_data(self) -> Union[List[List[str]], None]:
        data = self.fetch_data()
        cash_index = self.available_currencies.index(self.currency_name)
        cash_data = data['cash'][cash_index]
        return [[cash_data['date'], cash_data['value1'], cash_data['value2']]]


if __name__ == '__main__':
    setup_logger()
    rbc_client = RbcClient()
    parser = argparse.ArgumentParser()
    parser.add_argument("currency", help="desired currency name", type=str, choices=rbc_client.available_currencies)
    args = parser.parse_args()
    rbc_client.currency_name = args.currency
    tabulate_data = rbc_client.get_currency_data()
    print(tabulate(tabulate_data, TABULATE_HEADERS, tablefmt='grid'))
    rbc_client.close_http_client()
