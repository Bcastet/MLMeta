import os
import cassiopeia
import pickle
import json
import time


class database():
    def __init__(self, dbpath="D:/CassiopeiaDatabase"):
        self.dbpath = dbpath
        self.db_settings = database_settings()
        self.files_opened = {}

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

    def get_match(self, match_id, region):
        matchpath = os.path.join(self.dbpath, match_id + ".cass")
        if match_id in self.files_opened.keys():
            return self.files_opened[match_id]

        if os.path.exists(matchpath):
            try:
                # print(match_id + ".cass found in database, no call needed")
                match = pickle.load(open(matchpath, "rb"))
                self.files_opened[match_id] = match
                return match
            except (UnicodeDecodeError, EOFError) as e:
                print(str(e) + "for file " + matchpath)
                match = self.request_match(match_id, region, matchpath)
        else:
            match = self.request_match(match_id, region, matchpath)
        self.files_opened[match_id] = match
        return match

    def write_match(self, cassmatch, matchpath):
        pickle.dump(cassmatch, open(matchpath, "wb+"))
        self.db_settings.update_settings(cassmatch)
        return cassmatch

    def request_match(self, match_id, region, matchpath):
        match = cassiopeia.get_match(match_id, region=region)
        try:
            timeline = match.timeline.frames
        except:
            time.sleep(10)
            return self.request_match(match_id, region, matchpath)
            #raise Exception("No timeline found in match", match_id, region)
        self.write_match(match, matchpath)
        return match


class database_settings():
    def __init__(self, dbpath="D:/CassiopeiaDatabase"):
        self.settings_file = os.path.join(dbpath, "dbsettings.json")
        self.json = json.load(open(self.settings_file, 'r'))
        self.last_match_timestamp = self.json["last_match"]
        self.first_match_timestamp = self.json["first_match"]

    def update_settings(self, new_match):
        if new_match.creation.int_timestamp > self.last_match_timestamp:
            self.json["last_match"] = new_match.creation.int_timestamp
        if new_match.creation.int_timestamp < self.first_match_timestamp:
            self.json["first_match"] = new_match.creation.int_timestamp

    def write_new_json(self):
        with open(self.settings_file, "w+") as s:
            json.dump(self.json, s)
