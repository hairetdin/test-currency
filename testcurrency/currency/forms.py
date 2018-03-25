# -*- coding: utf-8 -*-

from decimal import Decimal
from django import forms
from .models import Currency


class CurrencyForm(forms.Form):
    currency = forms.ModelChoiceField(queryset=Currency.objects.filter(show_rate=True))


class ConverterForm(forms.Form):
    amount_money =forms.DecimalField(max_digits=16, decimal_places=2, initial=Decimal('5.00'), required=True)
    currency1 = forms.ModelChoiceField(label='From', queryset=Currency.objects.filter(show_rate=True), initial=Currency.objects.first())
    currency2 = forms.ModelChoiceField(label='To',queryset=Currency.objects.filter(show_rate=True), initial=Currency.objects.first())
