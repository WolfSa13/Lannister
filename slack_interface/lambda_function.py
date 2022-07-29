import json

from utils import base64_encoder, func_to_invoke
from slack_interface_message_services import respond_with_error_return_menu, respond_with_menu

STATUS_CODE_200 = {
    "isBase64Encoded": True,
    "statusCode": 200,
    "headers": {},
    "body": ""
}


def lambda_handler(event, context):
    body = event['body']
    isBase64Encoded = event['isBase64Encoded']

    # check if event body was decoded
    if isBase64Encoded:
        body = base64_encoder(body)
    else:
        body = json.loads(body)

    # when the command was called in the chat
    if 'challenge' in body:
        return body

    if 'event' in body and body['event']['type'] == 'team_join':
        function = func_to_invoke('worker')

        data = {
            "user": body['event']['user'],
            "action_id": 'worker_team_join'
        }

        function(data)

    if 'command' in body and body['command'] == '/start':
        user_slack_id = body['user_id']
        respond_with_menu(body['response_url'], user_slack_id)

    # when the button was clicked in the chat
    elif body['type'] == 'block_actions' and 'response_url' in body:
        action_id = body['actions'][0]['action_id']

        # when 'Return to main menu' button was clicked
        if action_id.startswith('start'):
            user_slack_id = body['user']['id']
            respond_with_menu(body['response_url'], user_slack_id)

            return STATUS_CODE_200

        elif action_id.split('_')[0] not in ['worker', 'request', 'bonus']:
            respond_with_error_return_menu(body['response_url'])

            return STATUS_CODE_200

        function = func_to_invoke(action_id.split('_')[0])

        data = {
            "response_url": body['response_url'],
            "trigger_id": body['trigger_id'],
            "user": body['user'],
            "action_id": action_id
        }

        function(data)

    # when the modal was submitted
    elif body['type'] == 'view_submission':

        callback_id = body['view']['callback_id']
        function = func_to_invoke(callback_id.split('_')[0])

        data = {
            "body": body,
            "action_id": callback_id
        }

        function(data)

    return STATUS_CODE_200
