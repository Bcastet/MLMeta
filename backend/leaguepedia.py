import arrow
import mwclient
import json
import cassiopeia
import requests
import pprint
import threading
from mwrogue import esports_client
import numpy as np

site = mwclient.Site('lol.fandom.com', path='/')
client = esports_client.EsportsClient('lol')
id_to_role = [None, "TOP_LANE", "JUNGLE", "MID_LANE", "BOT_LANE", "UTILITY", "TOP_LANE", "JUNGLE", "MID_LANE",
              "BOT_LANE", "UTILITY"]


def get_request(query, headers=None):
    if headers is None:
        headers = {
            'Cookie': '__cfduid=d745d380f87ac90a18b25ba92131e45f71564919182; _ga=GA1.2.381925966.1564919182; _gcl_au=1.1.150909138.1564919182; _hjid=b6f65300-68b9-455e-8e4d-afb0c836ca3d; _fbp=fb.1.1564919182544.1840726074; C3UID-694=3827007951564919184; C3UID=3827007951564919184; _tli=1203570653703679646; _scid=10eaa156-51ef-4136-b45d-cd09f90fb6e2; _tlp=2820:16705877; ajs_group_id=null; s_fid=384EB5EF5DE3AC28-24E0CA12D47819CE; new_visitor=false; ajs_user_id=null; PVPNET_LANG=en_US; PVPNET_REGION=euw; s_nr=1581353828960-New; rp2=1581353828960-Repeat; _tlv=63.1564919184.1579730543.1581353831.82.1.1; _tlc=www.google.com%2F:1581353831:forums.euw.leagueoflegends.com%2Fboard%2Fshowthread.php%3Ft%3D446403:leagueoflegends.com; _gid=GA1.2.2037781151.1581521551; ping_session_id=55a15731-1778-45f3-b9ca-60f1745ed9ce; PVPNET_TOKEN_EUW=eyJkYXRlX3RpbWUiOjE1ODE1MjE1NTc1MjMsImdhc19hY2NvdW50X2lkIjoyMjU4MjM1NjIsInB2cG5ldF9hY2NvdW50X2lkIjoyMjU4MjM1NjIsInN1bW1vbmVyX25hbWUiOiJOZW9YZW5lc2lzIiwidm91Y2hpbmdfa2V5X2lkIjoiOTAzNDc1MmIyYjQ1NjA0NGFlODdmMjU5ODJkYWQwN2QiLCJzaWduYXR1cmUiOiJZK0MzY3FXSWJvL1FrY3pEcGlnRjNRR25VMWRqK3pNVFZqc1JHTGRqRzJ3djFoWUl0WkhjYzR2NjRmS3RNUmhFdGl0bVVkT05rT3BQeTl1a3VBeFJCNStCbzIvTndST1BLU292MnJRTVZyTnpPVnViWC9jUjhyK25PdzhPb0dUWDdlZHd6MFBhSDk1RWE0OWlabzZTR3BDUzdRL054L1NrNWtUOTM0eWh6QWs9In0%3D; PVPNET_ACCT_EUW=NeoXenesis; PVPNET_ID_EUW=225823562; id_token=eyJraWQiOiJzMSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJiYTEwN2ExNC04MmIwLTVhZTAtYTMzMy0zMDEzOWI1NzQzYzMiLCJjb3VudHJ5IjoiZnJhIiwicGxheWVyX3Bsb2NhbGUiOiJmci1GUiIsImFtciI6WyJwYXNzd29yZCJdLCJpc3MiOiJodHRwczpcL1wvYXV0aC5yaW90Z2FtZXMuY29tIiwibG9sIjpbeyJjdWlkIjoyMjU4MjM1NjIsImNwaWQiOiJFVVcxIiwidWlkIjoyMjU4MjM1NjIsInVuYW1lIjoiTmVvblhlbmVzaXNFdmFuZ2VsaW9uIiwicHRyaWQiOm51bGwsInBpZCI6IkVVVzEiLCJzdGF0ZSI6IkVOQUJMRUQifV0sImxvY2FsZSI6ImVuX1VTIiwiYXVkIjoicnNvLXdlYi1jbGllbnQtcHJvZCIsImFjciI6InVybjpyaW90OmJyb256ZSIsInBsYXllcl9sb2NhbGUiOiJmci1GUiIsImV4cCI6MTU4MTYwNzk1NiwiaWF0IjoxNTgxNTIxNTU2LCJhY2N0Ijp7ImdhbWVfbmFtZSI6Ik5lb1hlbmVzaXMiLCJ0YWdfbGluZSI6IkVVVyJ9LCJqdGkiOiJJVWFGZ1d6cnp2WSIsImxvZ2luX2NvdW50cnkiOiJmcmEifQ.WLIItKOx5DnyQ1IW2amOHkzyTovdP0FpzmV7XbkDtJrreQjrciEesGTHPPoY1l83dDw8XJ1of3vYpK42330WAt7RVaHt9cF300Yqm1qcSgAsC8_K0WjQtXWisnsyt2hunv_GKQ_HI0x1iub5HJ59u-x3i0Nq9bWz0Cy5mYPgPr4; id_hint=sub%3Dba107a14-82b0-5ae0-a333-30139b5743c3%26lang%3Den%26game_name%3DNeoXenesis%26tag_line%3DEUW%26id%3D225823562%26summoner%3DNeoXenesis%26region%3DEUW1%26tag%3Deuw'}
    r = requests.get(query, headers=headers)
    try:
        toRet = json.loads(r.content)
        # print("Successfully loaded query "+query)
        assert (
                       "gameVersion" in toRet.keys() or "tjstats" in query or "timeline" in query) and 'errorCode' not in toRet.keys()
        return toRet
    except Exception as e:
        print(e)
        if r.status_code == 404:
            print(query + "failed")
            raise e
        else:
            import time
            if "acs" in query and "gameHash" not in query:
                query = query[:-9]
            print(r.content)
            print("Can't get query " + query + " backing off for 10 seconds. Reason : " + str(e))
            time.sleep(10)
            return get_request(query)


