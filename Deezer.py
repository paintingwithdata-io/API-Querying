import pandas as pd
import requests
from pandas import json_normalize

# Sets url variable from API to pull album data and gets json as response
url = "https://api.deezer.com/album/302127"
response = requests.get(url)

# Create dictionaries to select key columns and rename later
album_cols = {'cols': ['id', 'title', 'upc', 'genre_id', 'label', 'duration',
                       'fans', 'rating', 'release_date', 'record_type', 'available',
                       'type', 'artist.id', 'artist.name', 'artist.type']}
track_cols = {'cols': ['id', 'title', 'duration', 'rank', 'explicit_lyrics',
                       'type']}
album_rename = {'id': 'album_id', 'title': 'album_title'}
track_rename = {'id': 'track_id', 'title': 'track_title', 'duration': 'track_duration',
                'rank': 'track_rank'}

# Create a json object from the response and then a dataframe after normalizing json data
data = response.json()
json_df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')

# Create a dataframe with the album information, reduced to the key cols from album_cols
# then rename the id column for clarity
album_df = json_df[album_cols['cols']]
album_df = album_df.rename(columns=album_rename)
album_df['m_key'] = 1

# Create a dataframe with the track information by turning
# the tracks.data series into a list, and then into a dataframe,
# which only includes columns from track_cols. end by renaming cols for clarity
track_series = json_df['tracks.data']
track_list = list(track_series[0])
track_df = pd.DataFrame(track_list)[track_cols['cols']]
track_df = track_df.rename(columns=track_rename)
track_df['m_key'] = 1

# Perform a merge to combine album and track data into single df
track_df = pd.merge(track_df, album_df[['album_title', 'm_key']], on='m_key', how='inner')

# Drop m_keys from dataframes (were only used for join)
# #Dev note: refactor this later to avoid using inplace. Works fine for now
group_df = [album_df, track_df]
for i in group_df:
    i.drop(i[['m_key']], axis=1, inplace=True)

print(track_df)
print(album_df)

# JSON Data metadata from the API
# Headers is a dictionary
# print(response.headers)
# Get the content-type from the dictionary.
# print(response.headers["content-type"])
