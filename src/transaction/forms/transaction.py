from datetime import date

from django import forms
from decimal import Decimal

import transaction.const

from finance.models import Coin, Currency


class TransactionForm(forms.Form):
    coin_id = forms.ChoiceField(
        choices=[(coin.pk, coin.name) for coin in Coin.objects.all()],
        required=True,
        label="Crypto Coin",
    )
    currency_id = forms.ChoiceField(
        choices=[(currency.pk, currency.name) for currency in Currency.objects.all()],
        required=True,
        label="Currency",
    )
    cost_for_one = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Cost For One",
        required=True,
    )
    count = forms.DecimalField(
        max_digits=10,
        decimal_places=4,
        required=True,
        label="Count",
    )
    spent = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label="Sum",
    )
    action = forms.ChoiceField(
        choices=transaction.const.TRANSACTION_ACTION_CHOICES,
        required=True,
        label="Action",
    )
    purchased_at = forms.DateField(
        label="Purchased Date",
        initial=date.today(),
        required=True,
    )

    def clean_spent(self) -> Decimal:
        spent: Decimal | None = self.cleaned_data.get('spent')
        if spent <= Decimal(0):
            raise forms.ValidationError('Invalid spent value.')

        return spent

    def clean_count(self) -> Decimal:
        count: Decimal | None = self.cleaned_data.get('count')
        if count <= Decimal(0):
            raise forms.ValidationError('Invalid count value.')

        return count

    def clean_purchased_at(self) -> date:
        purchased_at: date | None = self.cleaned_data.get('purchased_at')
        if purchased_at > date.today():
            raise forms.ValidationError('Invalid purchased date.')

        return purchased_at

    def clean_cost_for_one(self) -> Decimal:
        cost_for_one: Decimal | None = self.cleaned_data.get('cost_for_one')
        if cost_for_one <= Decimal(0):
            raise forms.ValidationError('Invalid cost value.')

        return cost_for_one

    def clean(self) -> dict:
        count: Decimal | None = self.cleaned_data.get('count')
        spent: Decimal | None = self.cleaned_data.get('spent')
        cost_for_one: Decimal | None = self.cleaned_data.get('cost_for_one')

        if not count or not spent or not cost_for_one:
            raise forms.ValidationError('Invalid transaction data.')

        if count * cost_for_one != spent:
            raise forms.ValidationError('Cost * cost for one is not equal to spent.')

        return self.cleaned_data
