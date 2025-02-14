from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Generator, ClassVar

import requests
from rest_framework import status

from config.settings.env import settings
import finance.const
from finance.sdks.exceptions import (
    FreeCurrencyApiUnknownApiException,
    FreeCurrencyApiSDKRateLimitExceededException,
)
from finance.sdks.exchange_rate import BaseExchangeRateSDK, CurrencyExchangeRateDTO


@dataclass
class FreeCurrencyApiSDK(BaseExchangeRateSDK):
    API_URL: ClassVar[str] = 'https://api.freecurrencyapi.com/v1/historical'
    API_KEY: ClassVar[str] = settings.app.FREE_CURRENCY_API_TOKEN

    def _parse_response(
        self,
        base_currency: str,
        response_date: str,
        data: dict,
    ) -> Generator[CurrencyExchangeRateDTO, None, None]:
        for target_currency, rate in data.get('data', {}).get(response_date, {}).items():
            yield CurrencyExchangeRateDTO(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=Decimal(rate),
                rate_datetime=datetime.fromisoformat(response_date),
            )

    def get_rate(
        self,
        currencies: list[str],
        target_date: datetime,
    ) -> Generator[CurrencyExchangeRateDTO, None, None]:
        headers = {'apikey': self.API_KEY}

        currencies = list(set(currencies) - {finance.const.CurrencyEnum.USD})
        if not currencies:
            return

        query_date = target_date.isoformat()

        params = {
            'date': query_date,
            'base_currency': finance.const.CurrencyEnum.USD,
            'currencies': ','.join(currencies),
        }
        response = requests.get(self.API_URL, headers=headers, params=params)
        data = response.json()

        if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            raise FreeCurrencyApiSDKRateLimitExceededException(f'SDK {self.__class__.__name__} API rate limit exceeded')
        elif response.status_code != status.HTTP_200_OK:
            raise FreeCurrencyApiUnknownApiException(f'SDK {self.__class__.__name__} error: {data}')

        yield from self._parse_response(finance.const.CurrencyEnum.USD, query_date, data)
