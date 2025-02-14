from django.db import models
from django.conf import settings


# TODO: nahyi?
class UserTrackedCoin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coin = models.ForeignKey('finance.Coin', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'coin')

    def __str__(self):
        return f'{self.user} tracks {self.coin.name} ({self.coin.code})'
