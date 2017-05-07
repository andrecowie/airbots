from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

account_sid = "ACab2ad5eeee1967081363cd2b768a07c5"
auth_token  = "8c6ef3b6bf1259204d5eb1d76770f7da"

client = TwilioRestClient(account_sid, auth_token)
phone = "+64210521138"
name = "Babara Gordon"

try:
	message = client.messages.create(body="Thanks "+name+" for helping to save NZ's native birdlife. - Team @ Squawk Squad",
	    to=phone,    # Replace with customer's number
	    from_="+12044008064") # Twilio number
except TwilioRestException as e:
	print(e)