# Booking Hotel Workflows - Step Functions Demo

---
This repository contains the source code for the Booking Hotel Workflows demo. This demo showcases how to use AWS Step Functions to orchestrate a workflow that books a hotel room.

---

## Architecture

The architecture of the Booking Hotel Workflows demo is shown below:

![Architecture](images/architecture.png)

## Prerequisites

To deploy the Booking Hotel Workflows demo, you need the following:

- An AWS account
- The AWS CLI installed
- The AWS CDK installed
- Python 3.11

## Deployment

To deploy the Booking Hotel Workflows demo, follow these steps:

1. Clone the GitHub repository:

    ```bash
    git clone
    ```
2. Change the directory:

    ```bash
    cd booking-hotel-workflows
    ```
3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4. Deploy the stack:

    ```bash
    cdk deploy
    ```
5. Confirm the deployment:

    ```bash
    Are you sure you want to deploy (y/n)?
    ```
6. Provide the confirmation:

    ```bash
    y
    ```
7. Wait for the stack to be deployed:

    ```bash
    booking-hotel-workflows: deploying...
    ```
8. View the resources created:

    ```bash
    Outputs:
    booking-hotel-workflows.StackName = <STACK_NAME>
    booking-hotel-workflows.StateMachineArn = <STATE_MACHINE_ARN>
    ```
9. Note the ARN of the state machine:

10. Update the state machine ARN in the `app.py` file:

    ```python
    state_machine_arn = "<STATE_MACHINE_ARN>"
    ```
11. Run the application:

    ```bash
    python app.py
    ```
12. View the output:

    ```bash
    {
        "booking_id": "1A2B3C4D5E6F",
        "status": "PENDING"
    }
    ```
13. View the state machine in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/states/home?region=us-east-1#/statemachines
    ```
14. View the state machine execution in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/states/home?region=us-east-1#/executions
    ```
15. View the state machine execution history in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/states/home?region=us-east-1#/executions/1A2B3C4D5E6F
    ```
16. View the state machine execution input and output in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/states/home?region=us-east-1#/executions/1A2B3C4D5E6F/input-output
    ```
17. View the state machine execution logs in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logStream:group=/aws/states/booking-hotel-workflows-BookingStateMachine-1A2B3C4D5E6F;stream=2022-01-01T00:00:00Z
    ```
18. View the state machine execution metrics in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#metricsV2:graph=~();namespace=AWS/States;dimensions=StateMachineArn;search=booking-hotel-workflows-BookingStateMachine-1A2B3C4D5E6F
    ```
19. View the state machine execution alarms in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#alarmsV2:alarmState=ALARM;search=booking-hotel-workflows-BookingStateMachine-1A2B3C4D5E6F
    ```
20. View the state machine execution events in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/eventbridge/home?region=us-east-1#/events
    ```
21. View the state machine execution notifications in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/topics
    ```
22. View the state machine execution history in the AWS Management Console:

    ```bash
    https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=booking-hotel-workflows-BookingHistoryTable;tab=items
    ```
