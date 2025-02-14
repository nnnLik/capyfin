from django.db import models


class Coin(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'
