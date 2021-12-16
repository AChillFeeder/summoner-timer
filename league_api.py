
from cassiopeia import Summoner, Champions, Rune, SummonerSpell
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

        response = {}

        for opponent in self.enemy_team:
            response[opponent["summonerName"]] = {
                "champion_name": Champions(region="NA").find(opponent["championId"]).name,
                "champion_icon": f'https://cdn.communitydragon.org/latest/champion/{opponent["championId"]}/square',
                "champion_vfx": f'https://cdn.communitydragon.org/latest/champion/{opponent["championId"]}/champ-select/sounds/sfx',
                "summoner_spells": [
                    {
                        "name": SummonerSpell(id=opponent["spell1Id"],region="NA").name,
                        "cooldown": SummonerSpell(id=opponent["spell1Id"],region="NA").cooldowns,
                        # "image": SummonerSpell(id=opponent["spell1Id"],region="NA").image
                        "image": f'http://ddragon.leagueoflegends.com/cdn/8.11.1/img/spell/{SummonerSpell(id=opponent["spell1Id"],region="NA").key}.png' 
                    },
                    {
                        "name": SummonerSpell(id=opponent["spell2Id"],region="NA").name,
                        "cooldown": SummonerSpell(id=opponent["spell2Id"],region="NA").cooldowns,
                        # "image": SummonerSpell(id=opponent["spell2Id"],region="NA").image
                        "image": f'http://ddragon.leagueoflegends.com/cdn/8.11.1/img/spell/{SummonerSpell(id=opponent["spell2Id"],region="NA").key}.png' 
                    }
                ],
                "has_cosmic_insight": "Cosmic Insight" in [Rune(id=runeID,region="NA").name for runeID in opponent["perks"]["perkIds"]]
            }

        # response = self.enemy_team

        return response
        
    

