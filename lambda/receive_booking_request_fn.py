import json


def handler(event, context):
    booking_request = event["bookingRequest"]
    print(f"Received booking request: {booking_request}")
    # Code handling the booking request
    # is_available true if room type is STANDARD, false otherwise
    is_available = booking_request['roomType'] == 'STANDARD'

    return {
        "roomAvailable": is_available,
        "bookingRequest": booking_request
    }
