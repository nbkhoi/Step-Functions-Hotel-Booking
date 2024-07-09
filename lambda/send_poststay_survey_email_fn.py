import json
import boto3


def handler(event, context):
    ses = boto3.client('ses')
    booking_details = event['bookingDetails']

    email_body = "We hope you enjoyed your stay. Please take a moment to complete our survey."

    response = ses.send_email(
        Source='thospitality.tma@gmail.com',
        Destination={'ToAddresses': [booking_details['email']]},
        Message={
            'Subject': {'Data': 'Post-Stay Survey'},
            'Body': {'Text': {'Data': email_body}}
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'emailSent': True})
    }