def get_cassmatch(versionId, buffer=None, matchSummary=None):
    version, riotPlatformGameId = versionId
    try:
        jsonMatch, jsonTimeline = client.get_data_and_timeline(riotPlatformGameId, version)
    except:
        try:
            jsonMatch, jsonTimeline = client.get_data_and_timeline(riotPlatformGameId, 4)
        except:
            pprint.pp(matchSummary)
            print(matchSummary["title"]["Blue"] + " vs " + matchSummary["title"]["Red"] + "could not load properly")
            raise Exception

    jsonMatch["platformId"] = "EUW1"
    match = cassiopeia.core.match.MatchData(**jsonMatch)
    match.region = "EUW"
    match.continent = "EUROPE"
    cassmatch = cassiopeia.core.Match.from_data(match)
    timelineData = cassiopeia.core.match.TimelineData(**jsonTimeline)
    cassmatch._timeline = cassiopeia.core.match.Timeline.from_data(timelineData)
    try:
        for frame in cassmatch.timeline.frames:
            assert frame is not None
        for participant in cassmatch.participants:
            assert participant is not None
    except ValueError as e:
        import os
        print("Could load properly match")
        raise e

    if buffer is not None and matchSummary is not None:
        matchSummary["title"]["MatchHistory"] = cassmatch
        buffer.append(matchSummary["title"])
    elif buffer is not None:
        buffer += cassmatch
    return cassmatch


