import os

from aws_cdk import (
    aws_apigatewayv2 as _apigwv2,
    aws_iam as _iam,
    aws_events as _events,
    core
)

class WebSocketApiGtwStack(core.Construct):

    def __init__(self, scope: core.Construct, construct_id: str, apigw_role: _iam.Role, eventBus: _events.EventBus, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        myApi = _apigwv2.CfnApi(self, construct_id,
            protocol_type="WEBSOCKET",
            route_selection_expression="${request.body.language}",
            name=construct_id
        )

        integration = _apigwv2.CfnIntegration(self, "EventBusIntegration",
            api_id=myApi.ref,
            integration_type="AWS",
            integration_method="POST",
            integration_uri=f"arn:aws:apigateway:{os.environ['CDK_DEFAULT_REGION']}:events:path//",
            credentials_arn=apigw_role.role_arn,
            template_selection_expression="application/json",
            request_parameters={
                    "integration.request.header.X-Amz-Target": "'AWSEvents.PutEvents'",
                    "integration.request.header.Content-Type": "'application/x-amz-json-1.1'",
            },
            request_templates={
                "application/json":'#set($language=$input.params(\'language\'))\n{"Entries": [{"Source": "com.amazon.alexa.$language",' + \
                                       ' "Detail": "$util.escapeJavaScript($input.body)",' + \
                                       ' "Resources": ["resource1", "resource2"], ' + \
                                       ' "DetailType": "myDetailType", "EventBusName": "' + eventBus.event_bus_name + '"}]}'
            }
        )

        germanRoute = _apigwv2.CfnRoute(self, "MyGermanRoute",
            api_id=myApi.ref,
            route_key="german",
            target=f"integrations/{integration.ref}",
            route_response_selection_expression='$default'
        )

        genericIntegrationResponse = _apigwv2.CfnIntegrationResponse(self, "genericIntegrationResponse",
            api_id=myApi.ref,
            integration_id=integration.ref,
            integration_response_key="/200/"
        )

        genericRouteResponse = _apigwv2.CfnRouteResponse(self, "genericRouteResponse",
            api_id=myApi.ref,
            route_id=germanRoute.ref,
            route_response_key="$default"
        )

        defaultRoute = _apigwv2.CfnRoute(self, "MyDefaultRoute",
            api_id=myApi.ref,
            route_key="$default",
            target=f"integrations/{integration.ref}",
        )

        myStage = _apigwv2.CfnStage(self, "MyStage",
            api_id=myApi.ref,
            stage_name="prod",
            auto_deploy=True
        )
        myStage.add_depends_on(defaultRoute)
        myStage.add_depends_on(germanRoute)
        myStage.add_depends_on(genericIntegrationResponse)

        core.CfnOutput(self, 
           "APIEndpoint",
           description="APIEndpoint",
           value=f"wss://{myApi.ref}.execute-api.{os.environ['CDK_DEFAULT_REGION']}.amazonaws.com/prod"
        )





