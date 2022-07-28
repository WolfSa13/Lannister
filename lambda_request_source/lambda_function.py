import json
import requests
import os

from message_services import *
from orm_services import RequestQuery, UsersQuery, RequestHistoryQuery

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')


def authenticate_request_list(request_list, user):
    return_list = []
    for request in request_list:
        if request['creator'] == user['id']:
            return_list.append(request)

    if 'administrator' in user['roles']:
        return request_list
    elif 'reviewer' in user['roles']:
        for request in request_list:
            if request['reviewer'] == user['id']:
                if request not in return_list:
                    return_list.append(request)

    return return_list


def lambda_handler(event, context):
    action_id = event['action_id']

    if action_id == 'request_start_menu':
        data = {
            "response_type": 'in_channel',
            "replace_original": True,
            "blocks": request_start_menu
        }

        response_url = event['response_url']

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id == 'request_payment_day':
        payment_date = RequestQuery.get_requests_by_payment_date()

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        for key, value in payment_date.items():
            attachments = generate_notification_payment_day(value)

            data = {
                "token": SLACK_BOT_TOKEN,
                "channel": key,
                "attachments": attachments
            }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith('request_list'):
        user = UsersQuery.get_user_by_slack_id(event['user']['id'])

        data = {
            "response_type": 'in_channel',
            "replace_original": True
        }

        if action_id == 'request_list':
            if 'administrator' in user['roles']:
                blocks = request_list_administrator_menu
            elif 'reviewer' in user['roles']:
                blocks = request_list_reviewer_menu
            else:
                blocks = worker_request_list_menu

            data["blocks"] = blocks

        elif action_id.startswith('request_list_worker'):
            if action_id == 'request_list_worker_pending_unpaid_requests':
                request_list = RequestQuery.get_worker_pending_unpaid_requests(user['id'])
                data['attachments'] = generate_request_block_list(request_list, user, action_id)
            elif action_id == 'request_list_worker_approved_denied_requests':
                request_list = RequestQuery.get_worker_approved_denied_requests(user['id'])
                data['attachments'] = generate_request_block_list(request_list, user, action_id)
            elif action_id == 'request_list_worker_deleted_requests':
                request_list = RequestQuery.get_worker_deleted_requests(user['id'])
                data['attachments'] = generate_request_block_list(request_list, user, action_id)

        elif action_id.startswith('request_list_reviewer'):
            if action_id == 'request_list_reviewer_menu':
                data['blocks'] = request_list_reviewer_menu
            elif action_id == 'request_list_reviewer_requests':
                if 'administrator' in user['roles']:
                    data['blocks'] = request_list_administrator_requests
                else:
                    data['blocks'] = request_list_reviewer_requests
            elif action_id == 'request_list_reviewer_to_review':
                request_list = RequestQuery.get_filtered_requests(reviewer_id=user['id'], status='created')
                data['attachments'] = generate_request_block_list(request_list, user, action_id)

        elif action_id.startswith('request_list_administrator'):
            if action_id == 'request_list_administrator_menu':
                data['blocks'] = request_list_administrator_menu
            elif action_id.startswith('request_list_administrator_all_requests'):
                if action_id == 'request_list_administrator_all_requests':
                    data['blocks'] = request_list_administrator_all_requests
                else:
                    query_name = action_id.split('_')[5]
                    request_list = RequestQuery.get_administrator_all_requests(query_name)
                    """
                    action_id - something like "request_list_administrator_all_requests_pending"
                    we get 6th word of it
                    query_name must be:
                        - "pending"
                        - "unpaid"
                        - "paid"
                        - "denied"
                        - "deleted"
                    """
                    data['attachments'] = generate_request_block_list(request_list, user, action_id)

        response_url = event['response_url']

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id == 'request_message_delete':
        data = {
            "delete_original": "true"
        }

        response_url = event['response_url']

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id == 'request_create':
        user = UsersQuery.get_user_by_slack_id(event['user']['id'])
        data = {
            "trigger_id": event['trigger_id'],
            "view": request_create_modal(user)
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith('request_edit'):
        user = UsersQuery.get_user_by_slack_id(event['user']['id'])
        request_id = int(action_id.split('_')[2])

        request = RequestQuery.get_requests(request_id)[0]

        data = {
            "trigger_id": event['trigger_id'],
            "view": request_edit_modal(request, user)
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith('request_history_'):
        request_id = int(action_id.split('_')[2])

        request_history_list = RequestHistoryQuery.get_request_history(request_id=request_id)

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

    elif action_id.startswith('request_status'):
        request_id = int(action_id.split('_')[3])

        editor_slack_id = event['user']['id']
        editor = UsersQuery.get_user_by_slack_id(editor_slack_id)

        response_url_message = 'https://slack.com/api/chat.postMessage'
        response_url_modal = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        if action_id.split('_')[2] == "approve":
            status = 'approved'
        else:
            status = 'denied'

        data = {
            'status': status
        }

        request_updated = RequestQuery.update_request(request_id, data)

        view = request_error_modal

        if request_updated:
            old_request = RequestQuery.get_requests(request_id=request_id)[0]
            RequestHistoryQuery.add_history(data, request_id=request_id, editor=editor['full_name'],
                                            old_request=old_request)
            request = RequestQuery.get_requests(request_id)[0]

            view = request_status_changed_successfully_modal(request_id, data)
            data_reviewer_massage = {
                "trigger_id": event['trigger_id'],
                "view": view
            }

            blocks = request_status_changed_successfully(request_id, data)
            data_creator_massage = {
                'token': SLACK_BOT_TOKEN,
                "blocks": blocks,
                'channel': request['creator_slack_id']
            }

            requests.post(response_url_modal, data=json.dumps(data_reviewer_massage), headers=headers)

            requests.post(response_url_message, data=json.dumps(data_creator_massage), headers=headers)

        else:
            data_error_message = {
                "trigger_id": event['trigger_id'],
                'view': view
            }
            requests.post(response_url_modal, data=json.dumps(data_error_message), headers=headers)

    elif action_id.startswith('request_delete_'):

        request_id = int(action_id.split('_')[2])

        data = {
            'status': 'deleted'
        }

        request_deleted = RequestQuery.update_request(request_id, data)

        view = request_error_modal

        if request_deleted:
            view = request_deleted_successfully_modal(request_id)

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

    elif action_id.startswith('request_modal_create'):

        creator_slack_id = event['body']['user']['id']
        creator = UsersQuery.get_user_by_slack_id(creator_slack_id)
        creator_id = creator['id']

        reviewer_block_id = event['body']['view']['blocks'][0]['block_id']
        reviewer_id = \
            event['body']['view']['state']['values'][reviewer_block_id]['static_select-action']['selected_option'][
                'value']
        reviewer_name = \
            event['body']['view']['state']['values'][reviewer_block_id]['static_select-action']['selected_option'][
                'text']['text']

        bonus_type_block_id = event['body']['view']['blocks'][1]['block_id']
        bonus_type_id = \
            event['body']['view']['state']['values'][bonus_type_block_id]['static_select-action']['selected_option'][
                'value']
        bonus_type_name = \
            event['body']['view']['state']['values'][bonus_type_block_id]['static_select-action']['selected_option'][
                'text']['text']

        payment_amount_block_id = event['body']['view']['blocks'][2]['block_id']
        payment_amount = event['body']['view']['state']['values'][payment_amount_block_id]['request_amount_input'][
            'value']

        payment_date_block_id = event['body']['view']['blocks'][3]['block_id']

        payment_date = event['body']['view']['state']['values'][payment_date_block_id]['request_date_input'][
            'selected_date']

        description_block_id = event['body']['view']['blocks'][4]['block_id']
        description = event['body']['view']['state']['values'][description_block_id]['request_description_input'][
            'value']
        description = description.replace('+', ' ')

        data = {
            'creator': int(creator_id),
            'reviewer': int(reviewer_id),
            'type_bonus': int(bonus_type_id),
            'payment_amount': int(payment_amount),
            'payment_date': str(payment_date),
            'description': description,
            'status': 'created'
        }

        request_id = RequestQuery.add_new_request(data)
        response_url_message = 'https://slack.com/api/chat.postMessage'
        response_url_modal = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        view = request_error_modal

        if request_id != 0:
            data['reviewer_name'] = reviewer_name.replace('+', ' ')
            data['bonus_name'] = bonus_type_name.replace('+', ' ')

            RequestHistoryQuery.add_history(data, request_id=request_id, editor=creator['full_name'])

            reviewer = UsersQuery.get_user_by_id(int(reviewer_id))
            reviewer_channel_id = reviewer['slack_id']

            creator_name = creator['full_name']
            blocks = request_created_successfully_reviewer(creator_name)
            data_reviewer_message = {
                'token': SLACK_BOT_TOKEN,
                'channel': reviewer_channel_id,
                "blocks": blocks
            }
            requests.post(response_url_message, data=json.dumps(data_reviewer_message), headers=headers)

            view = request_created_successfully_modal(request_id)
            data_creator_modal = {
                "trigger_id": event['body']['trigger_id'],
                'view': view
            }
            requests.post(response_url_modal, data=json.dumps(data_creator_modal), headers=headers)

        else:
            data_creator_modal = {
                "trigger_id": event['body']['trigger_id'],
                'view': view
            }
            requests.post(response_url_modal, data=json.dumps(data_creator_modal), headers=headers)

    elif action_id.startswith('request_modal_edit'):
        request_id = int(action_id.split('_')[3])

        editor_slack_id = event['body']['user']['id']
        creator = UsersQuery.get_user_by_slack_id(editor_slack_id)

        reviewer_block_id = event['body']['view']['blocks'][0]['block_id']
        reviewer_id = \
            event['body']['view']['state']['values'][reviewer_block_id]['static_select-action']['selected_option'][
                'value']
        reviewer_name = \
            event['body']['view']['state']['values'][reviewer_block_id]['static_select-action']['selected_option'][
                'text']['text']

        bonus_type_block_id = event['body']['view']['blocks'][1]['block_id']
        bonus_type_id = \
            event['body']['view']['state']['values'][bonus_type_block_id]['static_select-action']['selected_option'][
                'value']
        bonus_type_name = \
            event['body']['view']['state']['values'][bonus_type_block_id]['static_select-action']['selected_option'][
                'text']['text']

        payment_amount_block_id = event['body']['view']['blocks'][2]['block_id']
        payment_amount = event['body']['view']['state']['values'][payment_amount_block_id]['request_amount_input'][
            'value']

        payment_date_block_id = event['body']['view']['blocks'][3]['block_id']

        payment_date = event['body']['view']['state']['values'][payment_date_block_id]['request_date_input'][
            'selected_date']

        description_block_id = event['body']['view']['blocks'][4]['block_id']
        description = event['body']['view']['state']['values'][description_block_id]['request_description_input'][
            'value']
        description = description.replace('+', ' ')

        data = {
            'reviewer': int(reviewer_id),
            'type_bonus': int(bonus_type_id),
            'payment_amount': int(payment_amount),
            'payment_date': str(payment_date),
            'description': description
        }

        old_request = RequestQuery.get_requests(request_id=request_id)[0]
        request_updated = RequestQuery.update_request(request_id, data)

        response_url_message = 'https://slack.com/api/chat.postMessage'
        response_url_modal = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

        view = request_error_modal

        if request_updated:
            data['reviewer_name'] = reviewer_name.replace('+', ' ')
            data['bonus_name'] = bonus_type_name.replace('+', ' ')
            RequestHistoryQuery.add_history(data, request_id=request_id, editor=creator['full_name'],
                                            old_request=old_request)

            view = request_edited_successfully_modal(request_id)
            data_editor_modal = {
                "trigger_id": event['body']['trigger_id'],
                "view": view
            }

            blocks = request_change_successfully(request_id)
            data_information_massage = {
                'token': SLACK_BOT_TOKEN,
                "blocks": blocks
            }
            request = RequestQuery.get_requests(request_id)[0]

            if editor_slack_id == request['creator_slack_id']:
                data_information_massage['channel'] = request['reviewer_slack_id']
            elif editor_slack_id == request['reviewer_slack_id']:
                data_information_massage['channel'] = request['creator_slack_id']

            requests.post(response_url_modal, data=json.dumps(data_editor_modal), headers=headers)

            requests.post(response_url_message, data=json.dumps(data_information_massage), headers=headers)

        else:
            data = {
                "trigger_id": event['body']['trigger_id'],
                "view": view
            }

            requests.post(response_url_modal, data=json.dumps(data), headers=headers)
