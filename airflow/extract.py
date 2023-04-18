import requests
import pandas as pd
from datetime import datetime
import json

def return_dataframe():
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": "use ur cient id",
        "client_secret": "use ur client secret"
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

