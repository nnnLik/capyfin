from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transaction.forms import TransactionForm
from transaction.services import CreateTransactionService


class CreateTransactionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        form = TransactionForm(request.data)
        if not form.is_valid():
            return Response({'success': False, 'error': form.errors}, status=400)

        service = CreateTransactionService.build()
        service.execute(
            user_id=self.request.user.id,
            coin_id=form.cleaned_data['coin_id'],
            count=form.cleaned_data['count'],
            spent=form.cleaned_data['spent'],
            action=form.cleaned_data['action'],
            cost_for_one=form.cleaned_data['cost_for_one'],
            purchased_at=form.cleaned_data['purchased_at'],
        )
        return Response({'success': True})
