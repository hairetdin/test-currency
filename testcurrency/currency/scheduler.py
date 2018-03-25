# -*- coding: utf-8 -*-
import sys
import os
import django
sys.path.append('..')
os.environ["DJANGO_SETTINGS_MODULE"]= "testcurrency.settings"
django.setup()

import threading
import schedule
import time
import functools

import ext_currency_api

from currency import models
currency_show_list = ['CZK','EUR','PLN','USD']


def catch_exceptions(job_func, cancel_on_failure=True):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            return job_func(*args, **kwargs)
        except:
            import traceback
            print(traceback.format_exc())
            if cancel_on_failure:
                return schedule.CancelJob
    return wrapper

@catch_exceptions
def job():
    currencies = ext_currency_api.get_currencies()
    #print('currencies:',currencies)
    for item in currencies:
        # print(item, currencies[item])
        currency_obj, created = models.Currency.objects.get_or_create(code=item, name=currencies[item])
        if created and item in currency_show_list:
            currency_obj.show_rate = True
            currency_obj.save()
        if created:
            print(currency_obj)
    currencies_val = ext_currency_api.get_currencies_val()
    for item in currencies_val['rates']:
        currency_obj = models.Currency.objects.get(code=item)
        rate_obj, created = models.Rate.objects.get_or_create(currency=currency_obj)
        rate_obj.rate = currencies_val['rates'][item]
        rate_obj.save()
        print(rate_obj)
        #print(item, currencies_val['rates'][item])
    #print('currencies_val: ', currencies_val)

#schedule.every(10).seconds.do(job)
schedule.every().day.at("10:30").do(job)
def run_job():
    while True:
        schedule.run_pending()
        time.sleep(1)

# if __name__ == "__main__":
#     run_job()