def requestScoutedLeaguesGames(date, scoutedLeagues):
    toRet = []
    where = "MSG.RiotPlatformGameId!='' AND SG.DateTime_UTC>'" + date.format(
        'YYYY-MM-dd HH:mm:ss') + "' AND ("
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
                        fields="MSG.RiotVersion,MSG.MatchHistory,MSG.RiotPlatformGameId,MSG.RiotHash,PB.Team1Ban1,PB.Team1Ban2,PB.Team1Ban3,PB.Team1Ban4,PB.Team1Ban5,PB.Team2Ban1,PB.Team2Ban2,PB.Team2Ban3,PB.Team2Ban4,PB.Team2Ban5,PB.Team1Pick1,PB.Team1Pick2,PB.Team1Pick3,PB.Team1Pick4,PB.Team1Pick5,PB.Team2Pick1,PB.Team2Pick2,PB.Team2Pick3,PB.Team2Pick4,PB.Team2Pick5,PB.Team1,PB.Team2,PB.Winner,PB.Team1PicksByRoleOrder,PB.Team2PicksByRoleOrder,MSG.Blue,MSG.GameId,SG.Patch,MSG.Red,SG.DateTime_UTC",
                        order_by="SG.DateTime_UTC ASC,SG.N_GameInMatch ASC",
                        join_on="SG.GameId=MSG.GameId, MSG.GameId=PB.GameId")
    thrs = []
    for match in response['cargoquery']:
        if match["title"]["MatchHistory"] == "":
            match["title"]["MatchHistory"] = "http://matchhistory.na.leagueoflegends.com/en/#match-details/" + \
                                             match["title"]["RiotPlatformGameId"].replace("_", "/") + "?gameHash=" + \
                                             match["title"]["RiotHash"]
        thr = threading.Thread(target=get_cassmatch, args=(
            (match["title"]["RiotVersion"], match["title"]["RiotPlatformGameId"]), toRet, match))
        thr.start()
        thrs.append(thr)
        if len(thrs) == 1:
            import time
            time.sleep(10)

    for thr in thrs:
        thr.join()

    assert len(response['cargoquery']) == len(toRet)

    if len(response['cargoquery']) == 150:
        most_recent_game = response['cargoquery'][149]["title"]["DateTime UTC"]
        toRet += requestScoutedLeaguesGames(most_recent_game, scoutedLeagues)
    print(len(toRet))
    return toRet


def get_LPL_data(url, buffer, match):
    game_in_match = int(match["title"]["N GameInMatch"]) - 1
    try:
        matchId = url.split("bmid=")[1]
    except IndexError as e:
        raise Exception(
            url + " " + match["title"]["Team1"] + " " + match["title"]["Team2"] + " " + match["title"]["GameId"])

    url = "https://open.tjstats.com/match-auth-app/open/v1/compound/matchDetail?matchId=" + matchId
    options = {"Authorization": "7935be4c41d8760a28c05581a7b1f570"}
    try:
        data = get_request(url, headers=options)["data"]["matchInfos"][game_in_match]
    except KeyError as e:
        pprint.pprint(match)
        raise e
    if match is not None:
        match["title"]["MatchHistory"] = data
    if buffer is not None:
        buffer.append(match["title"])
        return match
    return data


def requestLPLGames(date):
    toRet = []
    site = mwclient.Site('lol.fandom.com', path='/')
    where = "MSG.MatchHistory!='' AND SG.DateTime_UTC>'" + date.format(
        'YYYY-MM-dd HH:mm:ss') + "' AND (SG.OverviewPage LIKE '%LPL/%' )"
    #where += "OR SG.OverviewPage LIKE '%LDL/%')"
    response = site.api("cargoquery",
                        limit=150,
                        tables="ScoreboardGames=SG,MatchScheduleGame=MSG,PicksAndBansS7=PB",
                        where=where,
                        fields="MSG.N_GameInMatch,MSG.MatchHistory,PB.Team1Ban1,PB.Team1Ban2,PB.Team1Ban3,PB.Team1Ban4,PB.Team1Ban5,PB.Team2Ban1,PB.Team2Ban2,PB.Team2Ban3,PB.Team2Ban4,PB.Team2Ban5,PB.Team1Pick1,PB.Team1Pick2,PB.Team1Pick3,PB.Team1Pick4,PB.Team1Pick5,PB.Team2Pick1,PB.Team2Pick2,PB.Team2Pick3,PB.Team2Pick4,PB.Team2Pick5,PB.Team1,PB.Team2,PB.Winner,PB.Team1PicksByRoleOrder,PB.Team2PicksByRoleOrder,MSG.Blue,MSG.GameId,SG.Patch,MSG.Red,SG.DateTime_UTC",
                        order_by="SG.DateTime_UTC ASC,SG.N_GameInMatch ASC",
                        join_on="SG.GameId=MSG.GameId, MSG.GameId=PB.GameId")
    thrs = []
    for match in response['cargoquery']:
        thr = threading.Thread(target=get_LPL_data, args=(match["title"]["MatchHistory"], toRet, match))
        thr.start()
        thrs.append(thr)

    for thr in thrs:
        thr.join()
    print(len(response['cargoquery']), len(toRet))
    assert len(response['cargoquery']) >= len(toRet) -1

    if len(response['cargoquery']) == 150:
        most_recent_game = response['cargoquery'][149]["title"]["DateTime UTC"]
        toRet += requestLPLGames(most_recent_game)

    return toRet


