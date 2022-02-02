import cassiopeia
import numpy as np
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import socket
import os
import json
import pprint
import arrow
import pickle
import threading
import time
from riot_requests import *
from sheetsutils import *
from formatter import *

cass_settings = {
    "global": {
        "version_from_match": "patch",
        "default_region": "EUW"
    },
    "plugins": {},
    "pipeline": {
        "Cache": {},
        "DDragon": {},
        "RiotAPI": {
            "api_key": "RIOT_API_KEY"
        }
    },
    "logging": {
        "print_calls": True,
        "print_riot_api_key": True,
        "default": "WARNING",
        "core": "WARNING"
    }
}
cassiopeia.apply_settings(cass_settings)
cassiopeia.set_riot_api_key("RGAPI-de025284-d4e8-4500-8131-5f72a5152abd")

now = arrow.utcnow()
# last_update = pickle.load(open("last_update.pkl"))
pickle.dump(now, open("last_update.pkl", "wb"))





# (cassiopeia.Region("EUW"),"EUROPE"),
content = []
summaries = []
# (cassiopeia.Region("EUW"), "EUROPE"),
# (cassiopeia.Region("KR"), "ASIA"),
"""
for region, continent in [(cassiopeia.Region("KR"), "ASIA"), (cassiopeia.Region("EUW"), "EUROPE")]:
    topplayers, grandmasters = getTopSoloQPlayers(region)
    #masters = getMastersSoloQPlayers(region)
    ids = getTopGameIds(topplayers, continent)
    print("IDS:", ids)
    ids = np.concatenate((ids, getTopGameIds(grandmasters, continent)), axis=0)
    print("IDS:", ids)
    #ids = np.concatenate((ids, getTopGameIds(masters, continent)), axis=0)
    ids = np.unique(ids)
    print("There are" + str(len(ids)) + " games in " + region.value)
    content += formatPerformances(ids, region)
    summaries += formatSummaries(ids, region)
"""
#pickle.dump(content, open('content.pickle', 'wb+'))
#pickle.dump(summaries, open('summaries.pickle', 'wb+'))
#pickle.dump(summaries, open('mastersummaries.pickle', 'wb+'))

content = pickle.load(open('content.pickle', "rb"))
summaries = pickle.load(open('summaries.pickle', "rb"))
print("Games read!")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('sheets', 'v4', credentials=creds)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if False:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)

import mlrating

# mlrating.get_champions_ratings(content)


# insertAndWrite(service, content, 0, "1Aeb3ailZuIaR6IAj2X6A2knwxjmB2d-lL4rOPiuoJlg", "Individual Performances")
# insertAndWrite(service, summaries, 1243210472, "1Aeb3ailZuIaR6IAj2X6A2knwxjmB2d-lL4rOPiuoJlg", "Game Summaries")

print(len(summaries), "matches")
uniques = []
index = 0

for row in summaries:
    if len(row) != len(summaries[0]):
        print(len(row), len(summaries[0]))
        print(row)
        row.remove(row[42])
        summaries[index] = row
    index += 1

print(len(uniques))
print(len(summaries) * len(summaries[0]))
summaries = np.array(summaries)
np.random.shuffle(summaries)
summaries = summaries[0:int(0.5*len(summaries))]
summaries = summaries.tolist()
print(len(summaries) * len(summaries[0]))


#summaries = summaries[0:int(0.5*len(summaries))]

insertAndWrite(service, summaries, 909719190, "1Gif8GF_9F9KE6LVIY0PoDA0bUSqNzzXTyZCHIXhAaFc", "Game Summaries")
#insertAndWrite(service, content, 0, "1Aeb3ailZuIaR6IAj2X6A2knwxjmB2d-lL4rOPiuoJlg", "Individual Performances")