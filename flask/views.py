from flask import render_template
from flaskexample import app
from flask import request 
import json 
from elasticsearch import Elasticsearch
#from flask.ext.reqarg import request_args

@app.route('/')
@app.route('/index')
def index():
   return render_template("cesa2.html")

es=Elasticsearch(["http://52.21.6.9:9200"])

@app.route('/output')
def cesareans_output():
	brand= request.args.get('Brand')
	type= request.args.get('Type')
	keyword= request.args.get('Keyword')
	rank = request.args.get('Rank')
	if rank == '0':
		res = es.search(index='insight',body={'query':{'match':{'description':brand+type+keyword}}},size=500)
		n = len(res["hits"]["hits"])

#example = {"cID":"vID"}
		example = {}
		count = {}
		sortcount = []
#video_count = {"cID": "view count"}
		video_score = {}
		video_count = {}

		for i in range(n):
			vID = res["hits"]["hits"][i]["_source"]["videoID"]
			cID = res["hits"]["hits"][i]["_source"]["channelID"]
			views = int(res["hits"]["hits"][i]["_source"]["views"])
			if cID not in video_count.keys():
				video_count[cID] = views
				example[cID] = vID
			else:
				video_count[cID] = video_count.get(cID,0) + views
			
		for cID in video_count.keys():
			m = video_count[cID]
			if m not in count.keys():
				count[m] = cID
				sortcount.append(m)

#channel_sorted = sorted(video_count.items(), key=lambda kv: kv[1],reverse = True)
		sortcount.sort(reverse=True)
		births = []
		for item in sortcount[:10]:
			cID = count[item]
			item = {}
			item["Channel ID"] = cID
			item["Total views of related videos"] = video_count[cID]
			item["Examples"] = "https://www.youtube.com/watch?v=" + example[cID]
			births.append(item)
      #the_result = ''
		return render_template("output.html", births = births)
	if rank == '1':
		res = es.search(index='insight',body={'query':{'match':{'description':brand+type+keyword}}},size=20)
		n = len(res["hits"]["hits"])
		births = []
		count = 0
		for i in range(n):
			vID = res["hits"]["hits"][i]["_source"]["videoID"]
			cID = res["hits"]["hits"][i]["_source"]["channelID"]
			views = int(res["hits"]["hits"][i]["_source"]["views"])
			if views >= 10000 and count <=9:
				count += 1
				item = {}
				item["Channel ID"] = cID
				item["Total views of related videos"] = views
				item["Examples"] = "https://www.youtube.com/watch?v=" + vID
				births.append(item)
      #the_result = ''
		return render_template("output.html", births = births)
	
	if rank == '2':
		res = es.search(index='insight',body={'query':{'match':{'description':brand+type+keyword}}},size=500)
		n = len(res["hits"]["hits"])

#example = {"cID":"vID"}
		example = {}
		count = {}
		sortcount = []
#video_count = {"cID": "view count"}
		video_score = {}
		video_count = {}

		for i in range(n):
			vID = res["hits"]["hits"][i]["_source"]["videoID"]
			cID = res["hits"]["hits"][i]["_source"]["channelID"]
			views = int(res["hits"]["hits"][i]["_source"]["views"])
			score = float(res["hits"]["hits"][i]["_score"])**3*views/1000
			if cID not in video_count.keys():
				video_score[cID] = score
				video_count[cID] = views
				example[cID] = vID
			else:
				video_score[cID] = video_score.get(cID,0) + score
				video_count[cID] = video_count.get(cID,0) + views
			
		for cID in video_score.keys():
			m = video_score[cID]
			if m not in count.keys():
				count[m] = cID
				sortcount.append(m)

#channel_sorted = sorted(video_count.items(), key=lambda kv: kv[1],reverse = True)
		sortcount.sort(reverse=True)
		births = []
		for item in sortcount[:10]:
			cID = count[item]
			item = {}
			item["Channel ID"] = cID
			item["Total views of related videos"] = video_count[cID]
			item["Examples"] = "https://www.youtube.com/watch?v=" + example[cID]
			births.append(item)
      #the_result = ''
		return render_template("output.html", births = births)
			