#!/usr/bin/python3

import credentials
import requests
import argparse
import re

"""
This script was derived from the login.py script from the wikimedia repo
https://github.com/wikimedia/mediawiki-api-demos/blob/e8fad403ab71134091f6ebf7d08ee00cb7565aab/python/login.py
"""

"""
MIT License

Copyright (c) 2022 Martin Hübner at Freifunk Berlin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


############
#  CONFIG  #
############

API_URL = "https://wiki.freifunk.net/api.php"

# (Sub)-String that marks a auto-generated bbb-configs section
SECTION_REGEX = ".*bbb-configs.*"
s = requests.Session()


################
#  FUNCTIOINS  #
################


# queries the article and looks for the number of the section
# containing the auto-generated configuration
def find_bbbconfigs_section(pagetitle: str):
    params = {
        "action": "parse",
        "page": pagetitle,
        "format": "json"
    }

    response = s.get(url=API_URL, params=params).json()
    sections = response.get("parse").get("sections")

    if not sections:
        raise ValueError("The given Wiki-page does not seem to exist.")
        exit(2)

    # iterate over sections and find bbb-config section
    i = 1
    bbb_configs_section = False
    for sec in sections:
        sec_title = sec.get("line")
        if re.search(SECTION_REGEX, sec_title):
            bbb_configs_section = True
            break
        i += 1

    if bbb_configs_section:
        return i
    else:
        raise ValueError("Theres no bbb-configs-section in the given article!")
        exit(1)


def get_login_token():
    # Get login token for API calls
    param_login_query = {
        'action': "query",
        'meta': "tokens",
        'type': "login",
        'format': "json"
    }

    r = s.get(url=API_URL, params=param_login_query)
    data = r.json()
    print(data)
    return data['query']['tokens']['logintoken']


def login_at_api(login_token):
    # Send a post request to login.
    params_login = {
        'action': "login",
        'lgname': credentials.username,
        'lgpassword': credentials.passwd,
        'lgtoken': login_token,
        'format': "json"
    }

    r = s.post(API_URL, data=params_login)
    data = r.json()


def fetch_csrf_token():
    # GET request to fetch CSRF token
    params_csrf = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    r = s.get(url=API_URL, params=params_csrf)
    data = r.json()

    return data['query']['tokens']['csrftoken']


def edit_section(article_title, section_number, csrf_token, new_text):
    # POST request to edit specific section in a page
    params_edit = {
        "action": "edit",
        "title": article_title,
        "section": section_number,  # 0=Introduction, 1=first_section, etc.
        "token": csrf_token,
        "bot": True,
        # "minor": True,
        "format": "json",
        "text": new_text,
        "summary": "Automatisches Update aus bbb-configs."
    }

    r = s.post(API_URL, data=params_edit)
    data = r.json()
    print(data)

if __name__ == '__main__':

    #####################
    #  ARGUMENT PARSER  #
    #####################

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--title", help="article which should be edited.", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--text", help="String which should be posted into section.")
    group.add_argument("-f", "--file", help="Read text from a file")
    args = parser.parse_args()


    ########################
    #  Paste text to Wiki  #
    ########################

    section = find_bbbconfigs_section(args.title)

    pagetxt = ""  # Text that gets posted into the specific article section
    if args.text:
        pagetxt = args.text
    else:
        pagetxt = open(args.file, "r").read()

    login_token = get_login_token()
    login_at_api(login_token)
    csrf_token = fetch_csrf_token()

    edit_section(args.title, section, csrf_token, pagetxt)

    s.close()
