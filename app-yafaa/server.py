from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from datetime import datetime
import eloClub as eloClub
import pandas as pd


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

#! ****************** contact Page
@app.route('/contact')
def contact_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var
    }
    return render_template('contact.html', **additional_data, aboutcss="aboutcss")

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
            selected_year = request.form.get('season')
            # Convert the string date to a datetime object
            # date_object = datetime.strptime(selected_year, '%Y-%m-%d')
            elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year,league_name )
        else:
            # Default to the current year
            selected_year = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"
            elo_eng = eloClub.process_clubs_elo_for_year_and_league(selected_year, league_name)

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
        years = [ year for year in range(2010, 2023 + 1)]

        #? Tretement for elo data
        if league_code =='eng':
            league_name = '39data'
        if league_code =='fra':
            league_name = '61data'
        if league_code =='ger':
            league_name = '78data'
        if league_code =='esp':
            league_name = '135data'
        if league_code =='ita':
            league_name = '140data'
        
        # Read the CSV file
        df = pd.read_csv('static/flats/fixt/'+league_name+'.csv')
        fixture_ids = []
        selected_data_fixt= []

        if request.method == 'POST':
            form_type = request.form.get('form_type', '')
            if form_type == 'season_form':
                # Data from the first form
                selected_year = request.form.get('season')
                # Filter the DataFrame based on the selected season
                selected_data = df[df['league_season'] == int(selected_year)]
                fixture_ids = selected_data['fixture_id'].tolist()
                print(fixture_ids)

            elif form_type == 'fixture_form':
                # Data from the first form
                selected_fixture = request.form.get('fixture')
                # Filter the DataFrame based on the selected season
                selected_data_fixt = df[df['fixture_id'] == int(selected_fixture)]
        else:
            selected_data = df[df['league_season'] == int(date_var)]
            fixture_ids = selected_data['fixture_id'].tolist()
            # print(fixture_ids)

        #? send Data here : 
        additional_data = {
            'current_date': date_var,
            'active': 'side-bar__list-item--active',
            'active_link': league_code,
            'season_available': years,
            'fixture_ids' : fixture_ids,
            'selected_data_fixt':selected_data_fixt
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


    return render_template(navbar_selected+'/'+league_code+'.html', **additional_data,fixtcss="fixtcss")




if __name__ == '__main__':
    app.run(debug=True)
