import arrow
import mwclient
import json
import cassiopeia
import requests
import pprint
from formatter import *
import threading


def get_request(query, headers=None):
    if headers is None:
        headers = {
            'Cookie': '__cfduid=d745d380f87ac90a18b25ba92131e45f71564919182; _ga=GA1.2.381925966.1564919182; _gcl_au=1.1.150909138.1564919182; _hjid=b6f65300-68b9-455e-8e4d-afb0c836ca3d; _fbp=fb.1.1564919182544.1840726074; C3UID-694=3827007951564919184; C3UID=3827007951564919184; _tli=1203570653703679646; _scid=10eaa156-51ef-4136-b45d-cd09f90fb6e2; _tlp=2820:16705877; ajs_group_id=null; s_fid=384EB5EF5DE3AC28-24E0CA12D47819CE; new_visitor=false; ajs_user_id=null; PVPNET_LANG=en_US; PVPNET_REGION=euw; s_nr=1581353828960-New; rp2=1581353828960-Repeat; _tlv=63.1564919184.1579730543.1581353831.82.1.1; _tlc=www.google.com%2F:1581353831:forums.euw.leagueoflegends.com%2Fboard%2Fshowthread.php%3Ft%3D446403:leagueoflegends.com; _gid=GA1.2.2037781151.1581521551; ping_session_id=55a15731-1778-45f3-b9ca-60f1745ed9ce; PVPNET_TOKEN_EUW=eyJkYXRlX3RpbWUiOjE1ODE1MjE1NTc1MjMsImdhc19hY2NvdW50X2lkIjoyMjU4MjM1NjIsInB2cG5ldF9hY2NvdW50X2lkIjoyMjU4MjM1NjIsInN1bW1vbmVyX25hbWUiOiJOZW9YZW5lc2lzIiwidm91Y2hpbmdfa2V5X2lkIjoiOTAzNDc1MmIyYjQ1NjA0NGFlODdmMjU5ODJkYWQwN2QiLCJzaWduYXR1cmUiOiJZK0MzY3FXSWJvL1FrY3pEcGlnRjNRR25VMWRqK3pNVFZqc1JHTGRqRzJ3djFoWUl0WkhjYzR2NjRmS3RNUmhFdGl0bVVkT05rT3BQeTl1a3VBeFJCNStCbzIvTndST1BLU292MnJRTVZyTnpPVnViWC9jUjhyK25PdzhPb0dUWDdlZHd6MFBhSDk1RWE0OWlabzZTR3BDUzdRL054L1NrNWtUOTM0eWh6QWs9In0%3D; PVPNET_ACCT_EUW=NeoXenesis; PVPNET_ID_EUW=225823562; id_token=eyJraWQiOiJzMSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJiYTEwN2ExNC04MmIwLTVhZTAtYTMzMy0zMDEzOWI1NzQzYzMiLCJjb3VudHJ5IjoiZnJhIiwicGxheWVyX3Bsb2NhbGUiOiJmci1GUiIsImFtciI6WyJwYXNzd29yZCJdLCJpc3MiOiJodHRwczpcL1wvYXV0aC5yaW90Z2FtZXMuY29tIiwibG9sIjpbeyJjdWlkIjoyMjU4MjM1NjIsImNwaWQiOiJFVVcxIiwidWlkIjoyMjU4MjM1NjIsInVuYW1lIjoiTmVvblhlbmVzaXNFdmFuZ2VsaW9uIiwicHRyaWQiOm51bGwsInBpZCI6IkVVVzEiLCJzdGF0ZSI6IkVOQUJMRUQifV0sImxvY2FsZSI6ImVuX1VTIiwiYXVkIjoicnNvLXdlYi1jbGllbnQtcHJvZCIsImFjciI6InVybjpyaW90OmJyb256ZSIsInBsYXllcl9sb2NhbGUiOiJmci1GUiIsImV4cCI6MTU4MTYwNzk1NiwiaWF0IjoxNTgxNTIxNTU2LCJhY2N0Ijp7ImdhbWVfbmFtZSI6Ik5lb1hlbmVzaXMiLCJ0YWdfbGluZSI6IkVVVyJ9LCJqdGkiOiJJVWFGZ1d6cnp2WSIsImxvZ2luX2NvdW50cnkiOiJmcmEifQ.WLIItKOx5DnyQ1IW2amOHkzyTovdP0FpzmV7XbkDtJrreQjrciEesGTHPPoY1l83dDw8XJ1of3vYpK42330WAt7RVaHt9cF300Yqm1qcSgAsC8_K0WjQtXWisnsyt2hunv_GKQ_HI0x1iub5HJ59u-x3i0Nq9bWz0Cy5mYPgPr4; id_hint=sub%3Dba107a14-82b0-5ae0-a333-30139b5743c3%26lang%3Den%26game_name%3DNeoXenesis%26tag_line%3DEUW%26id%3D225823562%26summoner%3DNeoXenesis%26region%3DEUW1%26tag%3Deuw'}
    r = requests.get(query, headers=headers)
    try:
        toRet = json.loads(r.content)
        return toRet
    except:
        import time
        time.sleep(10)
        if ("acs" in query and "gameHash" not in query):
            query = query[:-9]
        print("Can't get query " + query + " backing off for 10 seconds")
        return get_request(query)


