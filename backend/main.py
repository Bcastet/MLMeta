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
from mlrating import *


if __name__ == '__main__':
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
            "print_calls": False,
            "print_riot_api_key": True,
            "default": "WARNING",
            "core": "WARNING"
        }
    }
    cassiopeia.apply_settings(cass_settings)
    cassiopeia.set_riot_api_key("RGAPI-de025284-d4e8-4500-8131-5f72a5152abd")
    print("Settings applied!;")
    now = arrow.utcnow()
    # last_update = pickle.load(open("last_update.pkl"))
    pickle.dump(now, open("last_update.pkl", "wb"))

    # (cassiopeia.Region("EUW"),"EUROPE"),
    content = []
    summaries = []
    # (cassiopeia.Region("EUW"), "EUROPE"),
    # (cassiopeia.Region("KR"), "ASIA"),


    for region, continent in [ (cassiopeia.Region("EUW"), "EUROPE")]:
        topplayers, grandmasters = getTopSoloQPlayers(region)
        #masters = getMastersSoloQPlayers(region)
        ids = getTopGameIds(topplayers, continent)
        print("IDS:", ids)
        ids = np.concatenate((ids, getTopGameIds(grandmasters, continent)), axis=0)
        print("IDS:", ids)
        #ids = np.concatenate((ids, getTopGameIds(masters, continent)), axis=0)
        ids = np.unique(ids)
        np.random.shuffle(ids)
        ids = ids[0:len(ids)//2]
        print("There are" + str(len(ids)) + " games in " + region.value)
        summaries += formatSummaries(ids, region)
        content += formatPerformances(ids, region)

    pickle.dump(content, open('content.pickle', 'wb+'))
    pickle.dump(summaries, open('summaries.pickle', 'wb+'))

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
    summaries = summaries[np.argsort(summaries[:, 3 - 1])]
    summaries = summaries.tolist()
    print(len(summaries) * len(summaries[0]))


    #summaries = summaries[0:int(0.5*len(summaries))]

    insertAndWrite(service, summaries, 909719190, "1Gif8GF_9F9KE6LVIY0PoDA0bUSqNzzXTyZCHIXhAaFc", "Game Summaries")
    #insertAndWrite(service, content, 0, "1Aeb3ailZuIaR6IAj2X6A2knwxjmB2d-lL4rOPiuoJlg", "Individual Performances")

    content = pickle.load(open('content.pickle', "rb"))
    summaries = pickle.load(open('summaries.pickle', "rb"))
    print("OK!")


    # %%

    def separateGames(formattedGames):
        toRet = {}
        for game in formattedGames:
            champion_role_patch = game[10] + "-" + game[8] + "-" + game[3]
            if champion_role_patch not in toRet.keys():
                toRet[champion_role_patch] = np.array([game])
            else:
                toRet[champion_role_patch] = np.vstack([toRet[champion_role_patch], np.array(game)])
        return toRet


    print("ok")
    separated_games = separateGames(content)

    ratings = get_champions_ratings(separated_games)

    # %%

    rrates = get_many_champions_rrate(ratings)
    import pprint

    pprint.pprint(rrates)
    content = map_dict(rrates)
    insertAndWrite(service, content, 0, "1Gif8GF_9F9KE6LVIY0PoDA0bUSqNzzXTyZCHIXhAaFc", "Champions Ratings")


    # %%

    def formatIndivPerfs(ratings):
        for rating in ratings:
            """print(rating.champion, rating.get_games_amount(), "games")
            print(rating.games.shape)
            print(rating.games[:, 0:12].shape)"""
            try:
                toRet = np.vstack([toRet, np.c_[rating.games[:, 0:12], rating.performances]])
            except:
                toRet = np.c_[rating.games[:, 0:12], rating.performances]
        return toRet


    content = formatIndivPerfs(ratings).tolist()
    insertAndWrite(service, content, 191365170, "1Gif8GF_9F9KE6LVIY0PoDA0bUSqNzzXTyZCHIXhAaFc", "Individual Performances")

    # %%

    champions_with_xp_scaling = []
    for champion_rating in ratings:
        print(champion_rating.correls[4], champion_rating.correls[10])
        if champion_rating.correls[4] > champion_rating.correls[10] and len(champion_rating.games) > 100:
            print(champion_rating.champion)
            champions_with_xp_scaling.append(champion_rating.champion)

    print(champions_with_xp_scaling)