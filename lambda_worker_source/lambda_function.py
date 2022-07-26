import json
import requests
import os
from message_services import *
from orm_services import UsersQuery

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
RESPONSE_URL = 'https://slack.com/api/views.open'


# start action, that print three button
def lambda_handler(event, context):
    action_id = event['action_id']

    if action_id == "worker_get":
        user = UsersQuery.get_user_by_slack_id(event['user_slack_id'])

        return user

    elif action_id == "worker_start_menu":
        data = {
            "response_type": 'in_channel',
            "replace_original": False,
            "blocks": user_start_menu
        }

        response_url = event['response_url']

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith("worker_list"):

        users_list = UsersQuery.get_users()
        attachments = generate_user_block_list(users_list)

        data = {
            "response_type": 'in_channel',
            "replace_original": False,
            "attachments": attachments

        }

        response_url = event['response_url']

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    # create new user modal window
    elif action_id.startswith("worker_create"):
        data = {
            "trigger_id": event['trigger_id'],
            "view": worker_create_modal
        }

        response_url = RESPONSE_URL

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id == "worker_modal_create":
        full_name_block_id = event['body']['view']['blocks'][0]['block_id']
        full_name = event['body']['view']['state']['values'][full_name_block_id]['full_name_input']['value']
        full_name = full_name.replace('+', ' ')

        position_block_id = event['body']['view']['blocks'][1]['block_id']
        position = event['body']['view']['state']['values'][position_block_id]['position_input']['value']
        position = check_if_cpp_dev(position)

        roles_block_id = event['body']['view']['blocks'][2]['block_id']
        roles = []

        selected_options = event['body']['view']['state']['values'][roles_block_id]['worker_roles_input'][
            'selected_options']
        for option in selected_options:
            roles.append(int(option['value']))

        slack_id_block_id = event['body']['view']['blocks'][3]['block_id']
        slack_id = event['body']['view']['state']['values'][slack_id_block_id]['slack_id_input']['value']

        data = {
            'full_name': full_name,
            'position': position,
            'roles': roles,
            'slack_id': slack_id
        }

        users_created = UsersQuery.add_new_user(data)
        blocks = [error_message]

        if users_created:
            blocks = [user_created_successfully(full_name)]

        data = {
            "token": SLACK_BOT_TOKEN,
            'channel': event['body']['user']['id'],
            "blocks": blocks
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    # modal window for edit user profile
    elif action_id.startswith("worker_edit"):
        user_id = int(action_id.split('_')[2])
        user = UsersQuery.get_users(user_id)[0]

        if user:
            data = {
                "trigger_id": event['trigger_id'],
                "view": worker_edit_modal(user)
            }

        response_url = RESPONSE_URL
        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith("worker_modal_edit"):

        user_id = int(action_id.split('_')[3])

        full_name_block_id = event['body']['view']['blocks'][0]['block_id']
        full_name = event['body']['view']['state']['values'][full_name_block_id]['full_name_input']['value']
        full_name = full_name.replace('+', ' ')

        position_block_id = event['body']['view']['blocks'][1]['block_id']
        position = event['body']['view']['state']['values'][position_block_id]['position_input']['value']
        position = check_if_cpp_dev(position)

        roles_block_id = event['body']['view']['blocks'][2]['block_id']
        roles = []

        selected_options = event['body']['view']['state']['values'][roles_block_id]['worker_roles_input'][
            'selected_options']

        for option in selected_options:
            roles.append(int(option['value']))

        slack_id_block_id = event['body']['view']['blocks'][3]['block_id']
        slack_id = event['body']['view']['state']['values'][slack_id_block_id]['slack_id_input']['value']

        data = {
            'full_name': full_name,
            'position': position,
            'roles': roles,
            'slack_id': slack_id
        }

        users_updated = UsersQuery.update_user(user_id, data)
        blocks = [error_message]

        if users_updated:
            blocks = [user_edited_successfully]

        data = {
            "token": SLACK_BOT_TOKEN,
            'channel': event['body']['user']['id'],
            "blocks": blocks
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith("worker_delete_"):
        user_id = int(action_id.split('_')[2])

        user_deleted = UsersQuery.delete_user(user_id)

        blocks = [error_message]
        if user_deleted:
            blocks = [user_deleted_successfully]

        data = {
            'token': SLACK_BOT_TOKEN,
            'channel': event['user']['id'],
            "blocks": blocks
        }

        response_url = 'https://slack.com/api/chat.postMessage'
        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)
