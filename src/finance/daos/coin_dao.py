from finance.models import Coin


class CoinDAO:
    def fetch_all_coins_id(self) -> list[str]:
        return [coin_id for coin_id in Coin.objects.values_list('code', flat=True)]
