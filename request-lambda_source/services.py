from const import back_to_request_start_menu_button
from orm_services import UsersQuery, TypeBonusesQuery
import datetime


def generate_request_block_list(request_list):
    attachments = []

    for request in request_list:

        updated_at = request['updated_at']
        if not updated_at:
            updated_at = "Wasn't updated yet."

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
                            "text": f"*Creation date:* {request['created_at']}\n*Payment date:* {payment_date}\n*Last changed:* {updated_at}"
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
