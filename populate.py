import requests
import datetime
import time
import calendar
import argparse
import base64
from flask import Flask, request, jsonify
import flask
import json

parser = argparse.ArgumentParser(
    description='Incremental export of Zendesk tickets.')
parser.add_argument('email', type=str,
                    help='Your Zendesk email account')
parser.add_argument('api_token', type=str,
                    help='Your Zendesk API token')
parser.add_argument('subdomain', type=str, help='Your Zendesk subdomain')

args = parser.parse_args()
email = args.email
api_token = args.api_token
subdomain = args.subdomain

url = "https://{}.zendesk.com".format(subdomain)
auth = "{}/token:{}".format(email, api_token)
send_auth = base64.b64encode(auth.encode()).decode()
post_api = "/api/v2/tickets/create_many.json"

data = {"tickets": []}

for i in range(100):
    data["tickets"].append({"subject": str(i), "comment":  {
        "body": "The smoke is very colorful."}, "priority": "normal"})

data = json.dumps(data)
response = requests.post(url + post_api,
                         headers={'Authorization': 'Basic {}'.format(send_auth), 'Content-Type': 'application/json'}, data=data)

print(response.text)
print(response.status_code)
