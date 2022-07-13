import json
import boto3

from services import base64_encoder, respond_with_error_return_menu, respond_with_menu

function_ARN = 'arn:aws:lambda:us-east-1:740564522202:function:'

# DO NOT CHANGE ANYTHING!
status_code_200 = {
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

    # when the command was called in the chat
    if 'command' in body and body['command'] == '/start':
        respond_with_menu(body['response_url'])

    # when the button was clicked in the chat
    elif body['type'] == 'block_actions':
        action_id = body['actions'][0]['action_id']

        # when 'Return to main menu' button was clicked
        if action_id.startswith('start'):
            respond_with_menu(body['response_url'])
            return status_code_200

        # check if correct action_id was sent
        elif action_id.split('_')[0] not in ['worker', 'request', 'bonus']:
            respond_with_error_return_menu(body['response_url'])
            return status_code_200

        # example: worker-lambda, request-lambda, bonus-lambda
        lambda_name = action_id.split('_')[0] + '-lambda'

        # example 'arn:aws:lambda:us-east-1:740564522202:function:workers-lambda'
        function_name = function_ARN + lambda_name

        client = boto3.client('lambda')

        data = {
            "response_url": body['response_url'],
            "trigger_id": body['trigger_id'],
            "user": body['user'],
            "action_id": action_id
        }

        response = client.invoke(
            FunctionName=function_name,
            InvocationType='Event',
            Payload=json.dumps(data)
        )

    # when the modal was submitted
    elif body['type'] == 'view_submission':

        callback_id = body['view']['callback_id']

        # example: worker-lambda, request-lambda, bonus-lambda
        lambda_name = callback_id.split('_')[0] + '-lambda'

        # example 'arn:aws:lambda:us-east-1:740564522202:function:workers-lambda'
        function_name = function_ARN + lambda_name

        client = boto3.client('lambda')

        data = {
            "body": body,
            "action_id": callback_id
        }

        response = client.invoke(
            FunctionName=function_name,
            InvocationType='Event',
            Payload=json.dumps(data)
        )

    # return 200 OK status
    return status_code_200
