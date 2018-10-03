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

es=Elasticsearch([host ip])

@app.route('/output')
def cesareans_output():
	brand= request.args.get('Brand')
	type= request.args.get('Type')
	keyword= request.args.get('Keyword')
	res = es.search(index='insight',body={'query':{'match':{'description':brand+type+keyword}}},size=500)
	n = len(res["hits"]["hits"])

#example = {"cID":"vID"}
	example = {}
	count = {}
	sortcount = []
#video_count = {"cID": "view count"}
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
		#births.append(dict(Channel ID = info["channelID"][i], Total views of related videos=info["views"][i], \
		#Examples=info["example"][i]))
		births.append(item)
      #the_result = ''
	return render_template("output.html", births = births)
