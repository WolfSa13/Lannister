request_start_menu = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Requests"
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
                    "text": "Request list"
                },
                "action_id": "request_list"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Create request"
                },
                "action_id": "request_create"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Return to main menu"
                },
                "action_id": "start"
            }
        ]
    }
]

back_to_request_start_menu_button = {
    "color": "#008000",
    "blocks": [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Back"
                    },
                    "action_id": "request_start_menu"
                }
            ]
        }
    ]
}

start_menu = [
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
                "action_id": "worker_start_menu"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Requests"
                },
                "action_id": "request_start_menu"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Bonuses"
                },
                "action_id": "bonus_start_menu"
            }
        ]
    }
]


def request_created_successfully():
    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Request was created successfully"
            }
        }
    ]


def request_edited_successfully():
    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Request was edited successfully"
            }
        }
    ]


def request_deleted_successfully():
    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Request was deleted successfully"
            }
        }
    ]
