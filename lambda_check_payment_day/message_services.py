from datetime import date
from time_utils import datetime_converter, date_converter


def generate_notification_payment_day(request_list):
    current_date = date.today().strftime("%Y-%m-%d")
    attachments = []
    info_string = {
        "color": "#09ab19",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"These requests have to be paid today: {date_converter(current_date)}"
                }
            }
        ]
    }

    attachments.append(info_string)

    for request in request_list:
        request_item = {
            "color": "#09ab19",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Request #{request['id']}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Creator:* {request['creator_name']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Creation date:* {datetime_converter(request['created_at'])}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Bonus type:* {request['type']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Payment amount:*  {request['payment_amount']}$"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Description:* {request['description']}"
                        }
                    ]
                }
            ]
        }
        attachments.append(request_item)

    return attachments

