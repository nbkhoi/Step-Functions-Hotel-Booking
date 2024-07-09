from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks, Duration, CfnOutput
)
from constructs import Construct


class HotelBookingWfStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM role for Lambda
        role = iam.Role(self, "LambdaExecutionRole",
                        assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                        managed_policies=[
                            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                            iam.ManagedPolicy.from_aws_managed_policy_name(
                                "service-role/AWSLambdaVPCAccessExecutionRole")
                        ]
                        )

        # Create Lambda functions
        # Lambda function to receive booking request
        receive_booking_fn = _lambda.Function(self, "ReceiveBookingFn",
                                              runtime=_lambda.Runtime.PYTHON_3_11,
                                              handler="receive_booking_request_fn.handler",
                                              code=_lambda.Code.from_asset("lambda"),
                                              role=role
                                              )
        # Lambda function to confirm booking
        confirm_booking_fn = _lambda.Function(self, "ConfirmBookingFn",
                                              runtime=_lambda.Runtime.PYTHON_3_11,
                                              handler="confirm_booking_fn.handler",
                                              code=_lambda.Code.from_asset("lambda"),
                                              role=role
                                              )
        # Lambda function to send confirmation email
        send_confirmation_email_fn = _lambda.Function(self, "SendConfirmationEmailFn",
                                                      runtime=_lambda.Runtime.PYTHON_3_11,
                                                      handler="send_confirmation_email_fn.handler",
                                                      code=_lambda.Code.from_asset("lambda"),
                                                      role=role
                                                      )
        # Lambda function to send welcome email
        send_welcome_email_fn = _lambda.Function(self, "SendWelcomeEmailFn",
                                                 runtime=_lambda.Runtime.PYTHON_3_11,
                                                 handler="send_welcome_email_fn.handler",
                                                 code=_lambda.Code.from_asset("lambda"),
                                                 role=role
                                                 )
        send_reminder_email_fn = _lambda.Function(self, "SendReminderEmailFn",
                                                  runtime=_lambda.Runtime.PYTHON_3_11,
                                                  handler="send_reminder_email_fn.handler",
                                                  code=_lambda.Code.from_asset("lambda"),
                                                  role=role
                                                  )
        send_poststay_survey_fn = _lambda.Function(self, "SendPostStaySurveyFn",
                                                   runtime=_lambda.Runtime.PYTHON_3_11,
                                                   handler="send_poststay_survey_email_fn.handler",
                                                   code=_lambda.Code.from_asset("lambda"),
                                                   role=role
                                                   )
        # Lambda function to notify no availability
        notify_no_availability_fn = _lambda.Function(self, "NotifyNoAvailabilityFn",
                                                     runtime=_lambda.Runtime.PYTHON_3_11,
                                                     handler="notify_no_availability_fn.handler",
                                                     code=_lambda.Code.from_asset("lambda"),
                                                     role=role
                                                     )

        # Create steps for the state machine
        # Receiving booking request step
        receive_booking_request_step = sfn_tasks.LambdaInvoke(self, "Receive Booking Request",
                                                              lambda_function=receive_booking_fn,
                                                              output_path="$.Payload"
                                                              )

        # Check room availability step
        check_room_availability_step = sfn.Choice(self, "Room Available?")

        # Confirm booking step
        confirm_booking_step = sfn_tasks.LambdaInvoke(self, "Confirm Booking",
                                                      lambda_function=confirm_booking_fn,
                                                      output_path="$.Payload"
                                                      )

        # Send confirmation email step
        send_confirmation_email_step = sfn_tasks.LambdaInvoke(self, "Send Confirmation Email",
                                                              lambda_function=send_confirmation_email_fn,
                                                              output_path="$.Payload"
                                                              )

        # Send welcome email wait step
        # Wait until the time specified in the waitTimestamp before sending the welcome email
        send_welcome_email_wait_step = sfn.Wait(self, "Wait for Welcome Email",
                                                time=sfn.WaitTime.timestamp_path("$.waitTimestamp")
                                                )

        # Send welcome email step
        send_welcome_email_step = sfn_tasks.LambdaInvoke(self, "Send Welcome Email",
                                                         lambda_function=send_welcome_email_fn,
                                                         output_path="$.Payload"
                                                         )

        # Notify no availability step
        notify_no_availability_step = sfn_tasks.LambdaInvoke(self, "Notify No Availability",
                                                             lambda_function=notify_no_availability_fn,
                                                             output_path="$.Payload"
                                                             )

        # Define state machine
        definition = receive_booking_request_step.next(
            check_room_availability_step
            .when(sfn.Condition.boolean_equals("$.roomAvailable", True),
                  confirm_booking_step.next(send_confirmation_email_step).next(send_welcome_email_wait_step).next(
                      send_welcome_email_step))
            .otherwise(notify_no_availability_step)
        )

        state_machine = sfn.StateMachine(
            self, "HotelBookingStateMachine",
            definition=definition
        )

        CfnOutput(self, "StackName", value=self.stack_name)
        CfnOutput(self, "StateMachineArn", value=state_machine.state_machine_arn)

