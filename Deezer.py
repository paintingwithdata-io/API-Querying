import pandas as pd
import requests
from pandas import json_normalize

# Sets url variable from API to pull album data and gets json as response
url = "https://api.deezer.com/album/302127"
response = requests.get(url)

# Create dictionaries to select key columns
album_cols = {'cols': ['id', 'title', 'upc', 'genre_id', 'label', 'duration',
                    'fans', 'rating', 'release_date', 'record_type', 'available',
                    'tracklist', 'type', 'genres.data', 'artist.id', 'artist.name',
                    'artist.tracklist', 'artist.type']}

# Create a json object from the response and then a dataframe after normalizing json data.
data = response.json()
json_df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')

# Create a dataframe with the album information, reduced to the key cols from album_cols
album_df = json_df[album_cols['cols']]

# Create a dataframe with the track information by turning
# the tracks.data series into a list and then into a dataframe
track_series = json_df['tracks.data']
track_list = list(track_series[0])
track_df = pd.DataFrame(track_list)


print(album_df)
print(track_df)



#JSON Data metadata from the API
# Headers is a dictionary
    #print(response.headers)
# Get the content-type from the dictionary.
    #print(response.headers["content-type"])