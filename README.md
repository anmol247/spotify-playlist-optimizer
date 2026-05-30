# Spotify Playlist Optimizer

A Python-based Spotify playlist analysis tool built using FastAPI and Spotipy.

## Features

### Spotify Integration
- Spotify OAuth 2.0 authentication
- Fetch user playlists
- Fetch playlist tracks
- Playlist metadata extraction

### Playlist Analytics
- Playlist statistics
- Top artist analysis
- Total playlist duration
- Average song length

### Playlist Utilities
- Duplicate track detection
- Track extraction and transformation

### Telegram Bot (In Progress 🚧)
- Telegram Bot integration
- Playlist commands
- Analytics via chat interface
- Spotify assistant experience

## Tech Stack

- Python
- FastAPI
- Spotipy
- Spotify Web API
- Telegram Bot API

## Current Endpoints

| Endpoint | Description |
|-----------|------------|
| `/` | Spotify login |
| `/callback` | OAuth callback |
| `/playlist/{playlist_id}` | Fetch playlist tracks |
| `/playlist/{playlist_id}/duplicates` | Detect duplicate songs |
| `/playlist/{playlist_id}/stats` | Playlist analytics |

## Learning Goals

This project explores:

- OAuth 2.0 Authentication
- REST API Integration
- Data Aggregation
- Backend Development with FastAPI
- Telegram Bot Development
- Recommendation & Analytics Systems

## Roadmap

- [x] Spotify OAuth
- [x] Playlist retrieval
- [x] Duplicate detection
- [x] Playlist analytics
- [ ] Telegram bot integration
- [ ] Playlist assistant commands
- [ ] Automated playlist recommendations