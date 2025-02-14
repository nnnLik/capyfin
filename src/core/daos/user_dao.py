from core.models import UserDetails


class UserDAO:
    def get_user_main_currency_by_user_id(self, user_id) -> str:
        details, _ = UserDetails.objects.get_or_create(user_id=user_id)
        return details.currency_id
