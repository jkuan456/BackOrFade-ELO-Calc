import pandas as pd
from flask import Flask, jsonify, request
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

app = Flask(__name__)


fullTeams = [
    "Man City",
    "Arsenal",
    "Liverpool",
    "Aston Villa",
    "Newcastle",
    "Tottenham",
    "Man United",
    "Chelsea",
    "West Ham",
    "Brighton",
    "Brentford",
    "Crystal Palace",
    "Fulham",
    "Everton",
    "Bournemouth",
    "Wolves",
    "Forest",
    "Burnley",
    "Luton",
    "Sheffield United"
]

teams = [team.replace(" ", "").lower() for team in fullTeams]

today = datetime.now()
lastWeek = today - relativedelta(days = 7)

todayDf = pd.read_csv('http://api.clubelo.com/{}-{}-{}'.format(today.year, today.month, today.day))

lastDf = pd.read_csv('http://api.clubelo.com/{}-{}-{}'.format(lastWeek.year, lastWeek.month, lastWeek.day))


def getElo(team):
    todayDf = pd.read_csv(f'http://api.clubelo.com/{today.year}-{today.month:02d}-{today.day:02d}')
    mask = todayDf['Club'] == team
    if not mask.any():
        return "Team not found in the database", 404  # Handling the case where no team matches

    value = todayDf.loc[mask, 'Elo'].iloc[0]  # Directly accessing the first matching Elo rating
    return int(value)


getElo('Arsenal')

@app.route('/teams', methods=['POST'])
def get_rank():
    # Payload = team
    if not request.json or not 'team' in request.json:
        return jsonify({'message': 'Bad request'}), 400
    team = request.json['team']
    print(team)
    return jsonify({'rating': getElo(team)})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')



