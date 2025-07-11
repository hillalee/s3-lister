#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.serverless_stack import ServerlessStack


app = cdk.App()

email = app.node.try_get_context("email")
if not email:
    raise Exception("Please provide an email with -c email=your@email.com")
# files_to_upload = "./sample_files"

ServerlessStack(app, "ServerlessS3ListerStack", email=email) #, files_to_upload=files_to_upload)
app.synth()
