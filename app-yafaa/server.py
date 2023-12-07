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
    graph_json = fig.to_json()

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
@app.route('/fra')
def fra_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var,
        'active':'side-bar__list-item--active',
        'active_link':'fra'    
    }
    return render_template('fixt/fra.html', **additional_data)


#! ****************** ger Page
@app.route('/ger')
def ger_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var,
        'active':'side-bar__list-item--active',
        'active_link':'ger'

    }
    return render_template('fixt/ger.html', **additional_data)

    #****************** esp Page
@app.route('/esp')
def esp_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var,
        'active':'side-bar__list-item--active',
        'active_link':'esp'

    }
    return render_template('fixt/esp.html', **additional_data)

    #****************** ita Page
@app.route('/ita')
def ita_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var,
        'active':'side-bar__list-item--active',
        'active_link':'ita'

    }
    return render_template('fixt/ita.html', **additional_data)


if __name__ == '__main__':
    app.run(debug=True)
