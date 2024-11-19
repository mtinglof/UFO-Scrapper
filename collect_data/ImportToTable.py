import pymysql
import pandas as pd
import os
from tqdm import tqdm  

# Database connection details
connection = pymysql.connect(
    host=os.getenv('db_host'),     
    port=os.getenv('db_port'),
    user=os.getenv('db_user'),
    password=os.getenv('db_pass'),
    database=os.getenv('db_name')  
)

try:
    # Read the CSV file into a pandas DataFrame
    csv_file_path = 'exports/cleaned_reports.csv'
    data = pd.read_csv(csv_file_path)
    data = data.where(pd.notnull(data), None) 
    
    # Define a SQL query template for inserting data
    insert_query = """
        INSERT INTO reported_sightings 
        (LINK, OCCURRED, CITY, STATE, COUNTRY, SHAPE, SUMMARY, REPORTED, MEDIA, EXPLANATION, LAT, LONG, POP) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Open a cursor and iterate over the DataFrame to insert data with a loading bar
    with connection.cursor() as cursor:
        for _, row in tqdm(data.iterrows(), total=len(data), desc="Loading data into SQL"):
            cursor.execute(insert_query, (
                row['LINK'],
                row['OCCURRED'],
                row['CITY'],
                row['STATE'],
                row['COUNTRY'],
                row['SHAPE'],
                row['SUMMARY'],
                row['REPORTED'],
                row['MEDIA'],
                row['EXPLANATION'],
                row['LAT'],
                row['LONG'],
                row['POP']
            ))
        # Commit the transaction
        connection.commit()

finally:
    # Close the connection
    connection.close()

print("Data insertion completed!")
