from typing import cast

from django.contrib import messages
from django.http import HttpRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transaction.forms import TransactionForm


class CreateTransactionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        form = TransactionForm(request.POST)
        if not form.is_valid():
            messages.error(cast(HttpRequest, request), 'Error occurred')
            return render(request, 'dashboard/create_transaction.html', {'form': form})

        # Обработка данных формы
        coin_id = form.cleaned_data['coin_id']
        count = form.cleaned_data['count']
        spent = form.cleaned_data['spent']
        action = form.cleaned_data['action']
        user = request.user

        # Создание новой транзакции
        transaction = Transaction.objects.create(
            user=user,
            coin_id=coin_id,
            count=count,
            spent=spent,
            action=action,
            purchased_at=date.today(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        messages.success(request, 'Транзакция успешно добавлена.')
        return redirect('dashboard')  # Перенаправление на дашборд или другую страницу


    return render(request, 'dashboard/create_transaction.html', {'form': form})
