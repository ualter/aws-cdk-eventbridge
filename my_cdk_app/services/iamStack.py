from aws_cdk import (
    aws_iam as _iam,
    aws_events as _events,
    core
)

class IamStack(core.Construct):

    @property
    def apiGatewayRole(self):
        return self._apiGatewayRole

    def __init__(self, scope: core.Construct, construct_id: str, eventBus: _events.EventBus,  **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.createRoleAPIGateway(eventBus)

    
    def createRoleAPIGateway(self, eventBus):
        #Create Role for API Gateway to write in our created EventBus
        policyStatement = _iam.PolicyStatement(
            actions=["events:PutEvents"],
            #resources=["arn:aws:events:eu-central-1:411078575449:event-bus/mycdkappMyLanguageBusF9C152DE"]
            resources=[eventBus.event_bus_arn],
        )
        polices = [_iam.PolicyDocument(
            statements=[policyStatement]
        )]
        self._apiGatewayRole = _iam.Role(
             self,"MyAPIGWRole",
             assumed_by=_iam.ServicePrincipal(service="apigateway"),
             inline_policies=polices
        )
        
