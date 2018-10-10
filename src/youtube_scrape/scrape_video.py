from apiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy
import csv
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')  

# set up Youtube API key which can be requested from Google Console
DEVELOPER_KEY = "your API key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
pafy.set_api_key("your API key")

# this function save the scraped video information into csv file
def add_data(keyword,vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments):

# save the keyword used for search, video ID, title, description, author, published date, number of views, duration,
# number of likes/dislikes, rating score, category of video, and user comments into file
	data = [keyword, vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments]
	with open(keyword+"_new_scrape.csv", "a") as fp:
	    wr = csv.writer(fp, dialect='excel')
	    wr.writerow(data)

# set up connection with Youtube API
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

# scrape video information given video ID
def getID(videoId=None):

# need url link to video to scrape
	url = "https://www.youtube.com/watch?v=" + videoId
  
# Request fro Metadata of the Video
	try:
		video = pafy.new(url)
		try:
    
# if video comment is not disabled, scrape user comment
			results = youtube.commentThreads().list(
		    part="snippet",
		    maxResults=100,
		    videoId=videoId,
		    textFormat="plainText"
		  ).execute()
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
# if video comment is not disabled, scrape user comment
				  		results = youtube.commentThreads().list(
	  		  part="snippet",
	  		  maxResults=100,
	  		  videoId=videoId,
	  		  textFormat="plainText",
	  		  pageToken=nextPageToken
	  		).execute()
		  				totalResults = int(results["pageInfo"]["totalResults"])
              
# pass videos if comments are disabled
			  		except: pass
            
				if halt == False:
		 	 		count += totalResults
		 	 		for item in results["items"]:

# save comment, author information
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
            
 # go to next page given current page token
							nextPageToken = results["nextPageToken"]
              
 # if last page, do not continue
						except KeyError, e:
							further = False

# Adding the full data to CSV
			add_data(keyword, videoId,video.title,video.description,video.author,video.published,video.viewcount, video.duration, video.likes, video.dislikes,video.rating,video.category,comments)
		
		except: pass
	except:pass

# file with all video and channel ID
filename = "video_ID.json"

with open(filename, "r") as read_file:
    info = json.load(read_file)
    for videoID in info['youID']:
    
# scrape information for every video in the file
		  getID(videoID)
