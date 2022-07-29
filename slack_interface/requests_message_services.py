from datetime import date, datetime

from workers_orm_services import UsersQuery
from bonuses_orm_services import TypeBonusesQuery
# from utils import datetime_converter, date_converter


def datetime_converter(date_time):
    date_time_obj = datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S.%f%z')
    converted_date_time = date_time_obj.strftime("%H:%M %d/%b/%y")

    return converted_date_time


def date_converter(date):
    date_obj = datetime.strptime(str(date), '%Y-%m-%d')
    converted_date = date_obj.strftime("%d/%b/%y")

    return converted_date

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

worker_request_list_menu = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Requests list"
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
                    "text": "Pending and unpaid yet"
                },
                "action_id": "request_list_worker_pending_unpaid_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Paid and denied"
                },
                "action_id": "request_list_worker_approved_denied_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Deleted"
                },
                "action_id": "request_list_worker_deleted_requests"
            },
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

request_list_reviewer_menu = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Requests list"
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
                    "text": "My requests"
                },
                "action_id": "request_list_reviewer_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Requests to review"
                },
                "action_id": "request_list_reviewer_to_review"
            },
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

request_list_reviewer_requests = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Requests list"
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
                    "text": "Pending and unpaid yet"
                },
                "action_id": "request_list_worker_pending_unpaid_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Paid and denied"
                },
                "action_id": "request_list_worker_approved_denied_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Deleted"
                },
                "action_id": "request_list_worker_deleted_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Back"
                },
                "action_id": "request_list_reviewer_menu"
            }
        ]
    }
]

request_list_administrator_menu = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Requests list"
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
                    "text": "My requests"
                },
                "action_id": "request_list_reviewer_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Requests to review"
                },
                "action_id": "request_list_reviewer_to_review"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "All requests"
                },
                "action_id": "request_list_administrator_all_requests"
            },
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

request_list_administrator_requests = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Requests list"
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
                    "text": "Pending and unpaid yet"
                },
                "action_id": "request_list_worker_pending_unpaid_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Paid and denied"
                },
                "action_id": "request_list_worker_approved_denied_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Deleted"
                },
                "action_id": "request_list_worker_deleted_requests"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Back"
                },
                "action_id": "request_list_administrator_menu"
            }
        ]
    }
]

request_list_administrator_all_requests = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "All requests"
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
                    "text": "Pending"
                },
                "action_id": "request_list_administrator_all_requests_pending"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Not paid"
                },
                "action_id": "request_list_administrator_all_requests_unpaid"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Paid"
                },
                "action_id": "request_list_administrator_all_requests_paid"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Denied"
                },
                "action_id": "request_list_administrator_all_requests_denied"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Deleted"
                },
                "action_id": "request_list_administrator_all_requests_deleted"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Back"
                },
                "action_id": "request_list_administrator_menu"
            }
        ]
    }
]

back_to_request_start_menu_button = {
    "type": "button",
    "text": {
        "type": "plain_text",
        "text": "Back"
    },
    "action_id": "request_list"
}

update_request_list_worker_pending_unpaid_requests_button = {
    "type": "button",
    "text": {
        "type": "plain_text",
        "text": "Update"
    },
    "action_id": "request_list_worker_pending_unpaid_requests"
}

back_to_request_list_reviewer_menu = {
    "type": "button",
    "text": {
        "type": "plain_text",
        "text": "Back"
    },
    "action_id": 'request_list_reviewer_menu'
}

update_request_list_reviewer_to_review_button = {
    "type": "button",
    "text": {
        "type": "plain_text",
        "text": "Update"
    },
    "action_id": 'request_list_reviewer_to_review'
}

back_to_request_list_reviewers_requests = {
    "type": "button",
    "text": {
        "type": "plain_text",
        "text": "Back"
    },
    "action_id": 'request_list_reviewer_requests'
}

