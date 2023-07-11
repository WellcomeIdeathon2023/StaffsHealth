import os
from pyngrok import ngrok
from twilio.rest import Client

from project_configs import PHONE_NUMBER_SID, ACCOUNT_SID, AUTH_TOKEN


if __name__ == '__main__':

    http_tunnel = ngrok.connect(5000)
    ngrok_webhook = http_tunnel.public_url + "/sms"

    print(ngrok_webhook)

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    all_phone_numbers = client \
        .incoming_phone_numbers.list()

    incoming_phone_number = client \
        .incoming_phone_numbers(PHONE_NUMBER_SID) \
        .update(sms_url=ngrok_webhook)
    # TODO: obfuscate SID

    while True:
        pass
