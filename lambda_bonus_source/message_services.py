def generate_bonus_block_list(bonus_list, user):
    attachments = []

    for bonus in bonus_list:
        bonus_item = {
            "color": "#008000",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": bonus['type']
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Description:* {bonus['description']}"
                        }
                    ]
                }
            ]
        }

        if 'administrator' in user['roles']:
            admin_buttons = {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Edit"
                        },
                        "action_id": f"bonus_edit_{bonus['id']}"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Delete"
                        },
                        "style": "danger",
                        "action_id": f"bonus_delete_{bonus['id']}"
                    }
                ]
            }
            bonus_item['blocks'].append(admin_buttons)

        attachments.append(bonus_item)

    attachments.append(back_to_bonus_start_menu_button)

    return attachments


bonus_edited_successfully = {
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": "Bonus was edited successfully"
    }
}


def bonus_created_successfully(name):
    return {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": f"Bonus {name} was created successfully"
        }
    }


bonus_deleted_successfully = {
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": f"Bonus was deleted successfully"
    }
}

error_message = {
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": f"An error occurred. Are You sure, that You've done right action? When yes, try again!"
    }
}


def bonus_start_menu(user):
    bonus_start_menu_const = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Bonuses"
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
                        "text": "Bonus List"
                    },
                    "action_id": "bonus_list"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Return to main menu"
                    },
                    "action_id": "start_menu"
                }
            ]
        }
    ]

    if 'administrator' in user['roles']:
        create_button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Create bonus"
            },
            "action_id": "bonus_create"
        }
        bonus_start_menu_const[2]['elements'].insert(1, create_button)

    return bonus_start_menu_const


back_to_bonus_start_menu_button = {
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
                    "action_id": "bonus_start_menu"
                }
            ]
        }
    ]
}

bonus_create_modal = {
    "title": {
        "type": "plain_text",
        "text": "Create new bonus"
    },
    "submit": {
        "type": "plain_text",
        "text": "Create"

    },
    "type": "modal",
    "callback_id": "bonus_modal_create",
    "close": {
        "type": "plain_text",
        "text": "Cancel"
    },
    "blocks": [
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "Bonus name"
            },
            "element": {
                "type": "plain_text_input",
                "action_id": "bonus_name_input"
            },
        },
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "Description"
            },
            "element": {
                "type": "plain_text_input",
                "action_id": "bonus_description_input",
                "multiline": True
            }
        }
    ]
}


def bonus_edit_modal(bonus):
    return {
        "title": {
            "type": "plain_text",
            "text": "Edit bonus"
        },
        "submit": {
            "type": "plain_text",
            "text": "Save"

        },
        "type": "modal",
        "callback_id": f"bonus_modal_edit_{bonus['id']}",
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            {
                "type": "input",
                "label": {
                    "type": "plain_text",
                    "text": "Bonus name"
                },
                "element": {
                    "type": "plain_text_input",
                    "action_id": "bonus_name_input",
                    "initial_value": bonus['type']
                },
            },
            {
                "type": "input",
                "label": {
                    "type": "plain_text",
                    "text": "Description"
                },
                "element": {
                    "type": "plain_text_input",
                    "action_id": "bonus_description_input",
                    "initial_value": bonus['description'],
                    "multiline": True
                }
            }
        ]
    }
