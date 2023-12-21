from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from datetime import datetime
import eloClub as eloClub
import pickle
import pandas as pd
from YAFAADataVisualization import yafaaSQL,yaffaPLT

app = Flask(__name__)


#! ****************** Home Page
@app.route('/')
def index_home():
    date_var = datetime.now().year
    date_new = datetime.now()

    database = yafaaSQL()
    df_eng = pd.read_csv('static/flats/fixt/39data.csv')
    df_fra = pd.read_csv('static/flats/fixt/61data.csv')
    df_ger = pd.read_csv('static/flats/fixt/78data.csv')
    df_ita = pd.read_csv('static/flats/fixt/135data.csv')
    df_esp = pd.read_csv('static/flats/fixt/140data.csv')
    year_df_eng = database.select_by_season(df_eng, date_var)
    year_df_fra = database.select_by_season(df_fra, date_var)
    year_df_ger = database.select_by_season(df_ger, date_var)
    year_df_ita = database.select_by_season(df_ita, date_var)
    year_df_esp = database.select_by_season(df_esp, date_var)
    teams_summary_eng = database.team_goals_summary(year_df_eng)
    teams_summary_fra = database.team_goals_summary(year_df_fra)
    teams_summary_ger = database.team_goals_summary(year_df_ger)
    teams_summary_ita = database.team_goals_summary(year_df_ita)
    teams_summary_esp = database.team_goals_summary(year_df_esp)
    aggregated_goals_pl_eng = database.aggregate_columns(teams_summary_eng, ['total_goals'], aggregation='sum')
    aggregated_goals_pl_fra = database.aggregate_columns(teams_summary_fra, ['total_goals'], aggregation='sum')
    aggregated_goals_pl_ger = database.aggregate_columns(teams_summary_ger, ['total_goals'], aggregation='sum')
    aggregated_goals_pl_ita = database.aggregate_columns(teams_summary_ita, ['total_goals'], aggregation='sum')
    aggregated_goals_pl_esp = database.aggregate_columns(teams_summary_esp, ['total_goals'], aggregation='sum')
    elo_eng = eloClub.process_clubs_elo_for_year_and_league(f"{date_new.year}-{date_new.month}-{date_new.day}",'ENG-Premier League' )
    elo_fra = eloClub.process_clubs_elo_for_year_and_league(f"{date_new.year}-{date_new.month}-{date_new.day}",'FRA-Ligue 1' )
    elo_ger = eloClub.process_clubs_elo_for_year_and_league(f"{date_new.year}-{date_new.month}-{date_new.day}",'GER-Bundesliga' )
    elo_esp = eloClub.process_clubs_elo_for_year_and_league(f"{date_new.year}-{date_new.month}-{date_new.day}",'ESP-La Liga' )
    elo_ita = eloClub.process_clubs_elo_for_year_and_league(f"{date_new.year}-{date_new.month}-{date_new.day}",'ITA-Serie A' )
    print(elo_eng.iloc[0].elo)
    #* Plotting 
    # plt_instance = yaffaPLT()

    # fig = plt_instance.plot_metric(label="Total Goals Scored", column_name="sum_of_total_goals", dataframe=aggregated__goals_pl, prefix="", suffix=" Goals", bold_label=True)
    # fig
    additional_data = {
        'current_date': date_var,
        'eng_goals':aggregated_goals_pl_eng['sum_of_total_goals'].iloc[0],
        'fra_goals':aggregated_goals_pl_fra['sum_of_total_goals'].iloc[0],
        'ger_goals':aggregated_goals_pl_ger['sum_of_total_goals'].iloc[0],
        'ita_goals':aggregated_goals_pl_ita['sum_of_total_goals'].iloc[0],
        'esp_goals':aggregated_goals_pl_esp['sum_of_total_goals'].iloc[0],
        'elo_eng':elo_eng.iloc[0],
        'elo_fra':elo_fra.iloc[0],
        'elo_ger':elo_ger.iloc[0],
        'elo_esp':elo_esp.iloc[0],
        'elo_ita':elo_ita.iloc[0],
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

#! ****************** prediction Page

with open('predictions/pl_predictions.csv', 'rb') as myFile:
    pl_pred = pickle.load(myFile)
    
with open('prem_clean_fixtures_and_dataframes/2019_2020_2021_2022_2023_additional_stats_dict.txt', 'rb') as myFile:
    additional_stats_dict = pickle.load(myFile)    


#with open('/home/matthaythornthwaite/Football_Prediction_Project/web_server/pl_predictions.csv', 'rb') as myFile:
#    pl_pred = pickle.load(myFile)

#removing all past predictions if they still exist in the predictions df
current_date = datetime.today().strftime('%Y-%m-%d')
for j in range(len(pl_pred)):
    game_date = pl_pred['Game Date'].loc[j]
    if game_date < current_date:
        pl_pred = pl_pred.drop([j], axis=0)
pl_pred = pl_pred.reset_index(drop=True)        


#creating our iterator that we will use in the for loop in our index file.
max_display_games = 10
iterator_len = len(pl_pred) - 1
if iterator_len > max_display_games:
    iterator_len = max_display_games
iterator = range(iterator_len)

#creating our iterator that we will use in the for loop in our index file. Checking first that there is enough data.
max_additional_display_games = 5
dict_keys = list(additional_stats_dict.keys())
min_length = 100
for i in dict_keys:
    df_len = len(additional_stats_dict[i])
    if df_len < min_length:
        min_length = df_len
if max_additional_display_games > min_length:
    max_additional_display_games = min_length
iterator2 = range(max_additional_display_games)


@app.route('/prediction')
def prediction_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var
    }
    return render_template('prediction.html', **additional_data,
                           cssmodel="stylemodel",
                           jsmodel="scriptmodel",
                           pl_pred=pl_pred, 
                           iterator=iterator,
                           iterator2=iterator2,
                           additional_stats_dict=additional_stats_dict)

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
            league_name = '140data'
        if league_code =='ita':
            league_name = '135data'
        
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
                teams_home_name = selected_data['teams_home_name'].tolist()
                teams_away_name = selected_data['teams_away_name'].tolist()
                fixture_ids = selected_data['fixture_id'].tolist()
                selected_data_fixt = df[df['fixture_id'] == fixture_ids[0]]
                print(selected_data_fixt)
                selected_year = int(selected_year)

            elif form_type == 'fixture_form':
                # Data from the first form
                selected_fixture = request.form.get('fixture')
                # Filter the DataFrame based on the selected season
                selected_data_fixt = df[df['fixture_id'] == int(selected_fixture)]
                league_season_value = selected_data_fixt['league_season'].iat[0]
                selected_data = df[df['league_season'] == int(league_season_value)]
                teams_home_name = selected_data['teams_home_name'].tolist()
                teams_away_name = selected_data['teams_away_name'].tolist()

                fixture_ids = fixture_ids

        else:
            selected_data = df[df['league_season'] == int(date_var)]
            fixture_ids = selected_data['fixture_id'].tolist()
            teams_home_name = selected_data['teams_home_name'].tolist()
            # teams_home_name = selected_data['teams_home_name'].drop_duplicates().tolist()
            teams_away_name = selected_data['teams_away_name'].tolist()
            selected_data_fixt = df[df['fixture_id'] == fixture_ids[0]]
            selected_year = int(date_var)   
            # print("-----------------> ",fixture_ids[0])
            # print(selected_data_fixt.columns)

        #? send Data here : 
        additional_data = {
            'current_date': date_var,
            'active': 'side-bar__list-item--active',
            'active_link': league_code,
            'season_available': years,  
            'fixture_ids' : fixture_ids,
            'selected_data_fixt':selected_data_fixt,
            'teams_home_name_v':teams_home_name,
            'teams_away_name_v':teams_away_name
        }
    

    #?----------------- case of stats navbar selected
    if navbar_selected =='stats' and (league_code in ('eng','fra','ger','esp','ita')):
        #? Get Current Year
        date_var = datetime.now().year
        years = [ year for year in range(2017, 2023)]
        league_name = ''
        #? Get season
        #? Tretement for elo data
        if league_code =='eng':
            league_name = '39data'
        if league_code =='fra':
            league_name = '61data'
        if league_code =='ger':
            league_name = '78data'
        if league_code =='esp':
            league_name = '140data'
        if league_code =='ita':
            league_name = '135data'
        
        # Read the CSV file
        df_goals = pd.read_csv('static/flats/fixt/'+league_name+'.csv')
        # df_goals = pd.read_csv('static/flats/fixt/39data.csv')
        
        # Read the CSV file

        if request.method == 'POST':
            selected_year = int(request.form.get('season'))
            selected_team1 = request.form.get('team1')
            selected_team2 = request.form.get('team2')
            df_card = pd.read_csv('static/flats/stats/'+str(selected_year)+'/season-'+str(selected_year)+'-misc.csv')
            list_teams = df_card["team"].tolist()
            # list_opponent = df_card["opponent"].tolist()
            series_teams = pd.Series(list_teams)
            cleaned_teams = series_teams.drop_duplicates().dropna().tolist()
            selected_row1 = df_card.loc[(df_card['team'] == selected_team1) & (df_card['opponent'] == selected_team2)]
            selected_row2 = df_card.loc[(df_card['opponent'] == selected_team1) & (df_card['team'] == selected_team2)]
            #? ---------
            database = yafaaSQL()
            year_df = database.select_by_season(df_goals, selected_year)
            teams_summary = database.team_goals_summary(year_df)
            aggregated_columns = database.aggregate_columns(teams_summary, ['total_goals', 'home_goals', 'away_goals'], aggregation='sum')  
            plt_instance = yaffaPLT()
            key_cols = ['total_goals', None, None, None]
            plot_cols = ['home_goals', 'away_goals']
            x_column = 'team_name'
            title = "Home & Away Goals"
            fig = plt_instance.plot_stacked_bar(key_cols, plot_cols, x_column, teams_summary, title=title)
              
        else:
            # Default to the current year
            selected_year = date_var
            df_card = pd.read_csv('static/flats/stats/'+str(selected_year-1)+'/season-'+str(selected_year-1)+'-misc.csv')
            list_teams = df_card["team"].tolist()
            # Convert the list to a pandas Series to leverage pandas functionality
            series_teams = pd.Series(list_teams)
            cleaned_teams = series_teams.drop_duplicates().dropna().tolist()
            selected_team1 = "Arsenal"
            selected_team2 = "Liverpool"            
            selected_row1 = df_card.loc[(df_card['team'] == "Arsenal") & (df_card['opponent'] == "Liverpool")]
            selected_row2 = df_card.loc[(df_card['team'] == "Liverpool") & (df_card['opponent'] == "Arsenal")]
             #? ---------
            database = yafaaSQL()
            year_df = database.select_by_season(df_goals, selected_year)
            teams_summary = database.team_goals_summary(year_df)
            aggregated_columns = database.aggregate_columns(teams_summary, ['total_goals', 'home_goals', 'away_goals'], aggregation='sum')  
            plt_instance = yaffaPLT()
            key_cols = ['total_goals', None, None, None]
            plot_cols = ['home_goals', 'away_goals']
            x_column = 'team_name'
            title = "Home & Away Goals"
            fig = plt_instance.plot_stacked_bar(key_cols, plot_cols, x_column, teams_summary, title=title)
            # print(selected_row.columns)

        #? figure displaying : 
        # fig = eloClub.plot_elo_histogram(elo_eng, league_name)
        # graph_json = fig

        #? send Data here : 
        additional_data = {
            'current_date': date_var,
            'active': 'side-bar__list-item--active',
            'active_link': league_code,
            'season_available': years,
            'selected_year': selected_year,
            'cleaned_teams':cleaned_teams,
            'selected_row1':selected_row1,
            'selected_row2':selected_row2,
            'selected_team1':selected_team1,
            'selected_team2':selected_team2,
            'fig':fig
            # 'elo_data': elo_eng.to_dict(orient='records'),  # Convert DataFrame to a list of dictionaries
            # 'graph_json':graph_json
        }

    #? -------------- process the else case : 
    if navbar_selected not in ('elo','fixt','stats'):
        return redirect(url_for('index_home'))


    return render_template(navbar_selected+'/'+league_code+'.html', **additional_data,fixtcss="fixtcss")




if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000,debug=True)
