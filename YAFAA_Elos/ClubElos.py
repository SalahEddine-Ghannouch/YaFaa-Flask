import soccerdata as sd
import pandas as pd
from datetime import datetime, timedelta
from hdfs import InsecureClient
import os

##? these imports will be used later 
# import pandas as pd
# import matplotlib.pyplot as plt


# Defining the global variables
elo = sd.ClubElo()
leagues = elo.available_leagues()

class ClubsElosProcessor:
    def __init__(self):
        self.ClubsElos = pd.DataFrame()

    def week_num(self, date):
        week, year, _ = date.isocalendar()
        if date.month == 1 and week >= 52:
            year -= 1
        return f"Week {week}: {date}"
    

    def process_elos(self, start_year=2010, end_year=2023, leagues=leagues):

        for year in range(start_year, end_year + 1):
            start_date = datetime(year, 8, 7)

            while start_date <= datetime(2023, 7, 30) and (start_date.month < 7 or start_date.month > 7):
                elos = elo.read_by_date(f"{start_date.year}-{start_date.month}-{start_date.day}")
                filtered_seasons = elos[elos.league.isin(leagues)]
                filtered_seasons['rank'] = range(1, len(filtered_seasons) + 1)
                filtered_seasons['week'] = f"{start_date.year}-{start_date.month}-{start_date.day}"
                # filtered_seasons['season'] 
                self.ClubsElos = pd.concat([self.ClubsElos, filtered_seasons], ignore_index=False)
                start_date += timedelta(days=7)

        # Drop specific columns if they exist
        columns_to_drop = ['level', 'from', 'to']
        self.ClubsElos = self.ClubsElos.drop(columns=columns_to_drop, errors='ignore')


    def save_elos(self, output_directory=None, save_to_hadoop=False, hadoop_address=None):

        if output_directory is None:
            # Use the directory where the script is located
            output_directory = os.path.dirname(os.path.abspath(__file__))

        # Create the directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Dictionary to store DataFrames for each league
        league_dataframes = {}

        # Group by 'league' column and iterate over groups
        for league, group_df in self.ClubsElos.groupby('league'):
            # Store the DataFrame in the dictionary with the league name as the key
            league_dataframes[league] = group_df

        if save_to_hadoop:
            if hadoop_address is None:
                raise ValueError("Hadoop address is required when saving to Hadoop.")

            # Connect to Hadoop HDFS
            client = InsecureClient(hadoop_address)

            # Iterate through each league and DataFrame in the dictionary
            for league, df in league_dataframes.items():
                # Construct the HDFS filename
                hdfs_filename = f"{league.replace('-', '_').replace(' ', '_')}_elo.csv"

                # Save the DataFrame to HDFS
                with client.write(os.path.join(output_directory, hdfs_filename), encoding='utf-8') as writer:
                    df.to_csv(writer, index=True)
        else:
            # Iterate through each league and DataFrame in the dictionary
            for league, df in league_dataframes.items():
                # Construct the CSV filename
                csv_filename = f"{league.replace('-', '_').replace(' ', '_')}_elo.csv"

                # Save the DataFrame to a CSV file
                df.to_csv(os.path.join(output_directory, csv_filename), index=True)



#!!! This portion is just for testing
# # Create an instance of ClubElo
# elo = sd.ClubElo()
# # Create an instance of ClubsElosProcessor
# elo_processor = ClubsElosProcessor()
# # Process Elo ratings
# elo_processor.process_elos()
# # Save the processed Elo ratings to CSV files
# elo_processor.save_elos()
# # Print the resulting DataFrame
# print(elo_processor.ClubsElos)