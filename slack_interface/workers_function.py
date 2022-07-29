import json
import requests
import os
from workers_message_services import *
from workers_orm_services import UsersQuery

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
RESPONSE_URL = 'https://slack.com/api/views.open'


# start action, that print three button
def workers_function(event):
    action_id = event['action_id']

    if action_id == "worker_get":
        user = UsersQuery.get_user_by_slack_id(event['user_slack_id'])

        return user

    elif action_id == "worker_start_menu":
        data = {
            "response_type": 'in_channel',
            "replace_original": True,
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
            "replace_original": True,
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

        new_user_data = {
            'full_name': full_name,
            'position': position,
            'roles': roles,
            'slack_id': slack_id
        }

        users_created = UsersQuery.add_new_user(new_user_data)

        new_roles = []

        for role in roles:
            if role == 1:
                new_roles.append('worker')
            elif role == 2:
                new_roles.append('reviewer')
            elif role == 3:
                new_roles.append('administrator')

        new_user_data['roles'] = new_roles

        view = worker_error_modal()

        if users_created:
            view = worker_created_successfully_modal(new_user_data)

        data = {
            "trigger_id": event['body']['trigger_id'],
            "view": view
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id == 'worker_team_join':
        new_user_data = {
            'full_name': event['user']['real_name'],
            'roles': [1],
            'slack_id': event['user']['id']
        }

        users_created = UsersQuery.add_new_user(new_user_data)

        if users_created:
            blocks = [new_team_member_greeting]

            message_data = {
                "token": SLACK_BOT_TOKEN,
                'channel': event['user']['id'],
                "blocks": blocks
            }

            response_url = 'https://slack.com/api/chat.postMessage'

            headers = {
                'Content-type': 'application/json',
                "Authorization": "Bearer " + SLACK_BOT_TOKEN
            }

            requests.post(response_url, data=json.dumps(message_data), headers=headers)

    # modal window for edit user profile
    elif action_id.startswith("worker_edit"):
        user_id = int(action_id.split('_')[2])
        user = UsersQuery.get_user_by_id(user_id)

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

        print(data)
        res = requests.post(response_url, data=json.dumps(data), headers=headers)
        print(res.status_code)
        print(res.json())
        print('--------------------')

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
        user = UsersQuery.get_user_by_id(user_id)

        view = worker_error_modal()

        print('--------------------')
        print(event)
        print(users_updated)

        if users_updated:
            view = worker_edited_successfully_modal(user)

        view_data = {
            "trigger_id": event['body']['trigger_id'],
            "view": view
        }

        print(view_data)

        response_url = RESPONSE_URL

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        # res = requests.post(response_url, data=json.dumps(view_data), headers=headers)
        res = requests.post(response_url, json=view_data, headers=headers)
        print(res.status_code)
        print(res.json())
        print('--------------------')

    elif action_id.startswith("worker_delete_"):
        user_id = int(action_id.split('_')[2])

        user_deleted = UsersQuery.delete_user(user_id)

        view = worker_error_modal()

        if user_deleted:
            view = worker_deleted_successfully_modal

        data = {
            "trigger_id": event['trigger_id'],
            "view": view
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)
