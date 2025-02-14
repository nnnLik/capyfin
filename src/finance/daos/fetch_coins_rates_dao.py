from finance.models import ExchangeCoinRate, Coin
from finance.sdks.crypto import CoinPriceDTO


class FetchCoinsRatesDAO:
    def fetch_all_coins(self) -> tuple[str, ...]:
        return tuple(i for i in Coin.objects.values_list('code', flat=True))

    def create_coins_rates__bulk(
        self,
        prices: tuple[CoinPriceDTO, ...],
        batch_size: int = 500,
    ) -> None:
        objs: list[ExchangeCoinRate] = [
            ExchangeCoinRate(
                coin_id=i.code,
                rate=i.price,
                currency_id=i.currency,
                rate_datetime=i.rate_datetime,
            ) for i in prices
        ]

        ExchangeCoinRate.objects.bulk_create(
            objs=objs,
            batch_size=batch_size,
            update_conflicts=True,
            update_fields=['rate', 'currency', 'updated_at'],
            unique_fields=['coin', 'rate_datetime'],
        )
