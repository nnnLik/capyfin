from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Iterable


@dataclass(frozen=True, slots=True)
class CoinPriceDTO:
    code: str
    price: Decimal
    currency: str
    rate_datetime: datetime


@dataclass
class BaseCryptoSDK(ABC):
    @abstractmethod
    def get_price(
        self,
        coins: tuple[str, ...],
        time_start: str | None = None,
        time_end: str | None = None,
        interval: str | None = None,
    ) -> Iterable[CoinPriceDTO]:
        pass
