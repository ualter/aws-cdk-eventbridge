#!/usr/bin/env python3

from aws_cdk import core

from my_cdk_app.my_cdk_app_stack import MyCdkAppStack


app = core.App()
MyCdkAppStack(app, "my-cdk-app", env={'region': 'eu-central-1'})

app.synth()
