import requests
import pandas as pd



class FootballAPIClient:
    def __init__(self,api_key):
        self.api_key = api_key
        self.base_url = "https://api-football-beta.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
        }

    #! DONE
    def get_seasons(self):
        url = f"{self.base_url}/leagues/seasons"
        response = requests.get(url, headers=self.headers)
        return response.json()['response']


    #! DONE  
    def get_leagues(self):
        url = f"{self.base_url}/leagues"
        response = requests.get(url, headers=self.headers)
        # Extract only the 'league' column from the JSON response
        league_column = [entry['league'] for entry in response.json()['response']]
        league = pd.json_normalize(league_column, max_level=9)
        leagues = pd.DataFrame(league)
        return leagues
    

    #! DONE : get all statistics of each fixtures
    def get_fixtures_statistics(self, fixture_id, team=None):
        url = f"{self.base_url}/fixtures/statistics"
        querystring = {"fixture": str(fixture_id)}
        data_list = []
        # Add team to the query if provided
        if team is not None:
            querystring["team"] = str(team)
        data = requests.get(url, headers=self.headers, params=querystring)

        for team_stat in data.json()['response']:
            team_id = team_stat['team']['id']
            team_name = team_stat['team']['name']
            team_logo = team_stat['team']['logo']
            # Create a dictionary for the team
            team_data = {'TeamID': team_id, 'TeamName': team_name, 'TeamLogo': team_logo}
            # Extract and add each statistic to the team dictionary
            for stat in team_stat['statistics']:
                stat_type = stat['type']
                stat_value = stat['value']
                team_data[stat_type] = stat_value
    
            # Append the team dictionary to the list
            data_list.append(team_data)

        # Create DataFrame
        data_frame = pd.DataFrame(data_list)
        # Group by 'Team' column
        grouped_data = data_frame.groupby(['TeamID','TeamName','TeamLogo'])
        # data_frame.to_csv(f"fixtures-statistics-{fixture_id}.csv")
        return data_frame



    #! DONE : get all fixtures ids 
    def get_fixtures_ids(self, season_id, league_id):
        url = f"{self.base_url}/fixtures"
        querystring = {"season": str(season_id), "league": str(league_id)}
        data_list = []
        data = requests.get(url, headers=self.headers, params=querystring)

        for fixt in data.json()['response']:
            fixt_id = fixt['fixture']['id']
            # Create a dictionary for the team
            fix_data = {'FixtureID': fixt_id}
            # Append the team dictionary to the list
            data_list.append(fix_data)

        # Create DataFrame
        data_frame = pd.DataFrame(data_list)
        data_frame.to_csv(f"fixtures-ids-{league_id}-{season_id}.csv")
        return data_frame


    
    def get_all_fixtures_statistics_in_season(self, league_id, season):
        # Get all fixture IDs for the given league and season
        fixtures_ids_df = self.get_fixtures_ids(season, league_id)

        # Create an empty DataFrame to accumulate all statistics
        all_stats_df = pd.DataFrame()

        # Loop through fixture IDs and get statistics
        for _, row in fixtures_ids_df.iterrows():
            fixture_id = row['FixtureID']
            
            # Get statistics for the current fixture
            stats_df = self.get_fixtures_statistics(fixture_id)

            # Append the statistics to the accumulated DataFrame
            if not stats_df.empty:
                all_stats_df = pd.concat([all_stats_df, stats_df], ignore_index=True)

        # Save the accumulated DataFrame to a CSV file
        all_stats_df.to_csv(f"all-fixtures-statistics-{league_id}-{season}.csv", index=False)

        return all_stats_df


    def get_fixtures_events(self, season, league):
        url = f"{self.base_url}/fixtures/events"
        querystring = {"season": str(season), "league": str(league)}
        response = requests.get(url, headers=self.headers, params=querystring)
        return response.json()
    

 
    
    
 


   
        