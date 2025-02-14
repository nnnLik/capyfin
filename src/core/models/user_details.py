from django.db import models
from django.conf import settings

import finance.const


class UserDetails(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='user_details',
    )
    currency = models.ForeignKey(
        'finance.Currency',
        default=finance.const.CurrencyEnum.USD,
        on_delete=models.PROTECT,
    )
