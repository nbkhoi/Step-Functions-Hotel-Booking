import json


def handler(event, context):
    booking_request = event["bookingRequest"]
    # Logic to handle booking request
    return {
        "confirmationNumber": "1234567890",
        "bookingDetails": booking_request
    }
