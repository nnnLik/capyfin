import logging
import random
from dataclasses import dataclass
from typing import ClassVar

from finance.sdks.crypto import (
    BaseCryptoSDK,
    BinanceAPISDK,
    CoinPriceDTO,
)
from finance.sdks.exceptions import BaseRateLimitExceededException, BaseUnknownApiException


@dataclass
class CryptoPriceFetcherSDK(BaseCryptoSDK):
    _logger: ClassVar[logging.Logger] = logging.getLogger('crypto_price_fetcher__sdk')

    SDK_CLASSES: ClassVar[tuple[BaseCryptoSDK, ...]] = (BinanceAPISDK,)

    def get_price(
        self,
        coins: tuple[str, ...],
        time_start: str | None = None,
        time_end: str | None = None,
        interval: str | None = None,
    ) -> tuple[CoinPriceDTO, ...]:
        main_sdk_class: BaseCryptoSDK = random.choice(self.SDK_CLASSES)()

        for _ in range(len(self.SDK_CLASSES)):
            try:
                return tuple(
                    main_sdk_class.get_price(
                        coins=coins,
                        time_start=time_start,
                        time_end=time_end,
                        interval=interval,
                    )
                )
            except BaseRateLimitExceededException as e:
                self._logger.warning(f'{self.__class__.__name__} failed with {e.msg}')
                main_sdk_class = random.choice([sdk for sdk in self.SDK_CLASSES if sdk != main_sdk_class])()
            except BaseUnknownApiException as e:
                self._logger.error(f'{self.__class__.__name__} failed with {e.msg}')

        return tuple()
