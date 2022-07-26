from orm_services import RequestQuery
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

        payment_date = request['payment_date']

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
                            "text": f"*Bonus type:* {request['bonus_name']}"
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
                            "text": f"*Creation date:* {datetime_converter(request['created_at'])}\n"
                                    f"*Payment date:* {date_converter(payment_date)}"
                        }
                    ]
                },
            ]
        }
        attachments.append(request_item)

    return attachments

