import sys
sys.path.append("/Users/beibei/Documents/insight/project/youtubeAPI/youtube_tutorial")
from playlist import youtube_playlist
from playlistItems import youtube_playlistItems
from youtube_channels import youtube_search
import json
from apiclient.errors import HttpError
from apiclient.discovery import build
from oauth2client.tools import argparser

#this part test for just one round of search and print out the result
#test = youtube_search("spinners")
#just_json = test[1]

#token = test[0]
#youtube_search("spinners",token = token)
    #for video in just_json:
#  print video['snippet']['title']

#video_dict = {'youID':[]}
video_dict = {'channelID': [],'playlistID': [], 'videoID': [], 'type': []}
video_ID = []
channel_ID = []
playlist_ID = []
#, 'title':[], 'pub_date':[]}

#grab video according to keyword and save the token
def grab_channel(keyword, token=None):
    res = youtube_search(keyword)
    token = res[0]
    videos = res[1]
    for vid in videos:
          #video_dict['channelID'].append(vid['id']['channelId'])
          #video_dict['type'].append(keyword)
          channel_ID.append(vid['id']['channelId'])
          #video_dict['title'].append(vid['snippet']['title'])
          #video_dict['pub_date'].append(vid['snippet']['publishedAt'])
#print how many videos are added in the video dictionary
    print "added " + str(len(videos)) + " channels to a total of " + str(len(channel_ID))
    return token
    


keyword = "Fashion"
token = grab_channel(keyword)
#this part automate the process of grabing more and more videos for a certain type
while token != "last_page" and len(channel_ID) <2:
    token = grab_channel(keyword, token=token)

# now set up a list of keywords, and let api grade video ids according to the list
#keywordlist = open('keyword.txt')
#for line in keywordlist:
#    grab_videos(line, token=None)
def grab_playlist(id, token=None):
    res = youtube_playlist(id)
    token = res[0]
    videos = res[1]
    #print videos
    for vid in videos:           
          playlist_ID.append(vid['id'])
          video_dict['channelID'].append(id)
          video_dict['playlistID'].append(vid['id'])
          #index = len(video_dict['videoID'])
          #video_dict['index'].append(index)
          #video_ID.append(vid['id'])
          #print vid['id']
          #video_dict['title'].append(vid['snippet']['title'])
          #video_dict['pub_date'].append(vid['snippet']['publishedAt'])
#print how many videos are added in the video dictionary
#print "added " + str(len(videos)) + " videos to a total of " + str(index)
    return token
    
def grab_video(id, token = None):
    DEVELOPER_KEY = "AIzaSyCpXPYyDtSTCHcGM_Gy3ZIkDLObj_m0PJ4"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    try:
          res = youtube.playlistItems().list(
    part="snippet,contentDetails",
    maxResults=1,
    playlistId = id

  ).execute()
          if res:
              videoID = res["items"][0]["snippet"]["resourceId"]["videoId"]          
              video_ID.append(videoID)
              video_dict['videoID'].append(videoID)
          #index = len(video_dict['videoID'])
          #video_dict['index'].append(index)
          #print vid['id']
          #video_dict['title'].append(vid['snippet']['title'])
          #video_dict['pub_date'].append(vid['snippet']['publishedAt'])
#print how many videos are added in the video dictionary
#print "added " + str(len(videos)) + " videos to a total of " + str(index)
              return token
    except HttpError, e: pass            

for i in range(len(channel_ID)):
    channel = channel_ID[i]
    token = grab_playlist(channel)
    while token != "last_page" and len(playlist_ID) < (i+1)*5 :
            token = grab_playlist(channel, token=token)

#channel = channel_ID[0]
#grab_playlist(channel)

for playlistID in playlist_ID:
    grab_video(playlistID)
    video_dict['type'] = keyword
            
            


with open(keyword+'_ID_data.json', 'w') as outfile:
    json.dump(video_dict, outfile)

with open(keyword+'_videoID_only.json','w') as outfile2:
    json.dump(video_ID, outfile2)

with open(keyword+'_channelID_only.json','w') as outfile3:
    json.dump(channel_ID, outfile3)
    
with open(keyword+'_playlistID_only.json','w') as outfile4:
    json.dump(playlist_ID, outfile4)
