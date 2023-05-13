import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


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


@app.route('/showSummary', methods=['POST'])
def showSummary():
    # Check if email exist or check name and redirect to "welcome"
    if request.form.get('email'):
        club = [club for club in clubs if club['email'] == request.form['email']]
    else:
        club = [club for club in clubs if club['name'] == request.form['club']]
    if club:
        return render_template('welcome.html',
                               club=club[0],
                               competitions=competitions,
                               datetime=str(datetime.now())
                               )

    # else redirect to 'index' with message error
    else:
        flash('Sorry, that email wasn\'t found.')
        return redirect('/')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
        flash("This competition is over")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               datetime=str(datetime.now())
                               )
    elif foundClub and foundCompetition:
        return render_template('booking.html',
                               club=foundClub,
                               competition=foundCompetition
                               )
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions
                               )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    # check if enough places available
    if datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
        flash("This competition is over")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               datetime=str(datetime.now())
                               )
    elif 0 <= placesRequired <= 12 and placesRequired <= int(competition['numberOfPlaces']):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        # check if enough points available
        if int(club['points']) >= placesRequired:
            club['points'] = int(club['points']) - placesRequired
            flash('Great-booking complete!')
        else:
            flash('You don\'t have enough points available')
    else:
        flash('Not enough place available')
    return redirect('/showSummary', code=307)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
