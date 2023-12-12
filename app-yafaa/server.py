from flask import Flask, redirect, url_for
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
@app.route('/fixt')
def fixtures_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var
    }
    return render_template('fixture.html', **additional_data,fixtcss="fixtcss")


#! ****************** about Page
@app.route('/about')
def about_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var
    }
    return render_template('about.html', **additional_data, aboutcss="aboutcss")


#! ****************** stats Page
@app.route('/stats')
def stats_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var
    }
    return render_template('stats.html', **additional_data)


#! --------------- process all cases : 
@app.route('/<path:route_argument>', methods=['GET', 'POST'])
def dynamic_route(route_argument):
    
    # Split the route_argument into navbar_selected and league_code
    parts = route_argument.split('/')
    navbar_selected = parts[0]
    league_code = parts[1] if len(parts) > 1 else None


    #? ------------ case for elo navbar selected : 
    if navbar_selected =='elo' and (league_code in ('eng','fra','ger','esp','ita')):
        #? Get Current Year
        date_var = datetime.now().year
        league_name = ''
        #? Get season
        years = eloClub.generate_years()
        #? Tretement for elo data
        if league_code =='eng':
            league_name = 'ENG-Premier League'
        if league_code =='fra':
            league_name = 'FRA-Ligue 1'
        if league_code =='ger':
            league_name = 'GER-Bundesliga'
        if league_code =='esp':
            league_name = 'ESP-La Liga'
        if league_code =='ita':
            league_name = 'ITA-Serie A'
        
        if request.method == 'POST':
            selected_year = int(request.form.get('season'))
            elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year,league_name )
        else:
            # Default to the current year
            selected_year = date_var
            elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'ENG-Premier League')

        #? figure displaying : 
        fig = eloClub.plot_elo_histogram(elo_eng, league_name)
        graph_json = fig

        #? send Data here : 
        additional_data = {
            'current_date': date_var,
            'active': 'side-bar__list-item--active',
            'active_link': league_code,
            'season_available': years,
            'season_selected': selected_year,
            'elo_data': elo_eng.to_dict(orient='records'),  # Convert DataFrame to a list of dictionaries
            'graph_json':graph_json
        }
    
    #?----------------- case of fixtures navbar selected
    if navbar_selected =='fixt' and (league_code in ('eng','fra','ger','esp','ita')):
        #? Get Current Year
        date_var = datetime.now().year
        league_name = ''
        #? Get season
        years = eloClub.generate_years()
        #? Tretement for elo data
        if league_code =='eng':
            league_name = 'ENG-Premier League'
        if league_code =='fra':
            league_name = 'FRA-Ligue 1'
        if league_code =='ger':
            league_name = 'GER-Bundesliga'
        if league_code =='esp':
            league_name = 'ESP-La Liga'
        if league_code =='ita':
            league_name = 'ITA-Serie A'
        
        if request.method == 'POST':
            selected_year = int(request.form.get('season'))
            elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year,league_name )
        else:
            # Default to the current year
            selected_year = date_var
            elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'ENG-Premier League')

        #? figure displaying : 
        fig = eloClub.plot_elo_histogram(elo_eng, league_name)
        graph_json = fig

        #? send Data here : 
        additional_data = {
            'current_date': date_var,
            'active': 'side-bar__list-item--active',
            'active_link': league_code,
            'season_available': years,
            'season_selected': selected_year,
            # 'elo_data': elo_eng.to_dict(orient='records'),  # Convert DataFrame to a list of dictionaries
            # 'graph_json':graph_json
        }
    

    #?----------------- case of stats navbar selected
    if navbar_selected =='stats' and (league_code in ('eng','fra','ger','esp','ita')):
        #? Get Current Year
        date_var = datetime.now().year
        league_name = ''
        #? Get season
        years = eloClub.generate_years()
        #? Tretement for elo data
        if league_code =='eng':
            league_name = 'ENG-Premier League'
        if league_code =='fra':
            league_name = 'FRA-Ligue 1'
        if league_code =='ger':
            league_name = 'GER-Bundesliga'
        if league_code =='esp':
            league_name = 'ESP-La Liga'
        if league_code =='ita':
            league_name = 'ITA-Serie A'
        
        if request.method == 'POST':
            selected_year = int(request.form.get('season'))
            elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year,league_name )
        else:
            # Default to the current year
            selected_year = date_var
            elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year, 'ENG-Premier League')

        #? figure displaying : 
        fig = eloClub.plot_elo_histogram(elo_eng, league_name)
        graph_json = fig

        #? send Data here : 
        additional_data = {
            'current_date': date_var,
            'active': 'side-bar__list-item--active',
            'active_link': league_code,
            'season_available': years,
            'season_selected': selected_year,
            # 'elo_data': elo_eng.to_dict(orient='records'),  # Convert DataFrame to a list of dictionaries
            # 'graph_json':graph_json
        }

    #? -------------- process the else case : 
    if navbar_selected not in ('elo','fixt','stats'):
        return redirect(url_for('index_home'))


    return render_template(navbar_selected+'/'+league_code+'.html', **additional_data)




if __name__ == '__main__':
    app.run(debug=True)
