import pandas as pd
import numpy as np
import collections


# from leaguepedia import *

class championRatings():
    def __init__(self, champion, correls, averages, sds, values, wins, games):
        self.parameters = len(correls)
        self.champion = champion
        self.correls = correls
        self.averages = averages
        self.sds = sds
        self.values = values
        self.wins = wins
        self.games = games
        self.performances = self.getPerformances()
        self.patch = champion.split("-")[2]
        self.role = champion.split("-")[1]

    """
    calculates the performance column.
    """

    def getPerformances(self):
        columns = np.array([])
        for axis in range(self.parameters):
            standardized = (self.values[axis] - self.averages[axis]) / self.sds[axis]
            with_coeff = standardized * self.correls[axis]
            try:
                columns = np.vstack([columns, with_coeff])
            except:
                columns = np.array(with_coeff)

        # print(columns.shape, (len(self.values),self.values[0].shape))
        # individualPerformances = np.sum(columns, axis=0) / np.sum(np.abs(self.correls)) * 100

        individualPerformances = np.array([])
        columns = np.transpose(columns)
        for perfRow in columns:
            correls_sum = np.sum(np.abs(self.correls[np.logical_not(np.isnan(perfRow))]))
            individualPerformances = np.append(individualPerformances,
                                               np.sum(perfRow[np.logical_not(np.isnan(perfRow))]) / correls_sum * 100)

        mean = np.mean(individualPerformances)
        sd = np.std(individualPerformances)
        return ((individualPerformances - mean) / sd) * 100

    def formattedGames(self, headers=40):
        print(self.games[:][:headers].shape, len(self.games), len(self.performances))
        return np.column_stack([self.games[:][:headers], self.performances, self.wins])

    """champion compared is the column, self is the row"""

    def compare_champion(self, champion_compared):
        if self.champion == "Lux-UTILITY-11.24":
            print(champion_compared.champion)
        columns = np.array([])
        for axis in range(self.parameters):
            divider = np.max([np.abs(champion_compared.averages[axis] - self.averages[axis]), self.sds[axis]])
            standardized = (champion_compared.values[axis] - self.averages[axis]) / divider
            with_coeff = standardized * champion_compared.correls[axis]
            try:
                columns = np.vstack([columns, with_coeff])
            except:
                columns = np.array(with_coeff)

        # individualPerformances = np.sum(columns, axis=0) / np.sum(np.abs(champion_compared.correls))
        columns = np.transpose(columns)
        individualPerformances = np.array([])
        for perfRow in columns:
            correls_sum = np.sum(np.abs(champion_compared.correls[np.logical_not(np.isnan(perfRow))]))
            individualPerformances = np.append(individualPerformances,
                                               np.sum(perfRow[np.logical_not(np.isnan(perfRow))]) / correls_sum)
        return np.average(individualPerformances) * 100

    def get_winrate(self):
        return np.sum(self.wins) / len(self.wins)

    def get_games_amount(self):
        return len(self.wins)


"""
calculates all the champions ratings for separated games.
Must give the number of metrics used (parameters) and the number of headers for each row.
"""


def get_champions_ratings(separated_games, parameters=12, headers=12):
    toRet = []
    for champion_role_patch in separated_games.keys():
        print(champion_role_patch)
        try:
            # print(separated_games[champion_role_patch][:, 12+parameters])
            wins = separated_games[champion_role_patch][:, parameters + headers].astype(float)
            correls = np.array([])
            averages = np.array([])
            sds = np.array([])
            values = []

            for variable_type in range(parameters):
                vrows = separated_games[champion_role_patch][:, headers + variable_type].astype(float)
                vrows_filtered = vrows[np.logical_not(np.isnan(vrows))]
                wins_filtered = wins[np.logical_not(np.isnan(vrows))]
                correl = np.corrcoef(vrows_filtered, wins_filtered)[0][1]
                avg = np.median(vrows_filtered)
                sd = np.std(vrows_filtered)
                correls = np.append(correls, correl)
                averages = np.append(averages, avg)
                sds = np.append(sds, sd)
                values.append(vrows)
            championRating = championRatings(champion_role_patch, correls, averages, sds, values, wins,
                                             separated_games[champion_role_patch])
            toRet.append(championRating)
        except Exception as e:
            print(e)
            pass
    return toRet


"""
calculate the relative rating of a champion compared to a set.
will only compare 2 champions if they have the same role and patch.
"""


def get_champion_rrate(champion, ratings):
    rrates = np.array([])
    for rating in ratings:
        if rating.role == champion.role and rating.patch == champion.patch and not np.isnan(rating.correls[0]):
            rrate = rating.compare_champion(champion)
            if not np.isnan(rrate):
                rrates = np.append(rrates, rrate)
    return np.average(rrates)


"""
calculate the rating of every champion for a given set.
will only compare 2 champions if they have the same role and patch.
"""


def get_many_champions_rrate(ratings):
    rrates = {}
    for rating in ratings:
        rrates[rating.champion] = [get_champion_rrate(rating, ratings), rating.get_games_amount(), rating.get_winrate()]
    return rrates


"""
separate games list into a dict where every game is identified with his champion:
{"Gragas":[game1;game2...]}
"""


def separateGames(formattedGames, roleIndex=8):
    toRet = {}
    for game in formattedGames:
        champion_role_patch = game[10] + "-" + game[roleIndex] + "-" + game[3]
        if champion_role_patch not in toRet.keys():
            toRet[champion_role_patch] = np.array([game])
        else:
            toRet[champion_role_patch] = np.vstack([toRet[champion_role_patch], np.array(game)])
    return toRet


""" 
calculates rrates and game_summaries from the given set of acs_games and lpl_games
"""


def getCompetitiveDatabase(acs_games, lpl_games):
    import arrow
    import pprint
    content = []

    for game in lpl_games:
        content += formatLPLGame(game)

    games = acs_games

    games.sort(key=lambda game: game["DateTime UTC"])
    for game in games:
        formatCompetitiveGame(game, content)

    content = np.array(content)

    separated = separateGames(content, roleIndex=9)
    ratings = get_champions_ratings(separated, parameters=12, headers=54 - 14)
    rrates = get_many_champions_rrate(ratings)
    rrates = map_dict(rrates)

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

    return content, rrates