back_to_request_list_administrator_menu = {
    "type": "button",
    "text": {
        "type": "plain_text",
        "text": "Back"
    },
    "action_id": 'request_list_administrator_menu'
}

back_to_request_list_administrator_all_requests = {
    "type": "button",
    "text": {
        "type": "plain_text",
        "text": "Back"
    },
    "action_id": 'request_list_administrator_all_requests'
}


def update_request_list_administrator_all_requests_button(query_name):
    action_id = 'request_list_administrator_all_requests_' + query_name
    return {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": "Update"
        },
        "action_id": action_id
    }


request_list_buttons = {
    "color": "#008000",
    "blocks": [
        {
            "type": "actions",
            "elements": []
        }
    ]
}


def generate_request_block_list(request_list, user, action_id):
    attachments = []

    for request in request_list:
        approve_button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Approve"
            },
            "style": "primary",
            "action_id": f"request_status_approve_{request['id']}"
        }

        deny_button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Deny"
            },
            "style": "danger",
            "action_id": f"request_status_deny_{request['id']}"
        }

        delete_button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Delete"
            },
            "style": "danger",
            "action_id": f"request_delete_{request['id']}"
        }

        request_item = {
            "color": "#09ab19",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Request #{request['id']} " + request['status']
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
                            "text": f"*Creation date:* {datetime_converter(request['created_at'])}\n"
                                    f"*Payment date:* {date_converter(request['payment_date'])}"
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
                        }
                    ]
                }
            ]
        }

        if request['status'] == 'created':
            request_item['blocks'][-1]['elements'].append(
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Edit"
                    },
                    "action_id": f"request_edit_{request['id']}"
                }
            )

        if action_id == 'request_list_worker_pending_unpaid_requests':
            request_item['blocks'][4]['elements'].append(delete_button)
        elif action_id == 'request_list_reviewer_to_review':
            request_item['blocks'][4]['elements'].append(approve_button)
            request_item['blocks'][4]['elements'].append(deny_button)
        elif action_id.startswith('request_list_administrator_all_requests'):
            query_name = action_id.split('_')[5]
            if query_name in ['pending', 'unpaid']:
                request_item['blocks'][4]['elements'].append(approve_button)
                request_item['blocks'][4]['elements'].append(deny_button)

        attachments.append(request_item)

    attachments.append(
        {
            "color": "#008000",
            "blocks": [
                {
                    "type": "actions",
                    "elements": []
                }
            ]
        }
    )

    if 'administrator' in user['roles']:
        if action_id.startswith('request_list_worker'):
            if action_id == 'request_list_worker_pending_unpaid_requests':
                update_button = update_request_list_worker_pending_unpaid_requests_button
                attachments[-1]['blocks'][0]['elements'].append(update_button)

            attachments[-1]['blocks'][0]['elements'].append(back_to_request_list_reviewers_requests)

        elif action_id == 'request_list_reviewer_to_review':
            update_button = update_request_list_reviewer_to_review_button
            attachments[-1]['blocks'][0]['elements'].append(update_button)

            attachments[-1]['blocks'][0]['elements'].append(back_to_request_list_administrator_menu)

        elif action_id.startswith('request_list_administrator_all_requests_'):
            query_name = action_id.split('_')[5]
            if query_name in ['pending', 'unpaid']:
                update_button = update_request_list_administrator_all_requests_button(query_name)
                attachments[-1]['blocks'][0]['elements'].append(update_button)

            attachments[-1]['blocks'][0]['elements'].append(back_to_request_list_administrator_all_requests)

    elif 'reviewer' in user['roles']:
        if action_id.startswith('request_list_worker'):
            if action_id == 'request_list_worker_pending_unpaid_requests':
                update_button = update_request_list_worker_pending_unpaid_requests_button
                attachments[-1]['blocks'][0]['elements'].append(update_button)

            attachments[-1]['blocks'][0]['elements'].append(back_to_request_list_reviewers_requests)

        elif action_id == 'request_list_reviewer_to_review':
            update_button = update_request_list_reviewer_to_review_button
            attachments[-1]['blocks'][0]['elements'].append(update_button)

            attachments[-1]['blocks'][0]['elements'].append(back_to_request_list_reviewer_menu)
    else:
        if action_id.startswith('request_list_worker'):
            if action_id == 'request_list_worker_pending_unpaid_requests':
                update_button = update_request_list_worker_pending_unpaid_requests_button
                attachments[-1]['blocks'][0]['elements'].append(update_button)

            attachments[-1]['blocks'][0]['elements'].append(back_to_request_start_menu_button)

    print(attachments)
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
                    "action_id": "request_message_delete"
                }
            ]
        }
    ]
}


