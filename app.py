#!/usr/bin/env python3
import sys
import aws_cdk as cdk
from stacks.serverless_stack import ServerlessStack


app = cdk.App()
email = app.node.try_get_context("email")

if not email:
    email = "example@gmail.com" # default email for bootstrap and destory purpose

ServerlessStack(app, "HilaleeS3ListerStack", email=email) 
app.synth()
