from django.urls import path

from transaction.views import (
    CreateTransactionAPIView,
    DeleteTransactionAPIView,
)

urlpatterns = [
    path('create-transaction/', CreateTransactionAPIView.as_view(), name='create_transaction'),
    path('transaction/<int:transaction_id>/delete/', DeleteTransactionAPIView.as_view(), name='delete_transaction'),
]
