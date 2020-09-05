import pandas as pd
import requests
from pandas import json_normalize


# Sets url variable from API to pull album data and gets json as response
def get_album_deezer(url):
    # Create a response json object from the API endpoint
    response = requests.get(url).json()

    # JSON Data metadata from the API
    # Headers is a dictionary
    #   print(response.headers)
    # Get the content-type from the dictionary.
    #   print(response.headers["content-type"])

    # Create dictionaries to select key columns and rename later
    album_cols = {'cols': ['id', 'title', 'upc', 'genre_id', 'label', 'duration',
                           'fans', 'rating', 'release_date', 'record_type', 'available',
                           'type', 'artist.id', 'artist.name', 'artist.type']}
    track_cols = {'cols': ['id', 'title', 'duration', 'rank', 'explicit_lyrics',
                           'type']}
    album_rename = {'id': 'album_id', 'title': 'album_title'}
    track_rename = {'id': 'track_id', 'title': 'track_title', 'duration': 'track_duration',
                    'rank': 'track_rank'}

    # Creates a dataframe from the normalized json object
    json_df = json_normalize(response)

    # Create a dataframe with the album information, reduced to the key cols from album_cols
    # then rename columns for clarity
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
    df_list = [album_df, track_df]
    for i in df_list:
        i.drop(i[['m_key']], axis=1, inplace=True)

    return df_list


def get_fans_deezer(url, fans_df):
    # Create a response json object from the API endpoint
    # and a dataframe from the normalized json object
    response = requests.get(url).json()
    df = json_normalize(response)

    # Returns a list of the user dataframe and the url for the next fan batch
    while 'next' in response:
        # Create a dataframe with the fan information by turning
        # the df.data series into a list, and then into a dataframe
        # with the id column only
        fans_list = list(df['data'][0])
        fans_df = pd.DataFrame(fans_list)[['id']]

        print(response['next'])
        fans_df = fans_df.append(get_fans_deezer(response['next'], fans_df), ignore_index=True)
        break

    return fans_df
