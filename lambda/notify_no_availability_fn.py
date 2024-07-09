import json
import boto3


def handler(event, context):
    ses = boto3.client('ses')
    booking_details = event['bookingRequest']

    email_body = "Unfortunately, there are no rooms available for your requested dates."

    response = ses.send_email(
        Source='thospitality.tma@gmail.com',
        Destination={'ToAddresses': [booking_details['email']]},
        Message={
            'Subject': {'Data': 'No Room Availability'},
            'Body': {'Text': {'Data': email_body}}
        }
    )

    return {
        "emailResponse": response,
        "bookingRequest": booking_details
    }
