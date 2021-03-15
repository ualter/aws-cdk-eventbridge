from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_sns_subscriptions as subs,
    core
)

class EventBridgeStack(core.Construct):

    @property
    def eventBus(self):
        return self._eventBus

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self._eventBus = _events.EventBus(self, "MyLanguageBus")
    
    def createRule(self, id: str, name: str, eventPattern: str, _targets):
        return _events.Rule(self, id,
            rule_name=name,
            event_bus=self._eventBus,
            event_pattern=_events.EventPattern(source=[eventPattern]),
            targets=_targets
        )