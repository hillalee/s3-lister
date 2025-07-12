from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_s3_notifications as s3n,aws_s3_notifications as s3n,
    CfnOutput
)

from constructs import Construct



class ServerlessStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, 
                 email: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # create S3 bucket
        bucket = s3.Bucket(self, "hilalee-s3-bucket")


        # create SNS topic
        topic = sns.Topic(self, "hilalee-sns-topic")

        # add email subscription to the topic
        topic.add_subscription(subscriptions.EmailSubscription(email))

        
        # define iam role for lambda function - should only be able to use stacks resources
        iam_role = iam.Role(
            self, "hilaleeLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role for Lambda function to access S3 bucket and SNS topic",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )
        
        # add permissions to the role
        iam_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:ListBucket"],
            resources=[bucket.bucket_arn]
        ))
        iam_role.add_to_policy(iam.PolicyStatement(
            actions=["sns:Publish"],
            resources=[topic.topic_arn]
        ))
        
        # create lambda function with iam role
        lambda_function = _lambda.Function(
            self, "hilalee-lambda-s3-lister",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TOPIC_ARN": topic.topic_arn
            },
            role=iam_role)
        
        # EXTRA FEATURE: adds a trigger - lambda is invoked whenever new files are uploaded to the bucket
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(lambda_function)
        )
                
        CfnOutput(self, "BucketNameOutput",
                   value=bucket.bucket_name,
                   description="The name of the S3 bucket",
                   export_name="BucketName")
        CfnOutput(self, "TopicArnOutput",
                   value=topic.topic_arn,
                   description="The ARN of the SNS topic",
                   export_name="TopicArn")
        CfnOutput(self, "LambdaFunctionNameOutput",
                   value=lambda_function.function_name,
                   description="The name of the Lambda function",
                   export_name="LambdaFunctionName")
        
    
