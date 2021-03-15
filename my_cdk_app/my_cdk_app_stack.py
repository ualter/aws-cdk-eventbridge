from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_sns_subscriptions as subs,
    core
)

class MyCdkAppStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        myLambda = _lambda.Function(
            self, "MyEventProcessor",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            #code=_lambda.InlineCode("def main(event, context):\n\tprint(event)\n\treturn {'statusCode': 200, 'body': 'Hello, World'}"),
            handler='eventHandler.handler',
        )

        myEventBus = _events.EventBus(self, "MyLanguageBus")
        core.CfnOutput(self, 
           "BusName",
           description="Event Bus Name",
           value=myEventBus.event_bus_name
        )

        myRule = _events.Rule(self, "LambdaProcessorRule",
            rule_name="MyRule",
            event_bus=myEventBus,
            event_pattern=_events.EventPattern(source=['com.amazon.alexa.english']),
            targets=[_targets.LambdaFunction(myLambda)]
        )

        core.CfnOutput(self, 
           "MyRule",
           description="MyRule",
           value=myRule.rule_name
        )
