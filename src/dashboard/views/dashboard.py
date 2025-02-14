from dataclasses import asdict
from datetime import date
from decimal import Decimal
from typing import Literal

from django.contrib import messages
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest, HttpResponse

from dashboard.services import GetDashboardContextDataService
from dashboard.views import BaseTemplateView
from transaction.forms import TransactionForm
from transaction.services import CreateTransactionService


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
            'form': TransactionForm(),
        }

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        user: AbstractBaseUser = request.user
        form = TransactionForm(request.POST)
        service = CreateTransactionService.build()

        if not form.is_valid():
            messages.error(request, 'Error during transaction creation.')
            return self.get(request, *args, **kwargs)

        coin_id: str = form.cleaned_data['coin_id']
        currency_id: str = form.cleaned_data['currency_id']
        count: Decimal = form.cleaned_data['count']
        spent: Decimal = form.cleaned_data['spent']
        cost_for_one: Decimal = form.cleaned_data['cost_for_one']
        action: Literal['+', '-'] = form.cleaned_data['action']
        purchased_at: date = form.cleaned_data['purchased_at']

        service.execute(
            user.id,
            coin_id=coin_id,
            currency_id=currency_id,
            count=count,
            spent=spent,
            cost_for_one=cost_for_one,
            action=action,
            purchased_at=purchased_at,
        )

        messages.success(request, 'Transaction has been created.')
        return self.get(request, *args, **kwargs)
