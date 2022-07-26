from datetime import datetime


def datetime_converter(date_time):
    date_time_obj = datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S.%f%z')
    converted_date_time = date_time_obj.strftime("%H:%M %d/%b/%y")

    return converted_date_time


def date_converter(date):
    date_obj = datetime.strptime(str(date), '%Y-%m-%d')
    converted_date = date_obj.strftime("%d/%b/%y")

    return converted_date
