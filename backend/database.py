import os
import cassiopeia
import pickle
import json


class database():
    def __init__(self, dbpath="D:/CassiopeiaDatabase"):
        self.dbpath = dbpath
        self.db_settings = database_settings()
        self.files_opened = {}

    def get_match(self, match_id, region):
        matchpath = os.path.join(self.dbpath, match_id + ".cass")
        if match_id in self.files_opened.keys():
            return self.files_opened[match_id]

        if os.path.exists(matchpath):
            try:
                print(match_id + ".cass found in database, no call needed")
                match = pickle.load(open(matchpath, "rb"))
                self.files_opened[match_id] = match
                return match
            except (UnicodeDecodeError, EOFError) as e:
                print(str(e) + "for file "+matchpath)
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
        timeline = match.timeline.frames()
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
            json.dump(self.json,s)
