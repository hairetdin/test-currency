# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from . import models
from .forms import CurrencyForm, ConverterForm


class IndexView(generic.TemplateView):
    template_name = "index.html"


class JSONResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        if 'object' in context:
            data = self.object.as_json()
            dump = json.dumps(data)
        if 'object_list' in context:
            data = [ obj.as_json() for obj in self.object_list]
            dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')



class CurrencyListView(JSONResponseMixin, generic.ListView):
    model = models.Currency
    queryset = models.Currency.objects.filter(show_rate=True)
    template_name = 'currency/currency_list.html'

    def render_to_response(self, context):
        if self.request.GET.get('format') == 'json' or self.request.is_ajax():
            return self.render_to_json_response(context)
        else:
            context['json'] = self.render_to_json_response(context)
            return super(CurrencyListView, self).render_to_response(context)


class CurrencyDetailView(JSONResponseMixin, generic.DetailView):
    model = models.Currency
    template_name = 'currency/currency_detail.html'

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json' or self.request.is_ajax():
            return self.render_to_json_response(context)
        else:
            return super(CurrencyDetailView, self).render_to_response(context)


class AjaxExample(generic.TemplateView):
    template_name = "currency/ajax_example.html"
    form = CurrencyForm()

    def render_to_response(self, context):
        context['form'] = self.form
        return super(AjaxExample, self).render_to_response(context)


class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class Converter(generic.TemplateView):
    template_name = "currency/converter.html"
    form = ConverterForm()

    def render_to_response(self, context):
        context['form'] = self.form
        return super(Converter, self).render_to_response(context)

    def post(self,request):
        if request.is_ajax():
            form=ConverterForm(request.POST)
            response_data = {}
            if form.is_valid():
                amount_money = request.POST['amount_money']
                currency1 = request.POST['currency1']
                currency2 = request.POST['currency2']
                rate1=models.Rate.objects.get(currency_id=currency1)
                rate2=models.Rate.objects.get(currency_id=currency2)
                print(rate2)
                response_data['result'] = (Decimal(amount_money)/rate1.rate*rate2.rate).quantize(Decimal('0.01'))
            else:
                response_data['result'] = form.errors
            return JsonResponse(response_data)
