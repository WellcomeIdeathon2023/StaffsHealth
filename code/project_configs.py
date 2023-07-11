import os

# Project level configurations.  Please set this up for the individual workload.

PHONE_NUMBER_SID = None
ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

if not PHONE_NUMBER_SID:
    raise(ConnectionError("Twillio API phone number not set.  Check project_config file"))