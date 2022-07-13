import json
import requests

from bonus_list_generator import generate_bonus_block_list, get_bonus_by_id
from const import bonus_start_menu, start_menu, bonus_create_modal, edit_bonus_modal

token = 'xoxb-3816664220352-3794386068690-fMsc3SoJJSJdx335iWY0Jb7x'


def lambda_handler(event, context):
    # example_event = {
    #     'response_url': 'url',
    #     "trigger_id": body['trigger_id'],
    #     'action_id': action_id
    # }

    action_id = event['action_id']

    # button responsible for posting 3 buttons: Bonus list, Create_bonus, Return to main menu
    if action_id == 'bonus_start_menu':

        data = {
            "response_type": 'in_channel',
            "replace_original": False,
            "blocks": bonus_start_menu
        }

        response_url = event['response_url']

        headers = {'Content-type': 'application/json'}

        res = requests.post(response_url, data=json.dumps(data), headers=headers)

    # button responsible for posting list of possible bonuses
    elif action_id.startswith('bonus_list'):

        bonus_list = TypeBonusesQuery.get_bonuses()

        attachments = generate_bonus_block_list(bonus_list)

        data = {
            "response_type": 'in_channel',
            "replace_original": False,
            "attachments": attachments
        }

        response_url = event['response_url']

        headers = {'Content-type': 'application/json'}

        res = requests.post(response_url, data=json.dumps(data), headers=headers)

    # button responsible for posting modal, to create new bonus
    elif action_id.startswith('bonus_create'):
        data = {
            "trigger_id": event['trigger_id'],
            "view": bonus_create_modal
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + token
        }

        res = requests.post(response_url, data=json.dumps(data), headers=headers)

    # button responsible for returning to the start menu
    elif action_id.startswith('start'):
        data = {
            "response_type": 'in_channel',
            "replace_original": False,
            "blocks": start_menu
        }

        response_url = event['response_url']

        headers = {'Content-type': 'application/json'}

        res = requests.post(response_url, data=json.dumps(data), headers=headers)

    # buttons responsible for posting modal, to edit existing bonus
    elif action_id.startswith('bonus_edit'):
        bonus_id = int(action_id.split('_')[2])

        bonus_list = TypeBonusesQuery.get_bonuses()

        bonus = get_bonus_by_id(bonus_id, bonus_list)

        data = {
            "trigger_id": event['trigger_id'],
            "view": edit_bonus_modal(bonus['type'], bonus['description']),
            "bonus_id": bonus_id
        }

        response_url = 'https://slack.com/api/views.open'

        headers = {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + token
        }

        res = requests.post(response_url, data=json.dumps(data), headers=headers)

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

        res = requests.post(response_url, data=json.dumps(data), headers=headers)

    elif action_id.startswith('bonus_modal_create'):
        # event = {
        #     "action_id": callback_id,
        #     "body": body
        # }

        bonus_name_block_id = event['body']['view']['blocks'][0]['block_id']
        bonus_description_block_id = event['body']['view']['blocks'][1]['block_id']

        bonus_name = event['body']['view']['state']['values'][bonus_name_block_id]['bonus_name_input']['value']
        bonus_description = \
            event['body']['view']['state']['values'][bonus_description_block_id]['bonus_description_input']['value']

        data = {
            'name': bonus_name,
            'description': bonus_description
        }

        bonus_list = TypeBonusesQuery.add_new_bonus(data)

    elif action_id.startswith('bonus_modal_edit'):

        bonus_name_block_id = event['body']['view']['blocks'][0]['block_id']
        bonus_description_block_id = event['body']['view']['blocks'][1]['block_id']

        bonus_name = event['body']['view']['state']['values'][bonus_name_block_id]['bonus_name_input']['value']
        bonus_description = \
            event['body']['view']['state']['values'][bonus_description_block_id]['bonus_description_input']['value']

        data = {
            'name': bonus_name,
            'description': bonus_description
        }

        bonus_list = TypeBonusesQuery.update_bonuses(event['bonus_id'], data)
