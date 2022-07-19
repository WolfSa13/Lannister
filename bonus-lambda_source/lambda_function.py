import json
import requests
import os

from bonus_list_generator import generate_bonus_block_list, get_bonus_by_id
from const import bonus_start_menu, bonus_create_modal, bonus_edit_modal, bonus_created_successfully, bonus_edited_successfully
from orm_services import TypeBonusesQuery

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
CHANNEL = os.environ.get('CHANNEL')


def lambda_handler(event, context):
    """
    example_event = {
        'response_url': 'url',
        "trigger_id": body['trigger_id'],
        'action_id': action_id
    }
    """

    action_id = event['action_id']

    if action_id.startswith('bonus_list'):

        bonus_list = TypeBonusesQuery.get_bonuses()

        attachments = generate_bonus_block_list(bonus_list)

        data = {
            "response_type": 'in_channel',
            "replace_original": False,
            "attachments": attachments
        }

        response_url = event['response_url']

        headers = {'Content-type': 'application/json'}

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
        data = {
            "response_type": 'in_channel',
            "replace_original": False,
            "blocks": bonus_start_menu
        }

        response_url = event['response_url']

        headers = {'Content-type': 'application/json'}

    # buttons responsible for posting modal, to edit existing bonus
    elif action_id.startswith('bonus_edit'):
        bonus_id = int(action_id.split('_')[2])

        bonus = TypeBonusesQuery.get_bonuses(bonus_id)[0]

        if bonus:
            data = {
                "trigger_id": event['trigger_id'],
                "view": bonus_edit_modal(bonus_id, bonus['name'], bonus['description'])
            }

            response_url = 'https://slack.com/api/views.open'

            headers = {
                'Content-type': 'application/json',
                "Authorization": "Bearer " + SLACK_BOT_TOKEN
            }

    # buttons responsible for deleting bonus
    elif action_id.startswith('bonus_delete'):
        bonus_id = int(action_id.split('_')[2])

        bonus_list = TypeBonusesQuery.delete_bonuses(bonus_id)

        attachments = generate_bonus_block_list(bonus_list)

        data = {
            "response_type": 'in_channel',
            "replace_original": True,
            "attachments": attachments
        }

        response_url = event['response_url']

        headers = {'Content-type': 'application/json'}

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
            'name': bonus_name,
            'description': bonus_description
        }

        bonus_list = TypeBonusesQuery.add_new_bonus(data)

        attachments = generate_bonus_block_list(bonus_list)

        blocks = [bonus_created_successfully(bonus_name), bonus_start_menu[0]]

        data = {
            'token': SLACK_BOT_TOKEN,
            'channel': CHANNEL,
            "blocks": blocks
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

    elif action_id.startswith('bonus_modal_edit'):

        bonus_id = action_id.split('_')[3]

        bonus_name_block_id = event['body']['view']['blocks'][0]['block_id']
        bonus_description_block_id = event['body']['view']['blocks'][1]['block_id']

        bonus_name = event['body']['view']['state']['values'][bonus_name_block_id]['bonus_name_input']['value']
        bonus_name = bonus_name.replace('+', ' ')

        bonus_description = \
            event['body']['view']['state']['values'][bonus_description_block_id]['bonus_description_input']['value']
        bonus_description = bonus_description.replace('+', ' ')

        data = {
            'name': bonus_name,
            'description': bonus_description
        }

        bonus_list = TypeBonusesQuery.update_bonuses(bonus_id, data)

        attachments = generate_bonus_block_list(bonus_list)

        blocks = [bonus_edited_successfully, bonus_start_menu[0]]

        data = {
            'token': SLACK_BOT_TOKEN,
            'channel': CHANNEL,
            "blocks": blocks
        }

        response_url = 'https://slack.com/api/chat.postMessage'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + SLACK_BOT_TOKEN
        }

    res = requests.post(response_url, data=json.dumps(data), headers=headers)
