import sys
sys.path.append("/home/ubuntu")
# import the "youtube_search" function from "youtube_videos" file
from youtube_videos import youtube_search
import json

# store video ID, channel ID, video type (keyword for search), and index of video in video_dict dictionary.
video_dict = {'youID': [],'channelID': [], 'type': [],'index': []}
#a list of 
video_ID = []

# grab video according to keyword and save the token
def grab_videos(keyword, token):

# call the "youtube_search" function from the "youtube_videos" file
# call the Youtube API and list video information given keyword
    res = youtube_search(keyword, token)

# save token and video information separately
    token = res[0]
    videos = res[1]

    for vid in videos:
# save the video ID, channel ID, type, and index in the dictionary
          video_dict['youID'].append(vid['id']['videoId'])
          video_dict['type'].append(keyword)
          video_dict['channelID'].append(vid['snippet']['channelId'])
          index = len(video_dict['youID'])
          video_dict['index'].append(index)
          video_ID.append(vid['id']['videoId'])
          
# return page token, in order to retrieve next token
    return token

# filename is a list of keywords used for calling API
filename = "keyword.txt"

# reading keyword
with open(filename,"r") as input_file:
	i = 0
	for line in input_file:

# each keyword is used to get 500 video information 
   	 	key = line
   	 	token = grab_videos(key, token = None)

# telling me which keyword has been used
		print 'grabing ' + key
   
# this part automate the process of grabing more and more videos for a certain type
		while token != "last_page" and len(video_dict['youID']) <= 500*(i+1):
			token = grab_videos(key, token=token)
		i += 1
    
# telling me the total number of videos 
print str(len(video_dict["youID"]))

# save information to json file
with open(keyword+'_1.json', 'w') as outfile:
    json.dump(video_dict, outfile)
