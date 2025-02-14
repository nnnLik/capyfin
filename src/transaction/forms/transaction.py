from datetime import date
from decimal import Decimal

from django import forms

from transaction.const import TRANSACTION_ACTION_CHOICES
from transaction.models import Transaction
from finance.models import Coin


class TransactionForm(forms.ModelForm):
    coin_id = forms.ChoiceField(
        choices=[(coin.pk, coin.name) for coin in Coin.objects.all()],
        required=True,
        label='Crypto Coin',
    )
    cost_for_one = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Cost For One',
        required=True,
    )
    count = forms.DecimalField(
        max_digits=10,
        decimal_places=4,
        required=True,
        label='Count',
    )
    spent = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label='Sum',
    )
    action = forms.ChoiceField(
        choices=TRANSACTION_ACTION_CHOICES,
        required=True,
        label='Action',
    )
    purchased_at = forms.DateField(
        label='Purchased Date',
        initial=date.today,
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Transaction
        fields = ['purchased_at', 'coin', 'count', 'spent', 'cost_for_one', 'action']

    def clean_spent(self) -> Decimal:
        spent: Decimal | None = self.cleaned_data.get('spent')
        if not spent and spent <= Decimal(0):
            raise forms.ValidationError('Invalid spent value.')
        return spent

    def clean_count(self) -> Decimal:
        count: Decimal | None = self.cleaned_data.get('count')
        if not count and count <= Decimal(0):
            raise forms.ValidationError('Invalid count value.')
        return count

    def clean_purchased_at(self) -> date:
        purchased_at: date = self.cleaned_data.get('purchased_at')
        if purchased_at and purchased_at > date.today():
            raise forms.ValidationError('Invalid purchased date.')
        return purchased_at

    def clean_cost_for_one(self) -> Decimal:
        cost_for_one: Decimal | None = self.cleaned_data.get('cost_for_one')
        if not cost_for_one and cost_for_one <= Decimal(0):
            raise forms.ValidationError('Invalid cost value.')
        return cost_for_one

    def clean(self) -> dict:
        cleaned_data = super().clean()
        count = cleaned_data.get('count')
        spent = cleaned_data.get('spent')
        cost_for_one = cleaned_data.get('cost_for_one')

        if count and spent and cost_for_one:
            if count * cost_for_one != spent:
                raise forms.ValidationError('Count * Cost For One must equal Spent.')

        return cleaned_data
