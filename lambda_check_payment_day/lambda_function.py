import json
import requests
import os
import boto3
import datetime
from time_utils import *
from message_services import *
from orm_services import RequestQuery, UsersQuery, RequestHistoryQuery



def lambda_handler(event, context):
    region_name = os.environ.get('AWS_REGION')
    client = boto3.client("lambda", region_name=region_name)
    payload = {"Message": 'attachments'}
    resp = client.invoke(FunctionName='lambda_request_source', InvocationType="Event", Payload=json.dump(payload))

    return {
        'statusCode': 200
    }


