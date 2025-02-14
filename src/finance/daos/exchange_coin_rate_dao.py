from dataclasses import dataclass
from decimal import Decimal

import finance.const
from finance.daos import CurrencyConverterDAO
from finance.models import ExchangeCoinRate


@dataclass
class ExchangeCoinRateDAO:
    _currency_converter_dao: CurrencyConverterDAO()

    class CoinRateDoesNotExist(Exception):
        pass

    @classmethod
    def build(cls) -> 'ExchangeCoinRateDAO':
        return cls(
            _currency_converter_dao=CurrencyConverterDAO(),
        )

    def get_coin_rate(self, coin_code: str, currency: str) -> Decimal:
        try:
            usd_rate = (
                ExchangeCoinRate.objects.filter(
                    coin_id=coin_code,
                    currency_id=finance.const.CurrencyEnum.USD,
                )
                .order_by('rate_datetime')
                .last()
                .rate
            )
        except ExchangeCoinRate.DoesNotExist:
            raise self.CoinRateDoesNotExist

        return self._currency_converter_dao.convert(finance.const.CurrencyEnum.USD, currency, usd_rate)
