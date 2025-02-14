from dataclasses import dataclass
from typing import cast

from finance.daos import FetchCoinsRatesDAO
from finance.sdks.crypto import CryptoPriceFetcherSDK, CoinPriceDTO


@dataclass
class FetchCoinsRatesService:
    _fetch_coins_rates__dao: FetchCoinsRatesDAO
    _crypto_price_fetcher__sdk: CryptoPriceFetcherSDK

    @classmethod
    def build(cls) -> 'FetchCoinsRatesService':
        return cls(
            _fetch_coins_rates__dao=FetchCoinsRatesDAO(),
            _crypto_price_fetcher__sdk=CryptoPriceFetcherSDK(),
        )

    def execute(
        self,
        time_start: str | None = None,
        time_end: str | None = None,
        interval: str | None = None,
    ) -> None:
        coins = self._fetch_coins_rates__dao.fetch_all_coins()

        coin_prices = self._crypto_price_fetcher__sdk.get_price(
            coins=coins,
            time_start=time_start,
            time_end=time_end,
            interval=interval,
        )

        self._fetch_coins_rates__dao.create_coins_rates__bulk(cast(tuple[CoinPriceDTO, ...], coin_prices))
