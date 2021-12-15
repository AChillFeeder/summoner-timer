from flask import Flask
from league_api import LeagueApi

import json

app = Flask(__name__)

@app.route('/')
def index():
    pass

@app.route('/test')
def test():
    summoner_name = "7423"
    Summoner = LeagueApi(summoner_name)
    live_game = Summoner.live_game()

    return live_game



if __name__ == '__main__':
    app.run('0.0.0.0', 8000, True)
