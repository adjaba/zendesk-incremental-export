import requests
import datetime
import time
import calendar
import argparse
import base64
from flask import Flask, render_template, jsonify
import flask
import json

app = Flask(__name__, template_folder='templates')

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

# parse times
start_time = "15-12-2019 12:00 PM +0000"
start = datetime.datetime.strptime(
    start_time, "%d-%m-%Y %H:%M %p %z")
start_unix = calendar.timegm(start.timetuple())

end_time = "10-01-2020 12:00 PM +0000"
end = datetime.datetime.strptime(
    end_time, "%d-%m-%Y %H:%M %p %z")
end_unix = calendar.timegm(end.timetuple())

# req params
url = "https://{}.zendesk.com".format(subdomain)
start_api = "/api/v2/incremental/tickets/cursor.json?start_time={}"
cursor_api = "/api/v2/incremental/tickets/cursor.json?cursor={}"
auth = "{}/token:{}".format(email, api_token)
send_auth = base64.b64encode(auth.encode()).decode()

# request
results = []


def processTickets(results, ticketlist):
    """
    appends to results tickets that were created on and before end_unix \n
    returns updated results
    """
    for ticket in ticketlist:
        created_time = calendar.timegm(datetime.datetime.strptime(
            ticket["created_at"], '%Y-%m-%dT%H:%M:%SZ').timetuple())

        if start_unix <= created_time < end_unix:
            results.append(
                {"id": ticket['id'], "subject": ticket["subject"], "description": ticket['description'], "created_at": datetime.datetime.utcfromtimestamp(created_time).strftime('%b %d, %Y %H:%M:%S')})
    return results


def finish(results):
    results.sort(key=lambda ticket: int(ticket["id"]))
    return jsonify({"tickets": results})
    # with open('results.json', 'w') as f:
    #     json.dump(results, f)
    # exit()


def processResponse(response, results, get_cursor=None):
    """
    given a response, update results appropriately, wait if needed, and return the next cursor and whether or not to continue
    """
    print("processing cursor", get_cursor)

    go_on = True
    # rate limit
    if response.status_code == 429:
        print("Waiting...")
        time.sleep(int(response.headers['Retry-After']))
        return get_cursor, go_on

    # if error encountered, exit
    if response.status_code != 200:
        print('Status:', response.status_code,
              'Problem with the request. Exiting')
        go_on = False

    data = response.json()
    results = processTickets(results, data['tickets'])
    new_cursor = data["after_cursor"]

    if data["end_of_stream"]:
        go_on = False

    return new_cursor, go_on


@app.route("/", methods=["GET"])
def generate():
    """
    sends in json format - id, subject, description, and created_at fields of each ticket created within the aforementioned time range; the output tickets should be sorted by increasing created_at time
    """
    results = []
    response = requests.get(url + start_api.format(start_unix),
                            headers={'Authorization': 'Basic {}'.format(send_auth)})
    get_cursor, go_on = processResponse(response, results)

    while go_on:
        response = requests.get(url + cursor_api.format(get_cursor),
                                headers={'Authorization': 'Basic {}'.format(send_auth)})

        get_cursor, go_on = processResponse(
            response, results, get_cursor)

    results.sort(key=lambda ticket: int(ticket["id"]))
    with open('results.json', 'w') as f:
        json.dump(results, f)
    return render_template('index.html', data=(results, datetime.datetime.utcfromtimestamp(start_unix).strftime('%b %d, %Y %H:%M:%S'), datetime.datetime.utcfromtimestamp(end_unix).strftime('%b %d, %Y %H:%M:%S')))


if __name__ == "__main__":
    app.run(debug=True)
