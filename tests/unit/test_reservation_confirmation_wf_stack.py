import aws_cdk as core
import aws_cdk.assertions as assertions

from hotel_booking_wf.reservation_confirmation_wf_stack import ReservationConfirmationWfStack

# example tests. To run these tests, uncomment this file along with the example
# resource in reservation_confirmation_wf/reservation_confirmation_wf_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ReservationConfirmationWfStack(app, "reservation-confirmation-wf")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
