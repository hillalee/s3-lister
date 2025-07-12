#!/usr/bin/env python3
import sys
import aws_cdk as cdk
from stacks.serverless_stack import ServerlessStack


app = cdk.App()

skip_check = app.node.try_get_context("skip_email")
email = app.node.try_get_context("email")

if skip_check:
    email = "example@gmail.com" # default email for bootstrap purpose
elif not email: 
    raise Exception("Please provide an email with -c email=your@email.com")

ServerlessStack(app, "HilaleeS3ListerStack", email=email) #, files_to_upload=files_to_upload)
app.synth()
