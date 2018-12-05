# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACebd8e81956561265e06c86305bed368b'
auth_token = '1be5675a03a7daaa531088bda068a5a3'
client = Client(account_sid, auth_token)

def send():
    message = client.messages.create(
                              body='You need to restart the timer.',
                              from_='+19184714362',
                              to='+14055864014'
                          )