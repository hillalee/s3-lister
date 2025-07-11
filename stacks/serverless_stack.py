from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
)
from constructs import Construct
from aws_cdk import aws_s3_deployment as s3deploy



class ServerlessStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, 
                 email: str, files_to_upload: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # create S3 bucket
        bucket = s3.Bucket(self, "hilaleeBucket")
        print(f"Created bucket: {bucket.bucket_name}")


        # create SNS topic
        topic = sns.Topic(self, "hilaleeTopic")
        print(f"Created topic: {topic.topic_arn}")

        # TODO: best practice?
        email = self.node.try_get_context("email")
        if not email:
            raise Exception("You must pass -c email=your@email.com")

        topic.add_subscription(subscriptions.EmailSubscription(email))

        # create Lambda function
        lambda_function = _lambda.Function(
            self, "hilaleeFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TOPIC_ARN": topic.topic_arn
            }
        )

        # grant lambda permissions
        bucket.grant_read(lambda_function)
        topic.grant_publish(lambda_function)
        
        
        # # deploy files to S3 bucket  
        # s3deploy.BucketDeployment(
        #     self, "DeploySampleFiles",
        #     sources=[s3deploy.Source.asset("./sample_files")],  # local folder path
        #     destination_bucket=bucket
        # )
