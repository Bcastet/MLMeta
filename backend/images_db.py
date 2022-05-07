import numpy as np
import requests
from PIL import Image
from io import BytesIO
from os import path
import cloudinary
from cloudinary import uploader
import cassiopeia
import arrow

cloudinary.config(
        cloud_name="xenesis",
        api_key="436812349635739",
        api_secret="1sBjge7_-F7ByZ1SuigUc6nvXsA"
    )

def getTeamsLogos():

    current = requests.get("http://127.0.0.1:8000/competitiveGames/?format=json").json()
    rows = current["results"]
    while current["next"] != None:
        current = requests.get(current["next"]).json()
        rows += current["results"]
    print(rows)
    teams = []
    for row in rows:
        team_name = row["team1"]
        teams.append(team_name)
        team_name = row["team2"]
        teams.append(team_name)

    print(len(teams))
    teams = np.array(teams)
    teams = np.unique(teams)
    print(len(teams))
    print(teams)
    db = []
    for team in teams:
        if not path.exists("C:/Users/Xenesis/Pictures/TeamLogos/"+team+".png"):
            team_url = "https://lol.fandom.com/api.php?action=query&format=json&prop=imageinfo&titles=File%3A"+team+"logo%20square.png&iiprop=url"
            res = requests.get(team_url).json()
            logo_url = ""
            for k in res["query"]["pages"]:
                logo_url = res["query"]["pages"][k]["imageinfo"][0]["url"]
            print(logo_url)
            logo = requests.get(logo_url, stream=True).content
            Image.open(BytesIO(logo)).save("C:/Users/Xenesis/Pictures/TeamLogos/"+team+".png")
        team_data = {"name" : team, "logo" : open("C:/Users/Xenesis/Pictures/TeamLogos/"+team+".png","rb")}
        db.append(team_data)
        print(team)

    def post_images(images_data):
        for image in images_data:
            uploader.upload("C:/Users/Xenesis/Pictures/TeamLogos/" + image["name"] + ".png",
                            folder="teamsLogo/",
                            public_id=image["name"],
                            overwrite=True,
                            resource_type="image")


    post_images(db)

def getRunesAssets():
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
    runes = cassiopeia.Runes(region="EUW")
    for rune in runes:
        rune.image.image.save("C:/Users/Xenesis/Pictures/LeagueAssets/"+rune.name+".png")
        uploader.upload("C:/Users/Xenesis/Pictures/LeagueAssets/"+rune.name+".png",
                        folder="leagueAssets/",
                        public_id=rune.name,
                        overwrite=True,
                        resource_type="image")

getRunesAssets()