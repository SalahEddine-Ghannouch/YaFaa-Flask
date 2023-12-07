from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
import eloClub as eloClub


app = Flask(__name__)


#! ****************** Home Page
@app.route('/')
def index_home():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var
    }
    return render_template('index.html', **additional_data)

#! ****************** Fixtures Page
@app.route('/fixtures')
def fixtures_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var
    }
    return render_template('fixture.html', **additional_data,fixtcss="fixtcss")


#! ****************** eng Page
@app.route('/eng', methods=['GET', 'POST'])
def eng_func():

    #? Get Current Year
    date_var = datetime.now().year
    #? Get season
    years = eloClub.generate_years()
    #? Tretement for elo data
    if request.method == 'POST':
        selected_year = int(request.form.get('season'))
        elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'ENG-Premier League')
    else:
        # Default to the current year
        selected_year = date_var
        elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'ENG-Premier League')

    #? figure displaying : 
    fig = eloClub.plot_elo_histogram(elo_eng, 'ENG-Premier League')
    graph_json = fig

    #? send Data here : 
    additional_data = {
        'current_date': date_var,
        'active': 'side-bar__list-item--active',
        'active_link': 'eng',
        'season_available': years,
        'season_selected': selected_year,
        'elo_data': elo_eng.to_dict(orient='records'),  # Convert DataFrame to a list of dictionaries
        'graph_json':graph_json
    }

    return render_template('fixt/eng.html', **additional_data)


#! ****************** fra Page
@app.route('/fra', methods=['GET', 'POST'])
def fra_func():
    #? Get Current Year
    date_var = datetime.now().year
    #? Get season
    years = eloClub.generate_years()
    #? Tretement for elo data
    if request.method == 'POST':
        selected_year = int(request.form.get('season'))
        elo_fra = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'FRA-Ligue 1')
    else:
        # Default to the current year
        selected_year = date_var
        elo_fra = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'FRA-Ligue 1')

    #? figure displaying : 
    fig = eloClub.plot_elo_histogram(elo_fra, 'FRA-Ligue 1')
    graph_json = fig

    #? send Data here : 
    additional_data = {
        'current_date': date_var,
        'active': 'side-bar__list-item--active',
        'active_link': 'fra',
        'season_available': years,
        'season_selected': selected_year,
        'elo_data': elo_fra.to_dict(orient='records'),  # Convert DataFrame to a list of dictionaries
        'graph_json':graph_json
    }
    return render_template('fixt/fra.html', **additional_data)


#! ****************** ger Page
@app.route('/ger', methods=['GET', 'POST'])
def ger_func():
    #? Get Current Year
    date_var = datetime.now().year
    #? Get season
    years = eloClub.generate_years()
    #? Tretement for elo data
    if request.method == 'POST':
        selected_year = int(request.form.get('season'))
        elo_ger = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'GER-Bundesliga')
    else:
        # Default to the current year
        selected_year = date_var
        elo_ger = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'GER-Bundesliga')

    #? figure displaying : 
    fig = eloClub.plot_elo_histogram(elo_ger, 'GER-Bundesliga')
    graph_json = fig

    #? send Data here : 
    additional_data = {
        'current_date': date_var,
        'active': 'side-bar__list-item--active',
        'active_link': 'ger',
        'season_available': years,
        'season_selected': selected_year,
        'elo_data': elo_ger.to_dict(orient='records'),  # Convert DataFrame to a list of dictionaries
        'graph_json':graph_json
    }
    return render_template('fixt/ger.html', **additional_data)


#! ****************** esp Page
@app.route('/esp', methods=['GET', 'POST'])
def esp_func():
    #? Get Current Year
    date_var = datetime.now().year
    #? Get season
    years = eloClub.generate_years()
    #? Tretement for elo data
    if request.method == 'POST':
        selected_year = int(request.form.get('season'))
        elo_esp = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'ESP-La Liga')
    else:
        # Default to the current year
        selected_year = date_var
        elo_esp = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'ESP-La Liga')

    #? figure displaying : 
    fig = eloClub.plot_elo_histogram(elo_esp, 'ESP-La Liga')
    graph_json = fig

    #? send Data here : 
    additional_data = {
        'current_date': date_var,
        'active': 'side-bar__list-item--active',
        'active_link': 'esp',
        'season_available': years,
        'season_selected': selected_year,
        'elo_data': elo_esp.to_dict(orient='records'),  # Convert DataFrame to a list of dictionaries
        'graph_json':graph_json
    }
    return render_template('fixt/esp.html', **additional_data)


#! ****************** ita Page
@app.route('/ita', methods=['GET', 'POST'])
def ita_func():
     #? Get Current Year
    date_var = datetime.now().year
    #? Get season
    years = eloClub.generate_years()
    #? Tretement for elo data
    if request.method == 'POST':
        selected_year = int(request.form.get('season'))
        elo_ita = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'ITA-Serie A')
    else:
        # Default to the current year
        selected_year = date_var
        elo_ita = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'ITA-Serie A')

    #? figure displaying : 
    fig = eloClub.plot_elo_histogram(elo_ita, 'ITA-Serie A')
    graph_json = fig

    #? send Data here : 
    additional_data = {
        'current_date': date_var,
        'active': 'side-bar__list-item--active',
        'active_link': 'ita',
        'season_available': years,
        'season_selected': selected_year,
        'elo_data': elo_ita.to_dict(orient='records'),  # Convert DataFrame to a list of dictionaries
        'graph_json':graph_json
    }
    return render_template('fixt/ita.html', **additional_data)


if __name__ == '__main__':
    app.run(debug=True)
