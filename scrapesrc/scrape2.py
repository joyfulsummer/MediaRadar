from apiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy
import csv

import sys
reload(sys)
sys.setdefaultencoding('utf8')  

DEVELOPER_KEY = "AIzaSyC-UlA4kT-5yxG3aU24PbXrcGvWThnBnKs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
pafy.set_api_key("AIzaSyC-UlA4kT-5yxG3aU24PbXrcGvWThnBnKs")

def add_data(vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments):
	data = [vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments]
	with open("scraper.csv", "a") as fp:
	    wr = csv.writer(fp, dialect='excel')
	    wr.writerow(data)

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
	except HttpError as e: pass
linestring = open('data.txt')
data = []
for line in linestring:
    data.append(line.strip('\r\n').strip('"'))
#print data[0:5]
#scrape(data[0])
for i in range(20,50):
	getID(data[i])