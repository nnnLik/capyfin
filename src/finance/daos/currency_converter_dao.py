from decimal import Decimal, ROUND_HALF_UP
from functools import lru_cache

from finance.models import ExchangeCurrencyRate


class CurrencyConverterDAO:
    class ExchangeRateDoesNotExist(Exception):
        pass

    def _get_rate(self, base_currency: str, target_currency: str) -> Decimal:
        if base_currency == target_currency:
            return Decimal('1.00')

        if base_currency == "USD":
            try:
                return ExchangeCurrencyRate.objects.filter(
                    base_currency="USD",
                    target_currency=target_currency,
                ).order_by('rate_datetime').last().rate
            except ExchangeCurrencyRate.DoesNotExist:
                raise self.ExchangeRateDoesNotExist

        if target_currency == "USD":
            try:
                return Decimal('1.00') / ExchangeCurrencyRate.objects.filter(
                    base_currency="USD",
                    target_currency=base_currency,
                ).order_by('rate_datetime').last().rate
            except ExchangeCurrencyRate.DoesNotExist:
                raise self.ExchangeRateDoesNotExist

        usd_to_base = self._get_rate("USD", base_currency)
        usd_to_target = self._get_rate("USD", target_currency)

        return usd_to_target / usd_to_base

    @lru_cache
    def convert(
        self,
        base_currency: str,
        target_currency: str,
        amount: Decimal,
    ) -> Decimal:
        rate = self._get_rate(base_currency, target_currency)

        return (amount * rate).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
