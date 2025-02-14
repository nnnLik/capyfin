from typing import Literal

from django.conf import settings
from django.db import models

import finance.const
import transaction.const


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(
        'finance.Currency',
        default=finance.const.CurrencyEnum.USD,
        on_delete=models.PROTECT,
    )
    coin = models.ForeignKey('finance.Coin', on_delete=models.PROTECT)

    purchased_at = models.DateField()
    count = models.DecimalField(max_digits=20, decimal_places=10)
    spent = models.DecimalField(max_digits=15, decimal_places=2)
    cost_for_one = models.DecimalField(max_digits=15, decimal_places=6)
    action: Literal['+', '-'] = models.CharField(max_length=1, choices=transaction.const.TRANSACTION_ACTION_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.purchased_at} | {self.coin} ({self.action}) - {self.count} coins'
