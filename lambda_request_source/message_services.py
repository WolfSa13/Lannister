from orm_services import UsersQuery, TypeBonusesQuery

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


def generate_request_block_list(request_list):
    attachments = []

    for request in request_list:

        payment_date = request['payment_date']
        if not payment_date:
            payment_date = "Wasn't approved yet."

        request_item = {
            "color": "#09ab19",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Request #{request['id']}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Creator:* {request['creator_name']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Reviewer:* {request['reviewer_name']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Bonus type:* {request['bonus_name']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Payment amount:*  {request['payment_amount']}$"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Creation date:* {request['created_at']}\n*Payment date:* {payment_date}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Description:* {request['description']}"
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Changes history"
                            },
                            "action_id": f"request_history_{request['id']}"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Edit"
                            },
                            "action_id": f"request_edit_{request['id']}"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Delete"
                            },
                            "style": "danger",
                            "action_id": f"request_delete_{request['id']}"
                        }
                    ]
                },
            ]
        }
        attachments.append(request_item)

    attachments.append(back_to_request_start_menu_button)

    return attachments


def request_history_string(request_id):
    return {
        "color": "#008000",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"History of request #{request_id}"
                }
            }
        ]
    }


back_to_request_list_button = {
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
                    "action_id": "request_list"
                }
            ]
        }
    ]
}


def generate_request_history_block_list(request_history_list):
    """
    request_history_list = [
            {
                'id': 1,
                'request_id': 1,
                'timestamp': '24-07-2022 14:22',
                'editor_id': 1,
                'editor_name': 'Name',
                'changes': 'abc'
            }
        ]
    """

    attachments = [request_history_string(request_history_list[0]['request_id'])]

    for request_history_event in request_history_list:
        request_history_item = {
            "color": "#09ab19",
            "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Editor:* {request_history_event['editor_name']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*When:* {request_history_event['timestamp']}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Changes:* {request_history_event['changes']}"
                    }
                }
            ]
        }

        attachments.append(request_history_item)

    attachments.append(back_to_request_list_button)

    return attachments


def get_request_by_id(request_id, request_list):
    for request in request_list:
        if request['id'] == int(request_id):
            return request


def request_create_modal():
    reviewer_list = UsersQuery.get_reviewers()

    bonus_list = TypeBonusesQuery.get_bonuses()

    reviewer_options = []
    for reviewer in reviewer_list:
        reviewer_item = {
            "text": {
                "type": "plain_text",
                "text": reviewer['full_name']
            },
            "value": str(reviewer['id'])
        }
        reviewer_options.append(reviewer_item)

    bonus_options = []
    for bonus in bonus_list:
        bonus_item = {
            "text": {
                "type": "plain_text",
                "text": bonus['type']
            },
            "value": str(bonus['id'])
        }
        bonus_options.append(bonus_item)

    return {
        "title": {
            "type": "plain_text",
            "text": "Create bonus request"
        },
        "submit": {
            "type": "plain_text",
            "text": "Create"
        },
        "type": "modal",
        "callback_id": "request_modal_create",
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose reviewer"
                    },
                    "options": reviewer_options,
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Reviewer"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose requested bonus type"
                    },
                    "options": bonus_options,
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Bonus type"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "request_amount_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Payment amount"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "request_description_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Description"
                }
            }
        ]
    }


def request_edit_modal(request):
    reviewer_list = UsersQuery.get_reviewers()
    for reviewer in reviewer_list:
        if reviewer['id'] == request['reviewer']:
            current_reviewer = reviewer
            break

    bonus_list = TypeBonusesQuery.get_bonuses()
    for bonus in bonus_list:
        if bonus['id'] == request['type_bonus']:
            current_bonus = bonus
            break

    reviewer_options = []
    for reviewer in reviewer_list:
        reviewer_item = {
            "text": {
                "type": "plain_text",
                "text": reviewer['full_name']
            },
            "value": str(reviewer['id'])
        }
        reviewer_options.append(reviewer_item)

    bonus_options = []
    for bonus in bonus_list:
        bonus_item = {
            "text": {
                "type": "plain_text",
                "text": bonus['type']
            },
            "value": str(bonus['id'])
        }
        bonus_options.append(bonus_item)

    return {
        "title": {
            "type": "plain_text",
            "text": "Edit bonus request"
        },
        "submit": {
            "type": "plain_text",
            "text": "Save"
        },
        "type": "modal",
        "callback_id": f"request_modal_edit_{request['id']}",
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose reviewer"
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": current_reviewer['full_name']
                        },
                        "value": str(current_reviewer['id'])
                    },
                    "options": reviewer_options,
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Reviewer"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": current_bonus['type']
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": current_bonus['type']
                        },
                        "value": str(current_bonus['id'])
                    },
                    "options": bonus_options,
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Bonus type"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "initial_value": str(request['payment_amount']),
                    "action_id": "request_amount_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Payment amount"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "initial_value": str(request['description']),
                    "multiline": True,
                    "action_id": "request_description_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Description"
                }
            }
        ]
    }
