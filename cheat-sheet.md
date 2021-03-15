python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install --upgrade virtualenv

source .venv/bin/activate
pip install aws_cdk.aws_events_targets
cdk synth