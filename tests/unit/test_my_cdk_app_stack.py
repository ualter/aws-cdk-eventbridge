import json
import pytest

from aws_cdk import core
from my_cdk_app.my_cdk_app_stack import MyCdkAppStack


def get_template():
    app = core.App()
    MyCdkAppStack(app, "my-cdk-app")
    return json.dumps(app.synth().get_stack("my-cdk-app").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
