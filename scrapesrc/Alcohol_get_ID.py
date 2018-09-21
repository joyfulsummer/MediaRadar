import sys
sys.path.append("/home/ubuntu")
from youtube_videos_Joy7 import youtube_search
import json

#this part test for just one round of search and print out the result
#test = youtube_search("spinners")
#just_json = test[1]

#token = test[0]
#youtube_search("spinners",token = token)
    #for video in just_json:
#  print video['snippet']['title']

#video_dict = {'youID':[]}
video_dict = {'youID': [], 'type': [], 'index': []}
video_ID = []
#, 'title':[], 'pub_date':[]}

#grab video according to keyword and save the token
def grab_videos(keyword, token=None):
    res = youtube_search(keyword)
    token = res[0]
    videos = res[1]
    for vid in videos:      
          video_dict['youID'].append(vid['id']['videoId'])
          video_dict['type'].append(keyword)
          index = len(video_dict['youID'])
          video_dict['index'].append(index)
          video_ID.append(vid['id']['videoId'])
          #video_dict['title'].append(vid['snippet']['title'])
          #video_dict['pub_date'].append(vid['snippet']['publishedAt'])
#print how many videos are added in the video dictionary
#print "added " + str(len(videos)) + " videos to a total of " + str(index)
    return token

keyword = "Technology"

token = grab_videos(keyword)

#this part automate the process of grabing more and more videos for a certain type
while token != "last_page" and len(video_dict['youID']) <= 60000:
    token = grab_videos(keyword, token=token)

with open(keyword+'.json', 'w') as outfile:
    json.dump(video_dict, outfile)

with open(keyword+'_ID.json','w') as outfile2:
    json.dump(video_ID, outfile2)