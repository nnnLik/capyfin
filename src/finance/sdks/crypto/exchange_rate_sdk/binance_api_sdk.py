from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Generator

import requests
from rest_framework import status

import finance.const
from core.utils import convert_to_timestamp
from finance.sdks.crypto import BaseCryptoSDK, CoinPriceDTO
from finance.sdks.exceptions import (
    CoinMarketCapSDKRateLimitExceededException,
    CoinMarketCapSDKUnknownApiException,
)


@dataclass
class BinanceAPISDK(BaseCryptoSDK):
    LATEST_API_URL: ClassVar[str] = 'https://api.binance.com/api/v3/ticker/price'
    HISTORICAL_API_URL: ClassVar[str] = 'https://api.binance.com/api/v3/klines'

    def _parse_response(
        self,
        coin: str,
        data: dict,
        is_historical: bool = False,
    ) -> Generator[CoinPriceDTO, None, None]:
        if is_historical:
            for candle in data:
                yield CoinPriceDTO(
                    code=coin,
                    price=Decimal(candle[4]),
                    currency=finance.const.CurrencyEnum.USD,
                    rate_datetime=datetime.fromtimestamp(candle[0] / 1000),
                )
        else:
            yield CoinPriceDTO(
                code=coin,
                price=Decimal(data['price']),
                currency=finance.const.CurrencyEnum.USD,
                rate_datetime=datetime.now(),
            )

    def get_price(
        self,
        coins: tuple[str, ...],
        time_start: str | None = None,
        time_end: str | None = None,
        interval: str | None = None,
    ) -> Generator[CoinPriceDTO, None, None]:
        for coin in coins:
            pair = f'{coin}USDT'

            if time_start and time_end and interval:
                start_timestamp = convert_to_timestamp(time_start)
                end_timestamp = convert_to_timestamp(time_end)
                params = {
                    'symbol': pair,
                    'interval': interval,
                    'startTime': start_timestamp,
                    'endTime': end_timestamp,
                    'limit': 100,
                }
                response = requests.get(self.HISTORICAL_API_URL, params=params)
                is_historical = True
            else:
                response = requests.get(self.LATEST_API_URL, params={'symbol': pair})
                is_historical = False

            data = response.json()

            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                raise CoinMarketCapSDKRateLimitExceededException(
                    f'SDK {self.__class__.__name__} API rate limit exceeded'
                )
            elif response.status_code != status.HTTP_200_OK:
                raise CoinMarketCapSDKUnknownApiException(f'SDK {self.__class__.__name__} error: {data}')

            yield from self._parse_response(coin, data, is_historical)
