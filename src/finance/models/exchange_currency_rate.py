from django.db import models


class ExchangeCurrencyRate(models.Model):
    base_currency = models.ForeignKey(
        'finance.Currency',
        on_delete=models.PROTECT,
        related_name='base_currency',
    )
    target_currency = models.ForeignKey(
        'finance.Currency',
        on_delete=models.PROTECT,
        related_name='target_currency',
    )
    rate = models.DecimalField(max_digits=20, decimal_places=10)
    rate_datetime = models.DateTimeField(auto_now=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['base_currency', 'target_currency', 'rate_datetime'],
                name='unique_base_currency_rate_datetime',
            )
        ]

    def __str__(self):
        return f'Rate from {self.base_currency} to {self.target_currency} = {self.rate}'
