from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

spotify_client = None

# def get_spotify_client():

#     return spotipy.Spotify(
#         auth_manager=SpotifyOAuth(
#             client_id=os.getenv("SPOTIPY_CLIENT_ID"),
#             client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
#             redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
#             scope="playlist-read-private"
#         )
#     )

sp_oauth = SpotifyOAuth(
    client_id = os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI"),
    scope = "playlist-read-private"
)

@app.get("/")
def home():
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)

@app.get("/callback")
def callback(code: str):

    global spotify_client

    token_info = sp_oauth.get_access_token(code)

    spotify_client = spotipy.Spotify(
        auth=token_info["access_token"]
    )

    return {"message": "Login successful"}

@app.get("/playlist/{playlist_id}")
def get_playlist(playlist_id: str):

    playlist_data = spotify_client.playlist_items(playlist_id)

    results = []

    for item in playlist_data["items"]:

        track = item.get("item")

        if not track:
            continue

        results.append({
            "track_name": track.get("name"),
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "track_id": track.get("id")
        })

    return results


    # return results
    