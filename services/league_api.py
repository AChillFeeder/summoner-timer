
from cassiopeia import Summoner, Champions, Rune, SummonerSpell
from cassiopeia.cassiopeia import set_riot_api_key
import json

class LeagueApi:
    def __init__(self, summoner_name, region="NA") -> None:
        self.API_key = "RGAPI-5e7eb323-086e-4867-8dfe-c289d37b98df"
        set_riot_api_key(self.API_key)
        
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
                "has_cosmic_insight": "Cosmic Insight" in [Rune(id=runeID,region="NA").name for runeID in opponent["perks"]["perkIds"]],
                "summoner_spells": [
                    {
                        "name": SummonerSpell(id=opponent["spell1Id"],region="NA").name,
                        "cooldown": SummonerSpell(id=opponent["spell1Id"],region="NA").cooldowns,
                        "image": f'http://ddragon.leagueoflegends.com/cdn/8.11.1/img/spell/{SummonerSpell(id=opponent["spell1Id"],region="NA").key}.png' 
                    },
                    {
                        "name": SummonerSpell(id=opponent["spell2Id"],region="NA").name,
                        "cooldown": SummonerSpell(id=opponent["spell2Id"],region="NA").cooldowns,
                        "image": f'http://ddragon.leagueoflegends.com/cdn/8.11.1/img/spell/{SummonerSpell(id=opponent["spell2Id"],region="NA").key}.png' 
                    }
                ],
                
            }


        # Teleport is bugged and shows a cooldown of 0, setting the correct value manually
        # warn the user that TP scales with levels and so will show wrong values later in the game
        for player in response:
            for summoner_spell in response[player]["summoner_spells"]:
                if summoner_spell["name"] == "Teleport":
                    summoner_spell["cooldown"] = [420]

        static_data = {
            "lucidity boots": {
                "icon": "https://raw.communitydragon.org/latest/game/assets/items/icons2d/3158_class_t2_ionianbootsoflucidity.png",
                "haste": 12,
            },
            "cosmic insight": {
                "icon": "https://raw.communitydragon.org/latest/game/assets/perks/styles/inspiration/cosmicinsight/cosmicinsight.png",
                "haste": 18,
            }
        }

        return response , static_data # returns a json file of static data like: Cosmic insight and lucidity boots icon
        
    

