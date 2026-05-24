from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

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

    token_info = sp_oauth.get_access_token(code)

    sp = spotipy.Spotify(auth=token_info["access_token"])

    playlists_response = sp.current_user_playlists()

    results = []

    for playlist in playlists_response["items"]:

        results.append({
            "id": playlist.get("id"),
            "name": playlist.get("name"),
            "tracks": playlist.get("items", {}).get("total")
        })

    return results
    