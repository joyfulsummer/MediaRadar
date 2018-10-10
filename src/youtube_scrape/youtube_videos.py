from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# set up Youtube API key which can be requested from Google Console
DEVELOPER_KEY = "your API key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# this function calls the Youtube API and retrieve video ID given a specific keyword
def youtube_search(q, token=None,max_results=50,order="relevance", location=None, location_radius=None):

# establish connection with API
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    
# call the API and get a list of video ID given keyword
  search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results,
    location=location,
    locationRadius=location_radius

  ).execute()

  videos = []

  for search_result in search_response.get("items", []):
  
  # store result is result is video ID
    if search_result["id"]["kind"] == "youtube#video":
      videos.append(search_result)
  try:
  # get the next page token given current token for future API calls
      nexttok = search_response["nextPageToken"]
      return [nexttok, videos]
 
  # if already at the last page, return token as "last_page"
  except Exception as e:
      nexttok = "last_page"
      return [nexttok, videos]
