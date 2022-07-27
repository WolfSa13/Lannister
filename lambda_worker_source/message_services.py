roles_options = [
    {
        "text": {
            "type": "mrkdwn",
            "text": "worker"
        },
        "value": "1"
    },
    {
        "text": {
            "type": "mrkdwn",
            "text": "reviewer"
        },
        "value": "2"
    },
    {
        "text": {
            "type": "mrkdwn",
            "text": "administrator"
        },
        "value": "3"
    }
]


def get_user_by_id(user_id, users_list):
    for user in users_list:
        if user['id'] == int(user_id):
            return user

    return None


def generate_user_block_list(user_list):
    attachments = []

    for user in user_list:
        user_item = {
            "color": "#008000",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": user['full_name']
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Position:* {user['position']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Roles:* {', '.join(user['roles'])}"
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
                            "action_id": f"worker_edit_{user['id']}"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Delete"
                            },
                            "style": "danger",
                            "action_id": f"worker_delete_{user['id']}"
                        }
                    ]
                }
            ]
        }
        attachments.append(user_item)

    attachments.append(back_to_user_start_menu_button)

    return attachments


worker_create_modal = {
    "title": {
        "type": "plain_text",
        "text": "Create new user"
    },
    "submit": {
        "type": "plain_text",
        "text": "Create"
    },
    "type": "modal",
    "callback_id": "worker_modal_create",
    "close": {
        "type": "plain_text",
        "text": "Cancel"
    },
    "blocks": [
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "Full name"
            },
            "element": {
                "type": "plain_text_input",
                "action_id": "full_name_input"
            }
        },
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "Position"
            },
            "element": {
                "type": "plain_text_input",
                "action_id": "position_input"
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Role"
            },
            "accessory": {
                "type": "checkboxes",
                "options": roles_options,
                "action_id": "worker_roles_input"
            }
        },
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "Slack_id"
            },
            "element": {
                "type": "plain_text_input",
                "action_id": "slack_id_input"
            }
        }
    ]
}


def initial_role_block(role):
    if role == 'worker':
        value = '1'
    elif role == 'reviewer':
        value = '2'
    elif role == 'administrator':
        value = '3'

    return {
        "text": {
            "type": "mrkdwn",
            "text": role
        },
        "value": value
    }


def worker_edit_modal(user):
    initial_options = []
    for role in user['roles']:
        initial_options.append(initial_role_block(role))

    return {
        "title": {
            "type": "plain_text",
            "text": "Edit worker"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "type": "modal",
        "callback_id": "worker_modal_edit_" + str(user['id']),
        "blocks": [
            {
                "type": "input",
                "label": {
                    "type": "plain_text",
                    "text": "Full name"
                },
                "element": {
                    "type": "plain_text_input",
                    "action_id": "full_name_input",
                    "initial_value": user['full_name']
                }
            },
            {
                "type": "input",
                "label": {
                    "type": "plain_text",
                    "text": "Position"
                },
                "element": {
                    "type": "plain_text_input",
                    "action_id": "position_input",
                    "initial_value": user['position']
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Role"
                },
                "accessory": {
                    "type": "checkboxes",
                    "options": roles_options,
                    'initial_options': initial_options,
                    "action_id": "worker_roles_input"
                }
            },
            {
                "type": "input",
                "label": {
                    "type": "plain_text",
                    "text": "Slack_id"
                },
                "element": {
                    "type": "plain_text_input",
                    "action_id": "slack_id_input",
                    "initial_value": user['slack_id']
                }
            }
        ]
    }


error_message = {
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": "Operation is unsuccessful. Try again."
    }
}


def user_created_successfully(full_name):
    return {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": f"User {full_name} was created successfuly."
        }
    }


user_edited_successfully = {
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": "User was edited successfully"
    }
}

user_deleted_successfully = {
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": "User was deleted successfully"
    }
}

user_start_menu = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Workers"
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
                    "text": "Workers List"
                },
                "action_id": "worker_list"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Create worker"
                },
                "action_id": "worker_create"
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

back_to_user_start_menu_button = {
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
                    "action_id": "worker_start_menu"
                }
            ]
        }
    ]
}

new_team_member_greeting = {
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": "Welcome to the COXIT team!\nI am Lannister. To start work with me use the /start command"
    }
}


def check_if_cpp_dev(position):
    if 'c++' in position:
        return position.replace('c++', 'cpp').replace('+', ' ').replace('cpp', 'c++')
    elif 'C++' in position:
        return position.replace('C++', 'Cpp').replace('+', ' ').replace('Cpp', 'C++')

    return position.replace('+', ' ')
