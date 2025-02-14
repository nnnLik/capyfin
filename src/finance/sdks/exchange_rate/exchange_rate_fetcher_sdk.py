import logging
import random
from dataclasses import dataclass
from datetime import date
from typing import ClassVar

from finance.sdks.exchange_rate import (
    BaseExchangeRateSDK,
    FreeCurrencyApiSDK,
    CurrencyExchangeRateDTO,
)
from finance.sdks.exceptions import BaseRateLimitExceededException, BaseUnknownApiException


@dataclass
class ExchangeRateFetcherSDK(BaseExchangeRateSDK):
    _logger: ClassVar[logging.Logger] = logging.getLogger('exchange_rate_fetcher__sdk')

    SDK_CLASSES: ClassVar[tuple[BaseExchangeRateSDK, ...]] = (FreeCurrencyApiSDK,)

    def get_rate(
        self,
        currencies: list[str],
        target_date: date,
    ) -> tuple[CurrencyExchangeRateDTO, ...]:
        main_sdk_class: BaseExchangeRateSDK = random.choice(self.SDK_CLASSES)()

        for _ in range(len(self.SDK_CLASSES)):
            try:
                return tuple(main_sdk_class.get_rate(currencies, target_date))
            except BaseRateLimitExceededException as e:
                self._logger.warning(f'{self.__class__.__name__} failed with {e.msg}')
                main_sdk_class = random.choice([sdk for sdk in self.SDK_CLASSES if sdk != main_sdk_class])()
            except BaseUnknownApiException as e:
                self._logger.error(f'{self.__class__.__name__} failed with {e.msg}')

        return tuple()
