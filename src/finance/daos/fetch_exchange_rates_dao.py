from finance.models import ExchangeCurrencyRate, Currency
from finance.sdks.exchange_rate import CurrencyExchangeRateDTO


class FetchExchangeRatesDAO:
    def fetch_currencies_ids(self) -> list[str]:
        return [
            cur
            for cur in Currency.objects.values_list('code', flat=True)
        ]

    def create_exchange_rates__bulk(
        self,
        rates: tuple[CurrencyExchangeRateDTO, ...],
        batch_size: int = 500,
    ) -> None:
        objs: list[ExchangeCurrencyRate] = [
            ExchangeCurrencyRate(
                base_currency_id=i.base_currency,
                target_currency_id=i.target_currency,
                rate=i.rate,
                rate_datetime=i.rate_datetime,
            ) for i in rates
        ]

        ExchangeCurrencyRate.objects.bulk_create(
            objs=objs,
            batch_size=batch_size,
            update_fields=['rate', 'base_currency', 'target_currency', 'updated_at'],
            unique_fields=['base_currency', 'target_currency', 'rate_datetime'],
        )
