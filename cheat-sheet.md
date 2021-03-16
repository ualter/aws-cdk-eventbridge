```bash
# Just in case, might be useful
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install --upgrade virtualenv
python3 -m venv .venv


# Used Commands
source .venv/bin/activate
pip install aws_cdk.aws_events_targets
cdk bootstrap  # Check CloudFormation Stack if CDKToolkit stack (S3 Buckts) is already generated for the underline AWS Account/region
cdk list
cdk synth
cdk deploy
cdk destroy


# Testing
# Don't forget to change the Eventbus Name before, accordingly with the output of the "cdk deploy"
aws events put-events --entries file://putevents.json

# V1 API Gateway
ENDPOINT=https://9bvduztml5.execute-api.us-west-2.amazonaws.com/prod/
curl -X POST $ENDPOINT

# V2 API Gateway
# Valid Re (Defined Model Respected)
curl ${ENDPOINT}english --header 'Content-type:application/json' --data '{"UserID":"1234567","LanguageName":"en-us"}'
curl ${ENDPOINT}french --header 'Content-type:application/json' --data '{"UserID":"abcdefg","LanguageName":"en-gb"}'

# Invalid Request (Defined Model Disrespected)
# UserID is missing
curl ${ENDPOINT}english --header 'Content-type:application/json' --data '{"LanguageName":"en-us"}'
# UserID is the wrong 'type'
curl ${ENDPOINT}french --header 'Content-type:application/json' --data '{"UserID":100,"LanguageName":"en-gb"}'
# LanguageName is missing
curl ${ENDPOINT}english --header 'Content-type:application/json' --data '{"UserID":"1234567"}'
# LanguageName doesn't match the pattern we specified
curl ${ENDPOINT}french --header 'Content-type:application/json' --data '{"UserID":"abcdefg","LanguageName":"aaa-bb"}'


# V3 WebSocket
# To Test (site online connection WebSocket)
https://www.websocket.org/echo.html

Location: URL of the WebSocket API Gateway
Messages: 
{"UserID":"1234567","language":"english"}
{"UserID":"1234567","language":"german"}
{"UserID":"1234567","language":"french"}

```