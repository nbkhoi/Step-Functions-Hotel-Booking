import json
import boto3
from datetime import datetime, timedelta


def handler(event, context):
    ses = boto3.client('ses')
    booking_details = event['bookingDetails']
    confirmation_number = event['confirmationNumber']
    email_body = f"Your booking is confirmed. Confirmation number: {confirmation_number}"

    response = ses.send_email(
        Source='thospitality.tma@gmail.com',
        Destination={'ToAddresses': [booking_details['email']]},
        Message={
            'Subject': {'Data': 'Booking Confirmation'},
            'Body': {'Text': {'Data': email_body}}
        }
    )
    
    check_in_date = datetime.strptime(booking_details['checkInDate'], '%Y-%m-%d')
    waitTimestamp = (check_in_date - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    return {
        "bookingDetails": booking_details,
        "waitTimestamp": waitTimestamp
    }
