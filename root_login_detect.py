
def lambda_handler(event, context):
    try:
        # Check if 'detail' exists in the event
        if 'detail' not in event:
            raise KeyError('detail')

        # Extract event details
        user_identity = event['detail'].get('userIdentity', {})
        user_name = user_identity.get('userName', 'Unknown')
        event_time = event.get('time', 'Unknown')

        # Format the message
        message = f"Root login detected:\n\nUser: {user_name}\nTime: {event_time}\nEvent: ConsoleLogin"

        # Publish to SNS
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject="Root Login Detected",
            MessageGroupId="RootLoginGroup"  # Required for FIFO topics
        )

        # Log response (for debugging purposes)
        print(f"SNS Response: {response}")
        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully')
        }
    except KeyError as e:
        # Log the missing key for debugging
        print(f"KeyError: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Missing key in event: {e}")
        }
    except Exception as e:
        # Catch-all for any other exceptions
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal server error: {e}")
        }