def getBuildFormatted(participant: cassiopeia.core.match.Participant):
    items_ordered = []
    boots = ""
    for event in participant.timeline.events:
        if hasattr(event, "item_id"):
            if event.item_id < 7000:
                item = cassiopeia.core.Item(id=event.item_id, region="EUW")
            else:
                item = None
            if hasattr(item, "gold"):
                if event.type == "ITEM_PURCHASED" and item.gold.total > 1700:
                    if item.name not in items_ordered and len(items_ordered) <= 6:
                        items_ordered.append(item.name)
                if (
                        event.type == "ITEM_SOLD" or event.type == "ITEM_DESTROYED" or event.type == "ITEM_UNDO") and item.name != "Manamune" and participant.champion.name != "Viego" and len(
                    items_ordered) != 0:
                    if item.name == items_ordered[len(items_ordered) - 1]:
                        items_ordered.remove(item.name)
                        if participant.champion.name == "Viego":
                            print(item.name + " sold", items_ordered)
                if event.type == "ITEM_PURCHASED" and 'Boots' in item.tags:
                    boots = item.name

    if len(items_ordered) > 6:
        items_ordered = items_ordered[0:6]
    while len(items_ordered) < 6:
        items_ordered.append("")
    items_ordered.append(boots)
    if len(participant.stats.items) > 0 and participant.stats.items[len(participant.stats.items) - 1] is not None:
        items_ordered.append(participant.stats.items[len(participant.stats.items) - 1].name)
    else:
        items_ordered.append("")
    return items_ordered


def formatCompetitiveGame(matchSummary, buffer):
    print(matchSummary["GameId"])
    try:
        match = matchSummary["MatchHistory"]
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
                for t in match.teams:
                    if t != participant.team:
                        ennemy_team = t

                position = id_to_role[participant.id]
                passive_value = 0
                if participant.champion.name == "Ornn":
                    passive_value = 1000 * (participant.stats.level - 12)

                if participant.side.name == "blue":
                    opponents = matchSummary["Red"]
                else:
                    opponents = matchSummary["Blue"]

                patch = match.version.split(".")[0] + "." + match.version.split(".")[1]
                perfRow = [matchSummary["GameId"], matchSummary["GameId"].split("/")[0],
                           matchSummary["DateTime UTC"],
                           patch, (match.duration * 1000).seconds,
                           participant.to_dict()["summonerName"],
                           matchSummary[participant.side.name.capitalize()], opponents,
                           participant.side.name.capitalize(), position,
                           participant.champion.name
                           ]
                perfRow += [rune.name for rune in participant.runes]
                perfRow += [perk.name for perk in participant.stat_runes]
                perfRow += [p.champion.name for p in participant.team.participants]
                perfRow += [p.champion.name for p in ennemy_team.participants]
                perfRow += getBuildFormatted(participant)
                perfRow.append(participant.summoner_spell_d.name)
                perfRow.append(participant.summoner_spell_f.name)

                perfRow += [(participant.stats.kills + participant.stats.assists) / (
                        participant.stats.kills + participant.stats.assists + ennemy_team.total_kills),
                            participant.stats.deaths / ennemy_team.total_deaths,
                            participant.stats.total_damage_dealt_to_champions / ennemy_team.total_dmg,
                            participant.stats.total_damage_taken / ennemy_team.total_dmg,
                            (participant.stats.gold_spent + passive_value) / ennemy_team.total_golds,
                            participant.stats.total_heal / ennemy_team.total_dmg,
                            participant.stats.damage_self_mitigated / ennemy_team.total_dmg,
                            participant.stats.total_minions_killed / ennemy_team.total_golds,
                            participant.stats.wards_placed / ennemy_team.wards_placed,
                            participant.stats.wards_killed / ennemy_team.wards_placed,
                            participant.stats.level / ennemy_team.total_lvl,
                            participant.stats.time_CCing_others / ennemy_team.total_kills,
                            int(participant.stats.win),
                            participant.champion.name + "-" + position + "-" + patch]
                toRet.append(perfRow)
        buffer += toRet
    except Exception as e:
        # print(e)
        # pprint.pprint(matchSummary)
        raise e
    return toRet