def generate_request_history_block_list(request_history_list):
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
                            "text": f"*Editor:* {request_history_event['editor']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*When:* {datetime_converter(request_history_event['timestamp'])}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Changes:*\n{request_history_event['changes']}"
                    }
                }
            ]
        }

        attachments.append(request_history_item)

    attachments.append(back_to_request_list_button)

    return attachments


def request_created_successfully_reviewer(creator_name):
    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": f"{creator_name} created a request, and set You as a reviewer."
            }
        }
    ]


def request_created_successfully_modal(request_id):
    return {
        "title": {
            "type": "plain_text",
            "text": "Success"
        },
        "type": "modal",
        "close": {
            "type": "plain_text",
            "text": "Close"
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f'Request #{request_id} was created successfully.'
                }
            }
        ]
    }


def request_edited_successfully_modal(request_id):
    return {
        "title": {
            "type": "plain_text",
            "text": "Success"
        },
        "type": "modal",
        "close": {
            "type": "plain_text",
            "text": "Close"
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f'Request #{request_id} was edited successfully.'
                }
            }
        ]
    }


def request_change_successfully(request_id):
    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": f"Request #{request_id} was changed."
            }
        }
    ]


def request_status_changed_successfully(request_id, data):
    if data['status'] == 'approved':
        text = f'Congratulations, Your request #{request_id} was approved!'
    else:
        text = f'Unfortunately, Your request #{request_id} was denied.'

    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": text
            }
        }
    ]


def request_status_changed_successfully_modal(request_id, data):
    if data['status'] == 'approved':
        text = f'Request #{request_id} was approved successfully.'
    else:
        text = f'Request #{request_id} was denied successfully.'
    return {
        "title": {
            "type": "plain_text",
            "text": "Success"
        },
        "type": "modal",
        "close": {
            "type": "plain_text",
            "text": "Close"
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": text
                }
            }
        ]
    }


request_error_modal = {
    "title": {
        "type": "plain_text",
        "text": "Error"
    },
    "type": "modal",
    "close": {
        "type": "plain_text",
        "text": "Close"
    },
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Oops, something went wrong, please, try again!"
            }
        }
    ]
}


def request_deleted_successfully_modal(request_id):
    return {
        "title": {
            "type": "plain_text",
            "text": "Success"
        },
        "type": "modal",
        "close": {
            "type": "plain_text",
            "text": "Close"
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f'Request #{request_id} was deleted successfully.'
                }
            }
        ]
    }


def request_create_modal(user):
    reviewer_list = UsersQuery.get_reviewers()

    bonus_list = TypeBonusesQuery.get_bonuses()

    reviewer_options = []
    for reviewer in reviewer_list:
        if user['id'] == reviewer['id']:
            continue

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
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Pick a payment date:*"
                },
                "accessory": {
                    "type": "datepicker",
                    "initial_date": str(date.today()),
                    "action_id": "request_date_input"
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


def request_edit_modal(request, user):
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
        if user['id'] == reviewer['id']:
            continue

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
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Pick a payment date:*"
                },
                "accessory": {
                    "type": "datepicker",
                    "initial_date": str(request['payment_date']),
                    "action_id": "request_date_input"
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
