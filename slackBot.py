import os
import time
from slackclient import SlackClient
from dotenv import load_dotenv

load_dotenv('.env')

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

# def create_user_list:

def handle_event(event):
  if event['type'] == "message":
    handle_message(event)
  elif event['type'] == "presence_change":
    handle_presence_change(event)

def handle_message(event):
  print("Got message '" + event['text'] + "' from '" + event['user'] + "'")
  say_hello(event)

def handle_presence_change(event):
  print("Status change for ", event['user'])

def say_hello(event):
  if (event['text'].lower() == 'hello' or event['text'].lower() == 'hi'):
    response = sc.api_call(
      "users.info",
      user=event['user']
    )
    displayName = response['user']['profile']['display_name']
    realName = response['user']['real_name']
    if(displayName != ''):
      sc.api_call(
          "chat.postMessage",
          channel=event['channel'],
          text=  "Hi " + displayName + "! :tada:"
      )
    else:
      sc.api_call(
          "chat.postMessage",
          channel=event['channel'],
          text=  "Hi " + realName + "! :tada:"
      )

if sc.rtm_connect():
    print("StarterBot connected and running!")
    while True:
        events = sc.rtm_read()

        for event in events:
          handle_event(event)

        time.sleep(1)
