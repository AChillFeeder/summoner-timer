from flask import Flask, render_template, request, redirect, url_for
from flask import session

from services.league_api import LeagueApi
from functools import wraps


app = Flask(__name__)
app.secret_key = "random key"


def Checks(function):
    @wraps(function)
    def decorated_func(*args, **kwargs):
        if session.get('summoner_name'):
            return function(*args, **kwargs)
        else:
            return redirect("/")
    return decorated_func



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['summoner_name'] = request.form["summoner_name_input"]
        return redirect(url_for("live_game"))
    return render_template("index.html")


@app.route('/live_game')
@Checks
def live_game():
    Summoner = LeagueApi(session.get('summoner_name'))
    live_game, static_data = Summoner.live_game()
    return render_template("live_game.html", data=live_game, static_data=static_data)



    

if __name__ == '__main__':
    app.run('0.0.0.0', 8000, True)
