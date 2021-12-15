
from cassiopeia import Summoner, Champions
from cassiopeia.cassiopeia import set_riot_api_key
import json
from types import SimpleNamespace

class LeagueApi:
    def __init__(self, summoner_name, region="NA") -> None:
        set_riot_api_key("RGAPI-06cdaf93-f52b-4792-ae69-e12db5664c9c")
        
        self.summoner_name = summoner_name
        self.region = region

        self.summoner = Summoner(
            name=self.summoner_name,
            region=self.region
            )

    def live_game(self):
        self.current_match = self.summoner.current_match.to_dict()

        self.inGameSummoner = None # In game data of our Summoner
        for participant in self.current_match["participants"]: 
            if participant["summonerId"] == self.current_match["summonerId"]:
                self.inGameSummoner = participant

        self.enemy_team = [participant for participant in self.current_match["participants"] if participant["teamId"] != self.inGameSummoner["teamId"]]

        # inGameSummonerChampion = Champions(region="NA").find(self.inGameSummoner["championId"])


        response = {
            "summoner:": {
                "summoner_spells": ["", ""]
            }
        }

        return json.dumps(response)
        
    
    def championId_to_data(championID):
        response = {
            "champion_name": "",
            
        }

