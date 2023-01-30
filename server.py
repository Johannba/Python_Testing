from datetime import datetime
import json
from flask import Flask, make_response,render_template,request,redirect,flash,url_for

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club, clubs=clubs, competitions=competitions)
    except IndexError:
        flash("E-mail is unknown, please enter a valid e-mail !")
        return render_template('index.html')


@app.route('/book/<competition>/<club>', methods=['GET'])
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        if datetime.strptime(found_competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            flash("You cannot book places in a past competition")
            return render_template('welcome.html',club=found_club, clubs=clubs, competitions=competitions)
        else:
            return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',club=found_club, clubs=clubs, competitions=competitions)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    club_points = int(club['points'])
    if placesRequired <= 12:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = str(club_points - placesRequired)
        flash('Great-booking complete!')
    else:
        flash("You can't purchase more than 12 places !")
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
