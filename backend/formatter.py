import cassiopeia
from multiprocessing import Process, Pool
import time
import os
import numpy as np
import database
import tqdm

db = database.database()


def formatPerformances(gameIds, region):
    toRet = []
    thrs = []
    first_thread = True
    pool = Pool(10)
    arglist = []

    for gameId in gameIds:
        if "_" not in gameId:
            if region.value == "EUW":
                gameId = region.value + "1_" + gameId
            else:
                gameId = region.value + "_" + gameId

        args=(gameId, toRet, region)
        arglist.append(args)

        if first_thread:
            print("Sleeping, making calls")
            time.sleep(10)
            first_thread = False
    formatGame(arglist[0])
    result = []
    for x in tqdm.tqdm(pool.imap_unordered(formatGame, arglist), total=len(arglist)):
        result += x
        #print(len(result))
    return result


def vstack(prev, to_add):
    return np.vstack(prev, to_add)


def formatSummaries(gameIds, region):
    items = cassiopeia.Items(region=region)
    for item in items:
        assert hasattr(item, "gold")
    toRet = []
    thrs = []
    first_thread = True
    arglist = []
    for gameId in gameIds:
        if "_" not in gameId:
            if region.value == "EUW":
                gameId = region.value + "1_" + gameId
            else:
                gameId = region.value + "_" + gameId

        #thr = Process(target=formatGameSummary, args=(gameId, toRet, region, items), daemon=True)
        args=(gameId, toRet, region)
        arglist.append(args)
        if first_thread:
            print("Sleeping, making calls")
            time.sleep(10)
            first_thread = False

    formatGameSummary(arglist[0])
    result = []
    pool = Pool(10)
    print(arglist[0])
    for x in tqdm.tqdm(pool.imap_unordered(formatGameSummary, arglist), total=len(arglist)):
        result += x
        # print(len(result))
    return result


def formatGame(params):
    gameId, buffer, region = params
    try:
        match = db.get_match(gameId, region)
        #if not match.version.startswith("12.3"):
        #    return None
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
                participant.matchup = None
                for p in match.participants:
                    # pprint.pprint(p.to_dict())
                    if p.individual_position != "INVALID" and p.team_position == participant.team_position and p.summoner.name != participant.summoner.name:
                        participant.matchup = p
                        break

            for participant in match.participants:
                ennemy_team = ""
                for team in match.teams:
                    if team != participant.team:
                        ennemy_team = team

                position = participant.team_position.value if participant.team_position != None else ""
                muchamp = participant.matchup.champion.name if participant.matchup is not None else ""

                patch = match.version.split(".")[0] + "." + match.version.split(".")[1]
                passive_value = 0
                if participant.champion.name == "Ornn":
                    passive_value = 1000 * (participant.stats.level - 13)
                perfRow = [match.id, match.region.value, (match.creation.timestamp / 86400) + 25569.00,
                           patch, (match.duration * 1000).seconds,
                           participant.summoner.name,
                           participant.side.name, "", position, "", participant.champion.name,
                           muchamp, (participant.stats.kills + participant.stats.assists) / (
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
                           participant.stats.time_CCing_others / ennemy_team.total_kills, int(participant.stats.win),
                           participant.champion.name + "-" + position + "-" + patch]
                toRet.append(perfRow)
        buffer += toRet
        #print(match.id)
    except Exception as e:
        print(e)
        print(region)
        print(match.to_dict())
        raise e
        os._exit(1)
    return toRet


def formatGameSummary(params):
    gameId, buffer, region = params
    cass_items = cassiopeia.Items(region=region)
    try:
        toRet = []
        match = db.get_match(gameId, region)
        #if not match.version.startswith("12.3"):
        #    return None
        if (match.duration * 1000).seconds > 15 * 60:
            for participant in match.participants:
                participant.matchup = None
                for p in match.participants:
                    # pprint.pprint(p.to_dict())
                    if p.individual_position != "INVALID" and p.team_position == participant.team_position and p.summoner.name != participant.summoner.name:
                        participant.matchup = p
                        break

            for participant in match.participants:
                position = participant.team_position.value if participant.team_position != None else ""
                muchamp = participant.matchup.champion.name if participant.matchup is not None else ""
                prow = [match.id, match.region.value, (match.creation.timestamp / 86400) + 25569.00,
                        match.version.split(".")[0] + "." + match.version.split(".")[1],
                        (match.duration * 1000).seconds,
                        "",
                        participant.summoner.name, position, "", participant.champion.name, participant.side.name,
                        muchamp]
                prow += [rune.name for rune in participant.runes]
                for rune in participant.runes:
                    if isinstance(participant.runes[rune], list):
                        rperks = participant.runes[rune]
                    else:
                        rperks = participant.runes[rune][1]
                    prow += rperks
                prow += getBuildFormatted(participant, cass_items)
                prow += getSkillOrder(participant)
                prow.append(participant.summoner_spell_d.name)
                prow.append(participant.summoner_spell_f.name)
                prow += [p.champion.name for p in participant.team.participants]
                prow += [p.champion.name for p in participant.enemy_team.participants]
                prow += [int(participant.stats.win), participant.stats.kills, participant.stats.deaths,
                         participant.stats.assists]
                toRet.append(prow)
        buffer += toRet
    except Exception as e:
        print(e)
        print(region)
        raise e
        os._exit(1)
    return toRet


def getBuildFormatted(participant: cassiopeia.core.match.Participant, items_cass):
    items_ordered = []
    boots = ""
    for event in participant.timeline.events:
        try:
            if hasattr(event, "item_id"):
                item = None
                for it in items_cass:
                    if str(it.id) == str(event.item_id):
                        item = it
                        break
                if item is None:
                    raise Exception("Item " + str(event.item_id) + " was not found!")
                # item = cassiopeia.core.Item(id=event.item_id, region="EUW")
                if hasattr(item, "gold"):
                    if event.type == "ITEM_PURCHASED" and item.gold.total > 1700:
                        if item.name not in items_ordered and len(items_ordered) <= 6:
                            items_ordered.append(item.name)
                    if (
                            event.type == "ITEM_SOLD" or event.type == "ITEM_DESTROYED" or event.type == "ITEM_UNDO") and item.name != "Manamune" and participant.champion.name != "Viego" and len(
                        items_ordered) > 0:
                        if item.name == items_ordered[len(items_ordered) - 1]:
                            items_ordered.remove(item.name)
                    if event.type == "ITEM_PURCHASED" and 'Boots' in item.tags:
                        boots = item.name
                    # if event.type == "ITEM_SOLD" or event.type == "ITEM_DESTROYED" or event.type == "ITEM_UNDO" and 'Boots' in item.tags and item.name == boots:
                    #    boots = ""
        except Exception as e:
            print("Build error" + str(e))
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


def getSkillOrder(participant: cassiopeia.core.match.Participant):
    sko = [skill.keyboard_key.value for skill in participant.skill_order]
    while len(sko) < 23:
        sko.append("")
    return sko
