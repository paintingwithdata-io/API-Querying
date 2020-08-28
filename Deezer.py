# Python file defining Deezer endpoints
import scraper

# Sets url variable from API to pull album data and gets json as response
url = "https://api.deezer.com/album/302127"

# Runs url or list of urls through the scraper
# and returns a list of dataframes
dfs = scraper.get_data(url)



# JSON Data metadata from the API
# Headers is a dictionary
# print(response.headers)
# Get the content-type from the dictionary.
# print(response.headers["content-type"])
