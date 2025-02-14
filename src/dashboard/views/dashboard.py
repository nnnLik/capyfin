from django.contrib.auth.base_user import AbstractBaseUser

from dashboard.services import GetDashboardContextDataService
from dashboard.views import BaseTemplateView
from transaction.forms import TransactionForm


class DashboardTemplateView(BaseTemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        user: AbstractBaseUser = self.request.user
        service: GetDashboardContextDataService = GetDashboardContextDataService.build()

        context_dto = service.execute(user.id)

        return {
            'total_spent': str(context_dto.main_currency_common_info.total_spent),
            'total_assets': str(context_dto.main_currency_common_info.total_assets),
            'profit_loss': str(context_dto.main_currency_common_info.profit_loss),
            'profit_loss_in_perc': str(context_dto.main_currency_common_info.profit_loss_in_perc),
            'transactions': context_dto.transactions,
            'assets_labels': context_dto.assets_labels,
            'assets_values': [str(value) for value in context_dto.assets_values],
            'spending_labels': context_dto.spending_labels,
            'spending_values': [str(value) for value in context_dto.spending_values],
            'profit_loss_labels': context_dto.profit_loss_labels,
            'profit_loss_values': [str(value) for value in context_dto.profit_loss_values],
            'coins': context_dto.coins,
            'form': TransactionForm(),
        }