def get_cassmatch(url, buffer=None, matchSummary=None):
    splits = url.split("#match-details")
    newUri = "https://acs.leagueoflegends.com/v1/stats/game" + splits[1]
    jsonMatch = get_request(newUri)
    jsonMatch["platformId"] = "EUW1"
    newUri = newUri.replace("?", "/timeline?")
    jsonTimeline = get_request(newUri)
    match = cassiopeia.core.match.MatchData(**jsonMatch)
    timelineData = cassiopeia.core.match.TimelineData(**jsonTimeline)
    match.region = "EUW"
    match.continent = "EUROPE"
    cassmatch = cassiopeia.core.Match.from_data(match)
    timelineClean = cassiopeia.core.match.Timeline.from_data(timelineData)
    cassmatch._timeline = timelineClean
    cassmatch.comp_timeline = timelineData

    if buffer is not None and matchSummary is not None:
        matchSummary["title"]["MatchHistory"] = cassmatch
        buffer.append(matchSummary)
    elif buffer is not None:
        buffer += cassmatch
    return cassmatch


def requestScoutedLeaguesGames(date, scoutedLeagues):
    toRet = []
    site = mwclient.Site('lol.fandom.com', path='/')
    print(date)
    where = "SG.DateTime_UTC>'" + date.format('YYYY-MM-dd HH:mm:ss') + "' AND ("
    for leagueI in scoutedLeagues:
        where += "(SG.OverviewPage LIKE '%" + leagueI + "%')"
        if leagueI != scoutedLeagues[len(scoutedLeagues) - 1]:
            where += " OR "

    where += ")"
    print(where)
    response = site.api("cargoquery",
                        limit=150,
                        tables="ScoreboardGames=SG,MatchScheduleGame=MSG,PicksAndBansS7=PB",
                        where=where,
                        fields="MSG.MatchHistory,PB.Team1Ban1,PB.Team1Ban2,PB.Team1Ban3,PB.Team1Ban4,PB.Team1Ban5,PB.Team2Ban1,PB.Team2Ban2,PB.Team2Ban3,PB.Team2Ban4,PB.Team2Ban5,PB.Team1Pick1,PB.Team1Pick2,PB.Team1Pick3,PB.Team1Pick4,PB.Team1Pick5,PB.Team2Pick1,PB.Team2Pick2,PB.Team2Pick3,PB.Team2Pick4,PB.Team2Pick5,PB.Team1,PB.Team2,PB.Winner,PB.Team1PicksByRoleOrder,PB.Team2PicksByRoleOrder,MSG.Blue,MSG.GameId,SG.Patch,MSG.Red,SG.DateTime_UTC",
                        order_by="SG.DateTime_UTC DESC,SG.N_GameInMatch DESC",
                        join_on="SG.GameId=MSG.GameId, MSG.GameId=PB.GameId")
    thrs = []
    for match in response['cargoquery']:
        thr = threading.Thread(target=get_cassmatch, args=(match["title"]["MatchHistory"], toRet, match))
        thr.start()
        thrs.append(thr)

    for thr in thrs:
        thr.join()

    assert len(response['cargoquery']) == len(toRet)
    time.sleep(3)

    return toRet


