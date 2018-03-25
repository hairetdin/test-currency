# -*- coding: utf-8 -*-
import requests as http_requests


url_api_currencies = 'https://openexchangerates.org/api/currencies.json'
url_api_currencies_val = 'https://openexchangerates.org/api/latest.json'
app_id='18f544e958ef40db99e815d11a33d353'


def get_api_response(api_url, params=None):
    response = http_requests.get(api_url, params=params)
    data = {}
    if response.status_code == 200:
        data = response.json()
    else:
        data['error'] = response
    return data

def get_currencies(api_url=url_api_currencies):
    response=get_api_response(api_url)
    return response

def get_currencies_val(api_url=url_api_currencies_val, params=None, app_id=app_id):
    params = params or {'app_id': app_id, 'symbols': 'CZK,EUR,PLN,USD'}
    response=get_api_response(api_url, params)
    return response


if __name__ == "__main__":
    currencies = get_currencies()
    print('currencies:',currencies)
    currencies_val = get_currencies_val()
    print('currencies_val: ', currencies_val)
