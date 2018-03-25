# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal as D

from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    show_rate = models.BooleanField(default=False)

    def __unicode__(self):
        return u'{}'.format(self.code)

    def as_json(self):
        rate = None
        if self.rate_set.first():
            rate = str(self.rate_set.first().rate)
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "rate": rate
        }


class Rate(models.Model):
    currency = models.ForeignKey(Currency)
    rate = models.DecimalField(decimal_places=6, max_digits=16, default=D('0.000000'))
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{} {}'.format(self.currency.code, self.rate)

    def as_json(self):
        return {
            "id": self.id,
            "currency": self.currency.code,
            "currency_name": self.currency.name,
            "rate": self.rate,
            "date_updated": self.date_updated
        }
