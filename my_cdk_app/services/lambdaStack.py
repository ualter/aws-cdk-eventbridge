from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_sns_subscriptions as subs,
    core
)

class LambdaStack(core.Construct):

    @property
    def lambdaEventBusRuleTarget(self):
        return self._eventBusRuleTarget
    
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self._eventBusRuleTarget = _lambda.Function(
            self, "MyEventProcessor",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            #code=_lambda.InlineCode("def main(event, context):\n\tprint(event)\n\treturn {'statusCode': 200, 'body': 'Hello, World'}"),
            handler='eventHandler.handler',
        )
    
    