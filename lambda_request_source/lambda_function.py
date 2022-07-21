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

        RequestQuery.add_new_request(data)

        blocks = request_created_successfully()

        data = {
            'token': SLACK_BOT_TOKEN,
            'channel': creator_slack_id,
            "blocks": blocks
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith('request_modal_edit'):
        request_id = int(action_id.split('_')[3])

        creator_slack_id = event['body']['user']['id']
        # creator_id = UsersQuery.get_user_by_slack_id(creator_slack_id)['id']

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

        RequestQuery.update_request(request_id, data)

        blocks = request_edited_successfully()

        data = {
            'token': SLACK_BOT_TOKEN,
            'channel': creator_slack_id,
            'blocks': blocks
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)
