import json
import requests
import os
from message_services import generate_user_block_list, worker_create_modal, worker_edit_modal, get_user_by_id, \
    user_start_menu, user_created_successfully, user_edited_successfully
from orm_services import UsersQuery


SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
CHANNEL = os.environ.get('CHANNEL')
RESPONSE_URL = os.environ.get('RESPONSE_URL')


# start action, that print three button
def lambda_handler(event, context):
    action_id = event['action_id']

    if action_id == "worker_start_menu":
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

        res = requests.post(response_url, data=json.dumps(data), headers=headers)

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

        res = requests.post(response_url, data=json.dumps(data), headers=headers)


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
        res = requests.post(response_url, data=json.dumps(data), headers=headers)


    elif action_id == "worker_modal_create":
        full_name_block_id = event['body']['view']['blocks'][0]['block_id']
        full_name = event['body']['view']['state']['values'][full_name_block_id]['full_name_input']['value']
        full_name = full_name.replace('+', ' ')

        position_block_id = event['body']['view']['blocks'][1]['block_id']
        position = event['body']['view']['state']['values'][position_block_id]['position_input']['value']
        position = position.replace('+', ' ')

        roles_block_id = event['body']['view']['blocks'][2]['block_id']
        roles = []

        selected_options = event['body']['view']['state']['values'][roles_block_id]['worker_roles_input'][
            'selected_options']
        for option in selected_options:
            roles.append(option['value'])

        slack_id_block_id = event['body']['view']['blocks'][3]['block_id']
        slack_id = event['body']['view']['state']['values'][slack_id_block_id]['slack_id_input']['value']
        slack_id = slack_id.replace('+', ' ')

        data = {
            'full_name': full_name,
            'position': position,
            'roles': roles,
            'slack_id': slack_id
        }

        users = UsersQuery.add_new_user(data)
        blocks = [user_created_successfully(data), user_start_menu[0]]

        data = {
            "token": SLACK_BOT_TOKEN,
            'channel': CHANNEL,
            "blocks": blocks
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        res = requests.post(response_url, data=json.dumps(data), headers=headers)


    # modal window for edit user profile
    elif action_id.startswith("worker_edit"):
        user_id = int(action_id.split('_')[2])
        user = UsersQuery.get_users(user_id)
        user = get_user_by_id(user_id, user)

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
        res = requests.post(response_url, data=json.dumps(data), headers=headers)


    elif action_id.startswith("worker_modal_edit"):

        user_id = action_id.split('_')[3]

        full_name_block_id = event['body']['view']['blocks'][0]['block_id']
        full_name = event['body']['view']['state']['values'][full_name_block_id]['full_name_input']['value']
        full_name = full_name.replace('+', ' ')

        position_block_id = event['body']['view']['blocks'][1]['block_id']
        position = event['body']['view']['state']['values'][position_block_id]['position_input']['value']
        position = position.replace('+', ' ')

        roles_block_id = event['body']['view']['blocks'][2]['block_id']
        roles = []

        selected_options = event['body']['view']['state']['values'][roles_block_id]['worker_roles_input'][
            'selected_options']
        for option in selected_options:
            roles.append(option['value'])

        slack_id_block_id = event['body']['view']['blocks'][3]['block_id']
        slack_id = event['body']['view']['state']['values'][slack_id_block_id]['slack_id_input']['value']
        slack_id = slack_id.replace('+', ' ')

        data = {
            'full_name': full_name,
            'position': position,
            'roles': roles,
            'slack_id': slack_id
        }

        user = UsersQuery.update_user(int(user_id), data)
        blocks = [user_edited_successfully(data), user_start_menu[0]]

        data = {
            "token": SLACK_BOT_TOKEN,
            'channel': CHANNEL,
            "blocks": blocks
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        res = requests.post(response_url, data=json.dumps(data), headers=headers)



    elif action_id.startswith("worker_delete_"):
        user_id = int(action_id.split('_')[2])
        user = UsersQuery.delete_user(user_id)
        attachments = generate_user_block_list(user)
        data = {
            "response_type": 'in_channel',
            "replace_original": True,
            "attachments": attachments
        }

        response_url = event['response_url']
        headers = {
            'Content-type': 'application/json'
        }

        res = requests.post(response_url, data=json.dumps(data), headers=headers)

