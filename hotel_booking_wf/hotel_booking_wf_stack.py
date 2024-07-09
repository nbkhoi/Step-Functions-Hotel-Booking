from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks, Duration, CfnOutput,
    aws_apigatewayv2 as apigateways,
    aws_apigatewayv2_integrations as integrations
)
from constructs import Construct


class HotelBookingWfStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM role for Lambda
        role = iam.Role(self, "LambdaExecutionRole",
                        role_name=f"{self.stack_name}-lambda-execution-role",
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
                                              function_name=f"{self.stack_name}-receive-booking-fn",
                                              runtime=_lambda.Runtime.PYTHON_3_11,
                                              handler="receive_booking_request_fn.handler",
                                              code=_lambda.Code.from_asset("lambda"),
                                              role=role
                                              )
        # Lambda function to confirm booking
        confirm_booking_fn = _lambda.Function(self, "ConfirmBookingFn",
                                              function_name=f"{self.stack_name}-confirm-booking-fn",
                                              runtime=_lambda.Runtime.PYTHON_3_11,
                                              handler="confirm_booking_fn.handler",
                                              code=_lambda.Code.from_asset("lambda"),
                                              role=role
                                              )
        # Lambda function to send confirmation email
        send_confirmation_email_fn = _lambda.Function(self, "SendConfirmationEmailFn",
                                                      function_name=f"{self.stack_name}-send-confirmation-email-fn",
                                                      runtime=_lambda.Runtime.PYTHON_3_11,
                                                      handler="send_confirmation_email_fn.handler",
                                                      code=_lambda.Code.from_asset("lambda"),
                                                      role=role
                                                      )
        # Lambda function to send welcome email
        send_welcome_email_fn = _lambda.Function(self, "SendWelcomeEmailFn",
                                                 function_name=f"{self.stack_name}-send-welcome-email-fn",
                                                 runtime=_lambda.Runtime.PYTHON_3_11,
                                                 handler="send_welcome_email_fn.handler",
                                                 code=_lambda.Code.from_asset("lambda"),
                                                 role=role
                                                 )
        # Lambda function to notify no availability
        notify_no_availability_fn = _lambda.Function(self, "NotifyNoAvailabilityFn",
                                                     function_name=f"{self.stack_name}-notify-no-availability-fn",
                                                     runtime=_lambda.Runtime.PYTHON_3_11,
                                                     handler="notify_no_availability_fn.handler",
                                                     code=_lambda.Code.from_asset("lambda"),
                                                     role=role
                                                     )

        # Create steps for the state machine
        # Receiving booking request step
        receive_booking_request_step = sfn_tasks.LambdaInvoke(self, "Receive Booking Request",
                                                              state_name=f"{self.stack_name}-receive-booking-request-step",
                                                              lambda_function=receive_booking_fn,
                                                              output_path="$.Payload"
                                                              )

        # Check room availability step
        check_room_availability_step = sfn.Choice(self, "Room Available?",
                                                  state_name=f"{self.stack_name}-room-available-step"
                                                  )

        # Confirm booking step
        confirm_booking_step = sfn_tasks.LambdaInvoke(self, "Confirm Booking",
                                                      state_name=f"{self.stack_name}-confirm-booking-step",
                                                      lambda_function=confirm_booking_fn,
                                                      output_path="$.Payload"
                                                      )

        # Send confirmation email step
        send_confirmation_email_step = sfn_tasks.LambdaInvoke(self, "Send Confirmation Email",
                                                              state_name=f"{self.stack_name}-send-confirmation-email-step",
                                                              lambda_function=send_confirmation_email_fn,
                                                              output_path="$.Payload"
                                                              )

        # Send welcome email wait step
        # Wait until the time specified in the waitTimestamp before sending the welcome email
        send_welcome_email_wait_step = sfn.Wait(self, "Wait for Welcome Email",
                                                state_name=f"{self.stack_name}-wait-for-welcome-email-step",
                                                time=sfn.WaitTime.timestamp_path("$.waitTimestamp")
                                                )

        # Send welcome email step
        send_welcome_email_step = sfn_tasks.LambdaInvoke(self, "Send Welcome Email",
                                                         state_name=f"{self.stack_name}-send-welcome-email-step",
                                                         lambda_function=send_welcome_email_fn,
                                                         output_path="$.Payload"
                                                         )

        # Notify no availability step
        notify_no_availability_step = sfn_tasks.LambdaInvoke(self, "Notify No Availability",
                                                             state_name=f"{self.stack_name}-notify-no-availability-step",
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
            state_machine_name=f"{self.stack_name}-state-machine",
            definition=definition
        )

        role.add_to_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=[
                    "arn:aws:ses:ap-southeast-1:021492533335:identity/nbaokhoi@icloud.com",
                    "arn:aws:ses:ap-southeast-1:021492533335:identity/*"]
            )
        )
        # Lambda function to execute booking workflow
        execute_booking_workflow_fn = _lambda.Function(self, "ExecuteBookingWorkflowFn",
                                                       function_name=f"{self.stack_name}-execute-booking-workflow-fn",
                                                       runtime=_lambda.Runtime.PYTHON_3_11,
                                                       handler="execute_booking_workflow_fn.handler",
                                                       code=_lambda.Code.from_asset("lambda"),
                                                       environment={
                                                           "STATE_MACHINE_ARN": state_machine.state_machine_arn
                                                       }
                                                       )

        # Grant permission to the Lambda function to start the state machine
        state_machine.grant_start_execution(execute_booking_workflow_fn)
        # Create HTTP API Gateway
        http_api = apigateways.HttpApi(self, "HotelBookingApi",
                                       api_name=f"{self.stack_name}-api"
                                       )

        # Add integration for the API Gateway
        http_api_integration = integrations.HttpLambdaIntegration(id="BookingIntegration",
                                                                  handler=execute_booking_workflow_fn
                                                                  )
        # Add route for the API Gateway
        http_api.add_routes(path="/booking", methods=[apigateways.HttpMethod.POST], integration=http_api_integration)

        # Output the URL of the API Gateway
        CfnOutput(self, "ApiUrl", value=http_api.url, description="HTTP API url to execute the booking workflow")
        CfnOutput(self, "StackName", value=self.stack_name)
        CfnOutput(self, "StateMachineArn", value=state_machine.state_machine_arn)
