bonus_start_menu = [
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
                    "text": "Create bonus"
                },
                "action_id": "bonus_create"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Return to main menu"
                },
                "action_id": "bonus_main_menu"
            }
        ]
    }
]

back_to_bonus_menu_button = {
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
                    "action_id": "bonus_start"
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


def edit_bonus_modal(name, description):
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
        "callback_id": "bonus_modal_edit",
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
                    "initial_value": name
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
                    "initial_value": description,
                    "multiline": True
                }
            }
        ]
    }
