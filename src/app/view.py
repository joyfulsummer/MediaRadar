from flask import render_template
from flaskexample import app
from flask import request 
import json 
from elasticsearch import Elasticsearch
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
#from flask.ext.reqarg import request_args

#'index.html' in template folder is the input webpage to receive product description
@app.route('/')
@app.route('/index')
def index():
   return render_template("cesa2.html")

# create a Elasticsearch python client, input your list of ES host IP in []
es = Elasticsearch([your ES host IP])

#set up API key for calling Youtube API. API key can be requested in Google Console.
DEVELOPER_KEY = "your API key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# this function pull the url for channel banner image given a channel ID through calling Youtube API
def channel_banner(channel_id):

# setting up object for calling API
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    
# API calls, extract channel information given channel ID
  search_response = youtube.channels().list(
    part='brandingSettings',
    id=channel_id
  ).execute()

# return the url for the banner image to display later
  return search_response["items"][0]['brandingSettings']['image']['bannerImageUrl']

# directs to the output webpage to display result
@app.route('/')
@app.route('/output')  
def cesareans_output():

# get product brand, type, keyword, and rank criteria from input page
	brand= request.args.get('Brand')
	type= request.args.get('Type')
	keyword= request.args.get('Keyword')
	rank = request.args.get('Rank')

# rank by popularity
	if rank == '0':

# query Elastic Search and get information of 1000 videos which match the product description
		res = es.search(index='mixed',body={'query':{'match':{'description':brand+type+keyword}}},size=500,request_timeout=120)
		n = len(res["hits"]["hits"])

# set up variable for processing of information
# example stores the channelID:example_videoID pair
		example = {}
# count stores the channelID:total views of related video pair
		count = {}
# sortcount stores the sorted channel information after ranking by popularity
		sortcount = []
#video_score stores the video:similarity score pair
		video_score = {}
#video_count stores the video:views pair
		video_count = {}

		for i in range(n):

# pull video ID, channel ID, number of views and similarity score from Elastic Search 
			vID = res["hits"]["hits"][i]["_source"]["videoID"]
			cID = res["hits"]["hits"][i]["_source"]["channelID"]
			views = int(res["hits"]["hits"][i]["_source"]["views"])			
			score = float(res["hits"]["hits"][i]["_score"])

# store Elastic Search result into video_count, example, and video_score dictionary
			if cID not in video_count.keys():
				video_count[cID] = views
				example[cID] = vID
				video_score[cID] = score
			else:
				video_count[cID] = video_count.get(cID,0) + views

# store channelID: total number of views in video_count dictionary
		for cID in video_count.keys():
			m = video_count[cID]
			if m not in count.keys():
				count[m] = cID
				sortcount.append(m)

#sort channel ID according to total number of views of related videos
		sortcount.sort(reverse=True)

# channels is the list of channel information that will parse to output page to display
		channels = []

# retrieve the top five channel information as ranked previously
		for item in sortcount[:5]:
    
# get the channel ID, each item (info) in channels is a dictionary
			cID = count[item]
			info = {}

# channel ID, total views of related videos, similarity score is stored in info
			info["Channel ID"] = cID
		  info["Total views of related videos"] = video_count[cID]
			info["score"] = str(video_score[cID])

# url of example video given video ID
			info["Examples"] = "https://www.youtube.com/watch?v=" + example[cID]
# url of thumbnail image of example video
			info["images"] = "https://img.youtube.com/vi/"+ example[cID]+"/hqdefault.jpg"
# url to channel page given channel ID
			info["blogger_url"] = "https://www.youtube.com/channel/"+cID
# url to banner image of channel
      info["bloggers"] = channel_banner(cID)

# store dictionary in channels to be passed to output page
			channels.append(info)
		return render_template("output.html", channels = channels)

# rank by similarity
	if rank == '1':

# query Elastic Search for related videos with matched keyword, need only top 5 videos
		res = es.search(index='mixed',body={'query':{'match':{'description':brand+type+keyword}}},size=5,  request_timeout=120)
		n = len(res["hits"]["hits"])

# channels is the list of channel information that will parse to output page to display
		channels = []

		for i in range(n):
    
# pull video ID, channel ID, number of views and similarity score from Elastic Search 
			vID = res["hits"]["hits"][i]["_source"]["videoID"]
			cID = res["hits"]["hits"][i]["_source"]["channelID"]
			views = int(res["hits"]["hits"][i]["_source"]["views"])			
			score = float(res["hits"]["hits"][i]["_score"])

# channel ID, total views of related videos, similarity score is stored in a dictionary(info)
			info = {}
			info["Channel ID"] = cID
			info["Total views of related videos"] = views
			info["Examples"] = "https://www.youtube.com/watch?v=" + vID		
			info["score"] = str(score)
      
# url of thumbnail image of example video
			info["images"] = "https://img.youtube.com/vi/"+ vID+"/hqdefault.jpg"
# url to channel page given channel ID
			info["blogger_url"] = "https://www.youtube.com/channel/"+cID
# url to banner image of channel
			info["bloggers"] = channel_banner(cID)
      
# store dictionary in channels to be passed to output page
			channels.append(item)
		return render_template("output.html", channels = channels)
	
