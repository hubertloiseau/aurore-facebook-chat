#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Bot-Father
#
# Created:     04/01/2017
# Copyright:   (c) Bot-Father 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
import os
import sys
import json
from python_simsimi import SimSimi
from python_simsimi.language_codes import LC_ENGLISH
from python_simsimi.simsimi import SimSimiException
simSimi = SimSimi(
        conversation_language=LC_ENGLISH,
        conversation_key='16df5864-cfe2-4ae0-bec3-1881cc6149fb',
        conversation_request_url = 'http://sandbox.api.simsimi.com/request.p'
)

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "VERIFY_TOKEN":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    
                    try:
                        response = simSimi.getConversation(messaging_event["message"]["text"])
                        print response['response']
                        send_message(sender_id, response['response'])
                    except SimSimiException as e:
                        send_message(sender_id, "loi me no roi")
                    
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": "EAABc3XZBFDi8BABGFg9ZBOlzhYCGmhZAUjJERMyJojnfkUTtnbByFY3hw0ai7WhkIGlWgu9nYrxaRlkcIc46gPe8GJcuZCIZBWqUbQQObX7J8D9gl3SVIlUL3ZCZCzHkZBfoZAfapQ47eKjP9tOBAdSJ9mrZAuzUc663i3RipIERtILAZDZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_greetings(greeting_text):
	log("sending greetings")
	params = {
		"access_token": os.environ["PAGE_ACCESS_TOKEN"]
	}
	headers = {
		"Content-Type": "application/json"
	}
        
	data = json.dumps({
	"greeting": {
		"text": greeting_text
		}
	})
	r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=data)
	if r.status_code != 200:
		log(r.status_code)
		log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
