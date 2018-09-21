from apiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy
import csv
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')  

DEVELOPER_KEY = "APIkey"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
pafy.set_api_key("APIkey")

def add_data_csv(keyword,channelID, vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments):
	data = [keyword,channelID, vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments]
	with open(keyword+"_video_info.csv", "a") as fp:
	    wr = csv.writer(fp, dialect='excel')
	    wr.writerow(data)

def add_data(keyword,channelID, vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments):
	data = {'type':[], channelID:[],'videoID': [], 'title': [], 'description': [],'author':[],'published':[],\
	'viewcount':[], 'duration': [],'likes':[],'dislikes':[],'rating':[],'category':[],'comments':[]}
	#data = [vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments]
	data['type'] = keyword
	data['channelID'] = channelID
	data['videoID'] = vID
	data['title'] = title
	data['description'] = description
	data['author'] = author
	data['published'] = published
	data['viewcount'] = viewcount
	data['duration'] = duration
	data['likes'] = likes
	data['dislikes'] = dislikes
	data['rating'] = rating
	data['category'] = category
	data['comments'] = comments
	with open(keyword+'_video_info.json', 'w') as outfile:    
    		json.dump(data, outfile)
	#with open("scraper.csv", "a") as fp:
	#    wr = csv.writer(fp, dialect='excel')
	#    wr.writerow(data)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

#videoId = raw_input("ID of youtube video : \n")
def getID(keyword, channelID = None, playlistID=None):
    #title = None
    #description = None
    #author = None
    #published = None
    #viewcount = None
    #duration = None
    #likes=None
    #dislikes=None
    #rating=None
    #category=None
    comments=None
    videoID = None
    try:
	    res = youtube.playlistItems().list(
    part="snippet,contentDetails",
    maxResults=1,
    playlistId = playlistID

  ).execute()
	    try:
		    videoID = res["items"][0]["snippet"]["resourceId"]["videoId"]
          #index = len(video_dict['videoID'])
          #video_dict['index'].append(index)
          #print vid['id']
          #video_dict['title'].append(vid['snippet']['title'])
          #video_dict['pub_date'].append(vid['snippet']['publishedAt'])
#print how many videos are added in the video dictionary
#print "added " + str(len(videos)) + " videos to a total of " + str(index)
              #return token
	    except IndexError, e: pass
    except HttpError, e: pass
    if videoID != None:
	    url = "https://www.youtube.com/watch?v=" + videoID
#Request fro Metadata of the Video
	    try:
		    video = pafy.new(url)	    
		    try:
		        results = youtube.commentThreads().list(
		    part="snippet",
		    maxResults=100,
		    videoId=videoID,
		    textFormat="plainText"
		  ).execute()
		        totalResults = 0
		        totalResults = 0
		        totalResults = int(results["pageInfo"]["totalResults"])
		        count = 0
		        nextPageToken = ''
		        comments = []
		        further = True
		        first = True
		        while further:
		        	halt = False
		        	if first == False:
		  	    	    try:
			      		    results = youtube.commentThreads().list(
	  		  part="snippet",
	  		  maxResults=100,
	  		  videoId=videoID,
	  		  textFormat="plainText",
	  		  pageToken=nextPageToken
	  		).execute()
		  		    	    totalResults = int(results["pageInfo"]["totalResults"])
		  	    	    except googleapiclient.errors.HttpError as e: pass
				#if err.resp.status in [403, 400, 404]:
				#halt=True
				#further = False
					#print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
				    #halt = True
		        	if halt == False:
		  	    	    count += totalResults
		 	     	    for item in results["items"]:
				  	        comment = item["snippet"]["topLevelComment"]
				  	        author = comment["snippet"]["authorDisplayName"]
				  	        text = comment["snippet"]["textDisplay"]
				  	        comments.append([author,text])
		 	     	    if totalResults < 100:
					        further = False
					        first = False
		 	     	    else:
				        	further = True
				        	first = False
				        	try:  nextPageToken = results["nextPageToken"]
				        	except KeyError, e: pass
				        		#print "An KeyError error occurred: %s" % (e)
				    	    	#further = False
		    

		        add_data(keyword, channelID, videoID,video.title,video.description,video.author,video.published,video.viewcount, video.duration, video.likes, video.dislikes,video.rating,video.category,comments)
		        add_data_csv(keyword, channelID, videoID,video.title,video.description,video.author,video.published,video.viewcount, video.duration, video.likes, video.dislikes,video.rating,video.category,comments)
		    except HttpError as e: pass
	    except: pass		        	    
		    
#linestring = open('data.txt')
#data = []
#for line in linestring:
#    data.append(line.strip('\r\n').strip('"'))
#print data[0:5]
#scrape(data[0])
#for i in range(20,50):
#	getID(data[i])
keyword = "Education"

   
with open(keyword+"_ID_data.json", "r") as read_file:
    info = json.load(read_file)
    for i in range(len(info['playlistID'])):
		    channelID = info['channelID'][i]
		    playlistID = info['playlistID'][i]
		    if channelID and playlistID: getID(keyword, channelID, playlistID)

