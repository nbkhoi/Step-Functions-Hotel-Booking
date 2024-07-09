import json
import os

import boto3

sfs = boto3.client('stepfunctions')


def handler(event, context):
    booking_request = json.loads(event["body"])["bookingRequest"]
    sfs.start_execution(
        stateMachineArn=os.getenv('STATE_MACHINE_ARN'),
        input=json.dumps({
            "bookingRequest": booking_request
        })
    )
    return {
        "statusCode": 200,
        "body": json.dumps("Execution started")
    }
