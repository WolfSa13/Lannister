import json
import requests
import os

from message_services import *
from orm_services import RequestQuery

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')


def lambda_handler(event, context):
    requests_payment = RequestQuery.get_requests_by_payment_date()

    response_url = 'https://slack.com/api/chat.postMessage'

    headers = {
        'Content-type': 'application/json',
        "Authorization": "Bearer " + SLACK_BOT_TOKEN
    }

    for key, value in requests_payment.items():
        attachments = generate_notification_payment_day(value)

        data = {
            "token": SLACK_BOT_TOKEN,
            "channel": key,
            "attachments": attachments
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)
