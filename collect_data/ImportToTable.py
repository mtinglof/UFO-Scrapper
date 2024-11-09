import pymysql
import pandas as pd
import os
from tqdm import tqdm  

# Database connection details
connection = pymysql.connect(
    host=os.getenv('AWS_EP'),     
    user=os.getenv('AWS_NAME'),
    password=os.getenv('AWS_PASS'),
    database=os.getenv('AWS_DB')  
)

try:
    # Read the CSV file into a pandas DataFrame
    csv_file_path = 'cleaned_reports.csv'
    data = pd.read_csv(csv_file_path)
    data = data.where(pd.notnull(data), None) 
    
    # Define a SQL query template for inserting data
    insert_query = """
        INSERT INTO reported_sightings 
        (LINK, OCCURRED, CITY, STATE, COUNTRY, SHAPE, SUMMARY, REPORTED, MEDIA, EXPLANATION) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                row['EXPLANATION']
            ))
        # Commit the transaction
        connection.commit()

finally:
    # Close the connection
    connection.close()

print("Data insertion completed!")
