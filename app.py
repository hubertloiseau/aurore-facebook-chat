# -*- coding: utf-8 -*-
def main():
    pass

if __name__ == '__main__':
    main()
import os
import sys
import json
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
                    send_message(sender_id,ratp(message_text))                    
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    send_message(sender_id,ratp(message_text))
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
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

def ratp(destination):
    if destination:
        destination=destination.replace(" ","+").replace("-","+").lower()
    else:
        destination="massy+palaiseau"
    source = "gare+du+nord"
    r=requests.get("https://api-ratp.pierre-grimaud.fr/v2/rers/B/stations/"+source+"?destination=robinson+saint+remy+les+chevreuse&endingstation="+destination)
    if r.ok:
        r=r.json()
        horaire  = r['response']['schedules'][0]['message']
        return "Le prochain train a destination de "+destination.replace("+"," ")+" passera a "+source.replace("+"," ")+" a "+horaire
    else:
        return "Ecris correctement couillon ! Ou alors c'est peut etre moi qui deconne..."
if __name__ == '__main__':
    app.run(debug=True)

