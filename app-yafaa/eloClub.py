import soccerdata as sd
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

elo = sd.ClubElo()


#******************* get Years funct : 
def generate_years():
    years = []
    for year in range(1999, 2023 + 1):
        years.append(year)
    return years

#******************* get_available_leagues funct : 
def get_available_leagues():
    return elo.available_leagues()


#******************* def process_clubs_elo_for_year_and_league: funct : 
def process_clubs_elo_for_year_and_league(year, league):
    # Read end of season clubs elo for the specified year
    elos = elo.read_by_date(f'{year}-06-30')

    # Filter data for the specified league
    filtered_seasons = elos[elos.league == league]

    # Add 'rank' and 'season' columns
    filtered_seasons['rank'] = range(1, len(filtered_seasons) + 1)
    filtered_seasons['season'] = year 

    # Drop unnecessary columns
    filtered_seasons.drop(columns=['level', 'from', 'to'], inplace=True)
    # Extract the 'team' column
    teams = filtered_seasons.index.tolist()
    # Add 'teams' column to the DataFrame
    filtered_seasons['teams'] = teams

    return filtered_seasons


#******************* def plot_elo_histogram: funct : 
def plot_elo_histogram(league_df, league_name):
    fig = make_subplots(rows=1, cols=1)

    trace = go.Histogram(x=league_df['elo'], nbinsx=20, marker_color='blue', opacity=0.7)

    fig.add_trace(trace)

    fig.update_layout(
        xaxis_title_text='Elo Rating',
        yaxis_title_text='Frequency',
        showlegend=False,
        autosize=False,
        width=460,
        height=390
    )

    return fig.to_html(full_html=False)
