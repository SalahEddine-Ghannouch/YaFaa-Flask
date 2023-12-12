from pyspark.sql import SparkSession
import requests
from pyspark.sql.types import IntegerType, StringType, BooleanType,StructField,StructType


# Create a SparkSession
spark = SparkSession.builder.appName("API_Data").getOrCreate()

# Define the API endpoint and headers
url = "https://api-football-beta.p.rapidapi.com/fixtures"


headers = {
    "X-RapidAPI-Key": "4f42dc8240mshd4066cda199474cp129104jsnfcdbca819eca",
    "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
}

leagues = [39, 135, 140, 78, 61]
years = range(2010, 2024)

# Define the schema for the 'response' DataFrame
response_schema =StructType([
StructField('fixture_id',IntegerType(),True),  
StructField('fixture_referee',StringType(),True),  
StructField('fixture_timezone',StringType(),True),  
StructField('fixture_date',StringType(),True),  
StructField('fixture_timestamp',IntegerType(),True),  
StructField('fixture_periods_first',IntegerType(),True),  
StructField('fixture_periods_second',IntegerType(),True),  
StructField('venue_id',IntegerType(),True), 
StructField('venue_name',StringType(),True),  
StructField('venue_city',StringType(),True),  
StructField('status_long',StringType(),True),  
StructField('status_short',StringType(),True),  
StructField('status_elapsed',IntegerType(),True),  
StructField('league_id',IntegerType(),True),  
StructField('league_name',StringType(),True),  
StructField('league_country',StringType(),True),  
StructField('league_logo',StringType(),True),  
StructField('league_flag',StringType(),True),  
StructField('league_season',IntegerType(),True),  
StructField('league_round',StringType(),True),  
StructField('teams_home_id',IntegerType(),True),  
StructField('teams_home_name',StringType(),True),  
StructField('teams_home_logo',StringType(),True),  
StructField('teams_home_winner',BooleanType(),True),  
StructField('teams_away_id',IntegerType(),True),  
StructField('teams_away_name',StringType(),True),  
StructField('teams_away_logo',StringType(),True),  
StructField('teams_away_winner',BooleanType(),True),  
StructField('goals_home',IntegerType(),True),  
StructField('goals_away',IntegerType(),True),  
StructField('score_halftime_home',IntegerType(),True),  
StructField('score_halftime_away',IntegerType(),True),  
StructField('score_fulltime_home',IntegerType(),True),  
StructField('score_fulltime_away',IntegerType(),True),  
StructField('score_extratime_home',IntegerType(),True),  
StructField('score_extratime_away',IntegerType(),True),  
StructField('score_penalty_home',IntegerType(),True),  
StructField('score_penalty_away',IntegerType(),True)])
# Create an empty list to store flattened data
flattened_data = []


for league in leagues:
    for year in years:
        response = requests.get( url, headers=headers, params={"season": year, "league": league})
        if response.status_code == 200:
            
            # Convert the JSON response to a PySpark DataFrame
            json_data = response.json()
            
            # Extract 'response' part from the API data
            response_data = json_data.get('response', [])

            # Flatten the 'response' JSON and append to the list
            for item in response_data:
                    # Ensure 'item' is a dictionary before extracting data
                if isinstance(item, dict):
                    flattened_item = {
                    "fixture_id": item.get("fixture", {}).get("id"),
                    "fixture_referee": item.get("fixture", {}).get("referee"),
                    "fixture_timezone": item.get("fixture", {}).get("timezone"),
                    "fixture_date": item.get("fixture", {}).get("date"),
                    "fixture_timestamp": item.get("fixture", {}).get("timestamp"),
                    "fixture_period_first": item.get("fixture", {}).get("periods", {}).get("first"),
                    "fixture_period_second": item.get("fixture", {}).get("periods", {}).get("second"),
                    "venue_id": item.get("fixture", {}).get("venue", {}).get("id"),
                    "venue_name": item.get("fixture", {}).get("venue", {}).get("name"),
                    "venue_city": item.get("fixture", {}).get("venue", {}).get("city"),
                    "status_long": item.get("fixture", {}).get("status", {}).get("long"),
                    "status_short": item.get("fixture", {}).get("status", {}).get("short"),
                    "status_elapsed": item.get("fixture", {}).get("status", {}).get("elapsed"),
                    "league_id": item.get("league", {}).get("id"),
                    "league_name": item.get("league", {}).get("name"),
                    "league_country": item.get("league", {}).get("country"),
                    "league_logo": item.get("league", {}).get("logo"),
                    "league_flag": item.get("league", {}).get("flag"),
                    "league_season": item.get("league", {}).get("season"),
                    "league_round": item.get("league", {}).get("round"),
                    "teams_home_id": item.get("teams", {}).get("home", {}).get("id"),
                    "teams_home_name": item.get("teams", {}).get("home", {}).get("name"),
                    "teams_home_logo": item.get("teams", {}).get("home", {}).get("logo"),
                    "teams_home_winner": item.get("teams", {}).get("home", {}).get("winner"),
                    "teams_away_id": item.get("teams", {}).get("away", {}).get("id"),
                    "teams_away_name": item.get("teams", {}).get("away", {}).get("name"),
                    "teams_away_logo": item.get("teams", {}).get("away", {}).get("logo"),
                    "teams_away_winner": item.get("teams", {}).get("away", {}).get("winner"),
                    "goals_home": item.get("goals", {}).get("home"),
                    "goals_away": item.get("goals", {}).get("away"),
                    "score_halftime_home": item.get("score", {}).get("halftime", {}).get("home"),
                    "score_halftime_away": item.get("score", {}).get("halftime", {}).get("away"),
                    "score_fulltime_home": item.get("score", {}).get("fulltime", {}).get("home"),
                    "score_fulltime_away": item.get("score", {}).get("fulltime", {}).get("away"),
                    "score_extratime_home": item.get("score", {}).get("extratime", {}).get("home"),
                    "score_extratime_away": item.get("score", {}).get("extratime", {}).get("away"),
                    "score_penalty_home": item.get("score", {}).get("penalty", {}).get("home"),
                    "score_penalty_away": item.get("score", {}).get("penalty", {}).get("away"),
                    }
                    flattened_data.append(flattened_item)

            # Create a PySpark DataFrame from the flattened data and defined schema
		    df = spark.createDataFrame(flattened_data, schema=response_schema)

            #print(df.head())
            # Show the DataFrame content
            #df.show(truncate=False)
            #print(df)

            # Specify the HDFS path where you want to write the CSV file
            #hdfs_output_path = "hdfs://hadoop-master:9000/fixtrues_test"  # Replace with your HDFS path
            # Write data to HDFS in CSV format
            #df.write.mode("overwrite").csv(hdfs_output_path)
            	   print(league,year)
            data_file = "AllData/"+str(league)+"_"+str(year)+".csv"
            df.write.csv(data_file, header=True)
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            
# Stop the SparkSession
spark.stop()
