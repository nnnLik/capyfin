from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Literal

from transaction.daos import TransactionDAO, TransactionDTO


@dataclass
class CreateTransactionService:
    _transaction_dao: TransactionDAO

    @classmethod
    def build(cls) -> 'CreateTransactionService':
        return cls(
            _transaction_dao=TransactionDAO(),
        )

    def execute(
        self,
        user_id: int,
        coin_id: str,
        currency_id: str,
        count: Decimal,
        spent: Decimal,
        cost_for_one: Decimal,
        action: Literal['+', '-'],
        purchased_at: date,
    ) -> None:
        transaction_dto = TransactionDTO(
            user_id=user_id,
            coin_id=coin_id,
            currency_id=currency_id,
            count=count,
            spent=spent,
            cost_for_one=cost_for_one,
            action=action,
            purchased_at=purchased_at,
        )

        self._transaction_dao.create_user_transaction_bulk([transaction_dto,])
