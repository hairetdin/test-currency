# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse

from currency.models import Currency, Rate


def create_currency(code, name, show_rate=False):
    return Currency.objects.create(code=code, name=name, show_rate=show_rate)

class CurrencyViewTests(TestCase):
    def test_currency_list_view(self):
        """
        If no currency exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('currencies'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no currencies.")
        self.assertQuerysetEqual(response.context['currency_list'], [])

    def test_currency_list_view_with_last_currency(self):
        """
        Currency with show_rate should be displayed
        """
        create_currency(code="BTC", name="Bitcoin", show_rate=True)
        response = self.client.get(reverse('currencies'))
        self.assertQuerysetEqual(
            response.context['currency_list'],
            ['<Currency: BTC>']
        )