def get_LPL_data(url, buffer, match):
    matchId = url.split("bmid=")[1]
    url = "https://open.tjstats.com/match-auth-app/open/v1/compound/matchDetail?matchId=" + matchId
    options = {"Authorization": "7935be4c41d8760a28c05581a7b1f570"}
    data = get_request(url, headers=options)
    if match is not None:
        match["title"]["MatchHistory"] = data
    if buffer is not None:
        buffer.append(match)
        return match
    return data


def requestLPLGames(date):
    toRet = []
    site = mwclient.Site('lol.fandom.com', path='/')
    print(date)
    where = "SG.DateTime_UTC>'" + date.format('YYYY-MM-dd HH:mm:ss') + "' AND (SG.OverviewPage LIKE '%LPL%')"
    print(where)
    response = site.api("cargoquery",
                        limit=150,
                        tables="ScoreboardGames=SG,MatchScheduleGame=MSG,PicksAndBansS7=PB",
                        where=where,
                        fields="MSG.MatchHistory,PB.Team1Ban1,PB.Team1Ban2,PB.Team1Ban3,PB.Team1Ban4,PB.Team1Ban5,PB.Team2Ban1,PB.Team2Ban2,PB.Team2Ban3,PB.Team2Ban4,PB.Team2Ban5,PB.Team1Pick1,PB.Team1Pick2,PB.Team1Pick3,PB.Team1Pick4,PB.Team1Pick5,PB.Team2Pick1,PB.Team2Pick2,PB.Team2Pick3,PB.Team2Pick4,PB.Team2Pick5,PB.Team1,PB.Team2,PB.Winner,PB.Team1PicksByRoleOrder,PB.Team2PicksByRoleOrder,MSG.Blue,MSG.GameId,SG.Patch,MSG.Red,SG.DateTime_UTC",
                        order_by="SG.DateTime_UTC DESC,SG.N_GameInMatch DESC",
                        join_on="SG.GameId=MSG.GameId, MSG.GameId=PB.GameId")
    thrs = []
    for match in response['cargoquery']:
        thr = threading.Thread(target=get_LPL_data, args=(match["title"]["MatchHistory"], toRet, match))
        thr.start()
        thrs.append(thr)
        time.sleep(30)

    for thr in thrs:
        thr.join()

    assert len(response['cargoquery']) == len(toRet)
    time.sleep(3)

    return toRet


