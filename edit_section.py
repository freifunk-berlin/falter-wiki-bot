#!/usr/bin/python3

import credentials
import requests
import argparse

""" derived from:
    login.py

    MediaWiki API Demos
    Demo of `Login` module: Sending post request to login
    MIT license
"""

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--section", help="give the section where the text should be pasted. (integer)", type=int, required=True)
parser.add_argument("-t", "--title", help="article which should be edited.", required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--text", help="String which should be posted into section.")
group.add_argument("-f", "--file", help="Read text from a file")
args = parser.parse_args()


pagetxt = "" # Text that gets posted into the specific article section
if args.text:
    pagetxt = args.text
else:
    pagetxt = open(args.file, "r").read()


URL = "https://wiki.freifunk.net/api.php"
s = requests.Session()

# Get login token for API
param_login_query = {
    'action':"query",
    'meta':"tokens",
    'type':"login",
    'format':"json"
}

r = s.get(url=URL, params=param_login_query)
data = r.json()
print(data)
LOGIN_TOKEN = data['query']['tokens']['logintoken']


# Send a post request to login.
params_login = {
    'action':"login",
    'lgname': credentials.username,
    'lgpassword': credentials.passwd,
    'lgtoken':LOGIN_TOKEN,
    'format':"json"
}
r = s.post(URL, data=params_login)
data = r.json()

# Step 3: GET request to fetch CSRF token
params_csrf = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}
r = s.get(url=URL, params=params_csrf)
data = r.json()

CSRF_TOKEN = data['query']['tokens']['csrftoken']

# POST request to edit specific section in a page
PARAMS_3 = {
    "action": "edit",
    "title": args.title,
    "section": args.section, # 0=Introduction, 1=first_section, etc.
    "token": CSRF_TOKEN,
    "bot": True,
    #"minor": True,
    "format": "json",
    "text": pagetxt,
    "summary": "Automatisches Update aus bbb-configs."

}
r = s.post(URL, data=PARAMS_3)
data = r.json()
print(data)