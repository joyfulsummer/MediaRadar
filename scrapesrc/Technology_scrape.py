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
pafy.set_api_key("API key")

def add_data(vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments):
	data = [vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments]
	data2 = {'videoID': [], 'title': [], 'description': [],'author':[],'published':[],\
	'viewcount':[], 'duration': [],'likes':[],'dislikes':[],'rating':[],'category':[],'comments':[]}
	#data = [vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments]
	data2['videoID'] = vID
	data2['title'] = title
	data2['description'] = description
	data2['author'] = author
	data2['published'] = published
	data2['viewcount'] = viewcount
	data2['duration'] = duration
	data2['likes'] = likes
	data2['dislikes'] = dislikes
	data2['rating'] = rating
	data2['category'] = category
	data2['comments'] = comments
	with open("scraper2.csv", "a") as fp:
	    wr = csv.writer(fp, dialect='excel')
	    wr.writerow(data)
	    
	with open("scraper2.json","w") as out_file:
	    json.dump(data2, out_file)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

#videoId = raw_input("ID of youtube video : \n")
def getID(videoId=None):
	url = "https://www.youtube.com/watch?v=" + videoId
#Request fro Metadata of the Video
	video = pafy.new(url)
	try:
		results = youtube.commentThreads().list(
		    part="snippet",
		    maxResults=100,
		    videoId=videoId,
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
        #print "."
				try:
			  		results = youtube.commentThreads().list(
	  		  part="snippet",
	  		  maxResults=100,
	  		  videoId=videoId,
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
					try:
						nextPageToken = results["nextPageToken"]
					except KeyError, e:
						print "An KeyError error occurred: %s" % (e)
						further = False

# Adding the full data to CSV
		add_data(videoId,video.title,video.description,video.author,video.published,video.viewcount, video.duration, video.likes, video.dislikes,video.rating,video.category,comments)
		#add_data2(videoId,video.title,video.description,video.author,video.published,video.viewcount, video.duration, video.likes, video.dislikes,video.rating,video.category,comments)
	except HttpError as e: pass

keyword = "Technology"
   
with open(keyword+".json", "r") as read_file:
    info = json.load(read_file)
    for videoID in info['youID']:
		#print videoID
		getID(videoID)
