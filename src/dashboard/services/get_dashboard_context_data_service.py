from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal

from core.daos import UserDAO
from finance.daos import CurrencyConverterDAO, ExchangeCoinRateDAO
from transaction.daos import TransactionDAO, TransactionReadDTO


@dataclass(frozen=True, slots=True)
class _MainCurrencyCommonInfoDTO:
    main_currency: str
    total_assets: Decimal
    total_spent: Decimal
    profit_loss: Decimal
    profit_loss_in_perc: Decimal


@dataclass(frozen=True, slots=True)
class DashboardContextDTO:
    main_currency_common_info: _MainCurrencyCommonInfoDTO
    transactions: list[TransactionReadDTO]
    assets_labels: list[str]
    assets_values: list[Decimal]
    spending_labels: list[str]
    spending_values: list[Decimal]
    profit_loss_labels: list[str]
    profit_loss_values: list[Decimal]


@dataclass
class GetDashboardContextDataService:
    _user_dao: UserDAO
    _transaction_dao: TransactionDAO
    _currency_converter_dao: CurrencyConverterDAO
    _exchange_coin_rate_dao: ExchangeCoinRateDAO

    @classmethod
    def build(cls) -> 'GetDashboardContextDataService':
        return cls(
            _user_dao=UserDAO(),
            _transaction_dao=TransactionDAO(),
            _currency_converter_dao=CurrencyConverterDAO(),
            _exchange_coin_rate_dao=ExchangeCoinRateDAO(),
        )

    def _convert_to_main_user_currency(
            self,
            main_user_currency: str,
            transaction_currency: str,
            amount: Decimal,
    ) -> Decimal:
        return self._currency_converter_dao.convert(
            base_currency=main_user_currency,
            target_currency=transaction_currency,
            amount=amount,
        )

    def execute(
            self,
            user_id: int,
    ) -> DashboardContextDTO:
        main_user_currency: str = self._user_dao.get_user_main_currency_by_user_id(user_id)
        user_transactions: list[TransactionReadDTO] = self._transaction_dao.fetch_user_transactions(user_id)

        total_assets: Decimal = Decimal('0')
        total_spent: Decimal = Decimal('0')
        assets_labels: list[str] = []
        assets_values: list[Decimal] = []
        spending_labels: list[str] = []
        spending_values: list[Decimal] = []
        profit_loss_labels: list[str] = []
        profit_loss_values: list[Decimal] = []

        for user_transaction in user_transactions:
            transaction_spent: Decimal = user_transaction.spent
            transaction_count: Decimal = user_transaction.count
            transaction_action: Literal['+', '-'] = user_transaction.action

            if user_transaction.currency_id != main_user_currency:
                transaction_spent = self._convert_to_main_user_currency(
                    main_user_currency=main_user_currency,
                    transaction_currency=user_transaction.currency_id,
                    amount=transaction_spent,
                )

            transaction_coin_rate_to_user_main_currency: Decimal = self._exchange_coin_rate_dao.get_coin_rate(
                coin_code=user_transaction.coin_id,
                currency=main_user_currency,
            )

            asset_value = (
                (transaction_count * transaction_coin_rate_to_user_main_currency)
                .quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP)
            )

            if transaction_action == '+':
                total_assets += asset_value
                total_spent += transaction_spent

                if user_transaction.coin_id not in assets_labels:
                    assets_labels.append(user_transaction.coin_id)
                    assets_values.append(asset_value)
                else:
                    idx = assets_labels.index(user_transaction.coin_id)
                    assets_values[idx] += asset_value

                if user_transaction.coin_id not in spending_labels:
                    spending_labels.append(user_transaction.coin_id)
                    spending_values.append(transaction_spent)
                else:
                    idx = spending_labels.index(user_transaction.coin_id)
                    spending_values[idx] += transaction_spent

            profit_loss_labels.append(str(user_transaction.purchased_at))
            profit_loss_values.append(transaction_spent - asset_value)

        profit_loss: Decimal = total_spent - total_assets
        profit_loss_in_perc: Decimal = (
            (profit_loss / total_spent * 100)
            .quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
        ) if total_spent > 0 else Decimal('0.00')

        return DashboardContextDTO(
            main_currency_common_info=_MainCurrencyCommonInfoDTO(
                main_currency=main_user_currency,
                total_assets=total_assets,
                total_spent=total_spent,
                profit_loss=profit_loss,
                profit_loss_in_perc=profit_loss_in_perc,
            ),
            transactions=user_transactions,
            assets_labels=assets_labels,
            assets_values=assets_values,
            spending_labels=spending_labels,
            spending_values=spending_values,
            profit_loss_labels=profit_loss_labels,
            profit_loss_values=profit_loss_values,
        )
