import copy
from const import back_to_bonus_menu_button

template = {
    "color": "#008000",
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                # change!
                "text": None
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    # change (add 'Name' after \n)
                    "text": "*Description:*\n"
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
                    # change!
                    "action_id": "bonus_edit_"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Delete"
                    },
                    "style": "danger",
                    # change!
                    "action_id": "bonus_delete_"
                }
            ]
        }
    ]
}


def get_bonus_by_id(bonus_id, bonus_list):
    for bonus in bonus_list:
        if bonus['id'] == bonus_id:
            return bonus

    return None


def generate_bonus_block_list(bonus_list, template=template):
    attachments = []

    for bonus in bonus_list:
        temp = copy.deepcopy(template)
        temp['blocks'][0]['text']['text'] = bonus['type']
        temp['blocks'][1]['fields'][0]['text'] += bonus['description']
        temp['blocks'][2]['elements'][0]['action_id'] += str(bonus['id'])
        temp['blocks'][2]['elements'][1]['action_id'] += str(bonus['id'])

        attachments.append(temp)

    attachments.append(back_to_bonus_menu_button)

    return attachments
