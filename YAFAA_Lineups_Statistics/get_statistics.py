from pyspark.sql import SparkSession

import requests

from pyspark.sql.types import IntegerType, StringType, StructField, StructType

# Create a SparkSession

spark = SparkSession.builder.appName("API_Data").getOrCreate()

# Define the API endpoint and headers

url = "https://api-football-beta.p.rapidapi.com/fixtures/statistics"

querystring = {"fixture":"37899"}

headers = {
	"X-RapidAPI-Key": "663502f1dcmshef755013c82c60cp15a6fejsn350986ce6b02",
	"X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:

    # Convert the JSON response to a PySpark DataFrame

    json_data = response.json()

    

    # Extract 'response' part from the API data

    response_data = json_data.get('response', [])



    # Define the schema for the 'response' DataFrame

    response_schema = StructType([
        StructField('team_id', IntegerType(), True),
   	    StructField('statistics_type', StringType(), True),
        StructField('statistics_value', StringType(), True),
	])


    # Create an empty list to store flattened data

    flattened_data = []

    # Flatten the 'response' JSON and append to the list
    for item in response_data:
        # Ensure 'item' is a dictionary before extracting data
        if isinstance(item, dict):
            team_id = item.get("team", {}).get("id")
            for p in item['statistics']:
                flattened_item = {
                    'team_id': team_id,
                    'statistics_type':p.get('type'),
                    'statistics_value':p.get('value')
                }
                flattened_data.append(flattened_item)




    # Create a PySpark DataFrame from the flattened data and defined schema

    df = spark.createDataFrame(flattened_data, schema=response_schema)
    

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