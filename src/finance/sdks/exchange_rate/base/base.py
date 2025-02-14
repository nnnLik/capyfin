from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Iterable


@dataclass(frozen=True, slots=True)
class CurrencyExchangeRateDTO:
    base_currency: str
    target_currency: str
    rate: Decimal
    rate_datetime: datetime


@dataclass
class BaseExchangeRateSDK(ABC):
    @abstractmethod
    def get_rate(self, currencies: list[str], target_date: datetime)-> Iterable[CurrencyExchangeRateDTO]:
        pass
