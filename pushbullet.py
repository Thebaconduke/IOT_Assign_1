#!/usr/bin/env python3
import requests
import json

#API key for Pushbullet
pushb = ("o.RAo2yNzKkriw0b9yZOhCxyIKjX3oxVLJ")

#Formatting and API
def push_notification(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}

    #API
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + pushb, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something went wrong, sorry')
    else:
        print('Sent warning')

#Main
def send_data():
    cold = "Make sure to bring a sweater"
    push_notification("Temperature warning", cold)
