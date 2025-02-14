from dataclasses import dataclass
from datetime import date

from finance.daos import FetchExchangeRatesDAO
from finance.sdks.exchange_rate import ExchangeRateFetcherSDK


@dataclass
class FetchExchangeRatesService:
    _fetch_exchange_rates__dao: FetchExchangeRatesDAO
    _exchange_rate_fetcher__sdk: ExchangeRateFetcherSDK

    @classmethod
    def build(cls) -> 'FetchExchangeRatesService':
        return cls(
            _fetch_exchange_rates__dao=FetchExchangeRatesDAO(),
            _exchange_rate_fetcher__sdk=ExchangeRateFetcherSDK(),
        )

    def execute(self, target_date: date = date.today()) -> None:
        currencies_ids: list[str] = self._fetch_exchange_rates__dao.fetch_currencies_ids()

        coin_prices = self._exchange_rate_fetcher__sdk.get_rate(currencies_ids, target_date)
        self._fetch_exchange_rates__dao.create_exchange_rates__bulk(coin_prices)
