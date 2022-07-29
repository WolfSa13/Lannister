import requests
from utils import *


def get_main_menu_blocks(user_slack_id):
    workers_action_id = 'worker_start_menu'
    requests_action_id = 'request_start_menu'
    bonuses_action_id = 'bonus_start_menu'

    function_name = resolve_function_name('worker')

    data = {
        "user_slack_id": user_slack_id,
        "action_id": 'worker_get'
    }

    response = json.load(invoke_request_response_lambda(function_name, data)['Payload'])
    user_roles = response['roles']

    start_menu = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Hi, I'm here. What do you want to do?"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Requests"
                    },
                    "action_id": requests_action_id
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Bonuses"
                    },
                    "action_id": bonuses_action_id
                }
            ]
        }
    ]

    worker_button = {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": "Workers"
        },
        "action_id": workers_action_id
    }

    if 'administrator' in user_roles:
        start_menu[2]['elements'].insert(0, worker_button)

    return start_menu


def respond_with_menu(response_url, user_slack_id):
    data = {
        'response_type': 'in_channel',
        "blocks": get_main_menu_blocks(user_slack_id)
    }

    headers = {
        'Content-type': 'application/json'
    }

    requests.post(response_url, data=json.dumps(data), headers=headers)


def respond_with_error_return_menu(response_url):
    data = {
        'response_type': 'in_channel',
        "text": "Something went wrong. Please try again.",
        "blocks": get_main_menu_blocks()
    }

    headers = {
        'Content-type': 'application/json'
    }

    requests.post(response_url, data=json.dumps(data), headers=headers)
