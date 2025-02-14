from decimal import Decimal

from finance.models import ExchangeCoinRate


class ExchangeCoinRateDAO:
    class CoinRateDoesNotExist(Exception):
        pass

    def get_coin_rate(
        self,
        coin_code: str,
        currency: str,
    ) -> Decimal:
        try:
            return ExchangeCoinRate.objects.filter(
                coin_id=coin_code,
                currency_id=currency,
            ).order_by('rate_datetime').last().rate
        except ExchangeCoinRate.DoesNotExist:
            raise self.CoinRateDoesNotExist