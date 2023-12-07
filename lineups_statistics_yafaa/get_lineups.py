from pyspark.sql import SparkSession

import requests

from pyspark.sql.types import IntegerType, StringType, BooleanType, StructField, StructType



# Create a SparkSession

spark = SparkSession.builder.appName("API_Data").getOrCreate()



# Define the API endpoint and headers

url = "https://api-football-beta.p.rapidapi.com/fixtures/lineups"

querystring = {"fixture":"37899"}

headers = {
	"X-RapidAPI-Key": "663502f1dcmshef755013c82c60cp15a6fejsn350986ce6b02",
	"X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

#print(response.json())

# Check if the request was successful and process the data

if response.status_code == 200:

    # Convert the JSON response to a PySpark DataFrame

    json_data = response.json()

    

    # Extract 'response' part from the API data

    response_data = json_data.get('response', [])




    # Define the schema for the 'response' DataFrame

    response_schema_team = StructType([
        StructField('team_id', IntegerType(), True),
   	    StructField('team_name', StringType(), True),
   	    StructField('team_logo', StringType(), True),
        StructField('coach_id', IntegerType(), True),
        StructField('coach_name', StringType(), True),
        StructField('formation', StringType(), True),
	])

    response_schema_players = StructType([
        StructField('team_id', IntegerType(), True),
        StructField('player_id', IntegerType(), True),
        StructField('player_name', StringType(), True),
        StructField('player_number', IntegerType(), True),
        StructField('player_position', StringType(), True),
        StructField('is_main', BooleanType(), True),
    ])


    # Create an empty list to store flattened data

    flattened_data_team = []
    flattened_data_players = []

    # Flatten the 'response' JSON and append to the list
    for item in response_data:
        # Ensure 'item' is a dictionary before extracting data
        if isinstance(item, dict):
            flattened_item_team = {
                "team_id": item.get("team", {}).get("id"),
     			"team_name": item.get("team", {}).get("name"),
     			"team_logo": item.get("team", {}).get("logo"),
     			"coach_id": item.get("coach", {}).get("id"),
     			"coach_name": item.get("coach", {}).get("name"),
    			"formation": item.get("formation"),
            }
            team_id = item.get("team", {}).get("id")
            for p in item['startXI']:
                flattened_item_player = {
                    'team_id': team_id,
                    'player_id':p.get('player').get('id'),
                    'player_name':p.get('player').get('name'),
                    'player_number':p.get('player').get('number'),
                    'player_position':p.get('player').get('pos'),
                    'is_main': True
                }
                flattened_data_players.append(flattened_item_player)

            for p in item['substitutes']:
                flattened_item_player = {
                    'team_id': team_id,
                    'player_id':p.get('player').get('id'),
                    'player_name':p.get('player').get('name'),
                    'player_number':p.get('player').get('number'),
                    'player_position':p.get('player').get('pos'),
                    'is_main': False
                }
                flattened_data_players.append(flattened_item_player)

            flattened_data_team.append(flattened_item_team)

    # Create a PySpark DataFrame from the flattened data and defined schema

    df_team = spark.createDataFrame(flattened_data_team, schema=response_schema_team)
    df_players = spark.createDataFrame(flattened_data_players, schema=response_schema_players)
    

    df_team.show()
    df_players.show()
    

    # Specify the HDFS path where you want to write the CSV file

    #hdfs_output_path = "hdfs://hadoop-master:9000/fixtrues_test"  # Replace with your HDFS path



    # Write data to HDFS in CSV format

    #df.write.mode("overwrite").csv(hdfs_output_path)

    #print(df.head)	
    #df.write.csv("lineups_data.csv", header=True)

else:

    print("Failed to fetch data. Status code:", response.status_code)



# Stop the SparkSession

spark.stop()