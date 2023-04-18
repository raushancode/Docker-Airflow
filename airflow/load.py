import extract
import transform
from sqlalchemy import create_engine
import pandas as pd
import requests
import json
import datetime
import sqlite3
import psycopg2
from sqlalchemy.orm import sessionmaker

DATABASE_LOCATION = "sqlite:///spotify_top_songs.sqlite"

if __name__ == "__main__":
    load_df = extract.return_dataframe()
    if(transform.Data_Quality(load_df) == False):
        raise ("Failed at Data Validation")

    transformed_df = transform.transform_df(load_df)

#Loading into Database
    engine = create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

sql_query_1 = ''' CREATE TABLE IF NOT EXISTS spotify_top_songs (
                        song_date VARCHAR(200)
                        , song_name VARCHAR(200)
                        , artist_name VARCHAR(200)
                        ) '''
                       
cursor.execute(sql_query_1)
print("Opened database successfully")

try:
        transformed_df.to_sql("spotify_top_songs", engine, index=False, if_exists='append')
        print("sql generated")
except:
        print("Data already exists in the database")

# cursor.execute('DROP TABLE spotify_top_songs')
conn.commit()
cursor.close()
conn.close()
print("Close database successfully")
print(transformed_df)
    