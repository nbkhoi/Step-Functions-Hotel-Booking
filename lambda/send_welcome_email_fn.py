import json
import boto3


def handler(event, context):
    ses = boto3.client('ses')
    booking_details = event['bookingDetails']

    email_body = "Welcome! Here is some information about your stay."

    response = ses.send_email(
        Source='thospitality.tma@gmail.com',
        Destination={'ToAddresses': [booking_details['email']]},
        Message={
            'Subject': {'Data': 'Welcome Information'},
            'Body': {'Text': {'Data': email_body}}
        }
    )

    return {
        "bookingDetails": booking_details
    }