def formatLPLGame(game):
    lplrolemap = {"TOP": "TOP_LANE", "JUN": "JUNGLE", "MID": "MID_LANE", "BOT": "BOT_LANE", "SUP": "UTILITY"}

    LPLjson = game["MatchHistory"]
    toRet = []

    for team in LPLjson["teamInfos"]:
        team["totalKills"] = 0
        team["totalDmg"] = 0
        team["totalGolds"] = 0
        team["wardsPlaced"] = 0
        team["totalLvl"] = 0
        for participant in team["playerInfos"]:
            team["totalKills"] += participant["battleDetail"]["kills"]
            team["totalDmg"] += participant["damageDetail"]["heroDamage"]
            team["totalGolds"] += participant["otherDetail"]["spentGold"]
            team["wardsPlaced"] += participant["visionDetail"]["wardPlaced"]
            team["totalLvl"] += participant["otherDetail"]["level"]
        if team["totalKills"] == 0:
            team["totalKills"] = 1

    LPLjson["teamInfos"][0]["win"] = int(LPLjson["teamAId"] == LPLjson["matchWin"])
    LPLjson["teamInfos"][1]["win"] = int(LPLjson["teamBId"] == LPLjson["matchWin"])

    for side, team in enumerate(LPLjson["teamInfos"]):
        ennemy_team = LPLjson["teamInfos"][(side + 1) % 2]
        for participant in team["playerInfos"]:

            for ennemy in ennemy_team["playerInfos"]:
                if ennemy["playerLocation"] == participant["playerLocation"]:
                    muchamp = cassiopeia.Champion(id=ennemy["heroId"], region="EUW").name
            passive_value = 0
            if cassiopeia.Champion(id=participant["heroId"], region="EUW").name == "Ornn":
                passive_value = (participant["otherDetail"]["level"] - 12) * 1000
            if side == 0:
                participant["side"] = "Blue"
            else:
                participant["side"] = "Red"
            if participant["side"] == "Blue":
                opponents = game["Red"]
            else:
                opponents = game["Blue"]

            #formatting here
            perfRow = [game["GameId"], game["GameId"].split("/")[0],
                       game["DateTime UTC"],
                       game["Patch"], LPLjson["gameTime"],
                       participant["playerName"], game[participant["side"]], opponents,
                       participant["side"], lplrolemap[participant["playerLocation"]],
                       cassiopeia.Champion(id=participant["heroId"], region="EUW").name]

            perfRow += [cassiopeia.Rune(id=rune["runeId"], region="EUW").name for rune in participant["perkRunes"]]
            perfRow += [cassiopeia.Champion(id=p["heroId"], region="EUW").name for p in team["playerInfos"]]
            perfRow += [cassiopeia.Champion(id=p["heroId"], region="EUW").name for p in ennemy_team["playerInfos"]]
            items = []
            items += [cassiopeia.Item(id=i["itemId"], region="EUW").name for i in
                      filter(lambda item: item["itemId"] < 7000, participant["items"])]
            while len(items) < 8:
                items.append("")
            perfRow += items
            perfRow.append(cassiopeia.SummonerSpell(id=participant["spell1Id"], region="EUW").name)
            perfRow.append(cassiopeia.SummonerSpell(id=participant["spell2Id"], region="EUW").name)

            perfRow += [(participant["battleDetail"]["kills"] + participant["battleDetail"]["assist"]) / (
                    participant["battleDetail"]["kills"] + participant["battleDetail"]["assist"] +
                    ennemy_team["totalKills"]),
                        participant["battleDetail"]["death"] / team["totalKills"],
                        participant["damageDetail"]["heroDamage"] / ennemy_team["totalDmg"],
                        participant["DamageTakenDetail"]["damageTaken"] / ennemy_team["totalDmg"],
                        (participant["otherDetail"]["spentGold"] + passive_value) / ennemy_team["totalGolds"],
                        np.nan, np.nan,
                        participant["minionKilled"] / ennemy_team["totalGolds"],
                        participant["visionDetail"]["wardPlaced"] / ennemy_team["wardsPlaced"],
                        participant["visionDetail"]["wardKilled"] / ennemy_team["wardsPlaced"],
                        participant["otherDetail"]["level"] / ennemy_team["totalLvl"],
                        np.nan, int(team["teamId"] == LPLjson["matchWin"]),
                        cassiopeia.Champion(id=participant["heroId"], region="EUW").name + "-" + lplrolemap[
                            participant["playerLocation"]] + "-" + game["Patch"]]
            toRet.append(perfRow)
    return toRet


