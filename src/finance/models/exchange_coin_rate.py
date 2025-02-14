from django.db import models


class ExchangeCoinRate(models.Model):
    coin = models.ForeignKey('finance.Coin', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=20, decimal_places=10)
    currency = models.ForeignKey(
        'finance.Currency',
        on_delete=models.CASCADE,
    )
    rate_datetime = models.DateTimeField(auto_now=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('coin', 'rate_datetime')
