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

@app.get("/playlist/{playlist_id}/duplicates")
def find_duplicates(playlist_id: str):
    playlist_data = spotify_client.playlist_items(playlist_id)

    seen = set()
    duplicates = []

    for item in playlist_data["items"]:
        track = item.get("item")

        if not track:
            continue

        song_key = (track.get("name"), track["artists"][0]["name"])
        if song_key in seen:
            duplicates.append({
                "track_name": track.get("name"),
                "artist": track["artists"][0]["name"],
                # "album": track["album"]["name"],
                # "track_id": track.get("id")
            })
        else:
            seen.add(song_key)
    
    return duplicates

# @app.get("/playlist/{playlist_id}/audio-features")
# def get_audio_features(playlist_id: str):

#     if spotify_client is None:
#         return {"error": "Please login again"}

#     playlist_data = spotify_client.playlist_items(playlist_id)

#     track_ids = []

#     for item in playlist_data["items"]:

#         track = item.get("item")

#         if not track:
#             continue

#         track_id = track.get("id")

#         if track_id:
#             track_ids.append(track_id)

#     # audio_features = spotify_client.audio_features(track_ids)
#     # print(audio_features)
#     try:
#         audio_features = spotify_client.audio_features(track_ids)

#     except Exception as e:
#         return {"error": str(e)}

#     results = []

#     for item, features in zip(playlist_data["items"], audio_features):

#         track = item.get("item")

#         if not track or not features:
#             continue

#         results.append({
#             "track_name": track.get("name"),
#             "artist": track["artists"][0]["name"],
#             "energy": features.get("energy"),
#             "danceability": features.get("danceability"),
#             "tempo": features.get("tempo"),
#             "valence": features.get("valence")
#         })

#     return results
@app.get("/playlist/{playlist_id}/stats")
def playlist_stats(playlist_id: str):

    if spotify_client is None:
        return {"error": "Login Again"}
    
    playlist_data = spotify_client.playlist_items(playlist_id)

    total_tracks = 0
    total_duration_ms = 0
    artists_count = {}

    for item in playlist_data["items"]:

        track = item.get("item")

        if not track:
            continue

        total_tracks += 1
        total_duration_ms += track.get("duration_ms", 0)

        artist_name = track["artists"][0]["name"]
        artists_count[artist_name] = artists_count.get(artist_name, 0) + 1

    top_artist = sorted(artists_count.items(), key=lambda x: x[1], reverse=True)

    formatted_artists = []
    for artist, count in top_artist:
        formatted_artists.append({
            "artist": artist,
            "count": count
        })
    return {
        "total_tracks": total_tracks,
        "total_duration_ms": round(total_duration_ms / 60000, 2),
        "average_song_length_seconds": round((total_duration_ms / total_tracks) / 1000, 2),
        "top_artists": formatted_artists
    }

    