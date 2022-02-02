import cassiopeia
import arrow
import numpy as np
import threading

soloQ = cassiopeia.Queue.ranked_solo_fives


def getTopSoloQPlayers(region):
    challengers = cassiopeia.get_challenger_league(queue=soloQ, region=region)
    print(str(len(challengers))+ " challengers in "+region.value)
    grandmasters = cassiopeia.get_grandmaster_league(queue=soloQ, region=region)
    print(str(len(grandmasters)) + " grandmasters in " + region.value)
    return challengers, grandmasters


def getMastersSoloQPlayers(region):
    masters = cassiopeia.get_master_league(queue=soloQ, region=region)
    return masters


def getTopGameIds(topplayers, continent):
    hists = []
    thrs = []

    for topplayer in topplayers:
        start_time = arrow.get(1641944223)
        end_time = arrow.utcnow()
        thr = threading.Thread(target=add_hist, args=(continent, topplayer, start_time, end_time, hists))
        thr.start()
        thrs.append(thr)

    for thr in thrs:
        thr.join()

    hists = [match.id for match in hists]
    return np.array(hists)

def add_hist(continent, topplayer, start_time, end_time, buffer):
    hist = cassiopeia.get_match_history(continent=continent, puuid=topplayer.summoner.puuid,
                                        start_time=start_time, end_time=end_time,
                                        queue=cassiopeia.Queue.ranked_solo_fives, start=0, count=100)
    buffer.extend(hist)