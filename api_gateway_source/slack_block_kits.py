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
