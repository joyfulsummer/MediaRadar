import sys
sys.path.append("path to youtube_videos")
from youtube_videos import youtube_search
import json

#this part test for just one round of search and print out the result
#test = youtube_search("spinners")
#just_json = test[1]

#token = test[0]
#youtube_search("spinners",token = token)
    #for video in just_json:
#  print video['snippet']['title']

#video_dict = {'youID':[]}
video_dict = {'youID': [], 'type': []}
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
          video_ID.append(vid['id']['videoId'])
          #video_dict['title'].append(vid['snippet']['title'])
          #video_dict['pub_date'].append(vid['snippet']['publishedAt'])
#print how many videos are added in the video dictionary
    print "added " + str(len(videos)) + " videos to a total of " + str(len(video_dict['youID']))
    return token

#token = grab_videos("spinners")

#this part automate the process of grabing more and more videos for a certain type
    #while token != "last_page":
#token = grab_videos("spinners", token=token)

# now set up a list of keywords, and let api grade video ids according to the list
keywordlist = open('keyword.txt')
for line in keywordlist:
    grab_videos(line, token=None)

with open('data.json', 'w') as outfile:
    json.dump(video_dict, outfile)

with open('youID.json','w') as outfile2:
    json.dump(video_ID, outfile2)
