import json
import requests
import os

from message_services import *
from orm_services import RequestQuery, UsersQuery

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')


def lambda_handler(event, context):
    action_id = event['action_id']

    if action_id == 'request_start_menu':
        data = {
            "response_type": 'in_channel',
            "replace_original": False,
            "blocks": request_start_menu
        }

        response_url = event['response_url']

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id == 'request_list':

        request_list = RequestQuery.get_requests()

        attachments = generate_request_block_list(request_list)

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

    elif action_id == 'request_create':
        data = {
            "trigger_id": event['trigger_id'],
            "view": request_create_modal()
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith('request_edit'):
        request_id = int(action_id.split('_')[2])

        request = RequestQuery.get_requests(request_id)[0]

        data = {
            "trigger_id": event['trigger_id'],
            "view": request_edit_modal(request)
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith('request_history_'):
        request_id = int(action_id.split('_')[2])

        # request_history_list = query_to_get_history_requests(request_id)

        request_history_list = [
            {
                'id': 1,
                'request_id': request_id,
                'timestamp': '24-07-2022 14:22',
                'editor_id': 1,
                'editor_name': 'Vova',
                'changes': 'abc'
            },
            {
                'id': 2,
                'request_id': request_id,
                'timestamp': '23-07-2022 13:22',
                'editor_id': 1,
                'editor_name': 'Vitalik',
                'changes': 'abc'
            },
            {
                'id': 3,
                'request_id': request_id,
                'timestamp': '22-07-2022 20:22',
                'editor_id': 1,
                'editor_name': 'Mariana',
                'changes': 'abc'
            },
        ]

        attachments = generate_request_history_block_list(request_history_list)

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

    elif action_id.startswith('request_delete_'):
        request_id = int(action_id.split('_')[2])

        RequestQuery.delete_request(request_id)

        blocks = request_deleted_successfully()

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

    elif action_id.startswith('request_modal_create'):
        creator_slack_id = event['body']['user']['id']
        creator_id = UsersQuery.get_user_by_slack_id(creator_slack_id)['id']

        reviewer_block_id = event['body']['view']['blocks'][0]['block_id']
        reviewer_id = \
            event['body']['view']['state']['values'][reviewer_block_id]['static_select-action']['selected_option'][
                'value']

        bonus_type_block_id = event['body']['view']['blocks'][1]['block_id']
        bonus_type_id = \
            event['body']['view']['state']['values'][bonus_type_block_id]['static_select-action']['selected_option'][
                'value']

        payment_amount_block_id = event['body']['view']['blocks'][2]['block_id']
        payment_amount = event['body']['view']['state']['values'][payment_amount_block_id]['request_amount_input'][
            'value']

        description_block_id = event['body']['view']['blocks'][3]['block_id']
        description = event['body']['view']['state']['values'][description_block_id]['request_description_input'][
            'value']
        description = description.replace('+', ' ')

        data = {
            'creator': creator_id,
            'reviewer': reviewer_id,
            'type_bonus': bonus_type_id,
            'payment_amount': payment_amount,
            'description': description,
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        result = RequestQuery.add_new_request(data)
        if result == 1:
            reviewer = UsersQuery.get_user_by_slack_id(reviewer_id)
            channel_id = reviewer['slack_id']
            blocks = request_created_successfully() # new req
            data_reviewer_message = {
                'token': SLACK_BOT_TOKEN,
                'channel': channel_id,
                "blocks": blocks
            }
            requests.post(response_url, data=json.dumps(data_reviewer_message), headers=headers)


            blocks = request_created_successfully()
            data_creator_message = {
                'token': SLACK_BOT_TOKEN,
                'channel': creator_slack_id,
                'blocks': blocks
            }
            requests.post(response_url, data=json.dumps(data_creator_message), headers=headers)

        else:
            creator = UsersQuery.get_user_by_slack_id(creator_id)['id']
            channel_id = creator['slack_id']
            blocks = request_not_created()
            data_error_message = {
                'token': SLACK_BOT_TOKEN,
                'channel': channel_id,
                'blocks': blocks
            }

            requests.post(response_url, data=json.dumps(data_error_message), headers=headers)

    elif action_id.startswith('request_modal_edit'):
        request_id = int(action_id.split('_')[3])
        editor_slack_id = event['body']['user']['id']
        editor_id = UsersQuery.get_user_by_slack_id(editor_slack_id)['id']

        reviewer_block_id = event['body']['view']['blocks'][0]['block_id']
        reviewer_id = \
            event['body']['view']['state']['values'][reviewer_block_id]['static_select-action']['selected_option'][
                'value']

        bonus_type_block_id = event['body']['view']['blocks'][1]['block_id']
        bonus_type_id = \
            event['body']['view']['state']['values'][bonus_type_block_id]['static_select-action']['selected_option'][
                'value']

        payment_amount_block_id = event['body']['view']['blocks'][2]['block_id']
        payment_amount = event['body']['view']['state']['values'][payment_amount_block_id]['request_amount_input'][
            'value']

        description_block_id = event['body']['view']['blocks'][3]['block_id']
        description = event['body']['view']['state']['values'][description_block_id]['request_description_input'][
            'value']
        description = description.replace('+', ' ')

        data = {
            'reviewer': reviewer_id,
            'type_bonus': bonus_type_id,
            'payment_amount': payment_amount,
            'description': description,
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        result = RequestQuery.update_request(request_id, data)

        blocks = request_edited_successfully()
        data_editor_massage = {
            'token': SLACK_BOT_TOKEN,
            "blocks": blocks
        }

        blocks = request_change_successfully()
        data_information_massage = {
            'token': SLACK_BOT_TOKEN,
            "blocks": blocks
        }

        if result == 1:
            request = RequestQuery.get_requests(request_id)

            if editor_slack_id == request['creator_slack_id']:
                  data_information_massage['channel'] = request['reviewer_slack_id']
                  data_editor_massage['channel'] = request['creator_slack_id']
            elif editor_slack_id == request['reviewer_slack_id']:
                data_information_massage['channel'] = request['creator_slack_id']
                data_editor_massage['channel'] = request['reviewer_slack_id']

            requests.post(response_url, data=json.dumps(data_editor_massage), headers=headers)

            requests.post(response_url, data=json.dumps(data_information_massage), headers=headers)

        else:

            blocks = request_error_edit()
            data_error_message = {
                'token': SLACK_BOT_TOKEN,
                'channel': editor_slack_id,
                'blocks': blocks
            }
            requests.post(response_url, data=json.dumps(data_error_message), headers=headers)




