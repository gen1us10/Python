from django import forms
from .models import Table, Transaction

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('name', 'color')

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('title', 'amount', 'currency', 'date', 'table', 'categories')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
