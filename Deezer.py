# Python file defining Deezer endpoints
import scraper
import pandas as pd

# Loop through charts to most popular albums as proportion of Album Fans / Artist Fans



url = "https://api.deezer.com/album/6910779"

# Create an empty dataframe to pass through and collect fan data
blank_df = pd.DataFrame()

# Runs url or list of urls through the scraper
# and returns a list of dataframes
dfs = scraper.get_album_deezer(url)
fans_df = scraper.get_fans_deezer(url+'/fans', blank_df)

print(fans_df)
