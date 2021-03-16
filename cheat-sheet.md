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

ENDPOINT=https://9bvduztml5.execute-api.us-west-2.amazonaws.com/prod/
curl -X POST $ENDPOINT
```