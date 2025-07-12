import boto3
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    sns = boto3.client('sns')

    bucket = os.environ["BUCKET_NAME"]
    topic = os.environ["TOPIC_ARN"]

    response = s3.list_objects_v2(Bucket=bucket)
    files = [obj['Key'] for obj in response.get('Contents', [])]
    message = "\n".join(files) if files else "Bucket is empty"
    if message != "Bucket is empty":
        message = "The following files are in the bucket {bucket}:\n\n" + message
    message += "You got this messgae because a Lambda function was invoked.\n"
    message += "\n\n made with ❤️ by Hilalee - linkedin.com/in/hilalee"

    sns.publish(TopicArn=topic, Message=message, Subject=f"S3 Bucket Contents")

    return {"status": "success", "files": files}
