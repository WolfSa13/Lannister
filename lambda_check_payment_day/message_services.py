from orm_services import UsersQuery, TypeBonusesQuery
from datetime import date
from time_utils import datetime_converter, date_converter




def request_string(request_id):
    return {
        "color": "#008000",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"Tha payment day of #{request_id} is today!"
                }
            }
        ]
    }


def generate_notification_payment_day(request_list):
    """
    request_list = [
            {
                id': 1,
                'request_id': 1,
                'creator': 'Name',
                'bonus_type': 'bonus_name',
                'creation date': '24-07-2022 14:22',
                'payment_amount': '200$',
            }
        ]
    """

    attachments = [request_string(request_list[0].request_id)]

    for request_history_event in request_list:
        request_history_item = {
            "color": "#09ab19",
            "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Editor:* {request_history_event.editor}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*When:* {datetime_converter(request_history_event.timestamp)}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Changes:*\n{request_history_event.changes}"
                    }
                }
            ]
        }

        attachments.append(request_history_item)

    return attachments


def get_request_by_id(request_id, request_list):
    for request in request_list:
        if request['id'] == int(request_id):
            return request

