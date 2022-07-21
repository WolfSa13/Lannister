from utils import base64_encoder, resolve_function_name, invoke_lambda
from message_services import respond_with_error_return_menu, respond_with_menu

STATUS_CODE_200 = {
    "isBase64Encoded": True,
    "statusCode": 200,
    "headers": {},
    "body": ""
}


def lambda_handler(event, context):
    print(event)
    body = event['body']
    isBase64Encoded = event['isBase64Encoded']

    # check if event body was decoded
    if isBase64Encoded:
        body = base64_encoder(body)

    # when the command was called in the chat
    if 'command' in body and body['command'] == '/start':
        respond_with_menu(body['response_url'])

    # when the button was clicked in the chat
    elif body['type'] == 'block_actions':
        action_id = body['actions'][0]['action_id']
        lambda_to_invoke = action_id.split('_')[0]

        # when 'Return to main menu' button was clicked
        if action_id.startswith('start'):
            respond_with_menu(body['response_url'])

            return STATUS_CODE_200
        # check if correct action_id was sent
        elif lambda_to_invoke not in ['worker', 'request', 'bonus']:
            respond_with_error_return_menu(body['response_url'])

            return STATUS_CODE_200

        function_name = resolve_function_name(lambda_to_invoke)

        data = {
            "response_url": body['response_url'],
            "trigger_id": body['trigger_id'],
            "user": body['user'],
            "action_id": action_id
        }

        invoke_lambda(function_name, data)

    # when the modal was submitted
    elif body['type'] == 'view_submission':

        callback_id = body['view']['callback_id']
        lambda_to_invoke = callback_id.split('_')[0]

        # example 'arn:aws:lambda:us-east-1:740564522202:function:worker-lambda'
        function_name = resolve_function_name(lambda_to_invoke)

        data = {
            "body": body,
            "action_id": callback_id
        }

        invoke_lambda(function_name, data)

    return STATUS_CODE_200
