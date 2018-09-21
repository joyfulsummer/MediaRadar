from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "API key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_playlist(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  try:

    search_response = youtube.playlists().list(
    part="id",
    maxResults=max_results,
    channelId = q

  ).execute()
  

    videos = []

    for search_result in search_response.get("items", []):
      if search_result["kind"] == "youtube#playlist":
        videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return(nexttok, videos)
    except Exception as e:
        nexttok = "last_page"
        return(nexttok, videos)
  except HttpError,e: pass
