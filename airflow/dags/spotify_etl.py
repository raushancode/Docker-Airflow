import requests
import pandas as pd
from datetime import datetime
import json
from sqlalchemy import create_engine
import sqlite3
import psycopg2
from sqlalchemy.orm import sessionmaker

def return_dataframe():
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": "3ffea4ed6eb9442c8328411f31144ba3",
        "client_secret": "a2ca59ecb52a476190565bccafa7ae7f"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    token = response.json()["access_token"]
    header = {
        "Authorization" : "Bearer {token}".format(token=token)
    }

    r = requests.get("https://api.spotify.com/v1/playlists/37i9dQZF1DX0XUfTFmNBRM", headers = header)
    data = r.json()
    # data1 = json.dumps(data, indent=4)
    # print(data1)

    today = str(datetime.today().date())
    timestamp = []
    artist_name = []
    song_name = []
    items_list = data["tracks"]["items"]

    for item in items_list:
        song_name.append(item["track"]["album"]["name"])
        artist_name.append(item["track"]["album"]["artists"][0]["name"])
        timestamp.append(today)

    # prepare a dictionary to turn this into panda dataframe
    song_dict = {
        "song_name" : song_name,
        "artist_name" : artist_name,
        "song_date" : timestamp
    }

    df = pd.DataFrame(song_dict, columns=["song_date", "song_name", "artist_name"])
    return(df)

def Data_Quality(load_df):
    if load_df.empty:
        print("No Songs Extracted")
        return False
    if load_df.isnull().values.any():
        raise Exception("Null Value Found")

def Transform_df(load_df):
    # for future use, currently not transforming data
    return load_df

def spotify_etl():
    #Importing the songs_df from the Extract.py
    load_df=return_dataframe()
    Data_Quality(load_df)
    #calling the transformation
    Transformed_df=Transform_df(load_df)    
    print(load_df)
    return (load_df)

spotify_etl()