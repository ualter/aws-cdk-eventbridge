import os

from aws_cdk import (
    aws_apigateway as _apigw,
    aws_iam as _iam,
    aws_events as _events,
    core
)

class ApiGatewayStack(core.Construct):

    def __init__(self, scope: core.Construct, construct_id: str, apigw_role: _iam.Role, eventBus: _events.EventBus, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        #"mycdkappMyLanguageBusF9C152DE"

        integrationOptions = \
            _apigw.IntegrationOptions(
                credentials_role=apigw_role,
                request_parameters={
                    "integration.request.header.X-Amz-Target": "'AWSEvents.PutEvents'",
                    "integration.request.header.Content-Type": "'application/x-amz-json-1.1'",
                },
                request_templates={
                    "application/json":'{"Entries": [{"Source": "com.amazon.alexa.english", "Detail": "{ \\"key1\\": \\"value1\\", \\"key2\\": \\"value2\\" }",' + \
                                       ' "Resources": ["resource1", "resource2"], "DetailType": "myDetailType", "EventBusName": "' + eventBus.event_bus_name + '"}]}'
                },
                integration_responses=[_apigw.IntegrationResponse(
                    status_code="200",
                    response_templates={"application/json": ""},
                )]
            )
        

        # Integration API Gateway with EventBridge
        integrationEventBridge = _apigw.Integration(
            type=_apigw.IntegrationType("AWS"),
            integration_http_method="POST",
            options=integrationOptions,
            uri=f"arn:aws:apigateway:{os.environ['CDK_DEFAULT_REGION']}:events:path//"
        )

        myApi = _apigw.RestApi(self, construct_id)
        myApi.root.add_method("POST",
            integrationEventBridge,
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200"
                )
            ]
        )

        ## Lamdba Integration (Example)
        #my_api = apigateway.RestApi(self,"MyApi")
        #myfunction_integration = apigateway.LambdaIntegration(my_function)
        #test_resource = my_api.root.add_resource("test")
        #test_resource.add_method("GET", myfunction_integration)

        


