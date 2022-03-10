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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('sheets', 'v4', credentials=creds)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)


def col_to_letter(col):
    '''Gets the letter of a column number'''
    r = ''
    while col > 0:
        v = (col - 1) % 26
        r = chr(int(v) + 65) + r
        col = (col - v - 1) / 26
    return r


def insertAndWrite(service, content, sheetgid, spreadsheetid, sheetname, inserted=False):
    # print(content)
    body = {"requests": [
        {
            "insertDimension": {
                "range": {
                    "sheetId": sheetgid,
                    "dimension": "ROWS",
                    "startIndex": 1,
                    "endIndex": len(content) + 1
                },
                "inheritFromBefore": True
            }
        }
    ]
    }
    try:
        if not inserted:
            service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetid, body=body).execute()
            inserted = True
    except socket.timeout:
        inserted = True
    try:
        body = {
            'values': content
        }

        range_name = sheetname + "!A2:" + col_to_letter(len(content[0])) + str(len(content) + 1)
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheetid, valueInputOption="USER_ENTERED", range=range_name,
            body=body).execute()
    except socket.timeout:
        import time
        print("Trying again in 900 seconds")
        time.sleep(900)
        insertAndWrite(service, content, sheetgid, spreadsheetid, sheetname, inserted)


def map_dict(dict):
    toRet = []
    for key in dict.keys():
        if not np.isnan(dict[key][0]) and not np.isinf(dict[key][0]):
            row = [key] + dict[key]
            toRet.append(row)
        else:
            dict[key][0] = ""
            row = [key] + dict[key]
            toRet.append(row)
    return toRet


def serializeNparray(nparray):
    toRet = []
    for row in nparray:
        toRet.append(list(row))
