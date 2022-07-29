import json
import requests
import os

from bonuses_message_services import *
from bonuses_orm_services import TypeBonusesQuery
from workers_orm_services import UsersQuery

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')


def bonuses_function(event):
    action_id = event['action_id']

    if action_id.startswith('bonus_list'):
        user = UsersQuery.get_user_by_slack_id(event['user']['id'])

        bonus_list = TypeBonusesQuery.get_bonuses()

        attachments = generate_bonus_block_list(bonus_list, user)

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

    # button responsible for posting modal, to create new bonus
    elif action_id.startswith('bonus_create'):
        data = {
            "trigger_id": event['trigger_id'],
            "view": bonus_create_modal
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

    # button responsible for returning to the start menu
    elif action_id.startswith('bonus_start_menu'):
        user = UsersQuery.get_user_by_slack_id(event['user']['id'])
        data = {
            "response_type": 'in_channel',
            "replace_original": True,
            "blocks": bonus_start_menu(user)
        }

        response_url = event['response_url']

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

    # buttons responsible for posting modal, to edit existing bonus
    elif action_id.startswith('bonus_edit'):
        bonus_id = int(action_id.split('_')[2])

        bonus = TypeBonusesQuery.get_bonuses(bonus_id)

        if bonus:
            data = {
                "trigger_id": event['trigger_id'],
                "view": bonus_edit_modal(bonus)
            }

            response_url = 'https://slack.com/api/views.open'

            headers = {
                'Content-type': 'application/json',
                "Authorization": "Bearer " + SLACK_BOT_TOKEN
            }

    # buttons responsible for deleting bonus
    elif action_id.startswith('bonus_delete'):
        bonus_id = int(action_id.split('_')[2])

        bonus_deleted = TypeBonusesQuery.delete_bonuses(bonus_id)

        view = bonus_error_modal()

        if bonus_deleted:
            view = bonus_deleted_successfully_modal

        data = {
            "trigger_id": event['trigger_id'],
            "view": view
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

    elif action_id.startswith('bonus_modal_create'):
        '''
        event = {
            "action_id": callback_id,
            "body": body
        }
        '''

        bonus_name_block_id = event['body']['view']['blocks'][0]['block_id']
        bonus_description_block_id = event['body']['view']['blocks'][1]['block_id']

        bonus_name = event['body']['view']['state']['values'][bonus_name_block_id]['bonus_name_input']['value']
        bonus_name = bonus_name.replace('+', ' ')

        bonus_description = \
            event['body']['view']['state']['values'][bonus_description_block_id]['bonus_description_input']['value']
        bonus_description = bonus_description.replace('+', ' ')

        data = {
            'type': bonus_name,
            'description': bonus_description
        }

        bonus_created = TypeBonusesQuery.add_new_bonus(data)

        view = bonus_error_modal()

        if bonus_created:
            view = bonus_created_successfully_modal(data)

        data = {
            "trigger_id": event['body']['trigger_id'],
            "view": view
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

    elif action_id.startswith('bonus_modal_edit'):

        bonus_id = int(action_id.split('_')[3])

        bonus_name_block_id = event['body']['view']['blocks'][0]['block_id']
        bonus_description_block_id = event['body']['view']['blocks'][1]['block_id']

        bonus_name = event['body']['view']['state']['values'][bonus_name_block_id]['bonus_name_input']['value']
        bonus_name = bonus_name.replace('+', ' ')

        bonus_description = \
            event['body']['view']['state']['values'][bonus_description_block_id]['bonus_description_input']['value']
        bonus_description = bonus_description.replace('+', ' ')

        data = {
            'type': bonus_name,
            'description': bonus_description
        }

        bonus_updated = TypeBonusesQuery.update_bonuses(bonus_id, data)

        view = bonus_error_modal()

        if bonus_updated:
            view = bonus_edited_successfully_modal(data)

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
