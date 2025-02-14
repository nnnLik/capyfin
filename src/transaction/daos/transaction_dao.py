from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from transaction.models import Transaction


@dataclass(frozen=True, slots=True)
class TransactionDTO:
    user_id: int
    currency_id: str
    coin_id: str

    purchased_at: date
    count: Decimal
    spent: Decimal
    cost_for_one: Decimal
    action: Literal['+', '-']


@dataclass(frozen=True, slots=True)
class TransactionReadDTO(TransactionDTO):
    id: int

    created_at: datetime
    updated_at: datetime


class TransactionDAO:
    def fetch_user_transactions(self, user_id) -> list[TransactionReadDTO]:
        return [
            TransactionReadDTO(
                id=transaction.id,
                user_id=transaction.user_id,
                currency_id=transaction.currency_id,
                coin_id=transaction.coin_id,
                purchased_at=transaction.purchased_at,
                count=transaction.count,
                spent=transaction.spent,
                cost_for_one=transaction.cost_for_one,
                action=transaction.action,
                created_at=transaction.created_at,
                updated_at=transaction.updated_at
            )
            for transaction in Transaction.objects.filter(user_id=user_id)
        ]

    def create_user_transaction_bulk(
        self,
        transactions_dto: list[TransactionDTO],
        batch_size: int = 100,
    ) -> None:
        obj: list[Transaction] = [
            Transaction(
                user_id=i.user_id,
                currency_id=i.currency_id,
                coin_id=i.coin_id,
                purchased_at=i.purchased_at,
                count=i.count,
                spent=i.spent,
                cost_for_one=i.cost_for_one,
                action=i.action,
            )
            for i in transactions_dto
        ]

        Transaction.objects.bulk_create(
            objs=obj,
            batch_size=batch_size,
        )
