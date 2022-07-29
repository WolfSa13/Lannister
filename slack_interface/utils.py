import json
import os
import base64
from urllib.parse import unquote_to_bytes
from datetime import datetime

from requests_function import requests_function
from bonuses_function import bonuses_function
from workers_function import workers_function

BASE_URL = os.environ.get('BASE_URL')


def base64_encoder(body):
    decoded_data = base64.b64decode(body)
    decoded_data = unquote_to_bytes(decoded_data).decode(encoding='utf-8', errors='replace')

    if decoded_data.startswith('token'):
        items_list = list()
        for item in decoded_data.split('&'):
            item = tuple(item.split('='))
            items_list.append(item)
        body = dict(items_list)

        return body

    elif decoded_data.startswith('payload'):
        body = json.loads(decoded_data.split('=', 1)[1])

        return body


def func_to_invoke(function_name):
    if function_name == 'worker':
        function_to_invoke = workers_function

    elif function_name == 'request':
        function_to_invoke = requests_function

    else:
        function_to_invoke = bonuses_function

    return function_to_invoke


# def datetime_converter(date_time):
#     date_time_obj = datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S.%f%z')
#     converted_date_time = date_time_obj.strftime("%H:%M %d/%b/%y")
#
#     return converted_date_time
#
#
# def date_converter(date):
#     date_obj = datetime.strptime(str(date), '%Y-%m-%d')
#     converted_date = date_obj.strftime("%d/%b/%y")
#
#     return converted_date


def logger(data):
    print('--------------------------------------------------------------------')
    print('INFO:')
    print(data)
    print('--------------------------------------------------------------------')
