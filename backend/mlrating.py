import pandas as pd
import numpy as np
import collections


def get_champions_ratings(formattedGames):
    toRet = {}
    separated_games = {}
    for game in formattedGames:
        champion_role_patch = game[10] + "-" + game[8] + "-" + game[3]
        if champion_role_patch not in separated_games.keys():
            separated_games[champion_role_patch] = np.array([game])
        else:
            separated_games[champion_role_patch] = np.append(separated_games[champion_role_patch], np.array(game))

    for champion_role_patch in separated_games.keys():
        print(champion_role_patch)
        print(len(separated_games[champion_role_patch]))
        wins = separated_games[champion_role_patch][:, 24]

        for variable_type in range(12):
            pass


class championRatings():
    def __init__(self, champion, correls, averages, sds, values, wins, games):
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

    def getPerformances(self):
        columns = np.array([])
        for axis in range(12):
            standardized = (self.values[axis] - self.averages[axis]) / self.sds[axis]
            with_coeff = standardized * self.correls[axis]
            try:
                columns = np.vstack([columns, with_coeff])
            except:
                columns = np.array(with_coeff)

        individualPerformances = np.sum(columns, axis=0) / np.sum(np.abs(self.correls)) * 100
        return individualPerformances

    """champion compared is the column, self is the row"""

    def compare_champion(self, champion_compared):
        if self.champion == "Lux-UTILITY-11.24":
            print(champion_compared.champion)
        columns = np.array([])
        for axis in range(12):
            divider = np.max([np.abs(champion_compared.averages[axis] - self.averages[axis]), self.sds[axis]])
            standardized = (champion_compared.values[axis] - self.averages[axis]) / divider
            with_coeff = standardized * champion_compared.correls[axis]
            try:
                columns = np.vstack([columns, with_coeff])
            except:
                columns = np.array(with_coeff)

        individualPerformances = np.sum(columns, axis=0) / np.sum(np.abs(champion_compared.correls))
        return np.average(individualPerformances) * 100

    def get_winrate(self):
        return np.sum(self.wins) / len(self.wins)

    def get_games_amount(self):
        return len(self.wins)


def get_champions_ratings(separated_games):
    toRet = []
    for champion_role_patch in separated_games.keys():
        try:
            wins = separated_games[champion_role_patch][:, 24].astype(np.float)
            correls = np.array([])
            averages = np.array([])
            sds = np.array([])
            values = []

            for variable_type in range(12):
                vrows = separated_games[champion_role_patch][:, 12 + variable_type].astype(np.float)
                correl = np.corrcoef(vrows, wins)[0][1]
                avg = np.average(vrows)
                sd = np.std(vrows)
                correls = np.append(correls, correl)
                averages = np.append(averages, avg)
                sds = np.append(sds, sd)
                values.append(vrows)
            championRating = championRatings(champion_role_patch, correls, averages, sds, values, wins,
                                             separated_games[champion_role_patch])
            toRet.append(championRating)
        except:
            pass
    return toRet


print("ratings")

"""Gives rrate of a champion"""
def get_champion_rrate(champion, ratings):
    rrates = np.array([])
    for rating in ratings:
        if rating.role == champion.role and rating.patch == champion.patch:
            rrate = rating.compare_champion(champion)
            if not np.isnan(rrate):
                rrates = np.append(rrates, rrate)
    return np.average(rrates)

def get_many_champions_rrate(ratings):
    rrates = {}
    for rating in ratings:
        rrates[rating.champion] = [get_champion_rrate(rating, ratings), rating.get_games_amount(), rating.get_winrate()]
    return rrates