def formatCompetitiveGame(matchSummary, buffer):
    try:
        match = matchSummary["title"]["MatchHistory"]
        if not match.version.startswith("12.1"):
            return None
        toRet = []

        if (match.duration * 1000).seconds > 15 * 60:
            for team in match.teams:
                team.side
                team.total_dmg = 0
                team.total_kills = 1
                team.total_deaths = 1
                team.wards_placed = 1
                team.total_lvl = 0
                team.total_golds = 0
            """
            for participant in match.participants:
                for team in match.teams:
                    if team.side==participant.side:
                        participant.team = team"
            """

            for participant in match.participants:
                participant.team.total_dmg += participant.stats.total_damage_dealt_to_champions
                participant.team.total_kills += participant.stats.kills
                participant.team.total_deaths += participant.stats.deaths
                participant.team.wards_placed += participant.stats.wards_placed
                participant.team.total_lvl += participant.stats.level
                participant.team.total_golds += participant.stats.gold_spent
                participant.matchup = match.participants[(participant.id + 4) % 10]

            for participant in match.participants:
                ennemy_team = ""
                for team in match.teams:
                    if team != participant.team:
                        ennemy_team = team

                position = participant.team_position.value if participant.team_position != None else ""
                muchamp = participant.matchup.champion.name if participant.matchup is not None else ""

                patch = match.version.split(".")[0] + "." + match.version.split(".")[1]
                print(participant.to_dict()["summonerName"])
                perfRow = [matchSummary["GameId"], match.region.value, (match.creation.int_timestamp / 86400) + 25569.00,
                           patch, (match.duration * 1000).seconds,
                           participant.to_dict()["summonerName"],
                           participant.side.name, matchSummary["title"]["Team1"], position,
                           matchSummary["title"]["Team2"], participant.champion.name,
                           muchamp, (participant.stats.kills + participant.stats.assists) / (
                                   participant.stats.kills + participant.stats.assists + ennemy_team.total_kills),
                           participant.stats.deaths / ennemy_team.total_deaths,
                           participant.stats.total_damage_dealt_to_champions / ennemy_team.total_dmg,
                           participant.stats.total_damage_taken / ennemy_team.total_dmg,
                           participant.stats.gold_spent / ennemy_team.total_golds,
                           participant.stats.total_heal / ennemy_team.total_dmg,
                           participant.stats.damage_self_mitigated / ennemy_team.total_dmg,
                           participant.stats.total_minions_killed / ennemy_team.total_golds,
                           participant.stats.wards_placed / ennemy_team.wards_placed,
                           participant.stats.wards_killed / ennemy_team.wards_placed,
                           participant.stats.level / ennemy_team.total_lvl,
                           participant.stats.time_CCing_others / ennemy_team.total_kills, int(participant.stats.win),
                           participant.champion.name + "-" + position + "-" + patch]
                toRet.append(perfRow)
                print(perfRow)
        buffer += toRet
    except Exception as e:
        print(e)
        # pprint.pprint(matchSummary)
        raise e
    return toRet

def formatLPLGame(game):
    LPLjson = game["MatchHistory"]
    for team in LPLjson["data"]["matchInfos"]["teamInfos"]:
        for participant in team["playerInfos"]:
            perfRow = [game["GameId"], "LPL",  arrow.get(LPLjson["data"]["matchInfos"]["matchStartTime"]).int_timestamp,
                       game["Patch"], (arrow.get(LPLjson["data"]["matchInfos"]["matchEndTime"]) - arrow.get(LPLjson["data"]["matchInfos"]["matchStartTime"])).seconds,
                       participant["playerName"],
                       participant.side.name, game["title"]["Blue"], participant["playerLocation"],
                       game["title"]["Team2"], participant.champion.name,
                       muchamp, (participant.stats.kills + participant.stats.assists) / (
                               participant.stats.kills + participant.stats.assists + ennemy_team.total_kills),
                       participant.stats.deaths / ennemy_team.total_deaths,
                       participant.stats.total_damage_dealt_to_champions / ennemy_team.total_dmg,
                       participant.stats.total_damage_taken / ennemy_team.total_dmg,
                       participant.stats.gold_spent / ennemy_team.total_golds,
                       participant.stats.total_heal / ennemy_team.total_dmg,
                       participant.stats.damage_self_mitigated / ennemy_team.total_dmg,
                       participant.stats.total_minions_killed / ennemy_team.total_golds,
                       participant.stats.wards_placed / ennemy_team.wards_placed,
                       participant.stats.wards_killed / ennemy_team.wards_placed,
                       participant.stats.level / ennemy_team.total_lvl,
                       participant.stats.time_CCing_others / ennemy_team.total_kills, int(participant.stats.win),
                       participant.champion.name + "-" + position + "-" + patch]


if __name__ == '__main__':
    import leaguepedia
    import arrow
    from datetime import datetime
    import sys

    date = arrow.get('2022-01-01T00:00:00.000000+00:00')
    requestLPLGames(date)

    sys.exit(0)
    scouted_leagues = ["LEC/", "LCK/", "2021 Season World Championship/Main Event", "LFL"]
    games = leaguepedia.requestScoutedLeaguesGames(date, scouted_leagues)
    toRet = []
    # pprint.pprint(games)
    for game in games:
        formatCompetitiveGame(game, toRet)