def format_game_summary(matchSummary):
    headers = [
        matchSummary["GameId"],
        matchSummary["GameId"][0:3],
        matchSummary["Patch"],
        matchSummary["DateTime UTC"],
        matchSummary["MatchHistory"].duration,
        matchSummary["Blue"],
        matchSummary["Red"]
    ]
    toRet = []
    for participant in matchSummary["MatchHistory"].participants:
        row = headers


if __name__ == '__main__':
    print("Starting")
    import arrow
    from sheetsutils import insertAndWrite, service, map_dict
    from mlrating import *

    date = arrow.get('2022-01-01T00:00:00.000000+00:00')
    content = []

    lpl_games = requestLPLGames(date)
    pprint.pprint(lpl_games[0])
    for game in lpl_games:
        content += formatLPLGame(game)
    # "LFL_Division_2"
    scouted_leagues = ["LEC/", "LCK/", "LFL/", "LCS/", "LVP_SuperLiga/", "LCK_CL/"]
    games = requestScoutedLeaguesGames(date, scouted_leagues)

    games.sort(key=lambda game: game["DateTime UTC"])
    for game in games:
        formatCompetitiveGame(game, content)

    content = np.array(content)

    separated = separateGames(content, roleIndex=9)
    ratings = get_champions_ratings(separated, parameters=12, headers=54 - 14)
    rrates = get_many_champions_rrate(ratings)
    rrates = map_dict(rrates)
    formatted_games = []


    def formatIndivPerfs(ratings):
        for rating in ratings:
            try:
                toRet = np.vstack([toRet, np.c_[rating.games[:, 0:40], rating.performances, rating.wins]])
            except:
                toRet = np.c_[rating.games[:, 0:40], rating.performances, rating.wins]
        return toRet


    content = formatIndivPerfs(ratings)
    content = content[content[:, 2].argsort()]
    content = np.flipud(content)
    content = content.tolist()

    insertAndWrite(service, rrates, 0, "1WuSINK6z52qaIdh7GEEMQ9oOpIB_YcYrQYJxlwKrsLg", "Champions Ratings")
    insertAndWrite(service, content, 909719190, "1WuSINK6z52qaIdh7GEEMQ9oOpIB_YcYrQYJxlwKrsLg", "Game Summaries")

    for rating in ratings:
        if "JUNGLE" in rating.champion:
            print(rating.champion, len(rating.games))
            print("Correls", rating.correls)
            print("Avg", rating.averages)
            print("Stds", rating.sds)
            if rating.champion == "Trundle-JUNGLE-12.1":
                for r in ratings:
                    print(r.correls[0], r.correls[0] != np.nan)
                    if rating.role == r.role and r.patch == rating.patch and not np.isnan(r.correls[0]):
                        rrate = r.compare_champion(rating)
                        print(r.champion, rrate)
                        if not np.isnan(rrate):
                            rrates = np.append(rrates, rrate)
