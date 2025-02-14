from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class BaseRateLimitExceededException(Exception):
    msg: str


@dataclass(frozen=True, eq=False)
class BaseUnknownApiException(Exception):
    msg: str


@dataclass(frozen=True, eq=False)
class CoinMarketCapSDKRateLimitExceededException(BaseRateLimitExceededException):
    pass


@dataclass(frozen=True, eq=False)
class CoinMarketCapSDKUnknownApiException(BaseUnknownApiException):
    pass


@dataclass(frozen=True, eq=False)
class FreeCurrencyApiSDKRateLimitExceededException(BaseRateLimitExceededException):
    pass


@dataclass(frozen=True, eq=False)
class FreeCurrencyApiUnknownApiException(BaseUnknownApiException):
    pass
