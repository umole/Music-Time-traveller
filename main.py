import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from pprint import pprint


CLIENT_ID = "e160558fd5464da1bf72a514d5f72052"
CLIENT_SECRET = "05ab0de78c174106b9608543bea5fe3b"
REDIRECT_URI = "http://example.com"

date = "2016-07-19" #input("What year would you like to travel back to? Enter it in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
billboard = response.text

soup = BeautifulSoup(billboard, 'html.parser')
bb_list = [song.get_text().strip("\t\n") for song in soup.select(selector='li ul li h3')]
#print(bb_list)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope="playlist-modify-private"))
user_id = sp.current_user()
SPOTIFY_URI = user_id['uri']
SPOTIFY_ID = user_id['id']
SPOTIFY_URL = user_id['external_urls']

year = date.split('-')[0]
song_uri = []
for songs in bb_list:
    result = sp.search(q=f"track{songs} year{year}", type="track")
    #pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{songs} could not be found on spotify!")

#creatinfg a new private playlist in spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Hits", public=False, collaborative=False, description=f"This is a playlist of hit songs from {date}")
print(playlist)

#Adding songs found into a new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)




