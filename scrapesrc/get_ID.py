import sys
sys.path.append("/Users/beibei/Documents/insight/project/youtubeAPI/youtube_tutorial")
from playlist import youtube_playlist
from youtube_channels import youtube_search
import json

#this part test for just one round of search and print out the result
#test = youtube_search("spinners")
#just_json = test[1]

#token = test[0]
#youtube_search("spinners",token = token)
    #for video in just_json:
#  print video['snippet']['title']

#video_dict = {'youID':[]}
video_dict = {'channelID': [], 'videoID': [], 'type': []}
video_ID = []
channel_ID = []
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
    


keyword = "Media"
token = grab_channel(keyword)
#this part automate the process of grabing more and more videos for a certain type
while token != "last_page" and len(channel_ID) <300:
    token = grab_channel(keyword, token=token)

# now set up a list of keywords, and let api grade video ids according to the list
#keywordlist = open('keyword.txt')
#for line in keywordlist:
#    grab_videos(line, token=None)
def grab_videos(id, token=None):
    res = youtube_playlist(id)
    token = res[0]
    videos = res[1]
    #print videos
    for vid in videos:           
          video_dict['videoID'].append(vid['id'])
          video_dict['channelID'].append(id)
          video_dict['type'].append(keyword)
          #index = len(video_dict['videoID'])
          #video_dict['index'].append(index)
          video_ID.append(vid['id'])
          #print vid['id']
          #video_dict['title'].append(vid['snippet']['title'])
          #video_dict['pub_date'].append(vid['snippet']['publishedAt'])
#print how many videos are added in the video dictionary
#print "added " + str(len(videos)) + " videos to a total of " + str(index)
    return token

for i in range(len(channel_ID)):
    channel = channel_ID[i]
    token = grab_videos(channel)
#this part automate the process of grabing more and more videos for a certain type
    while token != "last_page" and len(video_ID) < (i+1)*200 :
            token = grab_videos(channel, token=token)


with open(keyword+'_ID_data.json', 'w') as outfile:
    json.dump(video_dict, outfile)

with open(keyword+'_videoID_only.json','w') as outfile2:
    json.dump(video_ID, outfile2)

with open(keyword+'_channelID_only.json','w') as outfile3:
    json.dump(channel_ID, outfile3)
