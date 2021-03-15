from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_sns_subscriptions as subs,
    core
)

from services.lambdaStack import LambdaStack
from services.eventBridgeStack import EventBridgeStack

class MyCdkAppStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambdaStack   = LambdaStack(self, "MyEventProcessor")
        myLanguageBus = EventBridgeStack(self,"MyLanguageBus")

        core.CfnOutput(self, 
           "BusName",
           description="Event Bus Name",
           value=myLanguageBus.eventBus.event_bus_name
        )

        myRule = myLanguageBus.createRule(
            id="LambdaProcessorRule",
            name="MyRule",
            eventPattern="com.amazon.alexa.english",
            _targets=[_targets.LambdaFunction(lambdaStack.lambdaEventBusRuleTarget)]

        )

        core.CfnOutput(self, 
           "MyRule",
           description="MyRule",
           value=myRule.rule_name
        )
