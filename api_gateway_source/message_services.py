import requests
import json


def get_main_menu_blocks():
    workers_action_id = 'worker_start_menu'
    requests_action_id = 'request_start_menu'
    bonuses_action_id = 'bonus_start_menu'

    return [
        {
            "type": "section",
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
                        "text": "Workers"
                    },
                    "action_id": workers_action_id
                },
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


def respond_with_menu(response_url):
    data = {
        'response_type': 'in_channel',
        "blocks": get_main_menu_blocks()
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
