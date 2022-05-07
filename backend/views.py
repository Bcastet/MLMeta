from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from .mlrating import *
from django.forms.models import model_to_dict


# Create your views here.

class ChampionRatingView(viewsets.ModelViewSet):
    serializer_class = ChampionRatingSerializer
    queryset = ChampionRating.objects.all()

    def get_queryset(self):
        id = self.request.query_params.get("id")
        patch = self.request.query_params.get("patch")
        role = self.request.query_params.get("role")
        leagues = self.request.query_params.get("leagues")
        print(leagues)
        if leagues is None:
            queryset = ChampionRating.objects.all()
            if id is not None:
                queryset = queryset.filter(id=id)
            if patch is not None:
                queryset = queryset.filter(patch=patch)
            if role is not None:
                queryset = queryset.filter(role=role)
            return queryset
        else:
            games = GameSummaryCompetitive.objects.all()
            leagues = leagues.split(",")
            print(leagues)
            if patch is not None:
                games = games.filter(patch=patch)
            if role is not None:
                games = games.filter(role=role)
            print(games.values())
            if leagues is not None:
                games = games.filter(league__in=leagues)
            games = games.values()
            orderedNames = ["gameid", "league", "date", "patch", "duration", "player", "team1", "team2", "side", "role",
                            "champion",
                            "keystone", "rune1", "rune2", "rune3", "rune4", "rune5", "statrune1", "statrune2",
                            "statrune3", "ally1", "ally2", "ally3", "ally4", "ally5", "ennemy1", "ennemy2", "ennemy3",
                            "ennemy4",
                            "ennemy5", "item1", "item2", "item3", "item4", "item5", "item6", "boots", "trinket",
                            "summoner1",
                            "summoner2", "relativeKills", "relativeDeaths", "relativeDamages", "relativeDamageTaken",
                            "relativeGolds",
                            "relativeDmgHealed", "relativeDmgMitigated", "relativeMinionsKilled", "relativeWardsPlaced",
                            "relativeWardsKilled", "relativeLevel", "relativeCCtime", "outcome", "performance"]
            content = np.array([])
            for i in range(len(games)):
                row = np.array([games[i][n] for n in orderedNames])
                try:
                    content = np.vstack([content, row])
                except:
                    content = row
            separated = separateGames(content, roleIndex=9)
            ratings = get_champions_ratings(separated, parameters=12, headers=54 - 14)
            rrates = get_many_champions_rrate(ratings)

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

            rrates = map_dict(rrates)
            content = []
            for row in rrates:
                if row[1] != "":
                    row_data = {"id": row[0], "rel_rate": row[1], "games": row[2], "winrate": row[3],
                                "name": row[0].split("-")[0],
                                "role": row[0].split("-")[1], "patch": row[0].split("-")[2]}
                    content.append(row_data)
            return content


class SoloQMatchPerformanceView(viewsets.ModelViewSet):
    serializer_class = GameSummarySerializerSoloQ
    queryset = GameSummarySoloQ.objects.all()


class TeamImagesView(viewsets.ModelViewSet):
    serializer_class = TeamImagesSerializers
    queryset = TeamImages.objects.all()


class ChampionsBuildPropertiesView(viewsets.ModelViewSet):
    serializer_class = ChampionsBuildPropertiesSerializer
    queryset = ChampionsBuildProperties

    def get_queryset(self):
        patch = self.request.query_params.get("patch")
        role = self.request.query_params.get("role")
        leagues = self.request.query_params.get("leagues")
        champion = self.request.query_params.get("champion")
        if leagues is not None:
            leagues = leagues.split(",")
        queryset = GameSummaryCompetitive.objects.all()
        if patch is not None:
            queryset = queryset.filter(patch=patch)
        if role is not None:
            queryset = queryset.filter(role=role)
        if leagues is not None:
            queryset = queryset.filter(league__in=leagues)
        if champion is not None:
            queryset = queryset.filter(champion=champion)
        games = queryset.values()
        if len(games) == 0:
            return [{"keystones": [], "first_items": []}]
        keystones = {}
        first_items = {}
        for game in games:
            if game["keystone"] not in keystones:
                obj = {"name": game["keystone"], "games": 1, "performance": [game["performance"]],
                       "winrate": game["outcome"], "relative_performance": [game["relative_performance"]]}
                keystones[game["keystone"]] = obj
            else:
                keystones[game["keystone"]]["games"] += 1
                keystones[game["keystone"]]["performance"].append(game["performance"])
                keystones[game["keystone"]]["winrate"] += game["outcome"]
                keystones[game["keystone"]]["relative_performance"].append(game["relative_performance"])

            if game["item1"] not in first_items:
                obj = {"name": game["item1"], "games": 1, "performance": [game["performance"]],
                       "winrate": game["outcome"], "relative_performance": [game["relative_performance"]]}
                first_items[game["item1"]] = obj
            else:
                first_items[game["item1"]]["games"] += 1
                first_items[game["item1"]]["performance"].append(game["performance"])
                first_items[game["item1"]]["winrate"] += game["outcome"]
                first_items[game["item1"]]["relative_performance"].append(game["relative_performance"])

        keystones_toRet = []
        for index, name in enumerate(keystones):
            keystones[name]["performance"] = np.average(keystones[name]["performance"])
            keystones[name]["winrate"] = keystones[name]["winrate"] / keystones[name]["games"]
            keystones[name]["relative_performance"] = np.average(keystones[name]["relative_performance"])
            keystones[name]["id"] = index
            keystones_toRet.append(keystones[name])

        first_items_toRet = []
        for index, name in enumerate(first_items):
            first_items[name]["performance"] = np.average(first_items[name]["performance"])
            first_items[name]["winrate"] = first_items[name]["winrate"] / first_items[name]["games"]
            first_items[name]["relative_performance"] = np.average(first_items[name]["relative_performance"])
            first_items_toRet.append(first_items[name])

        return [{"keystones": keystones_toRet, "first_items": first_items_toRet}]


class CompetitiveMatchPerformanceView(viewsets.ModelViewSet):
    serializer_class = GameSummarySerializerCompetitive
    queryset = GameSummaryCompetitive.objects.all()

    def get_queryset(self):
        print(self.request.query_params)
        id = self.request.query_params.get("gameid")
        patch = self.request.query_params.get("patch")
        role = self.request.query_params.get("role")
        leagues = self.request.query_params.get("leagues")
        champion = self.request.query_params.get("champion")
        if leagues is not None:
            leagues = leagues.split(",")
        print(leagues)
        queryset = GameSummaryCompetitive.objects.all()
        print(queryset)
        if id is not None:
            queryset = queryset.filter(gameid=id)
        if patch is not None:
            queryset = queryset.filter(patch=patch)
        if role is not None:
            queryset = queryset.filter(role=role)
        if leagues is not None:
            queryset = queryset.filter(league__in=leagues)
        if champion is not None:
            queryset = queryset.filter(champion=champion)
        return queryset
